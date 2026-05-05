from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    industry = Column(String(100))
    credits = Column(Float, default=1000.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    requests = relationship("DataRequest", back_populates="brand")