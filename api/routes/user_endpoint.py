from fastapi import HTTPException
from connect import supabase


async def getUser(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or " " not in auth_header:
        raise HTTPException(status_code=401, detail="Authorization token required")
    
    token = auth_header.split(" ")[1]
    try:
        response = supabase.auth.get_user(token)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def updateUser(request, user_update):
    auth_header = request.headers.get("Authorization")
    if not auth_header or " " not in auth_header:
        raise HTTPException(status_code=401, detail="Authorization token required")
    
    access_token = auth_header.split(" ")[1]
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