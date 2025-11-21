import re
from fastapi import HTTPException
from connect import supabase


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
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
    try:
        response = supabase.table("profiles").select("username").eq("username", username).execute()
        return len(response.data) > 0
    except Exception:
        return False


async def signup(email: str, password: str, username: str, handicap: int):
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    if await check_username_exists(username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        if response.user:
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