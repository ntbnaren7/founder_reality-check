from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# --- SQLAlchemy Models ---

class Startup(Base):
    __tablename__ = "startups"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    snapshots = relationship("Snapshot", back_populates="startup", order_by="Snapshot.version")

class Snapshot(Base):
    __tablename__ = "snapshots"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    startup_id = Column(String, ForeignKey("startups.id"))
    version = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Core Narrative
    problem = Column(Text, nullable=True)
    target_user = Column(Text, nullable=True)
    job_to_be_done = Column(Text, nullable=True)
    
    # Solution
    solution = Column(Text, nullable=True)
    value_prop = Column(Text, nullable=True)
    
    # Distribution
    primary_channel_type = Column(String, nullable=True)
    primary_channel_description = Column(Text, nullable=True)
    
    # Hypothesis
    hypothesis = Column(Text, nullable=True)
    metric = Column(String, nullable=True)
    timeframe = Column(String, nullable=True)
    
    # Risk & Next Steps
    tech_feasibility_notes = Column(Text, nullable=True)
    top_risks = Column(JSON, default=list) # List[str]
    declared_next_steps = Column(JSON, default=list) # List[str]
    
    startup = relationship("Startup", back_populates="snapshots")

# --- Pydantic Models ---

class StartupSnapshot(BaseModel):
    startup_id: str
    version: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    problem: Optional[str] = None
    target_user: Optional[str] = None
    job_to_be_done: Optional[str] = None
    
    solution: Optional[str] = None
    value_prop: Optional[str] = None
    
    primary_channel_type: Optional[Literal["cold_outreach", "community", "paid_ads", "partnerships", "marketplace", "product_led"]] = None
    primary_channel_description: Optional[str] = None
    
    hypothesis: Optional[str] = None
    metric: Optional[str] = None
    timeframe: Optional[str] = None
    
    tech_feasibility_notes: Optional[str] = None
    top_risks: List[str] = Field(default_factory=list)
    declared_next_steps: List[str] = Field(default_factory=list)

class DimensionReview(BaseModel):
    dimension: str
    severity: Literal["blocker", "major", "minor", "ok"]
    issue: Optional[str] = None
    evidence: Optional[str] = None
    recommendation: Optional[str] = None

class Experiment(BaseModel):
    title: str
    channel_type: str
    steps: List[str]
    success_criteria: str
    time_cost: str

class DriftItem(BaseModel):
    field: str
    before: Optional[str]
    after: Optional[str]
    classification: Literal["major_change", "minor_refinement"]
    comment: Optional[str] = None

class AnalysisResponse(BaseModel):
    snapshot: StartupSnapshot
    dimension_reviews: List[DimensionReview]
    experiments: List[Experiment]
    drift: List[DriftItem]
    status: Literal["BLOCKED", "OK"]
