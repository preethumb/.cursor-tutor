from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # e.g., "401k", "IRA", "Brokerage"
    institution = Column(String, nullable=False)
    positions = relationship("Position", back_populates="account")
    transactions = relationship("Transaction", back_populates="account") 