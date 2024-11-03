from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))
    transaction_type = Column(String, nullable=False)  # "BUY", "SELL", "DIVIDEND", "DEPOSIT", "WITHDRAWAL"
    symbol = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    total_amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    
    account = relationship("Account", back_populates="transactions")
    position = relationship("Position", back_populates="transactions") 