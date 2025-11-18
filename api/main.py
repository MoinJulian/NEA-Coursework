from fastapi import FastAPI, Request
from routes.user_endpoint import getUser, updateUser
from routes.signin_endpoint import signinEndpoint
from routes.signup_endpoint import signupEndpoint
from routes.dashboard_endpoint import getDashboard
from routes.leaderboard_endpoint import getLeaderboard
from routes.lesson_endpoint import getLessonById, submitAnswer, completeLesson
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

@app.get("/v1/dashboard")
async def dashboardRoute(request: Request):
    return await getDashboard(request)

@app.get("/v1/leaderboard")
async def leaderboardRoute(page: int = 1, per_page: int = 10):
    return await getLeaderboard(page, per_page)

@app.get("/v1/lessons/{lesson_id}")
async def getLessonRoute(lesson_id: str, request: Request):
    return await getLessonById(lesson_id, request)

@app.post("/v1/lessons/{lesson_id}/questions/{question_id}/answer")
async def submitAnswerRoute(lesson_id: str, question_id: str, request: Request):
    body = await request.json()
    selected_option_id = body.get("selected_option_id")
    return await submitAnswer(lesson_id, question_id, selected_option_id, request)

@app.post("/v1/lessons/{lesson_id}/complete")
async def completeLessonRoute(lesson_id: str, request: Request):
    body = await request.json()
    return await completeLesson(lesson_id, request, body)