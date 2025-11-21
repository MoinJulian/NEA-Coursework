from fastapi import HTTPException, Request
from auth.signin import signin

async def signinEndpoint(request: Request):
    body = await request.json()
    email = body["email"]
    password = body["password"]
    try:
        response = await signin(email, password)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))