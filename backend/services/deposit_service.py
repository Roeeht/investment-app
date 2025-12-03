"""Deposit service - handles deposit-related business logic"""

from sqlalchemy.orm import Session
from db.models import Deposit
from fastapi import HTTPException
from datetime import date
from typing import Dict, Any


def add_deposit(db: Session, user_id: int, amount: float) -> Dict[str, Any]:
    """Add a new deposit for user"""
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    
    try:
        deposit = Deposit(
            user_id=user_id,
            amount=amount,
            date=date.today()
        )
        db.add(deposit)
        db.commit()
        db.refresh(deposit)
        
        return {
            "deposit": deposit
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Deposit failed: {str(e)}")
