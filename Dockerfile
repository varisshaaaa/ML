# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (including those for psycopg2 and xgboost if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port and command
EXPOSE 8000
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}
