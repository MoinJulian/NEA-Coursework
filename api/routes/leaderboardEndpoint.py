from fastapi import HTTPException
from connect import supabase


async def getLeaderboard(page: int = 1, per_page: int = 10):
    try:
        offset = (page - 1) * per_page

        count_response = supabase.table("profiles").select("id", count="exact").execute()
        total = count_response.count if count_response.count else 0

        response = supabase.table("profiles").select(
            "username, xp, streak, handicap"
        ).order("xp", desc=True).range(offset, offset + per_page - 1).execute()
        
        return {
            "leaderboard": response.data if response.data else [],
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))