from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP)

    #  relationship
    deposits = relationship("Deposit", back_populates="user", cascade="all, delete")
    purchases = relationship("Purchase", back_populates="user", cascade="all, delete")
    user_stocks = relationship("UserStock", back_populates="user", cascade="all, delete")


class UserStock(Base):
    __tablename__ = "user_stocks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    index_name = Column(String, nullable=False)  # Store symbol directly instead of stock_id
    fund_number = Column(String, nullable=False)
    theoretical_precentage = Column(Numeric(2, 0))
    actual_precentage = Column(Numeric(2, 0))
    funds_spent = Column(Numeric(12, 2))
    theoretical_invested_money = Column(Numeric(12, 2))
    invested_money_balance = Column(Numeric(12, 2))
    link_to_etf_provider = Column(String)
    avg_purchase_stock_price = Column(Numeric(12, 2))
    comments = Column(String)

    #  relationship
    user = relationship("User", back_populates="user_stocks")

class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    amount = Column(Numeric(12, 2))
    date = Column(Date)

    user = relationship("User", back_populates="deposits")

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    date = Column(Date)
    stock_type = Column(String, nullable=False)  # Store symbol directly instead of stock_id
    amount_of_stocks = Column(Numeric(12, 4))
    price_per_stock = Column(Numeric(12, 2))
    fee = Column(Numeric(12, 3))
    total_purchase = Column(Numeric(12, 2))

    user = relationship("User", back_populates="purchases")
