# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        TKINTER CLIENT (GUI)                      │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │  Register  │  │   Login    │  │ Dashboard  │  │ Lessons  │ │
│  │    Page    │  │    Page    │  │    Page    │  │   Page   │ │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │         Session Management             │                    │
│  │  (JWT tokens, user profile)            │                    │
│  └────────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS Requests
                              │ (Authorization: Bearer <JWT>)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                          │  │
│  │  • /v1/signup          • /v1/dashboard                   │  │
│  │  • /v1/signin          • /v1/leaderboard                 │  │
│  │  • /v1/user            • /v1/lessons/{id}                │  │
│  │  • /v1/lessons/{id}/questions/{id}/answer                │  │
│  │  • /v1/lessons/{id}/complete                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               Business Logic Layer                        │  │
│  │  • Validation (email, password)                          │  │
│  │  • Authentication (JWT)                                   │  │
│  │  • Authorization (token verification)                     │  │
│  │  • XP Calculation                                         │  │
│  │  • Streak Management                                      │  │
│  │  • Hearts Management                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Background Tasks                               │  │
│  │  • Daily Reset (Hearts: 5, Streaks: check)              │  │
│  │  • Runs at midnight UTC                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Supabase Python Client
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SUPABASE SERVICES                             │
│                                                                  │
│  ┌────────────────────┐         ┌──────────────────────┐       │
│  │  Supabase Auth     │         │  Postgres Database   │       │
│  │                    │         │                      │       │
│  │  • User Creation   │         │  Tables:             │       │
│  │  • Authentication  │         │  • profiles          │       │
│  │  • JWT Generation  │         │  • lessons           │       │
│  │  • Token Refresh   │         │  • questions         │       │
│  │                    │         │  • options           │       │
│  └────────────────────┘         │  • completed_lessons │       │
│                                  └──────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### 1. User Registration Flow
```
User (Tkinter) → Register Form
                 ↓
              [Input: email, username, handicap, password]
                 ↓
POST /v1/signup ←
                 ↓
         [Validate Email Format]
         [Validate Password Strength]
         [Check Username Uniqueness]
                 ↓
         Supabase Auth.sign_up()
                 ↓
         Create Profile Record
         (xp=0, streak=0, hearts=5)
                 ↓
              Success Response
                 ↓
User (Tkinter) ← Display Success Message
```

### 2. User Login Flow
```
User (Tkinter) → Login Form
                 ↓
              [Input: email, password]
                 ↓
POST /v1/signin ←
                 ↓
         Supabase Auth.sign_in_with_password()
                 ↓
         Fetch User Profile from DB
                 ↓
         Return {
           session: {access_token, refresh_token},
           user: {id, email},
           profile: {username, xp, streak, hearts, ...}
         }
                 ↓
User (Tkinter) ← Store JWT + Profile in Session
                 ↓
              Navigate to Dashboard
```

### 3. Lesson Flow
```
User (Tkinter) → Click "Start Lesson"
                 ↓
GET /v1/lessons/{id} ←
[Authorization: Bearer <JWT>]
                 ↓
         [Verify JWT Token]
         [Check Hearts > 0]
         [Fetch Lesson + Questions + Options]
                 ↓
User (Tkinter) ← Display Question 1 of 10
                 ↓
              [User Selects Answer]
                 ↓
POST /v1/lessons/{id}/questions/{qid}/answer ←
[Authorization: Bearer <JWT>]
                 ↓
         [Check if Answer Correct]
         [If Wrong: Hearts -= 1]
         [Return Correct Answer if Wrong]
                 ↓
User (Tkinter) ← Show Feedback
                 ↓
              [Repeat for All Questions]
              [Retry Incorrect Questions]
                 ↓
POST /v1/lessons/{id}/complete ←
[accuracy, time_taken, mistakes]
                 ↓
         [Calculate XP: 100 - (mistakes * 5)]
         [Update Profile: xp, streak, last_lesson_date]
         [Insert to completed_lessons]
                 ↓
User (Tkinter) ← Show End-of-Lesson Screen
              (accuracy, xp earned, time, streak)
```

### 4. Daily Reset Flow
```
Background Task (FastAPI) → Wait until midnight UTC
                            ↓
                    [Execute Daily Reset]
                            ↓
              ┌─────────────┴─────────────┐
              ▼                           ▼
    Reset All Hearts to 5      Check Last Lesson Date
                               for Each User
                                    ↓
                            [If > 1 day ago]
                                    ↓
                            Reset Streak to 0
```

## Database Schema Relationships

```
auth.users (Supabase)
    │
    └─── profiles (1:1)
            │ id (FK)
            │
            ├─── completed_lessons (1:N)
            │      │ user_id (FK)
            │      │ lesson_id (FK)
            │      └─→ lessons
            │
            └─── [stats: xp, streak, hearts]

lessons
    │
    └─── questions (1:N)
            │ lesson_id (FK)
            │
            └─── options (1:N)
                   │ question_id (FK)
                   └─ [is_correct: boolean]
```

## Security Model

1. **Authentication**: JWT-based via Supabase Auth
2. **Authorization**: Bearer token in Authorization header
3. **Validation**: 
   - Email format validation
   - Password strength requirements
   - Username uniqueness
4. **Error Handling**: Proper HTTP status codes and error messages
5. **CORS**: Configured for cross-origin requests

## Key Features Implementation

### Hearts System
- Initial: 5 hearts per user
- Deduction: -1 heart per wrong answer
- Reset: Daily at midnight UTC
- Impact: If hearts = 0, lesson ends

### Streak System
- Calculation: Days with at least one lesson completed
- Update: On lesson completion
- Reset: Midnight UTC if no lesson completed previous day
- Freeze: Supported (2 per week, tracked in DB)

### XP System
- Base: 100 XP per lesson
- Penalty: -5 XP per mistake round
- Minimum: 0 XP
- Accumulation: Added to total XP in profile

### Leaderboard
- Sort: By XP (descending)
- Pagination: Configurable page size
- Display: Username, XP, Streak
- Update: Real-time based on DB queries

## Technology Stack

- **Backend**: Python 3.8+ with FastAPI
- **Frontend**: Python with Tkinter
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: Supabase Auth (JWT)
- **Communication**: HTTP/HTTPS with JSON
- **Background Tasks**: AsyncIO with FastAPI lifecycle
- **Documentation**: OpenAPI (Swagger) at /docs
