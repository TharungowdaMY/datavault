from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    request_id = Column(Integer, ForeignKey("data_requests.id"))
    user_earning = Column(Float)
    platform_cut = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)