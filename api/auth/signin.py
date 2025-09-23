from fastapi import HTTPException
from connect import supabase


async def signin(email: str, password: str):
    """
    Authenticate a user using their email and password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        Response object from the Supabase authentication API.

    Raises:
        HTTPException: If authentication fails or an error occurs during the process.
    """
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))