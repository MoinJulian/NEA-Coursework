# Migration from FastAPI to Flask

This document explains the changes made to convert the application from FastAPI to Flask.

## Key Changes

### 1. API Framework
- **Before**: FastAPI with async/await
- **After**: Flask with synchronous endpoints

### 2. Main Application File
- **Old**: `api/main.py` using FastAPI
- **New**: `api/app.py` using Flask

The old files (`api/main.py`, `api/auth/`, `api/routes/`) are kept for reference but are no longer used.

### 3. Authentication
- **Before**: Relied on Supabase Auth
- **After**: Custom JWT authentication with:
  - bcrypt for password hashing
  - Custom JWT token generation and verification
  - Decorator-based auth middleware (`@require_auth`)

### 4. Database Schema
- **Before**: Limited schema (basic lessons table)
- **After**: Complete schema with:
  - Extended users table with game mechanics (xp, streak, hearts)
  - Lessons table with JSONB questions
  - Completed lessons tracking
  - Sample data included

### 5. New Features Implemented

#### Backend
- Password validation (8+ chars, uppercase, lowercase, special char)
- Email validation with regex
- Username support for login
- Hearts system (5/day, reset at 00:00 UTC)
- Streak system with freeze support
- XP calculation based on performance
- Daily reset scheduler using APScheduler
- Comprehensive dashboard endpoint
- Leaderboard with pagination

#### Frontend
- Complete redesign of all pages
- API client wrapper for clean separation
- Dashboard with stats and next lesson
- Interactive lesson page with retry mechanism
- Leaderboard page with ranking
- Settings page with account management
- Proper session management

## File Structure Changes

### New Backend Files
```
api/
├── app.py (new main application)
├── scheduler.py (daily reset tasks)
├── utils/
│   ├── jwt_auth.py (JWT utilities)
│   ├── password.py (password hashing)
│   ├── validation.py (input validation)
│   └── game_logic.py (hearts, streak, XP)
└── supabase/
    └── schema.sql (complete database schema)
```

### New Frontend Files
```
app/
├── api_client.py (API wrapper)
├── session.py (updated session management)
└── pages/
    ├── createDashboardPage.py (new)
    ├── createLessonPage.py (new)
    ├── createLeaderboardPage.py (new)
    └── createSettingsPage.py (new)
```

## Running the Application

### Using the Old FastAPI Version
```bash
cd api
python main.py
# Uses FastAPI with Supabase Auth
```

### Using the New Flask Version
```bash
# Option 1: Use startup script
./start.sh  # Linux/Mac
start.bat   # Windows

# Option 2: Manual start
# Terminal 1 - Backend
cd api
python app.py

# Terminal 2 - Frontend
cd app
python main.py
```

## API Endpoint Changes

### Old FastAPI Endpoints
- POST `/v1/signup`
- POST `/v1/signin`
- GET `/v1/user`
- PUT `/v1/user`

### New Flask Endpoints
- POST `/register`
- POST `/login`
- GET `/user`
- GET `/dashboard`
- GET `/lessons`
- GET `/lesson/<id>`
- POST `/lesson/<id>`
- POST `/heart/deduct`
- GET `/leaderboard`
- PATCH `/settings`
- DELETE `/settings`

## Environment Variables

Both versions use `.env` file in the `api` directory, but Flask version adds:
- `JWT_SECRET` - for JWT token signing
- `PORT` - Flask port (default 5000)

## Dependencies Changes

### FastAPI Version
- FastAPI
- Uvicorn
- Supabase client with auth

### Flask Version
- Flask
- Flask-CORS
- bcrypt (for password hashing)
- PyJWT (for JWT tokens)
- APScheduler (for daily resets)
- Supabase client (for database only)

## Notes

1. The old FastAPI implementation is preserved in `api/main.py` and related files but is not used by the new system.
2. The new Flask implementation follows the specification more closely with custom authentication and game mechanics.
3. All business logic (hearts, streak, XP) is implemented in the Flask backend.
4. The Tkinter client communicates exclusively with the Flask API through the `api_client.py` wrapper.
