-- Complete Supabase schema for NEA Coursework Application
-- This schema defines all tables needed for the application

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
-- Stores user information including authentication and game progress
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    handicap INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0,
    streak_freeze_count INTEGER DEFAULT 0,
    hearts INTEGER DEFAULT 5,
    last_heart_reset TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_lesson_date DATE,
    deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_deleted ON users(deleted);

-- Lessons table
-- Stores lesson information with questions in JSONB format
CREATE TABLE IF NOT EXISTS lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_number INTEGER UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    questions JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for rule number lookups
CREATE INDEX IF NOT EXISTS idx_lessons_rule_number ON lessons(rule_number);

-- Completed lessons table
-- Tracks user progress on lessons
CREATE TABLE IF NOT EXISTS completed_lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    accuracy DECIMAL(5, 2) NOT NULL,
    xp_gained INTEGER NOT NULL,
    time_taken INTEGER NOT NULL, -- in seconds
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_completed_lessons_user_id ON completed_lessons(user_id);
CREATE INDEX IF NOT EXISTS idx_completed_lessons_lesson_id ON completed_lessons(lesson_id);
CREATE INDEX IF NOT EXISTS idx_completed_lessons_created_at ON completed_lessons(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Sample lesson data
-- Insert some sample lessons with questions
INSERT INTO lessons (rule_number, title, questions) VALUES
(1, 'Basic Golf Rules', '[
    {
        "question": "What is the maximum number of clubs allowed in a golf bag during a tournament?",
        "options": ["12 clubs", "14 clubs", "16 clubs"],
        "correct_answer": 1
    },
    {
        "question": "What should you do if your ball lands in a water hazard?",
        "options": ["Take a penalty stroke and drop behind the hazard", "Play it as it lies", "Get a free drop"],
        "correct_answer": 0
    },
    {
        "question": "When can you repair a pitch mark on the green?",
        "options": ["Only after finishing the hole", "Anytime on the green", "Before putting"],
        "correct_answer": 2
    },
    {
        "question": "What is the penalty for grounding your club in a bunker?",
        "options": ["No penalty", "One stroke penalty", "Two stroke penalty"],
        "correct_answer": 2
    },
    {
        "question": "Can you move a loose impediment in a hazard?",
        "options": ["Yes, always", "No, never", "Only if it does not move the ball"],
        "correct_answer": 1
    },
    {
        "question": "What is a provisional ball?",
        "options": ["A second ball played when the first might be lost", "A practice ball", "A ball used in bad weather"],
        "correct_answer": 0
    },
    {
        "question": "How many minutes do you have to search for a lost ball?",
        "options": ["3 minutes", "5 minutes", "10 minutes"],
        "correct_answer": 0
    },
    {
        "question": "Can you clean your ball on the fairway?",
        "options": ["Yes, always", "Only on the green", "No, never"],
        "correct_answer": 1
    },
    {
        "question": "What is the penalty for hitting the wrong ball?",
        "options": ["No penalty", "One stroke penalty", "Two stroke penalty"],
        "correct_answer": 2
    },
    {
        "question": "Can you remove sand from the green?",
        "options": ["Yes, sand is a loose impediment on the green", "No, never", "Only with a towel"],
        "correct_answer": 0
    }
]'::jsonb),
(2, 'Scoring and Handicaps', '[
    {
        "question": "What does par mean in golf?",
        "options": ["The number of strokes a scratch golfer should take", "The minimum number of strokes", "The maximum number of strokes"],
        "correct_answer": 0
    },
    {
        "question": "What is a birdie?",
        "options": ["One stroke under par", "One stroke over par", "Two strokes under par"],
        "correct_answer": 0
    },
    {
        "question": "What is an eagle?",
        "options": ["One stroke under par", "Two strokes under par", "Three strokes under par"],
        "correct_answer": 1
    },
    {
        "question": "What is a bogey?",
        "options": ["One stroke under par", "Par", "One stroke over par"],
        "correct_answer": 2
    },
    {
        "question": "How is a handicap index calculated?",
        "options": ["Based on your best 10 rounds", "Based on your average score", "Based on your best 8 of your last 20 scores"],
        "correct_answer": 2
    },
    {
        "question": "What is a scratch golfer?",
        "options": ["A golfer with a 0 handicap", "A beginner", "A professional golfer"],
        "correct_answer": 0
    },
    {
        "question": "In match play, what happens when you win a hole?",
        "options": ["You get a point", "You go 1 up", "You get a stroke"],
        "correct_answer": 1
    },
    {
        "question": "What is stroke play?",
        "options": ["Counting total strokes for all holes", "Playing against one opponent", "Playing with a time limit"],
        "correct_answer": 0
    },
    {
        "question": "What is a double bogey?",
        "options": ["One stroke over par", "Two strokes over par", "Three strokes over par"],
        "correct_answer": 1
    },
    {
        "question": "Can you adjust your handicap during a round?",
        "options": ["Yes, after every hole", "No, it is fixed for the round", "Only if approved by the committee"],
        "correct_answer": 1
    }
]'::jsonb),
(3, 'Etiquette and Safety', '[
    {
        "question": "What should you do before hitting your shot?",
        "options": ["Check that no one is in range ahead", "Take a practice swing", "Mark your ball"],
        "correct_answer": 0
    },
    {
        "question": "Who plays first on the tee?",
        "options": ["The player with the lowest handicap", "The player with honors from the previous hole", "The youngest player"],
        "correct_answer": 1
    },
    {
        "question": "What should you do with divots?",
        "options": ["Leave them", "Replace them or fill with sand/seed mix", "Collect them"],
        "correct_answer": 1
    },
    {
        "question": "Should you walk on someone else''s putting line?",
        "options": ["Yes, it does not matter", "No, avoid walking on the line", "Only if you are closer to the hole"],
        "correct_answer": 1
    },
    {
        "question": "What is the proper pace of play?",
        "options": ["As fast as possible", "Keep up with the group ahead", "Take your time for each shot"],
        "correct_answer": 1
    },
    {
        "question": "When should you yell fore?",
        "options": ["When your ball might hit someone", "When you hit a bad shot", "When you make a birdie"],
        "correct_answer": 0
    },
    {
        "question": "Should you talk during someone else''s shot?",
        "options": ["Yes, to encourage them", "No, maintain silence", "Only if they ask"],
        "correct_answer": 1
    },
    {
        "question": "How should you rake a bunker after playing from it?",
        "options": ["Leave it as is", "Rake it smooth from the entry point", "Only rake where you hit from"],
        "correct_answer": 1
    },
    {
        "question": "Can you use your phone on the course?",
        "options": ["Yes, anytime", "Only for emergencies or scoring apps", "No, never"],
        "correct_answer": 1
    },
    {
        "question": "What should you do if you are playing slowly?",
        "options": ["Continue at your pace", "Let faster groups play through", "Speed up only on the last hole"],
        "correct_answer": 1
    }
]'::jsonb)
ON CONFLICT (rule_number) DO NOTHING;
