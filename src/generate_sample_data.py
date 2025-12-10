import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_historical_data(days=30):
    """Generate synthetic historical AQI data"""
    
    cities = {
        "Lahore": {"base_pm25": 80, "variance": 30},
        "Karachi": {"base_pm25": 60, "variance": 20},
        "Islamabad": {"base_pm25": 50, "variance": 15},
        "Faisalabad": {"base_pm25": 70, "variance": 25},
        "Multan": {"base_pm25": 75, "variance": 28}
    }
    
    all_data = []
    
    print(f"Generating {days} days of data for {len(cities)} cities...")
    
    for city, params in cities.items():
        for day in range(days):
            for hour in range(24):
                timestamp = datetime.now() - timedelta(days=days-day, hours=24-hour)
                
                # Add patterns: higher pollution in morning/evening rush hours
                rush_hour_factor = 1.3 if hour in [7, 8, 9, 17, 18, 19] else 1.0
                
                # Add day pattern: worse on weekdays
                weekday_factor = 1.2 if timestamp.weekday() < 5 else 0.8
                
                # Generate values with noise
                pm25 = max(5, params['base_pm25'] * rush_hour_factor * weekday_factor + 
                          np.random.normal(0, params['variance']))
                pm10 = pm25 * 1.5 + np.random.normal(0, 10)
                
                all_data.append({
                    'timestamp': timestamp,
                    'city': city,
                    'aqi': min(5, max(1, int(pm25 / 30) + 1)),
                    'co': max(0, 200 + np.random.normal(0, 50)),
                    'no': max(0, 0.5 + np.random.normal(0, 0.2)),
                    'no2': max(0, 20 + np.random.normal(0, 10)),
                    'o3': max(0, 50 + np.random.normal(0, 20)),
                    'so2': max(0, 10 + np.random.normal(0, 5)),
                    'pm2_5': pm25,
                    'pm10': max(0, pm10),
                    'nh3': max(0, 5 + np.random.normal(0, 2))
                })
    
    df = pd.DataFrame(all_data)
    
    # Create directory if doesn't exist
    os.makedirs("data/raw", exist_ok=True)
    
    # Save to CSV
    df.to_csv("data/raw/aqi_data.csv", index=False)
    print(f"✅ Generated {len(df)} records")
    print(f"✅ Saved to: data/raw/aqi_data.csv")
    print(f"\nSample data:")
    print(df.head())
    print(f"\nData shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    df = generate_historical_data(days=30)
