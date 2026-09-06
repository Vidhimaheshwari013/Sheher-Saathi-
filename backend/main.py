from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ai.extraction import extract_complaint
from . import models, schemas
from .database import engine, get_db

# Creates the sheher_saathi.db file + complaints table on first run
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sheher Saathi API")

@app.get("/")
def root():
    return {"status": "Sheher Saathi backend is running"}

@app.post("/complaints", response_model=schemas.ComplaintOut)
def create_complaint(complaint: schemas.ComplaintCreate, db: Session = Depends(get_db)):
    analysis = extract_complaint(complaint.raw_text)

    issues = analysis.get("issues", [])
    first_issue = issues[0] if issues else {}

    db_complaint = models.Complaint(
        raw_text=complaint.raw_text,
        language=analysis.get("language"),
        category=first_issue.get("category"),
        location=first_issue.get("location"),
        severity=first_issue.get("severity"),
        duration=first_issue.get("duration"),
        affected_group=first_issue.get("affected_group"),
        followup_question=analysis.get("followup_question") if analysis.get("needs_followup") else None,
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@app.get("/complaints", response_model=List[schemas.ComplaintOut])
def get_complaints(db: Session = Depends(get_db)):
    return db.query(models.Complaint).all()

@app.post("/complaints/analyze")
def analyze_complaint(complaint: schemas.ComplaintCreate):
    result = extract_complaint(complaint.raw_text)
    return result

@app.post("/complaints/{complaint_id}/followup", response_model=schemas.ComplaintOut)
def answer_followup(complaint_id: int, payload: schemas.FollowupAnswer, db: Session = Depends(get_db)):
    db_complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    db_complaint.followup_answer = payload.answer

    # Re-run extraction combining original text + follow-up answer for richer detail
    combined_text = f"{db_complaint.raw_text}. Additional detail: {payload.answer}"
    analysis = extract_complaint(combined_text)
    issues = analysis.get("issues", [])
    first_issue = issues[0] if issues else {}

    db_complaint.severity = first_issue.get("severity") or db_complaint.severity
    db_complaint.duration = first_issue.get("duration") or db_complaint.duration
    db_complaint.location = first_issue.get("location") or db_complaint.location

    db.commit()
    db.refresh(db_complaint)
    return db_complaint