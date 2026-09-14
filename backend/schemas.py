from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    raw_text: str
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None

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
    followup_question: Optional[str] = None
    followup_answer: Optional[str] = None

    class Config:
        from_attributes = True

class FollowupAnswer(BaseModel):
    answer: str

class ComplaintAdminUpdate(BaseModel):
    status: Optional[str] = None
    verified: Optional[bool] = None