from fastapi import FastAPI, Request
from auth.signup import signup

app = FastAPI()

@app.post("/signup")
async def signup_endpoint(request: Request):
    body = await request.json()
    email = body["email"]
    password = body["password"]
    response = await signup(email, password)
    return response