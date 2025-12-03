"""Purchase service - handles purchase-related business logic"""

from sqlalchemy.orm import Session
from db.models import Purchase, UserStock
from fastapi import HTTPException
from datetime import date
from typing import List, Dict, Any


def get_user_purchases(db: Session, user_id: int, limit: int = 50) -> List[Purchase]:
    """Get user's purchase history"""
    purchases = db.query(Purchase).filter(
        Purchase.user_id == user_id
    ).order_by(Purchase.date.desc()).limit(limit).all()
    
    return purchases


def calculate_total_spent(db: Session, user_id: int) -> float:
    """Calculate total amount spent on purchases"""
    total = db.query(
        db.func.coalesce(db.func.sum(Purchase.quantity * Purchase.price_per_share), 0)
    ).filter(Purchase.user_id == user_id).scalar()
    
    return float(total or 0)


def record_purchase(
    db: Session, 
    user_id: int, 
    symbol: str, 
    quantity: float, 
    price_per_share: float
) -> Dict[str, Any]:
    """Record a stock purchase with the given price"""
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    if price_per_share <= 0:
        raise HTTPException(status_code=400, detail="Price per share must be positive")
    
    try:
        total_cost = quantity * price_per_share
        
        # Record the purchase
        purchase = Purchase(
            user_id=user_id,
            stock_symbol=symbol.upper(),
            quantity=quantity,
            price_per_share=price_per_share,
            date=date.today()
        )
        db.add(purchase)
        
        # Update user's stock holdings
        existing_holding = db.query(UserStock).filter(
            UserStock.user_id == user_id,
            UserStock.stock_symbol == symbol.upper()
        ).first()
        
        if existing_holding:
            # Calculate new average cost
            total_quantity = float(existing_holding.quantity) + quantity
            total_cost_basis = (
                float(existing_holding.quantity) * float(existing_holding.average_cost or 0)
            ) + total_cost
            new_average_cost = total_cost_basis / total_quantity
            
            existing_holding.quantity = total_quantity
            existing_holding.average_cost = new_average_cost
        else:
            # Create new holding
            new_holding = UserStock(
                user_id=user_id,
                stock_symbol=symbol.upper(),
                quantity=quantity,
                average_cost=price_per_share
            )
            db.add(new_holding)
        
        db.commit()
        db.refresh(purchase)
        
        return {
            "id": purchase.id,
            "symbol": symbol.upper(),
            "quantity": quantity,
            "price_per_share": price_per_share,
            "total_cost": total_cost,
            "date": purchase.date.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Purchase recording failed: {str(e)}")


def format_purchase(purchase: Purchase) -> Dict[str, Any]:
    """Format purchase data for API response"""
    return {
        "id": purchase.id,
        "symbol": purchase.stock_symbol,
        "quantity": float(purchase.quantity),
        "price_per_share": float(purchase.price_per_share),
        "total_amount": float(purchase.quantity) * float(purchase.price_per_share),
        "date": purchase.date.isoformat() if purchase.date else None
    }
