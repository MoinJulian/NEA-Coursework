from fastapi import FastAPI
import connect

app = FastAPI()

@app.get("/test")
def get_test_data():
    response = (connect.supabase.table("test").select("*").execute())
    return response.data