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