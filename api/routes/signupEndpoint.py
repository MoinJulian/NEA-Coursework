from fastapi import HTTPException, Request
from auth.signup import signup

async def signupEndpoint(request: Request):
    """
    Handles user signup requests.

    Args:
        request (Request): The incoming HTTP request containing user signup data in JSON format.

    Returns:
        Response: The result of the signup process, typically including user information or error details.

    Raises:
        KeyError: If required fields are missing from the request body.
        Any exceptions raised by the `signup` function.
    """
    body = await request.json()
    
    # Extract required fields
    email = body.get("email")
    password = body.get("password")
    username = body.get("username")
    handicap = body.get("handicap")
    
    # Validate required fields
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    if not password:
        raise HTTPException(status_code=400, detail="Password is required")
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    if handicap is None:
        raise HTTPException(status_code=400, detail="Handicap is required")
    
    try:
        response = await signup(email, password, username, handicap)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))