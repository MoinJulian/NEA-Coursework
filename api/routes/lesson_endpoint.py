from fastapi import HTTPException
from connect import supabase
from datetime import datetime, timezone, timedelta


async def getLessonById(lesson_id: str, request):
    """
    Get a lesson with all its questions and options.
    
    Args:
        lesson_id (str): The lesson UUID
        request: The request object for authentication
    
    Returns:
        dict: Lesson data with questions and options
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or " " not in auth_header:
        raise HTTPException(status_code=401, detail="Authorization token required")
    
    token = auth_header.split(" ")[1]
    
    try:
        # Verify user is authenticated
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        # Get user profile to check hearts
        profile = supabase.table("profiles").select("hearts").eq("id", user_id).single().execute()
        
        if not profile.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        if profile.data["hearts"] <= 0:
            raise HTTPException(status_code=400, detail="No hearts remaining. Come back tomorrow!")
        
        # Get lesson
        lesson = supabase.table("lessons").select("*").eq("id", lesson_id).single().execute()
        
        if not lesson.data:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        # Get questions for this lesson
        questions = supabase.table("questions").select("*").eq("lesson_id", lesson_id).order("question_order").execute()
        
        # Get options for each question
        lesson_data = lesson.data
        lesson_data["questions"] = []
        
        for question in questions.data if questions.data else []:
            options = supabase.table("options").select("*").eq("question_id", question["id"]).order("option_order").execute()
            question["options"] = options.data if options.data else []
            lesson_data["questions"].append(question)
        
        return {
            "lesson": lesson_data,
            "hearts": profile.data["hearts"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def submitAnswer(lesson_id: str, question_id: str, selected_option_id: str, request):
    """
    Submit an answer for a question.
    
    Args:
        lesson_id (str): The lesson UUID
        question_id (str): The question UUID
        selected_option_id (str): The selected option UUID
        request: The request object for authentication
    
    Returns:
        dict: Result of answer submission
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or " " not in auth_header:
        raise HTTPException(status_code=401, detail="Authorization token required")
    
    token = auth_header.split(" ")[1]
    
    try:
        # Verify user is authenticated
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        # Get the selected option
        option = supabase.table("options").select("*").eq("id", selected_option_id).single().execute()
        
        if not option.data:
            raise HTTPException(status_code=404, detail="Option not found")
        
        is_correct = option.data["is_correct"]
        
        # If wrong, deduct a heart
        if not is_correct:
            profile = supabase.table("profiles").select("hearts").eq("id", user_id).single().execute()
            
            if not profile.data:
                raise HTTPException(status_code=404, detail="Profile not found")
            
            current_hearts = profile.data["hearts"]
            
            if current_hearts > 0:
                supabase.table("profiles").update({"hearts": current_hearts - 1}).eq("id", user_id).execute()
            
            # Get the correct answer
            correct_option = supabase.table("options").select("*").eq("question_id", question_id).eq("is_correct", True).single().execute()
            
            return {
                "correct": False,
                "hearts_remaining": max(0, current_hearts - 1),
                "correct_answer": correct_option.data if correct_option.data else None
            }
        
        return {
            "correct": True
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def completeLesson(lesson_id: str, request, completion_data: dict):
    """
    Complete a lesson and update user stats.
    
    Args:
        lesson_id (str): The lesson UUID
        request: The request object for authentication
        completion_data (dict): Data about lesson completion (accuracy, time_taken, mistakes)
    
    Returns:
        dict: Result of lesson completion
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or " " not in auth_header:
        raise HTTPException(status_code=401, detail="Authorization token required")
    
    token = auth_header.split(" ")[1]
    
    try:
        # Verify user is authenticated
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        # Get user profile
        profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        
        if not profile.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Calculate XP earned (max 100, -5 per mistake round)
        mistakes = completion_data.get("mistakes", 0)
        xp_earned = max(0, 100 - (mistakes * 5))
        
        # Update profile
        current_xp = profile.data["xp"]
        current_streak = profile.data["streak"]
        
        # Check if this is a new day for streak calculation
        last_lesson_date = profile.data.get("last_lesson_date")
        today = datetime.now(timezone.utc).date()
        
        new_streak = current_streak
        if last_lesson_date:
            last_date = datetime.fromisoformat(str(last_lesson_date)).date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                # Consecutive day - increase streak
                new_streak = current_streak + 1
            elif days_diff > 1:
                # Streak broken - reset to 1
                new_streak = 1
            # If same day (days_diff == 0), keep current streak
        else:
            # First lesson ever
            new_streak = 1
        
        # Update profile
        supabase.table("profiles").update({
            "xp": current_xp + xp_earned,
            "streak": new_streak,
            "last_lesson_date": today.isoformat()
        }).eq("id", user_id).execute()
        
        # Record completed lesson
        supabase.table("completed_lessons").insert({
            "user_id": user_id,
            "lesson_id": lesson_id,
            "accuracy": completion_data.get("accuracy", 0),
            "xp_earned": xp_earned,
            "time_taken": completion_data.get("time_taken", 0),
            "mistakes": mistakes
        }).execute()
        
        return {
            "xp_earned": xp_earned,
            "new_streak": new_streak,
            "total_xp": current_xp + xp_earned,
            "accuracy": completion_data.get("accuracy", 0),
            "time_taken": completion_data.get("time_taken", 0)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
