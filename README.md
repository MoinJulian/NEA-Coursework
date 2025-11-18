# NEA Coursework - Language Learning Application

A full-stack language learning application built with FastAPI, Supabase, and Tkinter.

## Tech Stack

- **Backend:** FastAPI
- **Authentication:** Supabase Auth (email/password, JWT)
- **Database:** Supabase Postgres
- **Frontend:** Tkinter (Python GUI)
- **Communication:** HTTPS requests from Tkinter to FastAPI

## Features

### 1. User Registration & Authentication
- Email/password registration with validation
- Username must be unique
- Password requirements: ≥8 chars, uppercase, lowercase, special character
- JWT-based authentication
- Profile creation with default values (xp=0, streak=0, hearts=5)

### 2. User Dashboard
- Display user stats: XP, streak, hearts, lessons completed
- Show next available lesson
- Leaderboard preview (top 5)
- Quick access to start lessons

### 3. Lessons System
- Each lesson contains 10 questions with multiple choice options
- Wrong answer → show correct answer → hearts -1
- Retry incorrect questions until all are answered correctly
- End-of-lesson summary:
  - Accuracy percentage
  - XP earned (max 100, -5 per mistake round)
  - Time taken
  - Updated streak

### 4. Streak System
- +1 per day with at least one completed lesson
- Resets at 00:00 UTC if no lesson completed
- Streak freeze feature available (2 per week)

### 5. Hearts System
- 5 hearts per day
- -1 heart per wrong answer
- If hearts = 0 → lesson ends + streak reset
- Daily reset to 5 hearts at midnight UTC

### 6. Leaderboard
- Sorted by XP descending
- Shows username, XP, and streak
- Pagination support

## Setup Instructions

### Prerequisites
- Python 3.8+
- Supabase account and project
- PostgreSQL database (via Supabase)

### Backend Setup

1. Navigate to the API directory:
```bash
cd api
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `api` directory:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
```

5. Run the database migrations (execute SQL files in `api/supabase/tables/` in your Supabase SQL editor):
   - profiles.sql
   - lessons.sql
   - questions.sql
   - options.sql
   - completed_lessons.sql

6. (Optional) Seed sample data using the seed script:
```bash
python seed_data.py
```

7. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the app directory:
```bash
cd app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Tkinter application:
```bash
python main.py
```

## API Endpoints

### Authentication
- `POST /v1/signup` - Register a new user
- `POST /v1/signin` - Sign in and get JWT tokens

### User Management
- `GET /v1/user` - Get user information
- `PUT /v1/user` - Update user information
- `GET /v1/dashboard` - Get dashboard data

### Lessons
- `GET /v1/lessons/{lesson_id}` - Get lesson with questions
- `POST /v1/lessons/{lesson_id}/questions/{question_id}/answer` - Submit answer
- `POST /v1/lessons/{lesson_id}/complete` - Complete lesson

### Leaderboard
- `GET /v1/leaderboard` - Get leaderboard (paginated)

## Database Schema

### profiles
- id (uuid, FK to auth.users)
- username (text, unique)
- handicap (integer)
- xp (integer, default: 0)
- streak (integer, default: 0)
- hearts (integer, default: 5)
- last_lesson_date (date)
- streak_freezes_used (integer, default: 0)

### lessons
- id (uuid)
- title (text)
- description (text)
- order_number (integer)

### questions
- id (uuid)
- lesson_id (uuid, FK to lessons)
- question_text (text)
- question_order (integer)

### options
- id (uuid)
- question_id (uuid, FK to questions)
- option_text (text)
- is_correct (boolean)
- option_order (integer)

### completed_lessons
- id (uuid)
- user_id (uuid, FK to auth.users)
- lesson_id (uuid, FK to lessons)
- accuracy (numeric)
- xp_earned (integer)
- time_taken (integer, seconds)
- mistakes (integer)
- completed_at (timestamp)

## Development

### Running Tests
```bash
cd api
pytest
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable

## Daily Reset Tasks

The application includes automatic daily reset tasks that run at midnight UTC:
- Reset all users' hearts to 5
- Check and reset streaks for users who haven't completed lessons

These tasks are handled by the `utils/daily_reset.py` module.

## License

See LICENSE file for details.
