from fastapi import FastAPI, HTTPException, Request
from auth.signup import signup

app = FastAPI()

@app.post("/signup")
async def signup_endpoint(request: Request):
    """
    Handles user signup requests.

    Args:
        request (Request): The incoming HTTP request containing user signup data in JSON format.

    Returns:
        Response: The result of the signup process, typically including user information or error details.

    Raises:
        KeyError: If 'email' or 'password' is missing from the request body.
        Any exceptions raised by the `signup` function.
    """
    body = await request.json()
    email = body["email"]
    password = body["password"]
    try:
        response = await signup(email, password)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))