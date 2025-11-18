# Quick Reference Guide

## Common Commands

### Backend (FastAPI)

```bash
# Setup
cd api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Supabase credentials

# Run server
uvicorn main:app --reload

# Run with custom host/port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Seed database
python seed_data.py

# Run tests
python test_validation.py
```

### Frontend (Tkinter)

```bash
# Setup
cd app
pip install -r requirements.txt

# Run application
python main.py
```

### Database Setup (Supabase SQL Editor)

Run these SQL files in order:
1. `api/supabase/tables/profiles.sql`
2. `api/supabase/tables/lessons.sql`
3. `api/supabase/tables/questions.sql`
4. `api/supabase/tables/options.sql`
5. `api/supabase/tables/completed_lessons.sql`

## API Endpoints Reference

### Authentication
```bash
# Register
POST http://127.0.0.1:8000/v1/signup
Content-Type: application/json
{
  "email": "user@example.com",
  "username": "testuser",
  "handicap": 10,
  "password": "SecurePass123!"
}

# Login
POST http://127.0.0.1:8000/v1/signin
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### User Management
```bash
# Get user info
GET http://127.0.0.1:8000/v1/user
Authorization: Bearer <access_token>

# Get dashboard
GET http://127.0.0.1:8000/v1/dashboard
Authorization: Bearer <access_token>

# Update user
PUT http://127.0.0.1:8000/v1/user
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "email": "newemail@example.com",
  "password": "NewPass123!"
}
```

### Lessons
```bash
# Get lesson
GET http://127.0.0.1:8000/v1/lessons/{lesson_id}
Authorization: Bearer <access_token>

# Submit answer
POST http://127.0.0.1:8000/v1/lessons/{lesson_id}/questions/{question_id}/answer
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "selected_option_id": "<option_uuid>"
}

# Complete lesson
POST http://127.0.0.1:8000/v1/lessons/{lesson_id}/complete
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "accuracy": 85.5,
  "time_taken": 120,
  "mistakes": 2
}
```

### Leaderboard
```bash
# Get leaderboard
GET http://127.0.0.1:8000/v1/leaderboard?page=1&per_page=10
Authorization: Bearer <access_token>
```

## Common Issues & Solutions

### Issue: "No module named 'fastapi'"
**Solution**: Make sure you've activated the virtual environment and installed dependencies
```bash
cd api
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Connection refused" when running Tkinter app
**Solution**: Make sure the FastAPI server is running on port 8000
```bash
cd api
uvicorn main:app --reload
```

### Issue: "Authorization token required"
**Solution**: Make sure you're logged in and the session has an access_token. The token is obtained during login.

### Issue: Database tables don't exist
**Solution**: Run all SQL migration files in your Supabase SQL editor in the correct order (see Database Setup above)

### Issue: No lessons available
**Solution**: Run the seed script to create sample lessons
```bash
cd api
python seed_data.py
```

### Issue: "Profile not found"
**Solution**: Make sure the profiles table was created and the signup process completed successfully

## Password Requirements

When creating an account, passwords must meet these criteria:
- ✅ At least 8 characters long
- ✅ Contains at least one uppercase letter (A-Z)
- ✅ Contains at least one lowercase letter (a-z)
- ✅ Contains at least one special character (!@#$%^&*(),.?":{}|<>)

Examples of valid passwords:
- `SecurePass123!`
- `MyP@ssw0rd`
- `Test1234!@`

## Game Mechanics

### Hearts System
- Start with 5 hearts per day
- Lose 1 heart for each wrong answer
- If hearts reach 0, the lesson ends
- Hearts reset to 5 at midnight UTC

### Streak System
- Gain 1 streak for each day with at least one completed lesson
- Streak resets if no lesson completed by midnight UTC
- Consecutive days build your streak
- Streak is displayed on dashboard

### XP (Experience Points)
- Base reward: 100 XP per lesson
- Penalty: -5 XP for each mistake round
- Minimum: 0 XP (cannot go negative)
- XP accumulates and determines leaderboard position

### Lessons
- Each lesson has 10 questions
- Multiple choice format
- Must answer all questions correctly to complete
- Incorrect answers must be retried
- Time is tracked for leaderboard purposes

## Troubleshooting Checklist

Before asking for help, verify:
- [ ] Python 3.8+ is installed
- [ ] Virtual environment is activated
- [ ] All dependencies are installed
- [ ] .env file exists with correct Supabase credentials
- [ ] Supabase tables are created
- [ ] FastAPI server is running on port 8000
- [ ] No firewall blocking localhost connections
- [ ] Tkinter is installed (usually comes with Python)

## Useful URLs

When the backend is running:
- **API Root**: http://127.0.0.1:8000/
- **API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **API Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

## Development Tips

1. **Use API docs**: Visit `/docs` for interactive API testing
2. **Check logs**: FastAPI outputs detailed logs in the terminal
3. **Test validation**: Run `python test_validation.py` before deploying
4. **Monitor database**: Use Supabase dashboard to view data
5. **Debug mode**: Use `--reload` flag to auto-reload on code changes

## Environment Variables

Required in `api/.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
```

Get these from:
1. Go to your Supabase project
2. Settings → API
3. Copy Project URL and service_role key

## Next Steps After Setup

1. **Create first user**: Run Tkinter app and register
2. **Add lessons**: Run seed script or create manually in Supabase
3. **Test lesson flow**: Complete a lesson to verify XP, hearts, streak
4. **Check leaderboard**: Verify user appears with correct XP
5. **Test daily reset**: Wait until midnight UTC or manually trigger

## Support

For issues:
1. Check this quick reference
2. Review README.md for detailed setup
3. Check ARCHITECTURE.md for system design
4. Review IMPLEMENTATION.md for feature details
5. Check API logs for error messages
6. Verify Supabase connection and tables
