# RuleShot™ - Golf Rules Learning Application

A complete application for learning golf rules through interactive lessons, featuring a Flask backend, Tkinter GUI frontend, and Supabase database.

## Features

### User Management
- **Registration**: Email, username, password with validation, and golf handicap
- **Login**: Support for both email and username authentication
- **JWT Authentication**: Secure token-based authentication
- **Settings**: Update email, password, or delete account

### Lesson System
- **Interactive Lessons**: 10 questions per lesson with multiple choice answers
- **Wrong Answer Handling**: Shows correct answer when wrong
- **Retry Mechanism**: Repeat incorrect questions until all are correct
- **Progress Tracking**: Visual progress bar and question counter
- **Results**: Displays accuracy, XP earned, and time taken

### Gamification
- **Hearts System**: 5 hearts per day (resets at 00:00 UTC)
  - Lose 1 heart per wrong answer
  - Lesson cancelled if hearts reach 0, streak resets
- **Streak System**: Daily streak for completing lessons
  - +1 streak for each day with a completed lesson
  - 2 streak freezes per week
  - Resets if no lesson completed before 00:00 UTC
- **XP System**: Earn XP for completing lessons
  - Base: 100 XP per lesson
  - -5 XP per mistake round (retry of incorrect questions)
  - Minimum: 10 XP

### Leaderboard
- Weekly leaderboard sorted by XP
- Shows user's rank
- Pagination support

### Dashboard
- Next lesson to complete
- Current streak display
- Hearts remaining
- Leaderboard preview (top 5)
- Rules completed count
- Total XP

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: Tkinter (Python GUI)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Scheduler**: APScheduler for daily resets

## Project Structure

```
NEA-Coursework/
├── api/                          # Flask Backend
│   ├── app.py                   # Main Flask application
│   ├── connect.py               # Supabase connection
│   ├── scheduler.py             # Daily reset scheduler
│   ├── requirements.txt         # Backend dependencies
│   ├── .env.example            # Environment variables template
│   ├── utils/
│   │   ├── jwt_auth.py         # JWT token utilities
│   │   ├── password.py         # Password hashing utilities
│   │   ├── validation.py       # Input validation utilities
│   │   └── game_logic.py       # Hearts, streak, XP logic
│   └── supabase/
│       └── schema.sql          # Database schema with sample data
├── app/                         # Tkinter Frontend
│   ├── main.py                 # Main application entry point
│   ├── session.py              # Session management
│   ├── api_client.py           # API client wrapper
│   ├── requirements.txt        # Frontend dependencies
│   └── pages/
│       ├── createRegisterPage.py      # Registration page
│       ├── createLoginPage.py         # Login page
│       ├── createDashboardPage.py     # Dashboard page
│       ├── createLessonPage.py        # Lesson page
│       ├── createLeaderboardPage.py   # Leaderboard page
│       └── createSettingsPage.py      # Settings page
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Supabase account and project
- pip (Python package manager)

### Backend Setup

1. Navigate to the API directory:
```bash
cd api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Supabase credentials:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
JWT_SECRET=your_jwt_secret_key_change_in_production
PORT=5000
```

6. Set up the database:
   - Go to your Supabase project
   - Open the SQL Editor
   - Run the contents of `supabase/schema.sql`

7. Run the Flask backend:
```bash
python app.py
```

The backend will start on `http://127.0.0.1:5000`

### Frontend Setup

1. Open a new terminal and navigate to the app directory:
```bash
cd app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Tkinter application:
```bash
python main.py
```

## Usage

1. **Register**: Create a new account with email, username, password, and handicap
2. **Login**: Sign in with your email or username
3. **Dashboard**: View your stats, next lesson, and leaderboard preview
4. **Start Lesson**: Click on "Start Lesson" to begin learning
5. **Answer Questions**: Select answers and get immediate feedback
6. **Complete Lesson**: Finish all questions correctly to earn XP
7. **View Leaderboard**: See how you rank against other players
8. **Settings**: Update your account information

## API Endpoints

### Public Endpoints
- `POST /register` - Register a new user
- `POST /login` - Login with email/username and password

### Protected Endpoints (Require JWT Token)
- `GET /user` - Get current user profile
- `GET /dashboard` - Get dashboard data
- `GET /lessons` - List all lessons
- `GET /lesson/<id>` - Get specific lesson with questions
- `POST /lesson/<id>` - Submit lesson results
- `POST /heart/deduct` - Deduct a heart (wrong answer)
- `GET /leaderboard` - Get leaderboard with pagination
- `PATCH /settings` - Update user settings
- `DELETE /settings` - Delete user account

## Database Schema

### Tables

#### users
- `id` (UUID, Primary Key)
- `email` (VARCHAR, Unique)
- `username` (VARCHAR, Unique)
- `password_hash` (VARCHAR)
- `handicap` (INTEGER)
- `xp` (INTEGER)
- `streak` (INTEGER)
- `streak_freeze_count` (INTEGER)
- `hearts` (INTEGER)
- `last_heart_reset` (TIMESTAMP)
- `last_lesson_date` (DATE)
- `deleted` (BOOLEAN)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### lessons
- `id` (UUID, Primary Key)
- `rule_number` (INTEGER, Unique)
- `title` (VARCHAR)
- `questions` (JSONB) - Array of question objects
- `created_at` (TIMESTAMP)

#### completed_lessons
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `lesson_id` (UUID, Foreign Key)
- `accuracy` (DECIMAL)
- `xp_gained` (INTEGER)
- `time_taken` (INTEGER)
- `created_at` (TIMESTAMP)

## Scheduled Tasks

The application runs the following automated tasks:

- **Daily at 00:00 UTC**: Reset all users' hearts to 5
- **Daily at 00:01 UTC**: Check and reset streaks for users who didn't complete lessons
- **Weekly (Monday at 00:00 UTC)**: Reset streak freeze counts to 0

## Development

### Running Tests
(No tests currently implemented - to be added)

### Code Style
- Follow PEP 8 guidelines for Python code
- Use descriptive variable and function names
- Add docstrings to all functions

## Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with expiring tokens
- **Input Validation**: Email regex, password strength checks
- **SQL Injection Protection**: Supabase client handles parameterized queries
- **Soft Delete**: User accounts are marked as deleted, not removed

## License

See LICENSE file for details.

## Contributors

- MoinJulian

## Support

For issues and questions, please open an issue on GitHub.
