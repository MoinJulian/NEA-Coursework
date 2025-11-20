"""
Seed script to populate the database with sample lessons and questions.
Run this after setting up the database schema.
"""
from connect import supabase
import uuid


def seed_lessons():
    """Create sample lessons."""
    lessons = [
        {
            "id": str(uuid.uuid4()),
            "title": "Introduction to Grammar",
            "description": "Learn basic grammar rules",
            "order_number": 1
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Common Phrases",
            "description": "Learn commonly used phrases",
            "order_number": 2
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Numbers and Counting",
            "description": "Master numbers from 1 to 100",
            "order_number": 3
        }
    ]
    
    try:
        result = supabase.table("lessons").insert(lessons).execute()
        print(f"✓ Created {len(lessons)} lessons")
        return lessons
    except Exception as e:
        print(f"Error creating lessons: {e}")
        return []


def seed_questions(lessons):
    """Create sample questions for lessons."""
    if not lessons:
        print("No lessons to create questions for")
        return
    
    # Sample questions for lesson 1
    lesson1_id = lessons[0]["id"]
    questions = []
    
    for i in range(10):
        questions.append({
            "id": str(uuid.uuid4()),
            "lesson_id": lesson1_id,
            "question_text": f"Sample question {i+1}: What is the correct form?",
            "question_order": i + 1
        })
    
    try:
        result = supabase.table("questions").insert(questions).execute()
        print(f"✓ Created {len(questions)} questions for lesson 1")
        return questions
    except Exception as e:
        print(f"Error creating questions: {e}")
        return []


def seed_options(questions):
    """Create sample options for questions."""
    if not questions:
        print("No questions to create options for")
        return
    
    options = []
    
    for question in questions:
        question_id = question["id"]
        # Create 4 options per question, with one correct answer
        options.extend([
            {
                "id": str(uuid.uuid4()),
                "question_id": question_id,
                "option_text": "Option A (Correct)",
                "is_correct": True,
                "option_order": 1
            },
            {
                "id": str(uuid.uuid4()),
                "question_id": question_id,
                "option_text": "Option B",
                "is_correct": False,
                "option_order": 2
            },
            {
                "id": str(uuid.uuid4()),
                "question_id": question_id,
                "option_text": "Option C",
                "is_correct": False,
                "option_order": 3
            },
            {
                "id": str(uuid.uuid4()),
                "question_id": question_id,
                "option_text": "Option D",
                "is_correct": False,
                "option_order": 4
            }
        ])
    
    try:
        result = supabase.table("options").insert(options).execute()
        print(f"✓ Created {len(options)} options")
    except Exception as e:
        print(f"Error creating options: {e}")


def main():
    print("Starting database seeding...")
    print("-" * 50)
    
    # Check if tables exist by trying to query them
    try:
        supabase.table("lessons").select("id").limit(1).execute()
        print("✓ Database tables are accessible")
    except Exception as e:
        print(f"✗ Error accessing database tables: {e}")
        print("Please make sure you've run all the SQL migration files first!")
        return
    
    print("\nSeeding data...")
    print("-" * 50)
    
    lessons = seed_lessons()
    questions = seed_questions(lessons)
    seed_options(questions)
    
    print("-" * 50)
    print("✓ Database seeding complete!")
    print("\nYou can now start the application and create a user account.")


if __name__ == "__main__":
    main()