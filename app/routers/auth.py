from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.brand import Brand
from app.core.security import hash_password, verify_password, create_token
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

# ─── Schemas defined inline (clean and self-contained) ───────────────────────

class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    city: Optional[str] = None
    age: Optional[int] = None

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class BrandRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    industry: Optional[str] = None

class BrandLoginSchema(BaseModel):
    email: EmailStr
    password: str

# ─── User Routes ─────────────────────────────────────────────────────────────

@router.post("/register/user")
def register_user(data: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        city=data.city,
        age=data.age
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "city": user.city,
        "age": user.age,
        "wallet_balance": user.wallet_balance,
        "created_at": user.created_at
    }

@router.post("/login/user")
def login_user(data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": str(user.id), "type": "user"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "name": user.name
    }

# ─── Brand Routes ─────────────────────────────────────────────────────────────

@router.post("/register/brand")
def register_brand(data: BrandRegisterSchema, db: Session = Depends(get_db)):
    if db.query(Brand).filter(Brand.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    brand = Brand(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        industry=data.industry
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return {
        "id": brand.id,
        "name": brand.name,
        "email": brand.email,
        "industry": brand.industry,
        "credits": brand.credits,
        "created_at": brand.created_at
    }

@router.post("/login/brand")
def login_brand(data: BrandLoginSchema, db: Session = Depends(get_db)):
    brand = db.query(Brand).filter(Brand.email == data.email).first()
    if not brand or not verify_password(data.password, brand.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": str(brand.id), "type": "brand"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "brand_id": brand.id,
        "name": brand.name
    }

# ─── Health Check ─────────────────────────────────────────────────────────────

@router.get("/health")
def health():
    return {"status": "auth router working"}