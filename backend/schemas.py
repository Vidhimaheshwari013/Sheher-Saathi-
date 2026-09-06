from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    raw_text: str

class ComplaintOut(BaseModel):
    id: int
    raw_text: str
    language: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[int] = None
    duration: Optional[str] = None
    affected_group: Optional[str] = None
    status: str
    verified: bool
    created_at: datetime

    class Config:
        from_attributes = True