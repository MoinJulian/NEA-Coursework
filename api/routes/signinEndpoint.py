from fastapi import HTTPException, Request
from auth.signin import signin

async def signinEndpoint(request: Request):
    """
    Handles user signin requests.

    Args:
        request (Request): The incoming HTTP request containing user signin data in JSON format.

    Returns:
        Response: The result of the signin process, typically including user information or error details.

    Raises:
        KeyError: If 'email' or 'password' is missing from the request body.
        Any exceptions raised by the `signin` function.
    """
    body = await request.json()
    email = body["email"]
    password = body["password"]
    try:
        response = await signin(email, password)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))