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

    deposits = relationship("Deposit", back_populates="user", cascade="all, delete")
    purchases = relationship("Purchase", back_populates="user", cascade="all, delete")
    stocks = relationship("UserStock", back_populates="user", cascade="all, delete")

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String)

    users = relationship("UserStock", back_populates="stock")
    purchases = relationship("Purchase", back_populates="stock")

class UserStock(Base):
    __tablename__ = "user_stocks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))

    user = relationship("User", back_populates="stocks")
    stock = relationship("Stock", back_populates="users")

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
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    quantity = Column(Numeric(12, 4))
    price_per_share = Column(Numeric(12, 2))
    date = Column(Date)

    user = relationship("User", back_populates="purchases")
    stock = relationship("Stock", back_populates="purchases")
