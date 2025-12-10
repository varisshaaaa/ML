import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.xgboost
import joblib
import os
from datetime import datetime

class ModelTrainer:
    def __init__(self):
        self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment("air_quality_prediction")
        
    def load_features(self, filepath: str = "data/processed/aqi_features.csv") -> pd.DataFrame:
        """Load processed features"""
        return pd.read_csv(filepath)
    
    def prepare_data(self, df: pd.DataFrame):
        """Prepare features and target"""
        # Target: Next hour AQI
        df['target_aqi'] = df.groupby('city')['aqi'].shift(-1)
        df = df.dropna()
        
        feature_cols = [
            'pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co',
            'hour', 'day_of_week', 'month', 'is_weekend', 'is_rush_hour',
            'pm_ratio', 'health_risk_score',
            'pm2_5_lag_1h', 'pm2_5_lag_24h', 'pm2_5_rolling_mean_24h',
            'aqi_lag_1h', 'aqi_lag_24h'
        ]
        
        X = df[feature_cols]
        y = df['target_aqi']
        
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train_model(self, X_train, y_train, X_test, y_test):
        """Train XGBoost model with MLflow tracking"""
        with mlflow.start_run():
            params = {
                'objective': 'reg:squarederror',
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 6,
                'random_state': 42
            }
            
            mlflow.log_params(params)
            
            model = xgb.XGBRegressor(**params)
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            mlflow.log_metrics({
                "mse": mse,
                "rmse": rmse,
                "r2": r2
            })
            
            print(f"✅ Model Performance:")
            print(f"RMSE: {rmse:.4f}")
            print(f"R2 Score: {r2:.4f}")
            
            # Save model
            os.makedirs("models/saved_models", exist_ok=True)
            joblib.dump(model, "models/saved_models/xgboost_aqi_model.pkl")
            
            # Log model to MLflow
            mlflow.xgboost.log_model(model, "model")
            
            return model

if __name__ == "__main__":
    trainer = ModelTrainer()
    
    # Check if data exists
    if not os.path.exists("data/processed/aqi_features.csv"):
        print("Data not found. Please run feature_engineering.py first.")
    else:
        print("Loading data...")
        df = trainer.load_features()
        
        print("Preparing data...")
        X_train, X_test, y_train, y_test = trainer.prepare_data(df)
        
        print("Training model...")
        trainer.train_model(X_train, y_train, X_test, y_test)
