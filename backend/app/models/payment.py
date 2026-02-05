from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    checkout_id = Column(String(255), unique=True, index=True)
    device_id = Column(String(255), index=True)
    product_id = Column(String(255))
    amount = Column(Float)
    currency = Column(String(10))
    status = Column(String(50), default="pending")  # pending, completed, failed
    tokens_granted = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
