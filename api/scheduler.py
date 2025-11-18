"""
Scheduler for daily reset tasks (hearts, streak freezes)
Runs at 00:00 UTC daily
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from connect import supabase


def reset_daily_hearts():
    """
    Reset hearts for all users to 5
    Runs daily at 00:00 UTC
    """
    try:
        print(f"[{datetime.now(timezone.utc)}] Running daily hearts reset...")
        
        # Update all users' hearts to 5
        supabase.table("users").update({
            "hearts": 5,
            "last_heart_reset": datetime.now(timezone.utc).isoformat()
        }).neq("deleted", True).execute()
        
        print(f"[{datetime.now(timezone.utc)}] Hearts reset complete")
        
    except Exception as e:
        print(f"[{datetime.now(timezone.utc)}] Error resetting hearts: {str(e)}")


def reset_streak_freezes():
    """
    Reset streak freeze count for all users to 0
    Runs weekly on Monday at 00:00 UTC
    """
    try:
        print(f"[{datetime.now(timezone.utc)}] Running weekly streak freeze reset...")
        
        # Update all users' streak freeze count to 0
        supabase.table("users").update({
            "streak_freeze_count": 0
        }).neq("deleted", True).execute()
        
        print(f"[{datetime.now(timezone.utc)}] Streak freeze reset complete")
        
    except Exception as e:
        print(f"[{datetime.now(timezone.utc)}] Error resetting streak freezes: {str(e)}")


def check_and_reset_streaks():
    """
    Check for users who haven't completed a lesson yesterday
    and reset their streaks (unless they have streak freezes)
    Runs daily at 00:01 UTC
    """
    try:
        print(f"[{datetime.now(timezone.utc)}] Checking streaks...")
        
        from datetime import timedelta
        
        yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date()
        
        # Get all active users
        users_response = supabase.table("users").select("*").eq("deleted", False).execute()
        
        for user in users_response.data:
            last_lesson = user.get("last_lesson_date")
            
            if last_lesson:
                if isinstance(last_lesson, str):
                    last_lesson_date = datetime.fromisoformat(last_lesson).date()
                else:
                    last_lesson_date = last_lesson
                
                # If last lesson was not yesterday or today, reset streak
                if last_lesson_date < yesterday:
                    # Check if user has streak freezes
                    if user.get("streak_freeze_count", 0) < 2:
                        # Use a streak freeze
                        supabase.table("users").update({
                            "streak_freeze_count": user.get("streak_freeze_count", 0) + 1
                        }).eq("id", user["id"]).execute()
                        print(f"Used streak freeze for user {user['username']}")
                    else:
                        # Reset streak
                        supabase.table("users").update({
                            "streak": 0
                        }).eq("id", user["id"]).execute()
                        print(f"Reset streak for user {user['username']}")
        
        print(f"[{datetime.now(timezone.utc)}] Streak check complete")
        
    except Exception as e:
        print(f"[{datetime.now(timezone.utc)}] Error checking streaks: {str(e)}")


def init_scheduler():
    """
    Initialize the background scheduler
    """
    scheduler = BackgroundScheduler(timezone="UTC")
    
    # Reset hearts daily at 00:00 UTC
    scheduler.add_job(reset_daily_hearts, 'cron', hour=0, minute=0)
    
    # Check and reset streaks daily at 00:01 UTC
    scheduler.add_job(check_and_reset_streaks, 'cron', hour=0, minute=1)
    
    # Reset streak freezes weekly on Monday at 00:00 UTC
    scheduler.add_job(reset_streak_freezes, 'cron', day_of_week='mon', hour=0, minute=0)
    
    scheduler.start()
    
    print("Scheduler initialized. Daily tasks scheduled.")
    
    return scheduler
