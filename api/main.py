import connect

response = (connect.supabase.table("test").select("*").execute())

print(response)