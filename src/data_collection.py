import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List
import time

load_dotenv()

class AirQualityDataCollector:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        
        # Major cities coordinates
        self.cities = {
            "Lahore": {"lat": 31.5497, "lon": 74.3436},
            "Karachi": {"lat": 24.8607, "lon": 67.0011},
            "Islamabad": {"lat": 33.6844, "lon": 73.0479},
            "Faisalabad": {"lat": 31.4504, "lon": 73.1350},
            "Multan": {"lat": 30.1575, "lon": 71.5249}
        }
    
    def fetch_current_aqi(self, lat: float, lon: float) -> Dict:
        """Fetch current air quality data"""
        url = f"{self.base_url}?lat={lat}&lon={lon}&appid={self.api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def parse_aqi_data(self, data: Dict, city: str) -> Dict:
        """Parse API response into structured format"""
        if not data or 'list' not in data:
            return None
        
        aqi_data = data['list'][0]
        
        return {
            'timestamp': datetime.fromtimestamp(aqi_data['dt']),
            'city': city,
            'aqi': aqi_data['main']['aqi'],
            'co': aqi_data['components']['co'],
            'no': aqi_data['components']['no'],
            'no2': aqi_data['components']['no2'],
            'o3': aqi_data['components']['o3'],
            'so2': aqi_data['components']['so2'],
            'pm2_5': aqi_data['components']['pm2_5'],
            'pm10': aqi_data['components']['pm10'],
            'nh3': aqi_data['components']['nh3']
        }
    
    def collect_all_cities(self) -> pd.DataFrame:
        """Collect data for all cities"""
        all_data = []
        
        for city, coords in self.cities.items():
            print(f"Fetching data for {city}...")
            data = self.fetch_current_aqi(coords['lat'], coords['lon'])
            parsed = self.parse_aqi_data(data, city)
            
            if parsed:
                all_data.append(parsed)
            
            time.sleep(1)
        
        return pd.DataFrame(all_data)
    
    def save_data(self, df: pd.DataFrame, filepath: str = "data/raw/aqi_data.csv"):
        """Save data to CSV"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if os.path.exists(filepath):
            df.to_csv(filepath, mode='a', header=False, index=False)
        else:
            df.to_csv(filepath, index=False)
        
        print(f"✅ Data saved to {filepath}")

if __name__ == "__main__":
    collector = AirQualityDataCollector()
    df = collector.collect_all_cities()
    print(df.head())
    collector.save_data(df)
