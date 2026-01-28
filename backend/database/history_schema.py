from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    """Type of query made by user"""
    LOAN_INSIGHT = "loan_insight"
    SEARCH = "search"
    ANALYTICS = "analytics"
    GENERAL = "general"


class HistoryEntryBase(BaseModel):
    """Base model for history entry"""
    query: str
    response: str
    query_type: QueryType = QueryType.GENERAL


class HistoryEntryCreate(HistoryEntryBase):
    """Model for creating a new history entry"""
    user_id: str
    metadata: Optional[Dict[str, Any]] = None


class HistoryEntryInDB(HistoryEntryBase):
    """History entry as stored in database"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HistoryEntryResponse(BaseModel):
    """History entry for API responses"""
    id: str
    query: str
    response: str
    query_type: QueryType
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
