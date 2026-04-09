#!/bin/bash
echo "Running evaluation script..."
python inference.py

echo "Starting OpenEnv API Server..."
python app.py
