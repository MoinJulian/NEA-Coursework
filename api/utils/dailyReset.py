from connect import supabase
from datetime import datetime, timezone, timedelta
import asyncio


async def reset_hearts_daily():
    try:
        supabase.table("profiles").update({"hearts": 5}).neq("hearts", 5).execute()
        print(f"Hearts reset completed at {datetime.now(timezone.utc)}")
    except Exception as e:
        print(f"Error resetting hearts: {e}")


async def check_and_reset_streaks():
    try:
        today = datetime.now(timezone.utc).date()
        yesterday = today - timedelta(days=1)
        
        profiles = supabase.table("profiles").select("id, streak, last_lesson_date, streak_freezes_used").execute()
        
        for profile in profiles.data if profiles.data else []:
            last_lesson_date = profile.get("last_lesson_date")
            
            if last_lesson_date:
                last_date = datetime.fromisoformat(str(last_lesson_date)).date()
                
                if last_date < yesterday:
                    supabase.table("profiles").update({
                        "streak": 0
                    }).eq("id", profile["id"]).execute()
        
        print(f"Streak check completed at {datetime.now(timezone.utc)}")
    except Exception as e:
        print(f"Error checking streaks: {e}")


async def daily_reset_task():
    while True:
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = (tomorrow - now).total_seconds()
        
        await asyncio.sleep(seconds_until_midnight)
        await reset_hearts_daily()
        await check_and_reset_streaks()