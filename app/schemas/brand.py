from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BrandRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    industry: Optional[str] = None

class BrandLogin(BaseModel):
    email: EmailStr
    password: str

class BrandOut(BaseModel):
    id: int
    name: str
    email: str
    industry: Optional[str]
    credits: float
    created_at: datetime

    class Config:
        from_attributes = True