from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class DataRequest(Base):
    __tablename__ = "data_requests"
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signal_type = Column(String(50))
    offer_amount = Column(Float)
    status = Column(String(20), default="pending")
    computed_result = Column(JSON, nullable=True)
    access_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    brand = relationship("Brand", back_populates="requests")
    user = relationship("User", back_populates="requests")