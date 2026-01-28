from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class AuthProvider(str, Enum):
    """Authentication provider types"""
    GOOGLE = "google"
    EMAIL = "email"


class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    name: str
    picture: Optional[str] = None


class UserCreate(UserBase):
    """Model for creating a new user"""
    google_id: Optional[str] = None
    auth_provider: AuthProvider = AuthProvider.GOOGLE


class UserInDB(UserBase):
    """User model as stored in database"""
    id: Optional[str] = Field(None, alias="_id")
    google_id: Optional[str] = None
    auth_provider: AuthProvider = AuthProvider.GOOGLE
    is_active: bool = True
    is_verified: bool = True  # OAuth users are auto-verified
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserResponse(UserBase):
    """User model for API responses"""
    id: str
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserUpdate(BaseModel):
    """Model for updating user fields"""
    name: Optional[str] = None
    picture: Optional[str] = None
    is_active: Optional[bool] = None
