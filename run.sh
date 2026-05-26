#!/bin/bash

echo "🏗️ Starting AI Estimating Assistant..."

# Check if docker is running and start DB
if command -v docker-compose &> /dev/null; then
    docker-compose up -d
elif command -v docker &> /dev/null; then
    docker compose up -d
else
    echo "⚠️ Docker is not installed or not in PATH. Skipping DB startup."
fi

# Start Backend in background
echo "🚀 Starting FastAPI Backend on port 8000..."
source .venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start Frontend
echo "🎨 Starting Streamlit Frontend on port 8501..."
streamlit run frontend/app.py

# When frontend exits, kill backend
kill $BACKEND_PID
