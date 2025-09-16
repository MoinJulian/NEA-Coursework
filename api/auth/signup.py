from connect import supabase

async def signup(email: str, password: str):
    response = supabase.auth.sign_up({"email": email, "password": password})
    print(response)
    return response