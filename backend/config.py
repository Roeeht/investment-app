from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env

API_KEY = os.getenv("FMP_API_KEY")
