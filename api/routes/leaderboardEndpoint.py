from fastapi import HTTPException
from connect import supabase


async def getLeaderboard(page: int = 1, per_page: int = 10):
    """
    Get leaderboard sorted by XP descending.
    
    Args:
        page (int): Page number (1-indexed)
        per_page (int): Number of results per page
    
    Returns:
        dict: Leaderboard data with pagination info
    """
    try:
        offset = (page - 1) * per_page
        
        # Get total count
        count_response = supabase.table("profiles").select("id", count="exact").execute()
        total = count_response.count if count_response.count else 0
        
        # Get paginated leaderboard
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