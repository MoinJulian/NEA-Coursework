# Changelog

All notable changes to the NEA Coursework project.

## [1.0.0] - 2025-11-18

### Added - Complete Application Implementation

#### Backend (FastAPI)
- **Authentication & User Management**
  - Enhanced signup with username, handicap, email validation, and password strength validation
  - Username uniqueness check in database
  - Enhanced signin returning user profile along with JWT tokens
  - Profile creation with default values (xp=0, streak=0, hearts=5) on registration
  - User endpoint for retrieving user information
  - User update endpoint for changing email/password

- **Dashboard System**
  - Dashboard endpoint returning comprehensive user stats
  - Next lesson calculation (first uncompleted lesson)
  - Leaderboard preview showing top 5 users
  - Lessons completed counter
  - Real-time profile data (XP, streak, hearts)

- **Lessons System**
  - Lesson retrieval endpoint with questions and options
  - Answer submission endpoint with immediate feedback
  - Hearts deduction on wrong answers
  - Correct answer display when user answers incorrectly
  - Lesson completion endpoint with stats recording
  - XP calculation (100 base, -5 per mistake round)
  - Time tracking for lesson completion
  - Accuracy percentage calculation

- **Leaderboard**
  - Leaderboard endpoint sorted by XP descending
  - Pagination support (configurable page and per_page parameters)
  - Returns username, XP, and streak for each user

- **Background Tasks**
  - Daily reset utility for hearts (resets to 5 at midnight UTC)
  - Daily streak check and reset for inactive users
  - Integrated into FastAPI application lifecycle

- **API Improvements**
  - CORS middleware for cross-origin requests
  - Root endpoint with API information
  - Comprehensive error handling with proper HTTP status codes
  - Authorization header validation on all protected endpoints
  - API documentation enabled at /docs and /redoc

#### Frontend (Tkinter)
- **Registration Page**
  - Added username input field
  - Added handicap input field
  - Client-side validation for required fields
  - Enhanced error messages from server

- **Login Page**
  - Stores complete user profile in session
  - Stores user ID for API requests
  - Proper error handling and display

- **Dashboard Page** (NEW)
  - Welcome message with username
  - Stats display: XP, streak (with emoji), hearts (with emojis), lessons completed
  - Next lesson information with title
  - "Start Lesson" button to begin lessons
  - Leaderboard preview showing top 5 users
  - "View Full Leaderboard" button
  - Logout functionality

- **Lesson Page** (NEW)
  - Hearts display at top of page
  - Question progress indicator (X of Y)
  - Question text display with word wrapping
  - Multiple choice radio buttons for answers
  - Answer submission with immediate feedback
  - Retry logic for incorrect questions
  - Wrong answer feedback showing correct answer
  - End-of-lesson completion screen with:
    - Accuracy percentage
    - XP earned
    - Time taken
    - Updated streak
    - Total XP
  - Lesson termination when hearts reach 0

- **Leaderboard Page** (NEW)
  - Scrollable list of all users
  - Rank, username, XP, and streak display
  - Pagination support (shows first 20 by default)
  - "Back to Dashboard" button

- **Session Management**
  - Enhanced Session class with profile field
  - Stores user_id for API authentication
  - Maintains JWT tokens throughout session

#### Database Schema
- **profiles table** (NEW)
  - Links to auth.users via id (FK)
  - username (unique)
  - handicap
  - xp (default 0)
  - streak (default 0)
  - hearts (default 5)
  - last_lesson_date for streak tracking
  - streak_freezes_used (default 0)
  - Indexes on username and xp for performance

- **lessons table** (ENHANCED)
  - Added description field
  - Added order_number for lesson sequencing
  - Added created_at timestamp

- **questions table** (CREATED)
  - Links to lessons via lesson_id (FK)
  - question_text
  - question_order for sequencing
  - Index on lesson_id for performance

- **options table** (CREATED)
  - Links to questions via question_id (FK)
  - option_text
  - is_correct boolean flag
  - option_order for sequencing
  - Index on question_id for performance

