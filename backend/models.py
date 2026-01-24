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
