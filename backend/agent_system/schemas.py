from enum import Enum
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

# --- Enums ---

class IntentType(str, Enum):
    WHY_REJECTED = "why_rejected"
    WHY_APPROVED = "why_approved"
    SIMILAR_CASES = "similar_cases"
    RISK_ANALYSIS = "risk_analysis"
    AUDIT_REASON = "audit_reason"
    GENERAL_INQUIRY = "general_inquiry"

class RiskFlag(str, Enum):
    HIGH_DTI = "high_dti"
    LOW_CREDIT_SCORE = "low_credit_score"
    INCONSISTENT_INCOME = "inconsistent_income"
    EMPLOYMENT_GAP = "employment_gap"
    MISSING_DOCS = "missing_docs"
    OTHER = "other"

class ComplianceTone(str, Enum):
    AUDIT = "audit"
    BUSINESS = "business"
    NEUTRAL = "neutral"

# --- Models ---

class UserQueryInput(BaseModel):
    query_text: str
    user_role: Optional[str] = "loan_officer"  # e.g., loan_officer, auditor

class QueryIntentSchema(BaseModel):
    intent: IntentType
    loan_id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Extracted filters like amount range, term, etc.")
    top_k_hint: int = Field(default=5, description="Suggested number of cases to retrieve")
    compliance_tone: ComplianceTone = ComplianceTone.NEUTRAL
    confidence_score: float = Field(default=0.0, description="Confidence in intent detection (0-1)")

class RetrievedLoanCaseSchema(BaseModel):
    """Schema for a single retrieved loan case"""
    case_id: Optional[str] = None
    customer_name: Optional[str] = None
    loan_amount: Optional[float] = None
    approval_status: Optional[str] = None
    similarity_score: float
    original_data: Dict[str, Any] = Field(default_factory=dict, description="Raw data from the source")
    
class FinalResponseSchema(BaseModel):
    """The final structured response returned to the user"""
    query: str
    intent: IntentType
    retrieved_case_count: int
    summary: str
    evidence_points: List[str] = Field(default_factory=list, description="Bullet points of evidence from similar cases")
    risk_notes: List[str] = Field(default_factory=list, description="Risk factors identified")
    compliance_disclaimer: str
    structured_data: Optional[List[RetrievedLoanCaseSchema]] = None
