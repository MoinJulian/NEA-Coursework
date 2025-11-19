from fastapi import HTTPException
from connect import supabase


async def signin(email: str, password: str):
    """
    Authenticate a user using their email and password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: Response object containing session, user, and profile data.

    Raises:
        HTTPException: If authentication fails or an error occurs during the process.
    """
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # Fetch user profile
        if response.user:
            profile_response = supabase.table("profiles").select("*").eq("id", response.user.id).single().execute()
            
            return {
                "session": {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                },
                "user": {
                    "id": response.user.id,
                    "email": response.user.email
                },
                "profile": profile_response.data if profile_response.data else None
            }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))