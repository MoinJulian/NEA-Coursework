from fastapi import HTTPException
from connect import supabase


async def signup(email: str, password: str):
    """
    Registers a new user with the provided email and password using Supabase authentication.

    Args:
        email (str): The email address of the user to register.
        password (str): The password for the new user.

    Returns:
        dict: The response object from the Supabase sign-up process, containing user and session information.

    Raises:
        Any exceptions raised by the Supabase client during the sign-up process.
    """
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))