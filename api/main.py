from fastapi import FastAPI, Request
from routes.signin_endpoint import signinEndpoint
from routes.signup_endpoint import signupEndpoint
from auth.signup import signup

app = FastAPI()

@app.post("/signup")
async def signupRoute(request: Request):
    return await signupEndpoint(request)

@app.post("/signin")
async def signinRoute(request: Request):
    return await signinEndpoint(request)