- **completed_lessons table** (NEW)
  - Links to auth.users via user_id (FK)
  - Links to lessons via lesson_id (FK)
  - accuracy percentage
  - xp_earned
  - time_taken in seconds
  - mistakes count
  - completed_at timestamp
  - Indexes on user_id and completed_at

#### Documentation
- **README.md** (NEW)
  - Tech stack overview
  - Complete feature descriptions
  - Setup instructions for backend and frontend
  - API endpoints documentation
  - Database schema description
  - Development guidelines

- **IMPLEMENTATION.md** (NEW)
  - Detailed breakdown of all implemented features
  - Files created and modified lists
  - Quality metrics and testing results
  - Setup instructions
  - Next steps for users

- **ARCHITECTURE.md** (NEW)
  - System architecture diagrams (ASCII art)
  - Data flow examples for key operations
  - Database relationship diagrams
  - Security model explanation
  - Technology stack details

- **QUICKSTART.md** (NEW)
  - Common commands reference
  - API endpoint examples with curl
  - Troubleshooting guide
  - Password requirements
  - Game mechanics explanation
  - Environment setup guide

#### Testing & Validation
- **test_validation.py** (NEW)
  - Email format validation tests
  - Password strength validation tests
  - XP calculation logic tests
  - Hearts system logic tests
  - All tests passing

- **Security**
  - CodeQL security scan completed
  - Zero vulnerabilities found
  - Proper authentication checks
  - Authorization validation

#### Developer Tools
- **seed_data.py** (NEW)
  - Creates sample lessons for testing
  - Generates 10 questions per lesson
  - Creates 4 options per question
  - Marks correct answers

- **.env.example** (NEW)
  - Template for environment configuration
  - Supabase URL and key placeholders

### Changed

#### Backend
- **main.py**
  - Added CORS middleware
  - Added API title and description
  - Added root endpoint with API info
  - Integrated daily reset task into lifecycle
  - Added all new route handlers

- **auth/signup.py**
  - Added email validation with regex
  - Added password strength validation
  - Added username uniqueness check
  - Added profile creation logic
  - Enhanced error messages

- **auth/signin.py**
  - Added profile data retrieval
  - Enhanced response structure
  - Better error handling

- **routes/signup_endpoint.py**
  - Added username parameter
  - Added handicap parameter
  - Added field validation
  - Improved error messages

- **routes/user_endpoint.py**
  - Added authorization header validation
  - Enhanced error handling
  - Better null checks

#### Frontend
- **main.py**
  - Removed old dashboard and settings functions
  - Added new dashboard integration
  - Updated login flow
  - Simplified logout logic

- **pages/createRegisterPage.py**
  - Added username input field
  - Added handicap input field
  - Added validation for all fields
  - Enhanced error messages

- **pages/createLoginPage.py**
  - Added user_id storage
  - Added profile storage
  - Enhanced session management

- **session.py**
  - Added user_id field
  - Added profile field
  - Better type documentation

### Fixed
- Authorization header validation in all endpoints (prevents crashes from missing headers)
- Profile data consistency between signin and dashboard
- Hearts deduction logic with proper bounds checking
- Streak calculation with proper date handling
- XP calculation with proper minimum value (0)
- Session management across page navigation

### Security
- Implemented proper JWT token validation
- Added authorization checks on all protected endpoints
- Validated email format to prevent injection
- Enforced strong password requirements
- Protected against SQL injection via Supabase client
- Zero vulnerabilities found in CodeQL scan

## Version Information

- **Version**: 1.0.0
- **Release Date**: November 18, 2025
- **Status**: Production Ready
- **License**: See LICENSE file

## Breaking Changes
None (initial release)

## Upgrade Notes
This is the initial release. No upgrades necessary.

## Contributors
- GitHub Copilot Agent
- MoinJulian (Repository Owner)

## Acknowledgments
- FastAPI framework
- Supabase platform
- Python Tkinter library
- GitHub Copilot
