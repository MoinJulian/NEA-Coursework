@echo off
REM Start script for RuleShot™ application (Windows)
REM This script starts both the Flask backend and Tkinter frontend

echo Starting RuleShot™ Application...

REM Check if .env file exists in api directory
if not exist "api\.env" (
    echo Error: api\.env file not found!
    echo Please copy api\.env.example to api\.env and configure your Supabase credentials.
    pause
    exit /b 1
)

REM Start Flask backend in background
echo Starting Flask backend...
start /B python api\app.py

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Backend started successfully

REM Start Tkinter frontend
echo Starting Tkinter frontend...
python app\main.py

echo Application closed.
pause
