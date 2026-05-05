from pydantic import BaseModel
from datetime import datetime

class TransactionOut(BaseModel):
    id: int
    user_id: int
    brand_id: int
    request_id: int
    user_earning: float
    platform_cut: float
    created_at: datetime

    class Config:
        from_attributes = True