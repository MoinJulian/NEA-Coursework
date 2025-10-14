from fastapi import FastAPI, Request
from routes.user_endpoint import getUser, updateUser
from routes.signin_endpoint import signinEndpoint
from routes.signup_endpoint import signupEndpoint
from auth.signup import signup

app = FastAPI()

@app.post("/v1/signup")
async def signupRoute(request: Request):
    return await signupEndpoint(request)

@app.post("/v1/signin")
async def signinRoute(request: Request):
    return await signinEndpoint(request)

@app.get("/v1/user")
async def userRoute(request: Request):
    return await getUser(request)

@app.put("/v1/user")
async def updateUserRoute(request: Request, user_update: dict):
    return await updateUser(request, user_update)