"""User service - handles user-related business logic"""

from sqlalchemy.orm import Session
from db.models import User
from fastapi import HTTPException
import bcrypt


def check_user_exists(db: Session, username: str, email: str) -> bool:
    """Check if a user with given username or email already exists"""
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    return existing_user is not None


def create_user(db: Session, username: str, email: str, password: str) -> User:
    """Create a new user with hashed password"""
    
    # Check if user already exists
    if check_user_exists(db, username, email):
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    try:
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")


def get_user_by_id(db: Session, user_id: int) -> User:
    """Get user by ID, raise 404 if not found"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def verify_user_exists(db: Session, user_id: int) -> None:
    """Verify user exists, raise 404 if not found"""
    get_user_by_id(db, user_id)
