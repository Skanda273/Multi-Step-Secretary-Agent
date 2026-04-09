#!/bin/bash
echo "Running evaluation script..."
python inference.py

echo "Starting UI Server to keep Hugging Face Space running cleanly..."
# Serve the dashboard dist folder on port 7860
python -m http.server 7860 --directory openenv-dashboard/dist
