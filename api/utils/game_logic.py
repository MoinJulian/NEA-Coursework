"""
Business logic for hearts, streak, and XP systems
"""
from datetime import datetime, timezone, timedelta
from connect import supabase


def reset_hearts_if_needed(user_id: str) -> dict:
    """
    Check if hearts need to be reset (daily at 00:00 UTC)
    and reset them if needed
    
    Args:
        user_id: User's UUID
        
    Returns:
        Updated user data
    """
    # Get user data
    user_response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_response.data
    
    if not user:
        raise ValueError("User not found")
    
    last_reset = user.get("last_heart_reset")
    if last_reset:
        # Parse the timestamp
        if isinstance(last_reset, str):
            last_reset_dt = datetime.fromisoformat(last_reset.replace('Z', '+00:00'))
        else:
            last_reset_dt = last_reset
    else:
        last_reset_dt = datetime.now(timezone.utc) - timedelta(days=1)
    
    now = datetime.now(timezone.utc)
    
    # Check if it's a new day (00:00 UTC)
    if last_reset_dt.date() < now.date():
        # Reset hearts to 5
        update_response = supabase.table("users").update({
            "hearts": 5,
            "last_heart_reset": now.isoformat()
        }).eq("id", user_id).execute()
        
        return update_response.data[0] if update_response.data else user
    
    return user


def deduct_heart(user_id: str) -> dict:
    """
    Deduct one heart from user
    
    Args:
        user_id: User's UUID
        
    Returns:
        Updated user data
        
    Raises:
        ValueError: If user has no hearts left
    """
    # First reset hearts if needed
    user = reset_hearts_if_needed(user_id)
    
    hearts = user.get("hearts", 0)
    
    if hearts <= 0:
        raise ValueError("No hearts remaining")
    
    # Deduct one heart
    update_response = supabase.table("users").update({
        "hearts": hearts - 1
    }).eq("id", user_id).execute()
    
    return update_response.data[0] if update_response.data else user


def update_streak(user_id: str) -> dict:
    """
    Update user's streak after completing a lesson
    Increments streak if lesson completed on a new day
    Resets streak if more than 1 day has passed without a lesson
    
    Args:
        user_id: User's UUID
        
    Returns:
        Updated user data
    """
    user_response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_response.data
    
    if not user:
        raise ValueError("User not found")
    
    last_lesson = user.get("last_lesson_date")
    current_streak = user.get("streak", 0)
    
    today = datetime.now(timezone.utc).date()
    
    if last_lesson:
        # Parse the date
        if isinstance(last_lesson, str):
            last_lesson_date = datetime.fromisoformat(last_lesson).date()
        else:
            last_lesson_date = last_lesson
        
        # Calculate days difference
        days_diff = (today - last_lesson_date).days
        
        if days_diff == 0:
            # Same day, no streak change
            return user
        elif days_diff == 1:
            # Next day, increment streak
            new_streak = current_streak + 1
        else:
            # More than 1 day, reset streak
            new_streak = 1
    else:
        # First lesson ever
        new_streak = 1
    
    # Update user
    update_response = supabase.table("users").update({
        "streak": new_streak,
        "last_lesson_date": today.isoformat()
    }).eq("id", user_id).execute()
    
    return update_response.data[0] if update_response.data else user


def reset_streak(user_id: str) -> dict:
    """
    Reset user's streak to 0 (when they run out of hearts)
    
    Args:
        user_id: User's UUID
        
    Returns:
        Updated user data
    """
    update_response = supabase.table("users").update({
        "streak": 0
    }).eq("id", user_id).execute()
    
    return update_response.data[0] if update_response.data else user


def calculate_xp(total_questions: int, mistakes_count: int) -> int:
    """
    Calculate XP earned from a lesson
    Base XP: 100
    Deduction: -5 per mistake round (each retry of incorrect questions)
    
    Args:
        total_questions: Total number of questions in lesson
        mistakes_count: Number of times user had to retry incorrect questions
        
    Returns:
        XP earned (minimum 10)
    """
    base_xp = 100
    xp_deduction = mistakes_count * 5
    earned_xp = max(10, base_xp - xp_deduction)
    return earned_xp


def add_xp(user_id: str, xp: int) -> dict:
    """
    Add XP to user's total
    
    Args:
        user_id: User's UUID
        xp: Amount of XP to add
        
    Returns:
        Updated user data
    """
    user_response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_response.data
    
    if not user:
        raise ValueError("User not found")
    
    current_xp = user.get("xp", 0)
    new_xp = current_xp + xp
    
    update_response = supabase.table("users").update({
        "xp": new_xp
    }).eq("id", user_id).execute()
    
    return update_response.data[0] if update_response.data else user


def use_streak_freeze(user_id: str) -> dict:
    """
    Use a streak freeze (max 2 per week)
    
    Args:
        user_id: User's UUID
        
    Returns:
        Updated user data
        
    Raises:
        ValueError: If no streak freezes available
    """
    user_response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_response.data
    
    if not user:
        raise ValueError("User not found")
    
    freeze_count = user.get("streak_freeze_count", 0)
    
    if freeze_count >= 2:
        raise ValueError("No streak freezes remaining this week")
    
    update_response = supabase.table("users").update({
        "streak_freeze_count": freeze_count + 1
    }).eq("id", user_id).execute()
    
    return update_response.data[0] if update_response.data else user
