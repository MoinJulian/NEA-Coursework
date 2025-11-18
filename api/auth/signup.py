import re
from fastapi import HTTPException
from connect import supabase


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password requirements.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, ""


async def check_username_exists(username: str) -> bool:
    """Check if username already exists in profiles table."""
    try:
        response = supabase.table("profiles").select("username").eq("username", username).execute()
        return len(response.data) > 0
    except Exception:
        return False


async def signup(email: str, password: str, username: str, handicap: int):
    """
    Registers a new user with the provided information using Supabase authentication.

    Args:
        email (str): The email address of the user to register.
        password (str): The password for the new user.
        username (str): The unique username for the user.
        handicap (int): The user's handicap value.

    Returns:
        dict: The response object from the Supabase sign-up process, containing user and session information.

    Raises:
        HTTPException: If validation fails or registration encounters an error.
    """
    # Validate email
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate password
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Check username uniqueness
    if await check_username_exists(username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    try:
        # Create auth user
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        if response.user:
            # Create profile entry with default values
            profile_data = {
                "id": response.user.id,
                "username": username,
                "handicap": handicap,
                "xp": 0,
                "streak": 0,
                "hearts": 5,
                "streak_freezes_used": 0
            }
            supabase.table("profiles").insert(profile_data).execute()
        
        return {"status_code": 200, "data": response}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))