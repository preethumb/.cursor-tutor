from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Position(Base):
    __tablename__ = 'positions'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    symbol = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    cost_basis = Column(Float, nullable=False)
    current_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    account = relationship("Account", back_populates="positions")
    transactions = relationship("Transaction", back_populates="position") 