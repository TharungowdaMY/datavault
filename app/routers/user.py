from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.data_source import DataSource
from app.models.request import DataRequest
from app.models.transaction import Transaction
from app.core.encryption import encrypt_data
from app.core.signals import compute_signal
from app.core.security import decode_token, get_token
from datetime import datetime, timedelta

router = APIRouter()

def get_current_user(token: str = Depends(get_token), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if payload.get("type") != "user":
        raise HTTPException(status_code=403, detail="Not a user account")
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/upload")
def upload_data(
    data_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = file.file.read().decode("utf-8")
    encrypted = encrypt_data(content)
    source = DataSource(
        user_id=current_user.id,
        data_type=data_type,
        encrypted_blob=encrypted
    )
    db.add(source)
    db.commit()
    return {"message": "Data uploaded and encrypted successfully", "data_type": data_type}

@router.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sources = db.query(DataSource).filter(DataSource.user_id == current_user.id).all()
    pending = db.query(DataRequest).filter(
        DataRequest.user_id == current_user.id,
        DataRequest.status == "pending"
    ).all()
    return {
        "name": current_user.name,
        "wallet_balance": current_user.wallet_balance,
        "data_sources": [{"id": s.id, "type": s.data_type, "uploaded": s.uploaded_at} for s in sources],
        "pending_requests": len(pending)
    }

@router.get("/notifications")
def notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    requests = db.query(DataRequest).filter(
        DataRequest.user_id == current_user.id,
        DataRequest.status == "pending"
    ).all()
    return [
        {
            "request_id": r.id,
            "brand_id": r.brand_id,
            "signal_type": r.signal_type,
            "offer_amount": r.offer_amount,
            "created_at": r.created_at
        }
        for r in requests
    ]

@router.post("/accept/{request_id}")
def accept_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(DataRequest).filter(
        DataRequest.id == request_id,
        DataRequest.user_id == current_user.id,
        DataRequest.status == "pending"
    ).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    source = db.query(DataSource).filter(
        DataSource.user_id == current_user.id,
        DataSource.is_active == True
    ).first()
    if not source:
        raise HTTPException(status_code=400, detail="No data source found. Please upload a CSV first.")

    result = compute_signal(source.encrypted_blob, req.signal_type)
    platform_cut = round(req.offer_amount * 0.10, 2)
    user_earning = round(req.offer_amount - platform_cut, 2)

    req.status = "accepted"
    req.computed_result = result
    req.access_expires_at = datetime.utcnow() + timedelta(hours=24)
    current_user.wallet_balance = round(current_user.wallet_balance + user_earning, 2)

    transaction = Transaction(
        user_id=current_user.id,
        brand_id=req.brand_id,
        request_id=req.id,
        user_earning=user_earning,
        platform_cut=platform_cut
    )
    db.add(transaction)
    db.commit()

    return {
        "message": "Request accepted",
        "earned": user_earning,
        "new_balance": current_user.wallet_balance,
        "access_expires": req.access_expires_at
    }

@router.post("/reject/{request_id}")
def reject_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(DataRequest).filter(
        DataRequest.id == request_id,
        DataRequest.user_id == current_user.id,
        DataRequest.status == "pending"
    ).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = "rejected"
    db.commit()
    return {"message": "Request rejected"}

@router.get("/transactions")
def transactions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    txns = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    return [
        {"id": t.id, "earned": t.user_earning, "platform_cut": t.platform_cut, "date": t.created_at}
        for t in txns
    ]