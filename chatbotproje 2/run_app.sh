#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Application..."
echo "Access at: http://localhost:8000"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
