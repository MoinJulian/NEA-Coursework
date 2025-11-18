#!/bin/bash

# Start script for RuleShot™ application
# This script starts both the Flask backend and Tkinter frontend

echo "Starting RuleShot™ Application..."

# Check if .env file exists in api directory
if [ ! -f "api/.env" ]; then
    echo "Error: api/.env file not found!"
    echo "Please copy api/.env.example to api/.env and configure your Supabase credentials."
    exit 1
fi

# Start Flask backend in background
echo "Starting Flask backend..."
cd api
python app.py &
BACKEND_PID=$!
cd ..

# Wait a few seconds for backend to start
echo "Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Error: Flask backend failed to start"
    exit 1
fi

echo "Backend started successfully (PID: $BACKEND_PID)"

# Start Tkinter frontend
echo "Starting Tkinter frontend..."
cd app
python main.py

# When Tkinter closes, kill the backend
echo "Shutting down backend..."
kill $BACKEND_PID

echo "Application closed."
