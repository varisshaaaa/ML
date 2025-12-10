import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

class FeatureEngineer:
    def __init__(self):
        try:
            self.db_engine = create_engine(os.getenv("DATABASE_URL"))
            self.redis_client = redis.from_url(os.getenv("REDIS_URL"))
        except Exception as e:
            print(f"Warning: Database connection failed: {e}")
            self.db_engine = None
            self.redis_client = None
    
    def load_data(self, filepath: str = "data/raw/aqi_data.csv") -> pd.DataFrame:
        """Load raw data"""
        return pd.read_csv(filepath, parse_dates=['timestamp'])
    
    def create_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features"""
        df = df.copy()
        
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_rush_hour'] = df['hour'].isin([7, 8, 9, 17, 18, 19]).astype(int)
        
        return df
    
    def create_pollution_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create pollution-related features"""
        df = df.copy()
        
        df['total_pollution'] = (
            df['pm2_5'] + df['pm10'] + 
            df['no2'] + df['so2'] + df['o3']
        )
        
        df['pm_ratio'] = df['pm2_5'] / (df['pm10'] + 1)
        
        df['pollution_level'] = pd.cut(
            df['pm2_5'],
            bins=[0, 12, 35, 55, 150, 1000],
            labels=['Good', 'Moderate', 'Unhealthy_Sensitive', 'Unhealthy', 'Very_Unhealthy']
        )
        
        return df
    
    def create_health_risk_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create health risk score (0-100)"""
        df = df.copy()
        
        df['health_risk_score'] = (
            (df['pm2_5'] / 150 * 40) +
            (df['pm10'] / 250 * 30) +
            (df['no2'] / 200 * 15) +
            (df['o3'] / 180 * 10) +
            (df['so2'] / 100 * 5)
        ).clip(0, 100)
        
        return df
    
    def create_lag_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create lag features for time series"""
        df = df.copy()
        df = df.sort_values(['city', 'timestamp'])
        
        for col in ['pm2_5', 'pm10', 'aqi']:
            df[f'{col}_lag_1h'] = df.groupby('city')[col].shift(1)
            df[f'{col}_lag_24h'] = df.groupby('city')[col].shift(24)
            df[f'{col}_rolling_mean_24h'] = df.groupby('city')[col].rolling(24, min_periods=1).mean().reset_index(0, drop=True)
        
        return df
    
    def process_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all feature engineering steps"""
        print("Creating time features...")
        df = self.create_time_features(df)
        
        print("Creating pollution features...")
        df = self.create_pollution_features(df)
        
        print("Creating health risk score...")
        df = self.create_health_risk_score(df)
        
        print("Creating lag features...")
        df = self.create_lag_features(df)
        
        df = df.dropna()
        
        return df
    
    def save_to_postgres(self, df: pd.DataFrame, table_name: str = "aqi_features"):
        """Save features to PostgreSQL"""
        if self.db_engine:
            try:
                df.to_sql(table_name, self.db_engine, if_exists='replace', index=False)
                print(f"✅ Features saved to PostgreSQL table: {table_name}")
            except Exception as e:
                print(f"Warning: Could not save to PostgreSQL: {e}")
    
    def save_to_redis(self, df: pd.DataFrame):
        """Save latest features to Redis"""
        if self.redis_client:
            try:
                latest_data = df.groupby('city').tail(1)
                
                for _, row in latest_data.iterrows():
                    key = f"aqi:latest:{row['city']}"
                    value = row.to_dict()
                    value['timestamp'] = str(value['timestamp'])
                    
                    self.redis_client.setex(key, 3600, json.dumps(value, default=str))
                
                print(f"✅ Latest features cached in Redis for {len(latest_data)} cities")
            except Exception as e:
                print(f"Warning: Could not save to Redis: {e}")
    
    def run_pipeline(self, input_path: str = "data/raw/aqi_data.csv"):
        """Run complete feature engineering pipeline"""
        print("Loading data...")
        df = self.load_data(input_path)
        
        print("Processing features...")
        df_processed = self.process_features(df)
        
        print("Saving to PostgreSQL...")
        self.save_to_postgres(df_processed)
        
        print("Caching in Redis...")
        self.save_to_redis(df_processed)
        
        output_path = "data/processed/aqi_features.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_processed.to_csv(output_path, index=False)
        print(f"✅ Processed data saved to {output_path}")
        
        return df_processed

if __name__ == "__main__":
    engineer = FeatureEngineer()
    df = engineer.run_pipeline()
    print(df.head())
    print(f"\nShape: {df.shape}")
