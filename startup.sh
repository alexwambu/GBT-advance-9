#!/bin/bash

# Create required directories if they don't exist
mkdir -p static/logo
mkdir -p deployed_app

# Optionally touch default logo if none exists
if [ ! -f static/logo/logo.png ]; then
  echo "Creating placeholder logo..."
  curl -o static/logo/logo.png https://via.placeholder.com/150
fi

# Start the FastAPI application using uvicorn
echo "Launching FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 10000
