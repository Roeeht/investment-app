from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Deposit, Purchase
from services.protfolio_service import get_user_stocks_with_values
from services.user_service import create_user, verify_user_exists
from services.deposit_service import add_deposit as add_deposit_service
from services.purchase_service import (
    get_user_purchases, 
    calculate_total_spent,
    record_purchase,
    format_purchase
)
from services.fmp_api import fetch_stock

router = APIRouter()

# health check endpoint
@router.get("/health")
def health_check():
    return {"status": "healthy", "message": "Investment BE API is running"}

# user registration endpoint
@router.post("/users/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """Register a new user"""
    
    user = create_user(db, username, email, password)
    
    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }

# =============================================================================
# USER MANAGEMENT ENDPOINTS
# =============================================================================

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user details by ID"""
    from services.user_service import get_user_by_id
    
    user = get_user_by_id(db, user_id)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@router.get("/users/{user_id}/balance")
def get_balance(user_id: int, db: Session = Depends(get_db)):
    """Get user's available cash balance"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Calculate totals
    total_deposits = db.query(
        db.func.coalesce(db.func.sum(Deposit.amount), 0)
    ).filter(Deposit.user_id == user_id).scalar()
    
    total_purchases = db.query(
        db.func.coalesce(db.func.sum(Purchase.quantity * Purchase.price_per_share), 0)
    ).filter(Purchase.user_id == user_id).scalar()
    
    available_cash = float(total_deposits or 0) - float(total_purchases or 0)
    
    return {
        "user_id": user_id,
        "total_deposits": float(total_deposits or 0),
        "total_spent": float(total_purchases or 0),
        "available_cash": available_cash
    }

@router.get("/users/{user_id}/transactions")
def get_transactions(user_id: int, limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get combined deposits and purchases history"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Get deposits
    deposits = db.query(Deposit).filter(
        Deposit.user_id == user_id
    ).order_by(Deposit.date.desc()).limit(limit).all()
    
    # Get purchases
    purchases = db.query(Purchase).filter(
        Purchase.user_id == user_id
    ).order_by(Purchase.date.desc()).limit(limit).all()
    
    # Combine and format
    transactions = []
    
    for deposit in deposits:
        transactions.append({
            "type": "deposit",
            "amount": float(deposit.amount),
            "date": deposit.date.isoformat() if deposit.date else None,
            "description": f"Deposit: ${float(deposit.amount):.2f}"
        })
    
    for purchase in purchases:
        total = float(purchase.quantity) * float(purchase.price_per_share)
        transactions.append({
            "type": "purchase",
            "amount": -total,
            "date": purchase.date.isoformat() if purchase.date else None,
            "description": f"Purchase: {float(purchase.quantity)} shares of {purchase.stock_symbol} @ ${float(purchase.price_per_share):.2f}",
            "symbol": purchase.stock_symbol,
            "quantity": float(purchase.quantity),
            "price": float(purchase.price_per_share)
        })
    
    # Sort by date (most recent first)
    transactions.sort(key=lambda x: x["date"] if x["date"] else "", reverse=True)
    
    # Limit to requested amount
    transactions = transactions[:limit]
    
    return {
        "user_id": user_id,
        "transactions": transactions,
        "count": len(transactions)
    }

@router.get("/users/{user_id}/portfolio/summary")
def get_portfolio_summary(user_id: int, db: Session = Depends(get_db)):
    """Get portfolio summary with total values and gains"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Get balance info
    total_deposits = db.query(
        db.func.coalesce(db.func.sum(Deposit.amount), 0)
    ).filter(Deposit.user_id == user_id).scalar()
    
    total_purchases = db.query(
        db.func.coalesce(db.func.sum(Purchase.quantity * Purchase.price_per_share), 0)
    ).filter(Purchase.user_id == user_id).scalar()
    
    available_cash = float(total_deposits or 0) - float(total_purchases or 0)
    
    # Get portfolio stocks
    stocks = get_user_stocks_with_values(db, user_id)
    
    return {
        "user_id": user_id,
        "total_deposits": float(total_deposits or 0),
        "total_invested": float(total_purchases or 0),
        "available_cash": available_cash,
        "portfolio": stocks
    }

# =============================================================================
# USER STOCKS ENDPOINTS
# =============================================================================

@router.get("/users/{user_id}/stocks")
def get_user_stocks(user_id: int, db: Session = Depends(get_db)):
    """Get all stocks owned by a user with current values"""
    return get_user_stocks_with_values(db=db, user_id=user_id)

   

@router.post("/users/{user_id}/stocks")
def buy_stock(user_id: int, symbol: str, quantity: float, price: float, db: Session = Depends(get_db)):
    """Record stock purchase with specified price"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Record the purchase
    purchase_result = record_purchase(db, user_id, symbol, quantity, price)
    
    return {
        "message": "Stock purchase recorded successfully",
        "purchase": purchase_result
    }

@router.post("/users/{user_id}/stocks/sell")
def sell_stock(user_id: int, symbol: str, quantity: float, price: float, db: Session = Depends(get_db)):
    """Sell stock - reduce holdings and record as negative purchase"""
    from db.models import UserStock
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    if price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    
    # Check if user has this stock
    holding = db.query(UserStock).filter(
        UserStock.user_id == user_id,
        UserStock.stock_symbol == symbol.upper()
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail=f"You don't own any {symbol} stock")
    
    if float(holding.quantity) < quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient shares. You own {float(holding.quantity)} shares, trying to sell {quantity}"
        )
    
    try:
        # Record sale as negative purchase
        sale = Purchase(
            user_id=user_id,
            stock_symbol=symbol.upper(),
            quantity=-quantity,  # Negative for sale
            price_per_share=price,
            date=db.func.current_date()
        )
        db.add(sale)
        
        # Update holdings
        new_quantity = float(holding.quantity) - quantity
        
        if new_quantity == 0:
            # Sold all shares, remove holding
            db.delete(holding)
        else:
            # Update quantity
            holding.quantity = new_quantity
        
        db.commit()
        db.refresh(sale)
        
        total_value = quantity * price
        
        return {
            "message": "Stock sold successfully",
            "sale": {
                "id": sale.id,
                "symbol": symbol.upper(),
                "quantity": quantity,
                "price_per_share": price,
                "total_value": total_value,
                "date": sale.date.isoformat()
            },
            "remaining_shares": new_quantity
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sale failed: {str(e)}")

@router.delete("/users/{user_id}/stocks/{symbol}")
def delete_stock(user_id: int, symbol: str, db: Session = Depends(get_db)):
    """Remove a stock from user's portfolio (must have 0 shares)"""
    from db.models import UserStock
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Find the holding
    holding = db.query(UserStock).filter(
        UserStock.user_id == user_id,
        UserStock.stock_symbol == symbol.upper()
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found in portfolio")
    
    if float(holding.quantity) > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete stock with {float(holding.quantity)} shares. Sell all shares first."
        )
    
    try:
        db.delete(holding)
        db.commit()
        
        return {
            "message": f"Stock {symbol} removed from portfolio"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

# =============================================================================
# DEPOSITS ENDPOINTS
# =============================================================================

@router.get("/users/{user_id}/deposits")
def get_deposits(user_id: int, limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get user's deposit history"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Get deposits
    deposits = db.query(Deposit).filter(
        Deposit.user_id == user_id
    ).order_by(Deposit.date.desc()).limit(limit).all()
    
    deposit_list = [
        {
            "id": deposit.id,
            "amount": float(deposit.amount),
            "date": deposit.date.isoformat() if deposit.date else None
        }
        for deposit in deposits
    ]
    
    # Calculate total
    total = db.query(
        db.func.coalesce(db.func.sum(Deposit.amount), 0)
    ).filter(Deposit.user_id == user_id).scalar()
    
    return {
        "user_id": user_id,
        "deposits": deposit_list,
        "total_deposits": float(total or 0),
        "count": len(deposit_list)
    }

@router.post("/users/{user_id}/deposits")
def add_deposit_endpoint(user_id: int, amount: float, db: Session = Depends(get_db)):
    """Add money deposit for user"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Add deposit via service
    result = add_deposit_service(db, user_id, amount)
    deposit = result["deposit"]
    
    return {
        "message": "Deposit added successfully",
        "deposit": {
            "id": deposit.id,
            "amount": float(deposit.amount),
            "date": deposit.date.isoformat()
        }
    }

@router.put("/users/{user_id}/deposits/{deposit_id}")
def update_deposit(user_id: int, deposit_id: int, amount: float, db: Session = Depends(get_db)):
    """Update an existing deposit"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Find the deposit
    deposit = db.query(Deposit).filter(
        Deposit.id == deposit_id,
        Deposit.user_id == user_id
    ).first()
    
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    
    try:
        deposit.amount = amount
        db.commit()
        db.refresh(deposit)
        
        return {
            "message": "Deposit updated successfully",
            "deposit": {
                "id": deposit.id,
                "amount": float(deposit.amount),
                "date": deposit.date.isoformat() if deposit.date else None
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

@router.delete("/users/{user_id}/deposits/{deposit_id}")
def delete_deposit(user_id: int, deposit_id: int, db: Session = Depends(get_db)):
    """Delete a deposit"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Find the deposit
    deposit = db.query(Deposit).filter(
        Deposit.id == deposit_id,
        Deposit.user_id == user_id
    ).first()
    
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    
    try:
        db.delete(deposit)
        db.commit()
        
        return {
            "message": "Deposit deleted successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

# =============================================================================
# PURCHASES ENDPOINTS
# =============================================================================

@router.get("/users/{user_id}/purchases")
def get_purchases(user_id: int, limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get user's purchase history"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Get purchases from service
    purchases = get_user_purchases(db, user_id, limit)
    
    # Format each purchase
    purchase_list = [format_purchase(purchase) for purchase in purchases]
    
    total = calculate_total_spent(db, user_id)
    
    return {
        "user_id": user_id,
        "purchases": purchase_list,
        "total_spent": total,
        "count": len(purchase_list)
    }

@router.delete("/users/{user_id}/purchases/{purchase_id}")
def delete_purchase(user_id: int, purchase_id: int, db: Session = Depends(get_db)):
    """Delete a purchase record"""
    
    # Verify user exists
    verify_user_exists(db, user_id)
    
    # Find the purchase
    purchase = db.query(Purchase).filter(
        Purchase.id == purchase_id,
        Purchase.user_id == user_id
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    try:
        db.delete(purchase)
        db.commit()
        
        return {
            "message": "Purchase deleted successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

# =============================================================================
# STOCK DATA ENDPOINTS
# =============================================================================

@router.get("/stock")
def get_stock(symbol: str = Query(...)):
    """Get stock data from external API"""
    try:
        stock = fetch_stock(symbol.upper())
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

