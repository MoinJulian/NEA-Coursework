# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Supabase account with a project created
- Git

## Setup Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd NEA-Coursework
```

### 2. Set up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Project Settings → API
3. Copy your `Project URL` and `anon/public` key
4. Go to SQL Editor
5. Run the SQL script from `api/supabase/schema.sql`
   - This will create all tables (users, lessons, completed_lessons)
   - This will insert sample golf rules lessons

### 3. Configure Backend

```bash
cd api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your credentials:
# SUPABASE_URL=your_project_url_here
# SUPABASE_KEY=your_anon_key_here
# JWT_SECRET=your_random_secret_key_here
```

### 4. Configure Frontend

```bash
cd ../app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Run the Application

#### Option A: Use Startup Script (Recommended)

```bash
# From project root
./start.sh      # Linux/Mac
start.bat       # Windows
```

This will:
- Start the Flask backend on port 5000
- Wait for it to initialize
- Launch the Tkinter GUI
- Automatically clean up when you close the GUI

#### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd api
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd app
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

### 6. First Use

1. Click "Register" to create your first account
   - Enter email, username, password (min 8 chars, 1 upper, 1 lower, 1 special)
   - Optionally enter your golf handicap
   
2. Click "Login" to sign in
   - Use either your email or username
   
3. Explore the dashboard
   - View your stats
   - Check the leaderboard
   - Start your first lesson!

## Troubleshooting

### Backend won't start
- Check that `.env` file exists in `api/` directory
- Verify Supabase credentials are correct
- Ensure port 5000 is not already in use

### Frontend can't connect to backend
- Ensure backend is running on http://127.0.0.1:5000
- Check for any firewall blocking localhost connections

### Database errors
- Verify you ran the schema.sql in your Supabase SQL Editor
- Check that tables were created successfully
- Ensure your SUPABASE_KEY has the right permissions

### Import errors
- Make sure you activated the virtual environment
- Re-run `pip install -r requirements.txt`

## Testing the Application

### Test Flow
1. **Registration**: Create an account with all validation
2. **Login**: Sign in with email or username
3. **Dashboard**: View stats and next lesson
4. **Lesson**: Complete a lesson (10 questions)
   - Try answering some wrong to see heart deduction
   - See the retry mechanism for incorrect answers
5. **Leaderboard**: Check your ranking
6. **Settings**: Update email or password
7. **Logout**: Log out and log back in

### Daily Reset Testing
The application resets hearts at 00:00 UTC daily. To test:
- Check your hearts count
- Wait until 00:00 UTC (or modify the scheduler for testing)
- Hearts should reset to 5

## Docker Deployment (Optional)

```bash
# Make sure .env file is configured
docker-compose up --build
```

This will:
- Build the API container
- Start the Flask backend on port 5000
- Note: Tkinter GUI must still be run locally (can't run in container without X11)

## Features to Test

- [x] Registration with validation
- [x] Login with email/username
- [x] Dashboard data display
- [x] Lesson questions and answers
- [x] Hearts deduction on wrong answers
- [x] Retry mechanism for incorrect questions
- [x] XP calculation based on performance
- [x] Streak tracking
- [x] Leaderboard display
- [x] Settings updates
- [x] Account deletion

## Support

If you encounter any issues:
1. Check this guide first
2. Review the README.md for detailed information
3. Check the MIGRATION.md for framework changes
4. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version)
