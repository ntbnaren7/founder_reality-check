from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from .db import get_db, init_db, SessionLocal
from .models import Startup, Snapshot, AnalysisResponse, StartupSnapshot
from .services.snapshot_extractor import extract_snapshot
from .services.user_validator import validate_target_user
from .services.channel_enforcer import enforce_channel
from .services.hypothesis_enforcer import enforce_hypothesis
from .services.drift_analyzer import analyze_drift
from .services.review_engine import generate_reviews_and_experiments

app = FastAPI(title="Founder Reality-Check Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

class AnalyzeRequest(BaseModel):
    input_text: str

@app.post("/api/startups/{startup_id}/analyze", response_model=AnalysisResponse)
def analyze_startup(startup_id: str, request: AnalyzeRequest, db: Session = Depends(get_db)):
    # 1. Load latest snapshot
    db_startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not db_startup:
        db_startup = Startup(id=startup_id)
        db.add(db_startup)
        db.commit()
        current_version = 0
        latest_snapshot_orm = None
    else:
        latest_snapshot_orm = db.query(Snapshot).filter(Snapshot.startup_id == startup_id).order_by(Snapshot.version.desc()).first()
        current_version = latest_snapshot_orm.version if latest_snapshot_orm else 0

    # 2. Extract new snapshot draft
    try:
        new_snapshot_draft = extract_snapshot(startup_id, request.input_text, current_version)
    except Exception as e:
        print(f"Error extracting snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # 3. Run Validators
    user_validation = validate_target_user(new_snapshot_draft.target_user)
    
    # Update draft if improved user suggested and original was bad (optional, or just pass feedback)
    # For now, we keep the user's text but flag it.
    
    channel_enforcement = enforce_channel(new_snapshot_draft.primary_channel_description or request.input_text)
    # Apply enforcement to draft
    new_snapshot_draft.primary_channel_type = channel_enforcement.get("primary_channel_type")
    new_snapshot_draft.primary_channel_description = channel_enforcement.get("primary_channel_description")
    
    hypothesis_enforcement = enforce_hypothesis(new_snapshot_draft.dict())
    new_snapshot_draft.hypothesis = hypothesis_enforcement.get("hypothesis")
    new_snapshot_draft.metric = hypothesis_enforcement.get("metric")
    new_snapshot_draft.timeframe = hypothesis_enforcement.get("timeframe")

    validation_issues = {
        "user": user_validation,
        "channel": channel_enforcement,
        "hypothesis": hypothesis_enforcement
    }

    # 4. Drift Analysis
    drift_items = []
    if latest_snapshot_orm:
        # Convert ORM to Pydantic for comparison
        old_snapshot = StartupSnapshot(
            startup_id=latest_snapshot_orm.startup_id,
            version=latest_snapshot_orm.version,
            problem=latest_snapshot_orm.problem,
            target_user=latest_snapshot_orm.target_user,
            job_to_be_done=latest_snapshot_orm.job_to_be_done,
            solution=latest_snapshot_orm.solution,
            value_prop=latest_snapshot_orm.value_prop,
            primary_channel_type=latest_snapshot_orm.primary_channel_type,
            primary_channel_description=latest_snapshot_orm.primary_channel_description,
            hypothesis=latest_snapshot_orm.hypothesis,
            metric=latest_snapshot_orm.metric,
            timeframe=latest_snapshot_orm.timeframe,
            tech_feasibility_notes=latest_snapshot_orm.tech_feasibility_notes,
            top_risks=latest_snapshot_orm.top_risks or [],
            declared_next_steps=latest_snapshot_orm.declared_next_steps or []
        )
        drift_items = analyze_drift(old_snapshot, new_snapshot_draft)

    # 5. Review Engine
    reviews, experiments, status = generate_reviews_and_experiments(new_snapshot_draft, validation_issues)

    # 6. Save new snapshot
    new_orm = Snapshot(
        startup_id=startup_id,
        version=new_snapshot_draft.version,
        timestamp=new_snapshot_draft.timestamp,
        problem=new_snapshot_draft.problem,
        target_user=new_snapshot_draft.target_user,
        job_to_be_done=new_snapshot_draft.job_to_be_done,
        solution=new_snapshot_draft.solution,
        value_prop=new_snapshot_draft.value_prop,
        primary_channel_type=new_snapshot_draft.primary_channel_type,
        primary_channel_description=new_snapshot_draft.primary_channel_description,
        hypothesis=new_snapshot_draft.hypothesis,
        metric=new_snapshot_draft.metric,
        timeframe=new_snapshot_draft.timeframe,
        tech_feasibility_notes=new_snapshot_draft.tech_feasibility_notes,
        top_risks=new_snapshot_draft.top_risks,
        declared_next_steps=new_snapshot_draft.declared_next_steps
    )
    db.add(new_orm)
    db.commit()

    return AnalysisResponse(
        snapshot=new_snapshot_draft,
        dimension_reviews=reviews,
        experiments=experiments,
        drift=drift_items,
        status=status
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}
