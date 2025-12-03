import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import Base, engine
from db import models

if __name__ == "__main__":
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Tables created successfully (or already exist)!")
    except Exception as e:
        print(f"Error creating tables: {e}")