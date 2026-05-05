from pydantic import BaseModel
from typing import Optional, dict as Dict, Any
from datetime import datetime

class CreateQuery(BaseModel):
    signal_type: str
    offer_amount: float
    target_city: Optional[str] = None
    target_age_min: Optional[int] = None
    target_age_max: Optional[int] = None

class RequestOut(BaseModel):
    id: int
    brand_id: int
    user_id: int
    signal_type: str
    offer_amount: float
    status: str
    computed_result: Optional[dict] = None
    access_expires_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True