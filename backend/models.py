from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(String, nullable=False)
    language = Column(String, nullable=True)
    category = Column(String, nullable=True)
    location = Column(String, nullable=True)
    severity = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)
    affected_group = Column(String, nullable=True)
    status = Column(String, default="pending")
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    followup_question = Column(String, nullable=True)
    followup_answer = Column(String, nullable=True)