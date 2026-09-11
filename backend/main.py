from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from ai.extraction import extract_complaint
from . import models, schemas
from .database import engine, get_db
from ai.embeddings import get_embedding
from ai.faiss_index import complaint_index
from ai.clustering import cluster_complaints
from ai.priority import calculate_priority
from datetime import datetime, timedelta, timezone
from ai.extraction import summarize_cluster

# Creates the sheher_saathi.db file + complaints table on first run
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sheher Saathi API")

# Add CORS middleware to allow Vidhi's HTML/CSS frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (safe for local dev/hackathon)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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
    embedding = get_embedding(db_complaint.raw_text)
    complaint_index.add(db_complaint.id, embedding)
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

@app.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    complaints = db.query(models.Complaint).all()
    if not complaints:
        return {"clusters": []}

    ids = [c.id for c in complaints]
    embeddings = [get_embedding(c.raw_text) for c in complaints]
    labels = cluster_complaints(ids, embeddings)

    # Group complaints by cluster label
    grouped = {}
    for c in complaints:
        label = labels[c.id]
        if label == -1:
            continue  # skip unclustered/noise complaints
        grouped.setdefault(label, []).append(c)

    clusters = []

    VULNERABLE_KEYWORDS = ["children", "bachche", "bachchon", "elderly", "students", "senior"]

    for label, members in grouped.items():
        severities = [m.severity for m in members if m.severity is not None]
        has_vulnerable = any(
        m.affected_group and any(k in m.affected_group.lower() for k in VULNERABLE_KEYWORDS)
        for m in members
        )
        priority = calculate_priority(len(members), severities, has_vulnerable)

        clusters.append({
            "cluster_id": label,
            "size": len(members),
            "category": members[0].category,  # rough guess — Day 5 priority engine refines this
            "locations": list({m.location for m in members if m.location}),
            "complaint_ids": [m.id for m in members],
            "priority": priority,
        })

    return {"clusters": clusters}

@app.get("/clusters/{cluster_id}")
def get_cluster_detail(cluster_id: int, db: Session = Depends(get_db)):
    complaints = db.query(models.Complaint).all()
    ids = [c.id for c in complaints]
    embeddings = [get_embedding(c.raw_text) for c in complaints]
    labels = cluster_complaints(ids, embeddings)

    members = [c for c in complaints if labels.get(c.id) == cluster_id]
    if not members:
        raise HTTPException(status_code=404, detail="Cluster not found")
    summary = summarize_cluster([m.raw_text for m in members])
    return {
        "cluster_id": cluster_id,
        "size": len(members),
        "summary": summary,
        "complaints": [schemas.ComplaintOut.model_validate(m) for m in members],
    }

def evidence_label(complaint) -> str:
    if complaint.verified:
        return "verified"
    if complaint.category or complaint.location or complaint.severity:
        return "ai_inferred"
    return "citizen_reported"

@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    complaints = db.query(models.Complaint).all()
    total = len(complaints)
    verified = len([c for c in complaints if c.verified])

    by_category = {}
    for c in complaints:
        if c.category:
            by_category[c.category] = by_category.get(c.category, 0) + 1

    by_status = {}
    for c in complaints:
        by_status[c.status] = by_status.get(c.status, 0) + 1

    by_evidence_status = {}
    for c in complaints:
        label = evidence_label(c)
        by_evidence_status[label] = by_evidence_status.get(label, 0) + 1

    return {
        "total_complaints": total,
        "verified_count": verified,
        "by_category": by_category,
        "by_status": by_status,
        "by_evidence_status": by_evidence_status,
    }

@app.get("/memory")
def civic_memory(db: Session = Depends(get_db)):
    complaints = db.query(models.Complaint).all()
    location_category_counts = {}

    for c in complaints:
        if c.location and c.category:
            key = (c.location, c.category)
            location_category_counts[key] = location_category_counts.get(key, 0) + 1

    recurring = [
        {"location": loc, "category": cat, "occurrences": count}
        for (loc, cat), count in location_category_counts.items()
        if count >= 2  # "recurring" = seen more than once
    ]
    recurring.sort(key=lambda x: x["occurrences"], reverse=True)

    return {"recurring_issues": recurring}


@app.get("/pulse")
def civic_pulse(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    last_72h_start = now - timedelta(hours=72)
    prev_72h_start = now - timedelta(hours=144)

    complaints = db.query(models.Complaint).all()

    def in_range(c, start, end):
        created = c.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return start <= created < end

    current_window = [c for c in complaints if in_range(c, last_72h_start, now)]
    previous_window = [c for c in complaints if in_range(c, prev_72h_start, last_72h_start)]

    def count_by_category(items):
        counts = {}
        for c in items:
            if c.category:
                counts[c.category] = counts.get(c.category, 0) + 1
        return counts

    current_counts = count_by_category(current_window)
    previous_counts = count_by_category(previous_window)

    emerging = []
    for category, current_count in current_counts.items():
        previous_count = previous_counts.get(category, 0)
        if previous_count == 0 and current_count >= 2:
            emerging.append({
                "category": category,
                "current_72h": current_count,
                "previous_72h": previous_count,
                "status": "new_emerging_issue",
            })
        elif previous_count > 0 and current_count >= previous_count * 2:
            emerging.append({
                "category": category,
                "current_72h": current_count,
                "previous_72h": previous_count,
                "status": "rapid_increase",
            })

    return {
        "current_72h_total": len(current_window),
        "previous_72h_total": len(previous_window),
        "emerging_issues": emerging,
    }

