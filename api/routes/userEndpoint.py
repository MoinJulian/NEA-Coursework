from fastapi import HTTPException
from connect import supabase


async def getUser(request):
    token = request.headers.get("Authorization").split(" ")[1]
    try:
        response = supabase.auth.get_user(token)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def updateUser(request, user_update):
    access_token = request.headers.get("Authorization").split(" ")[1]
    try:
        if access_token is None:
            raise HTTPException(status_code=400, detail="Access token is required")
        
        user_id = supabase.auth.get_user(access_token).user.id
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid access token")
        response = supabase.auth.admin.update_user_by_id(
            user_id,
            {
                "email": user_update.get("email"),
                "password": user_update.get("password")
            }
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))