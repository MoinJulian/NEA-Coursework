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
            "title": "Foundations of the Rules of Golf",
            "description": "Understand the overall structure of the rules and key definitions every player must know.",
            "order_number": 1
        },
        {
            "id": str(uuid.uuid4()),
            "title": "How a Hole Is Played",
            "description": "Learn the sequence from teeing area to holing out, including proper pace of play and etiquette.",
            "order_number": 2
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Taking Relief: Free and Penalty",
            "description": "Covers unplayable balls, penalty areas, abnormal course conditions, and how to drop correctly.",
            "order_number": 3
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Ball Lost, Moved, or Wrong Ball",
            "description": "Handles common on-course incidents and the correct procedures to avoid unnecessary penalties.",
            "order_number": 4
        },
        {
            "id": str(uuid.uuid4()),
            "title": "On-Course Situations and Common Misunderstandings",
            "description": "Real-world examples: provisional balls, out of bounds, embedded balls, and frequent rule mistakes.",
            "order_number": 5
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
    
    questions = [
        # --- LESSON 1 ---
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "What is the definition of a “ball in play”?",
            "question_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "When does a ball become “lost” under the Rules of Golf?",
            "question_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "What is the purpose of the “definitions” section in the rulebook?",
            "question_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "When does a stroke count as made?",
            "question_order": 4
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "What is the general penalty in stroke play?",
            "question_order": 5
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "What is considered “abnormal course condition”?",
            "question_order": 6
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "What is the difference between “temporary water” and a “penalty area”?",
            "question_order": 7
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "When is a ball considered “at rest”?",
            "question_order": 8
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "What is the definition of a “stroke-and-distance” relief?",
            "question_order": 9
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[0]["id"],
            "question_text": "When does a player receive no penalty for accidentally moving their ball?",
            "question_order": 10
        },
        # --- LESSON 2 ---
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "Where must a player play from when starting a hole?",
            "question_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "What happens if a player tees off outside the teeing area?",
            "question_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "In which order should players generally play on the course?",
            "question_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "What is “Ready Golf”?",
            "question_order": 4
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "When is a ball considered holed?",
            "question_order": 5
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "What must a player do if their ball might interfere with another player?",
            "question_order": 6
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "What are a player’s options if their ball lies on the wrong green?",
            "question_order": 7
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "When may a player clean their ball?",
            "question_order": 8
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "What is the penalty for playing a shot from the wrong place?",
            "question_order": 9
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[1]["id"],
            "question_text": "What is the recommended pace-of-play guideline?",
            "question_order": 10
        },
        # --- LESSON 3 ---
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "When is a player allowed free relief from abnormal course conditions?",
            "question_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "What defines the “nearest point of complete relief”?",
            "question_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "What is the correct procedure for dropping a ball?",
            "question_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "How many club-lengths are allowed for free relief?",
            "question_order": 4
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "When can a player declare a ball unplayable?",
            "question_order": 5
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "What are the three relief options for an unplayable ball?",
            "question_order": 6
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "What is the standard penalty for taking unplayable-ball relief?",
            "question_order": 7
        },
        {            
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "When is relief allowed from a dangerous animal condition?",
            "question_order": 8
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "What determines the size of a “relief area”?",
            "question_order": 9
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[2]["id"],
            "question_text": "What relief options exist for a ball in a penalty area?",
            "question_order": 10
        },
        # --- LESSON 4 ---
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "After how many minutes of search is a ball officially lost?",
            "question_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "When does a player not receive a penalty for accidentally moving their ball?",
            "question_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "What must a player do after playing a wrong ball?",
            "question_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "When can a player replace a moved ball without penalty?",
            "question_order": 4
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "What is the penalty for playing a wrong ball in stroke play?",
            "question_order": 5
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "What happens if natural forces move a ball on the putting green?",
            "question_order": 6
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "When must a ball be replaced versus played from its new spot?",
            "question_order": 7
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "What are the options when a ball might be lost or out of bounds?",
            "question_order": 8
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "What is the purpose of a provisional ball?",
            "question_order": 9
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[3]["id"],
            "question_text": "When does a provisional ball become the ball in play?",
            "question_order": 10
        },
        # --- LESSON 5 ---
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "When is a provisional ball allowed?",
            "question_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "What is the penalty for hitting a ball out of bounds?",
            "question_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "How does a player identify an embedded ball?",
            "question_order": 3
        },
        {            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "When may a player take relief from an embedded ball?",
            "question_order": 4
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "What is the penalty for hitting another player’s equipment?",
            "question_order": 5
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "How must players mark their ball on the green?",
            "question_order": 6
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "What happens if a player accidentally hits their ball during a practice swing?",
            "question_order": 7
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "What are a player’s options if their ball hits a tree and returns behind them?",
            "question_order": 8
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "What must a player do if their ball stops against a flagstick that is in the hole?",
            "question_order": 9
        },
        {
            "id": str(uuid.uuid4()),
            "lesson_id": lessons[4]["id"],
            "question_text": "What is the correct procedure if a ball is suspected to be damaged?",
            "question_order": 10
        }
    ]
    
    try:
        result = supabase.table("questions").insert(questions).execute()
        print(f"✓ Created {len(questions)} questions for lesson 5")
        return questions
    except Exception as e:
        print(f"Error creating questions: {e}")
        return []


