from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.brand import Brand
from app.models.user import User
from app.models.request import DataRequest
from app.models.transaction import Transaction
from app.models.data_source import DataSource
from app.core.security import decode_token, get_token
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class QueryRequest(BaseModel):
    signal_type: str
    offer_amount: float
    target_city: Optional[str] = None
    target_age_min: Optional[int] = None
    target_age_max: Optional[int] = None

def get_current_brand(token: str = Depends(get_token), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "brand":
        raise HTTPException(status_code=403, detail="Not a brand account")
    brand = db.query(Brand).filter(Brand.id == int(payload["sub"])).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.get("/dashboard")
def dashboard(current_brand: Brand = Depends(get_current_brand), db: Session = Depends(get_db)):
    total_spent = db.query(Transaction).filter(Transaction.brand_id == current_brand.id).all()
    spent = sum(t.user_earning + t.platform_cut for t in total_spent)
    return {
        "name": current_brand.name,
        "credits": current_brand.credits,
        "total_spent": round(spent, 2),
        "total_queries": len(total_spent)
    }

@router.post("/query")
def create_query(
    data: QueryRequest,
    current_brand: Brand = Depends(get_current_brand),
    db: Session = Depends(get_db)
):
    query = db.query(User)
    if data.target_city:
        query = query.filter(User.city == data.target_city)
    if data.target_age_min:
        query = query.filter(User.age >= data.target_age_min)
    if data.target_age_max:
        query = query.filter(User.age <= data.target_age_max)

    matched_users = query.all()

    if not matched_users:
        raise HTTPException(status_code=404, detail="No users matched your query filters")

    total_cost = round(data.offer_amount * len(matched_users), 2)

    if current_brand.credits < total_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient credits. Need {total_cost}, have {current_brand.credits}"
        )

    requests_created = 0
    for user in matched_users:
        existing = db.query(DataRequest).filter(
            DataRequest.brand_id == current_brand.id,
            DataRequest.user_id == user.id,
            DataRequest.status == "pending"
        ).first()
        if not existing:
            req = DataRequest(
                brand_id=current_brand.id,
                user_id=user.id,
                signal_type=data.signal_type,
                offer_amount=data.offer_amount
            )
            db.add(req)
            requests_created += 1

    current_brand.credits -= total_cost
    db.commit()

    return {
        "message": "Query sent to matched users",
        "users_matched": len(matched_users),
        "requests_created": requests_created,
        "credits_spent": total_cost,
        "credits_remaining": current_brand.credits
    }

@router.get("/insights")
def get_insights(current_brand: Brand = Depends(get_current_brand), db: Session = Depends(get_db)):
    accepted = db.query(DataRequest).filter(
        DataRequest.brand_id == current_brand.id,
        DataRequest.status == "accepted"
    ).all()

    if not accepted:
        return {"message": "No accepted requests yet", "results": []}

    grouped = {}
    for r in accepted:
        grouped.setdefault(r.signal_type, []).append(r.computed_result)

    insights = {}
    for signal_type, results in grouped.items():
        valid = [r for r in results if r]
        if valid:
            keys = valid[0].keys()
            insights[signal_type] = {
                k: round(
                    sum(r[k] for r in valid if isinstance(r.get(k), (int, float))) / len(valid), 1
                )
                for k in keys
            }

    return {
        "total_responses": len(accepted),
        "insights": insights
    }