from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.brand import Brand
from app.models.transaction import Transaction
from app.models.request import DataRequest

router = APIRouter()

@router.get("/stats")
def platform_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_brands = db.query(Brand).count()
    total_transactions = db.query(Transaction).count()
    total_requests = db.query(DataRequest).count()
    all_txns = db.query(Transaction).all()
    platform_revenue = round(sum(t.platform_cut for t in all_txns), 2)

    return {
        "total_users": total_users,
        "total_brands": total_brands,
        "total_transactions": total_transactions,
        "total_requests": total_requests,
        "platform_revenue": platform_revenue
    }