from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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
    db_complaint = models.Complaint(raw_text=complaint.raw_text)
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@app.get("/complaints", response_model=List[schemas.ComplaintOut])
def get_complaints(db: Session = Depends(get_db)):
    return db.query(models.Complaint).all()