def seed_options(questions):
    """Create sample options for questions."""
    if not questions:
        print("No questions to create options for")
        return

    import uuid

    options = [
        # ---- LESSON 1 ----
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[0]["id"],
            "option_text": "A: A ball the player is using after a stroke from the teeing area.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[0]["id"],
            "option_text": "B: Any ball lying on the course, regardless of who hit it.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[0]["id"],
            "option_text": "C: Only a ball on the putting green.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[0]["id"],
            "option_text": "D: Only a ball declared in play by the marker.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[1]["id"],
            "option_text": "A: When not found within 3 minutes of search.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[1]["id"],
            "option_text": "B: When it rolls into deep rough.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[1]["id"],
            "option_text": "C: When another player plays it by accident.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[1]["id"],
            "option_text": "D: When it is unplayable.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[2]["id"],
            "option_text": "A: To clarify essential terms used throughout the rules.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[2]["id"],
            "option_text": "B: To give strategy tips for difficult holes.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[2]["id"],
            "option_text": "C: To explain scoring formats.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[2]["id"],
            "option_text": "D: To describe equipment standards.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[3]["id"],
            "option_text": "A: When the player makes a forward movement intending to hit the ball.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[3]["id"],
            "option_text": "B: Only when the ball travels at least one meter.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[3]["id"],
            "option_text": "C: Only when contact is made.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[3]["id"],
            "option_text": "D: Only after the scorecard is signed.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[4]["id"],
            "option_text": "A: Two penalty strokes.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[4]["id"],
            "option_text": "B: One penalty stroke.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[4]["id"],
            "option_text": "C: Loss of hole.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[4]["id"],
            "option_text": "D: Replay the stroke.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[5]["id"],
            "option_text": "A: Ground under repair, immovable obstructions, temporary water, animal holes.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[5]["id"],
            "option_text": "B: Any bunker.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[5]["id"],
            "option_text": "C: Any penalty area.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[5]["id"],
            "option_text": "D: Out-of-bounds.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[6]["id"],
            "option_text": "A: Temporary water gives free relief; penalty areas do not.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[6]["id"],
            "option_text": "B: Temporary water is always yellow; penalty areas are blue.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[6]["id"],
            "option_text": "C: Temporary water is always near greens.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[6]["id"],
            "option_text": "D: Penalty areas only appear on par 5 holes.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[7]["id"],
            "option_text": "A: When it stops moving and stays in position.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[7]["id"],
            "option_text": "B: When the player wants to hit it.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[7]["id"],
            "option_text": "C: When it’s on the fairway.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[7]["id"],
            "option_text": "D: When it’s on a tee.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[8]["id"],
            "option_text": "A: Playing again from the previous spot with one penalty stroke.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[8]["id"],
            "option_text": "B: Dropping two club-lengths from the ball.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[8]["id"],
            "option_text": "C: Free relief from abnormal conditions.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[8]["id"],
            "option_text": "D: Relief only available in bunkers.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[9]["id"],
            "option_text": "A: When searching for the ball.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[9]["id"],
            "option_text": "B: When preparing the backswing.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[9]["id"],
            "option_text": "C: When addressing the ball.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[9]["id"],
            "option_text": "D: When walking past other players.",
            "is_correct": False,
            "option_order": 4
        },
        # ---- LESSON 2 ----
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[10]["id"],
            "option_text": "A: From anywhere inside the teeing area.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[10]["id"],
            "option_text": "B: From one club-length behind the markers.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[10]["id"],
            "option_text": "C: From between the markers only.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[10]["id"],
            "option_text": "D: From anywhere on the tee box slope.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[11]["id"],
            "option_text": "A: Two penalty strokes.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[11]["id"],
            "option_text": "B: One penalty stroke.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[11]["id"],
            "option_text": "C: Replay the stroke without penalty.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[11]["id"],
            "option_text": "D: Loss of hole immediately.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[12]["id"],
            "option_text": "A: The player farthest from the hole plays first.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[12]["id"],
            "option_text": "B: The lowest handicap plays first.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[12]["id"],
            "option_text": "C: The highest score plays first.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[12]["id"],
            "option_text": "D: Order does not matter in stroke play.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[13]["id"],
            "option_text": "A: Players ready to play should hit when safe, regardless of order.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[13]["id"],
            "option_text": "B: Players always hit according to handicap.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[13]["id"],
            "option_text": "C: Only the fastest player may play.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[13]["id"],
            "option_text": "D: Only applies when putting.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[14]["id"],
            "option_text": "A: When any part of the ball is below the surface and at rest in the hole.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[14]["id"],
            "option_text": "B: Only when the flagstick is removed.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[14]["id"],
            "option_text": "C: Only when the ball stops in the center of the cup.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[14]["id"],
            "option_text": "D: Only when the marker confirms it.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[15]["id"],
            "option_text": "A: Lift the ball if it interferes and replace after the other player plays.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[15]["id"],
            "option_text": "B: Ignore interference.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[15]["id"],
            "option_text": "C: Mark it but do not move it.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[15]["id"],
            "option_text": "D: Add one penalty stroke and continue.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[16]["id"],
            "option_text": "A: The player must take free relief and cannot play from the wrong green.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[16]["id"],
            "option_text": "B: The player may play from the wrong green.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[16]["id"],
            "option_text": "C: The player must take penalty relief.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[16]["id"],
            "option_text": "D: No action required.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[17]["id"],
            "option_text": "A: When lifting the ball except in a few restricted situations.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[17]["id"],
            "option_text": "B: Only when on the fairway.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[17]["id"],
            "option_text": "C: Only when a referee is present.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[17]["id"],
            "option_text": "D: Never.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[18]["id"],
            "option_text": "A: Two penalty strokes.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[18]["id"],
            "option_text": "B: One penalty stroke.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[18]["id"],
            "option_text": "C: No penalty but stroke must be replayed.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[18]["id"],
            "option_text": "D: Loss of hole.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[19]["id"],
            "option_text": "A: Play at a prompt pace and be ready when it’s your turn.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[19]["id"],
            "option_text": "B: Always play within 20 seconds.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[19]["id"],
            "option_text": "C: Keep score while walking.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[19]["id"],
            "option_text": "D: Let all groups behind go through.",
            "is_correct": False,
            "option_order": 4
        },


        # ---- LESSON 3 ----
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[20]["id"],
            "option_text": "A: When abnormal conditions physically interfere with stance or swing.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[20]["id"],
            "option_text": "B: Anytime the lie is bad.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[20]["id"],
            "option_text": "C: Only on the fairway.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[20]["id"],
            "option_text": "D: Only when on the green.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[21]["id"],
            "option_text": "A: The point closest to the ball providing full relief without being nearer the hole.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[21]["id"],
            "option_text": "B: Any point two club-lengths away.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[21]["id"],
            "option_text": "C: A point chosen by the marker.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[21]["id"],
            "option_text": "D: A point chosen by the nearest player.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[22]["id"],
            "option_text": "A: Drop from knee height into the relief area.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[22]["id"],
            "option_text": "B: Drop from shoulder height.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[22]["id"],
            "option_text": "C: Roll the ball by hand.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[22]["id"],
            "option_text": "D: Place the ball instead of dropping.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[23]["id"],
            "option_text": "A: One club-length unless otherwise stated.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[23]["id"],
            "option_text": "B: Two club-lengths always.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[23]["id"],
            "option_text": "C: Unlimited distance.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[23]["id"],
            "option_text": "D: Only half a club-length.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[24]["id"],
            "option_text": "A: Anytime the player decides they cannot or should not play the ball.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[24]["id"],
            "option_text": "B: Only when the ball is in a bunker.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[24]["id"],
            "option_text": "C: Only when the ball is on the tee.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[24]["id"],
            "option_text": "D: Only when inside a penalty area.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[25]["id"],
            "option_text": "A: Stroke-and-distance, back-on-the-line, or two club-lengths relief.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[25]["id"],
            "option_text": "B: Free relief only.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[25]["id"],
            "option_text": "C: Drop anywhere on the fairway.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[25]["id"],
            "option_text": "D: Only replay from the tee.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[26]["id"],
            "option_text": "A: One penalty stroke.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[26]["id"],
            "option_text": "B: Two penalty strokes.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[26]["id"],
            "option_text": "C: No penalty.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[26]["id"],
            "option_text": "D: Loss of hole.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[27]["id"],
            "option_text": "A: When an animal threatens the player or interferes with the lie.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[27]["id"],
            "option_text": "B: Only when a referee approves.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[27]["id"],
            "option_text": "C: Only when on the putting green.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[27]["id"],
            "option_text": "D: Only when the ball is moving.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[28]["id"],
            "option_text": "A: Defined by the rule: one or two club-lengths depending on relief type.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[28]["id"],
            "option_text": "B: Always five meters.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[28]["id"],
            "option_text": "C: Always one meter.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[28]["id"],
            "option_text": "D: Always two meters.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[29]["id"],
            "option_text": "A: Play as it lies, take stroke-and-distance, or drop with penalty outside the area.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[29]["id"],
            "option_text": "B: Always drop for free.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[29]["id"],
            "option_text": "C: Must play from the penalty area.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[29]["id"],
            "option_text": "D: Only replay from the tee.",
            "is_correct": False,
            "option_order": 4
        },

        # ---- LESSON 4 ----
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[30]["id"],
            "option_text": "A: After 3 minutes of search.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[30]["id"],
            "option_text": "B: After 1 minute.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[30]["id"],
            "option_text": "C: After 5 minutes.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[30]["id"],
            "option_text": "D: Only when declared lost by the group.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[31]["id"],
            "option_text": "A: When searching or identifying the ball.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[31]["id"],
            "option_text": "B: When addressing the ball.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[31]["id"],
            "option_text": "C: When taking practice swings.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[31]["id"],
            "option_text": "D: When lining up a putt.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[32]["id"],
            "option_text": "A: Correct the mistake by playing the correct ball.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[32]["id"],
            "option_text": "B: Continue with the wrong ball.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[32]["id"],
            "option_text": "C: Replay the hole.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[32]["id"],
            "option_text": "D: No penalty ever applies.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[33]["id"],
            "option_text": "A: When moved accidentally on the putting green.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[33]["id"],
            "option_text": "B: When moved during the backswing.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[33]["id"],
            "option_text": "C: When moved by the wind.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[33]["id"],
            "option_text": "D: When moved by natural forces on the fairway.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[34]["id"],
            "option_text": "A: Two penalty strokes.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[34]["id"],
            "option_text": "B: One penalty stroke.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[34]["id"],
            "option_text": "C: Loss of the next hole.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[34]["id"],
            "option_text": "D: No penalty if unintentional.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[35]["id"],
            "option_text": "A: Replace the ball at its original spot.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[35]["id"],
            "option_text": "B: Play it as it lies.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[35]["id"],
            "option_text": "C: Take penalty relief.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[35]["id"],
            "option_text": "D: Continue without replacing.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[36]["id"],
            "option_text": "A: Replace it unless moved by natural forces off the putting green.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[36]["id"],
            "option_text": "B: Never replace it.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[36]["id"],
            "option_text": "C: Replace only if the marker says so.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[36]["id"],
            "option_text": "D: Replace only in bunkers.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[37]["id"],
            "option_text": "A: Play a provisional to save time if lost or OB is possible.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[37]["id"],
            "option_text": "B: Never play a provisional.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[37]["id"],
            "option_text": "C: Only after referee approval.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[37]["id"],
            "option_text": "D: Only when group agrees.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[38]["id"],
            "option_text": "A: When it is played from a point closer to the hole than the original ball.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[38]["id"],
            "option_text": "B: Immediately when announced.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[38]["id"],
            "option_text": "C: Only when the ball travels 50m.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[38]["id"],
            "option_text": "D: Only when the player signs the scorecard.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[39]["id"],
            "option_text": "A: When the original ball is lost or OB.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[39]["id"],
            "option_text": "B: When preferred lies are in effect.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[39]["id"],
            "option_text": "C: When on the green.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[39]["id"],
            "option_text": "D: When in a bunker.",
            "is_correct": False,
            "option_order": 4
        },

        # ---- LESSON 5 ----
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[40]["id"],
            "option_text": "A: When the ball may be lost or out of bounds.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[40]["id"],
            "option_text": "B: Anytime the player wants.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[40]["id"],
            "option_text": "C: Only on the fairway.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[40]["id"],
            "option_text": "D: Only during tournaments.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[41]["id"],
            "option_text": "A: Stroke-and-distance applies.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[41]["id"],
            "option_text": "B: One penalty stroke.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[41]["id"],
            "option_text": "C: Free relief allowed.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[41]["id"],
            "option_text": "D: No penalty in stroke play.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[42]["id"],
            "option_text": "A: When it is embedded in its own pitch mark in the general area.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[42]["id"],
            "option_text": "B: Only on the green.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[42]["id"],
            "option_text": "C: Only in bunkers.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[42]["id"],
            "option_text": "D: Whenever the ball is dirty.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[43]["id"],
            "option_text": "A: When in the general area and not in sand in bunkers.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[43]["id"],
            "option_text": "B: Only on tees.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[43]["id"],
            "option_text": "C: Only when plugged in bunkers.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[43]["id"],
            "option_text": "D: Only during winter rules.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[44]["id"],
            "option_text": "A: No penalty.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[44]["id"],
            "option_text": "B: One penalty stroke.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[44]["id"],
            "option_text": "C: Two penalty strokes.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[44]["id"],
            "option_text": "D: Replay required.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[45]["id"],
            "option_text": "A: Mark directly behind the ball before lifting.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[45]["id"],
            "option_text": "B: Mark in front of the ball.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[45]["id"],
            "option_text": "C: Mark anywhere within one meter.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[45]["id"],
            "option_text": "D: No marking required.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[46]["id"],
            "option_text": "A: One penalty stroke.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[46]["id"],
            "option_text": "B: Two penalty strokes.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[46]["id"],
            "option_text": "C: No penalty and replace.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[46]["id"],
            "option_text": "D: Loss of hole.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[47]["id"],
            "option_text": "A: Play it as it lies or take unplayable-ball relief.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[47]["id"],
            "option_text": "B: Replay from the tee only.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[47]["id"],
            "option_text": "C: Must take free relief.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[47]["id"],
            "option_text": "D: Declare ball lost immediately.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[48]["id"],
            "option_text": "A: The ball is holed with no penalty.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[48]["id"],
            "option_text": "B: Replace the ball.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[48]["id"],
            "option_text": "C: Add one penalty stroke.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[48]["id"],
            "option_text": "D: Replay the putt.",
            "is_correct": False,
            "option_order": 4
        },

        {
            "id": str(uuid.uuid4()),
            "question_id": questions[49]["id"],
            "option_text": "A: Mark and check the ball; replace if damaged.",
            "is_correct": True,
            "option_order": 1
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[49]["id"],
            "option_text": "B: Continue playing without checking.",
            "is_correct": False,
            "option_order": 2
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[49]["id"],
            "option_text": "C: Replace only with referee approval.",
            "is_correct": False,
            "option_order": 3
        },
        {
            "id": str(uuid.uuid4()),
            "question_id": questions[49]["id"],
            "option_text": "D: Take penalty relief.",
            "is_correct": False,
            "option_order": 4
        },
    ]


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