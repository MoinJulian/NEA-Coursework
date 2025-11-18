from fastapi import HTTPException
from connect import supabase
from datetime import datetime, timezone


async def getDashboard(request):
    """
    Get dashboard data for the authenticated user.
    
    Returns:
        dict: Dashboard data including next lesson, streak, hearts, xp, leaderboard, and lessons completed.
    """
    token = request.headers.get("Authorization").split(" ")[1]
    
    try:
        # Get authenticated user
        user_response = supabase.auth.get_user(token)
        user_id = user_response.user.id
        
        # Get user profile
        profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        
        if not profile.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Get completed lessons count
        completed = supabase.table("completed_lessons").select("id", count="exact").eq("user_id", user_id).execute()
        lessons_completed = completed.count if completed.count else 0
        
        # Get next lesson (first lesson not completed by user)
        all_lessons = supabase.table("lessons").select("id, title, description, order_number").order("order_number").execute()
        completed_lesson_ids = supabase.table("completed_lessons").select("lesson_id").eq("user_id", user_id).execute()
        completed_ids = [item["lesson_id"] for item in completed_lesson_ids.data] if completed_lesson_ids.data else []
        
        next_lesson = None
        for lesson in all_lessons.data if all_lessons.data else []:
            if lesson["id"] not in completed_ids:
                next_lesson = lesson
                break
        
        # Get leaderboard preview (top 5)
        leaderboard = supabase.table("profiles").select("username, xp, streak").order("xp", desc=True).limit(5).execute()
        
        return {
            "profile": profile.data,
            "next_lesson": next_lesson,
            "leaderboard_preview": leaderboard.data if leaderboard.data else [],
            "lessons_completed": lessons_completed
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
