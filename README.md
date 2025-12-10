# Air Quality Health Alert System 🌍🏥

A full-stack AI-powered application that monitors air quality, predicts health risks, and provides real-time alerts.

## 🚀 Key Features
- **Real-time Monitoring**: Fetches live AQI data from OpenWeatherMap.
- **AI Prediction**: XGBoost model predicts future air quality and health risks.
- **Interactive Dashboard**: React-based UI with dark mode, charts, and city selection.
- **Full Ops Pipeline**: Dockerized services for Database (PostgreSQL), Caching (Redis), and Experiment Tracking (MLflow).

---

## 🛠️ Prerequisites (Install these first!)

Since this is a full-stack advanced project, you need the following tools installed:

1.  **Python 3.10+**: [Download Here](https://www.python.org/downloads/)
    *   *Check:* `python --version`
2.  **Node.js (LTS Version)**: [Download Here](https://nodejs.org/) (Required for Frontend)
    *   *Check:* `node -v`
3.  **Docker Desktop**: [Download Here](https://www.docker.com/products/docker-desktop/) (Required for Database & Services)
    *   *Check:* `docker -v`

---

## ⚡ Quick Start Guide

### 1. Backend Setup (Python)

Open a terminal in the project root:

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate Initial Data
python src/generate_sample_data.py
```

### 2. Infrastructure Setup (Docker)

Make sure Docker Desktop is running, then:

```bash
# Start Database, Redis, and MLflow
docker-compose up -d
```

### 3. Frontend Setup (React)

Open a **new** terminal window:

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start the dashboard
npm run dev
```

Visit **http://localhost:5173** to see your app!

---

## 📂 Project Structure

```
├── config/              # Configuration files
├── data/                # Raw and processed datasets
├── frontend/            # React + Vite Application
│   ├── src/             # Frontend source code
│   └── public/          # Static assets
├── models/              # Saved ML models
├── src/                 # Backend Source Code
│   ├── api.py           # FastAPI Backend
│   ├── model_training.py # ML Training Script
│   └── ...
├── docker-compose.yml   # Services definition
└── requirements.txt     # Python dependencies
```

## 🧪 Testing

To run the full pipeline manually:

1.  **Collect Data**: `python src/data_collection.py`
2.  **Process Features**: `python src/feature_engineering.py`
3.  **Train Model**: `python src/model_training.py`
4.  **Start API**: `uvicorn src.api:app --reload`
