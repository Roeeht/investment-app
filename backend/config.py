from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env

API_KEY = os.getenv("FMP_API_KEY")
DB_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
