from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

class QueryRequest(BaseModel):
    query: str = Field(..., example="What is the average loan amount?")

class QueryResponse(BaseModel):
    answer: str
    method_used: str
    # agentic RAG fields
    intent: Optional[str] = None
    evidence_points: List[str] = Field(default_factory=list)
    risk_notes: List[str] = Field(default_factory=list)
    compliance_disclaimer: Optional[str] = None
    structured_data: Optional[List[Dict[str, Any]]] = None
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UploadResponse(BaseModel):
    message: str
    filename: str
    records_processed: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatItem(BaseModel):
    name: str
    value: Any
    color: Optional[str] = None

class DashboardStatsResponse(BaseModel):
    total_loans: int
    approval_rate: float
    avg_cibil: float
    avg_loan_amount: float
    loan_status_distribution: List[StatItem]
    loan_type_distribution: List[StatItem]
    recent_applications: List[Dict[str, Any]]

class LoanStatusDistributionResponse(BaseModel):
    distribution: Dict[str, int] = Field(..., example={"Approved": 100, "Rejected": 20})

class AverageCIBILResponse(BaseModel):
    average_scores: Dict[str, float] = Field(..., example={"Approved": 750.5, "Rejected": 600.0})

class RejectionPurposeResponse(BaseModel):
    rejections_by_purpose: Dict[str, int] = Field(..., example={"Home Loan": 15, "Personal Loan": 5})
