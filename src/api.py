from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import redis
import json
import os
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="Air Quality Health Alert API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis
try:
    redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
except Exception as e:
    print(f"Warning: Redis connection failed: {e}")
    redis_client = None

# Load Model
model_path = "models/saved_models/xgboost_aqi_model.pkl"
model = None
try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
except Exception as e:
    print(f"Warning: Could not load model: {e}")

class PredictionRequest(BaseModel):
    pm2_5: float
    pm10: float
    no2: float
    so2: float
    o3: float
    co: float
    city: str
    hour: int
    day_of_week: int

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "Air Quality Alert System"}

@app.get("/api/current/{city}")
def get_current_aqi(city: str):
    """Get latest cached AQI for a city"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis service unavailable")
        
    data = redis_client.get(f"aqi:latest:{city}")
    if not data:
        raise HTTPException(status_code=404, detail=f"No data found for {city}")
        
    return json.loads(data)

@app.post("/api/predict")
def predict_health_risk(request: PredictionRequest):
    """Predict future AQI and health risk"""
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Prepare input vector (simplified for demo)
    # In production, you'd need to reconstruct all lag features or fetch them from a feature store
    try:
        # Mocking complex features for simplicity
        input_data = pd.DataFrame([{
            'pm2_5': request.pm2_5,
            'pm10': request.pm10,
            'no2': request.no2,
            'so2': request.so2,
            'o3': request.o3,
            'co': request.co,
            'hour': request.hour,
            'day_of_week': request.day_of_week,
            'month': datetime.now().month,
            'is_weekend': 1 if request.day_of_week >= 5 else 0,
            'is_rush_hour': 1 if request.hour in [7, 8, 9, 17, 18, 19] else 0,
            'pm_ratio': request.pm2_5 / (request.pm10 + 1),
            'health_risk_score': 0, # Placeholder
            'pm2_5_lag_1h': request.pm2_5, # Placeholder
            'pm2_5_lag_24h': request.pm2_5, # Placeholder
            'pm2_5_rolling_mean_24h': request.pm2_5, # Placeholder
            'aqi_lag_1h': 50, # Placeholder
            'aqi_lag_24h': 50 # Placeholder
        }])
        
        # Calculate health risk score dynamically
        input_data['health_risk_score'] = (
            (request.pm2_5 / 150 * 40) +
            (request.pm10 / 250 * 30) +
            (request.no2 / 200 * 15) +
            (request.o3 / 180 * 10) +
            (request.so2 / 100 * 5)
        ).clip(0, 100)
        
        prediction = model.predict(input_data)[0]
        
        risk_level = "Low"
        if prediction > 100: risk_level = "Moderate"
        if prediction > 150: risk_level = "High"
        if prediction > 200: risk_level = "Critical" # fixed typo: Citical -> Critical
        
        return {
            "predicted_aqi": float(prediction),
            "risk_level": risk_level,
            "health_risk_score": float(input_data['health_risk_score'].iloc[0])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "database": "connected" if os.getenv("DATABASE_URL") else "not_configured",
        "redis": "connected" if redis_client else "unavailable",
        "model": "loaded" if model else "not_loaded"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
