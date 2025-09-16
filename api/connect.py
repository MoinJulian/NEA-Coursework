import os
from supabase import create_client, Client
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv(".env")

if env_path:
    load_dotenv(env_path)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)