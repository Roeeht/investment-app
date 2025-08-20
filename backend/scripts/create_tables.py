import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import Base, engine
from db import models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")