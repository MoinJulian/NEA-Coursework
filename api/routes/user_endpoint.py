from fastapi import HTTPException
from connect import supabase


async def userEndpoint(request):
    token = request.headers.get("Authorization").split(" ")[1]
    try:
        response = supabase.auth.get_user(token)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))