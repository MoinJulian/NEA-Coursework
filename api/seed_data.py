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
    
    options = [
        # ---- LESSON 1 ----
        "A: A ball the player is using after a stroke from the teeing area.",
        "B: Any ball lying on the course, regardless of who hit it.",
        "C: Only a ball on the putting green.",
        "D: Only a ball declared in play by the marker.",

        "A: When not found within 3 minutes of search.",
        "B: When it rolls into deep rough.",
        "C: When another player plays it by accident.",
        "D: When it is unplayable.",

        "A: To clarify essential terms used throughout the rules.",
        "B: To give strategy tips for difficult holes.",
        "C: To explain scoring formats.",
        "D: To describe equipment standards.",

        "A: When the player makes a forward movement intending to hit the ball.",
        "B: Only when the ball travels at least one meter.",
        "C: Only when contact is made.",
        "D: Only after the scorecard is signed.",

        "A: Two penalty strokes.",
        "B: One penalty stroke.",
        "C: Loss of hole.",
        "D: Replay the stroke.",

        "A: Ground under repair, immovable obstructions, temporary water, animal holes.",
        "B: Any bunker.",
        "C: Any penalty area.",
        "D: Out-of-bounds.",

        "A: Temporary water gives free relief; penalty areas do not.",
        "B: Temporary water is always yellow; penalty areas are blue.",
        "C: Temporary water is always near greens.",
        "D: Penalty areas only appear on par 5 holes.",

        "A: When it stops moving and stays in position.",
        "B: When the player wants to hit it.",
        "C: When it’s on the fairway.",
        "D: When it’s on a tee.",

        "A: Playing again from the previous spot with one penalty stroke.",
        "B: Dropping two club-lengths from the ball.",
        "C: Free relief from abnormal conditions.",
        "D: Relief only available in bunkers.",

        "A: When searching for the ball.",
        "B: When preparing the backswing.",
        "C: When addressing the ball.",
        "D: When walking past other players.",


        # ---- LESSON 2 ----
        "A: From anywhere inside the teeing area.",
        "B: From one club-length behind the markers.",
        "C: From between the markers only.",
        "D: From anywhere on the tee box slope.",

        "A: Two penalty strokes.",
        "B: One penalty stroke.",
        "C: Replay the stroke without penalty.",
        "D: Loss of hole immediately.",

        "A: The player farthest from the hole plays first.",
        "B: The lowest handicap plays first.",
        "C: The highest score plays first.",
        "D: Order does not matter in stroke play.",

        "A: Players ready to play should hit when safe, regardless of order.",
        "B: Players always hit according to handicap.",
        "C: Only the fastest player may play.",
        "D: Only applies when putting.",

        "A: When any part of the ball is below the surface and at rest in the hole.",
        "B: Only when the flagstick is removed.",
        "C: Only when the ball stops in the center of the cup.",
        "D: Only when the marker confirms it.",

        "A: Lift the ball if it interferes and replace after the other player plays.",
        "B: Ignore interference.",
        "C: Mark it but do not move it.",
        "D: Add one penalty stroke and continue.",

        "A: The player must take free relief and cannot play from the wrong green.",
        "B: The player may play from the wrong green.",
        "C: The player must take penalty relief.",
        "D: No action required.",

        "A: When lifting the ball except in a few restricted situations.",
        "B: Only when on the fairway.",
        "C: Only when a referee is present.",
        "D: Never.",

        "A: Two penalty strokes.",
        "B: One penalty stroke.",
        "C: No penalty but stroke must be replayed.",
        "D: Loss of hole.",

        "A: Play at a prompt pace and be ready when it’s your turn.",
        "B: Always play within 20 seconds.",
        "C: Keep score while walking.",
        "D: Let all groups behind go through.",


        # ---- LESSON 3 ----
        "A: When abnormal conditions physically interfere with stance or swing.",
        "B: Anytime the lie is bad.",
        "C: Only on the fairway.",
        "D: Only when on the green.",

        "A: The point closest to the ball providing full relief without being nearer the hole.",
        "B: Any point two club-lengths away.",
        "C: A point chosen by the marker.",
        "D: A point chosen by the nearest player.",

        "A: Drop from knee height into the relief area.",
        "B: Drop from shoulder height.",
        "C: Roll the ball by hand.",
        "D: Place the ball instead of dropping.",

        "A: One club-length unless otherwise stated.",
        "B: Two club-lengths always.",
        "C: Unlimited distance.",
        "D: Only half a club-length.",

        "A: Anytime the player decides they cannot or should not play the ball.",
        "B: Only when the ball is in a bunker.",
        "C: Only when the ball is on the tee.",
        "D: Only when inside a penalty area.",

        "A: Stroke-and-distance, back-on-the-line, or two club-lengths relief.",
        "B: Free relief only.",
        "C: Drop anywhere on the fairway.",
        "D: Only replay from the tee.",

        "A: One penalty stroke.",
        "B: Two penalty strokes.",
        "C: No penalty.",
        "D: Loss of hole.",

        "A: When an animal threatens the player or interferes with the lie.",
        "B: Only when a referee approves.",
        "C: Only when on the putting green.",
        "D: Only when the ball is moving.",

        "A: Defined by the rule: one or two club-lengths depending on relief type.",
        "B: Always five meters.",
        "C: Always one meter.",
        "D: Always two meters.",

        "A: Play as it lies, take stroke-and-distance, or drop with penalty outside the area.",
        "B: Always drop for free.",
        "C: Must play from the penalty area.",
        "D: Only replay from the tee.",


        # ---- LESSON 4 ----
        "A: After 3 minutes of search.",
        "B: After 1 minute.",
        "C: After 5 minutes.",
        "D: Only when declared lost by the group.",

        "A: When searching or identifying the ball.",
        "B: When addressing the ball.",
        "C: When taking practice swings.",
        "D: When lining up a putt.",

        "A: Correct the mistake by playing the correct ball.",
        "B: Continue with the wrong ball.",
        "C: Replay the hole.",
        "D: No penalty ever applies.",

        "A: When moved accidentally on the putting green.",
        "B: When moved during the backswing.",
        "C: When moved by the wind.",
        "D: When moved by natural forces on the fairway.",

        "A: Two penalty strokes.",
        "B: One penalty stroke.",
        "C: Loss of the next hole.",
        "D: No penalty if unintentional.",

        "A: Replace the ball at its original spot.",
        "B: Play it as it lies.",
        "C: Take penalty relief.",
        "D: Continue without replacing.",

        "A: Replace it unless moved by natural forces off the putting green.",
        "B: Never replace it.",
        "C: Replace only if the marker says so.",
        "D: Replace only in bunkers.",

        "A: Play a provisional to save time if lost or OB is possible.",
        "B: Never play a provisional.",
        "C: Only after referee approval.",
        "D: Only when group agrees.",

        "A: When it is played from a point closer to the hole than the original ball.",
        "B: Immediately when announced.",
        "C: Only when the ball travels 50m.",
        "D: Only when the player signs the scorecard.",

        "A: When the original ball is lost or OB.",
        "B: When preferred lies are in effect.",
        "C: When on the green.",
        "D: When in a bunker.",


        # ---- LESSON 5 ----
        "A: When the ball may be lost or out of bounds.",
        "B: Anytime the player wants.",
        "C: Only on the fairway.",
        "D: Only during tournaments.",

        "A: Stroke-and-distance applies.",
        "B: One penalty stroke.",
        "C: Free relief allowed.",
        "D: No penalty in stroke play.",

        "A: When it is embedded in its own pitch mark in the general area.",
        "B: Only on the green.",
        "C: Only in bunkers.",
        "D: Whenever the ball is dirty.",

        "A: When in the general area and not in sand in bunkers.",
        "B: Only on tees.",
        "C: Only when plugged in bunkers.",
        "D: Only during winter rules.",

        "A: No penalty.",
        "B: One penalty stroke.",
        "C: Two penalty strokes.",
        "D: Replay required.",

        "A: Mark directly behind the ball before lifting.",
        "B: Mark in front of the ball.",
        "C: Mark anywhere within one meter.",
        "D: No marking required.",

        "A: One penalty stroke.",
        "B: Two penalty strokes.",
        "C: No penalty and replace.",
        "D: Loss of hole.",

        "A: Play it as it lies or take unplayable-ball relief.",
        "B: Replay from the tee only.",
        "C: Must take free relief.",
        "D: Declare ball lost immediately.",

        "A: The ball is holed with no penalty.",
        "B: Replace the ball.",
        "C: Add one penalty stroke.",
        "D: Replay the putt.",

        "A: Mark and check the ball; replace if damaged.",
        "B: Continue playing without checking.",
        "C: Replace only with referee approval.",
        "D: Take penalty relief.",
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