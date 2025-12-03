from sqlalchemy.orm import Session
from db.models import UserStock
from fastapi import HTTPException
from db.models import User, UserStock

def get_user_stocks_with_values(db: Session, user_id: int):

    """
    Load all user stocks and do any calculations you want.
    This is the place for your logic.
    """

    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Load stocks
    stocks = (
    db.query(
        UserStock.index_name,
        UserStock.fund_number, 
        UserStock.theoretical_precentage,
        UserStock.actual_precentage,
        UserStock.funds_spent,
        UserStock.theoretical_invested_money,
        UserStock.invested_money_balance,
        UserStock.link_to_etf_provider,
        UserStock.avg_purchase_stock_price,
        UserStock.comments
    )
    .filter(UserStock.user_id == user_id)
    .all()
)
    
    return stocks        