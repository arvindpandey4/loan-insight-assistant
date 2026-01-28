from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from .config import get_auth_settings

security = HTTPBearer()


class TokenData(BaseModel):
    """Token payload data"""
    email: str
    name: str
    picture: Optional[str] = None
    exp: Optional[datetime] = None


class UserInfo(BaseModel):
    """User information from token"""
    email: str
    name: str
    picture: Optional[str] = None


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    settings = get_auth_settings()
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        TokenData if valid, None otherwise
    """
    settings = get_auth_settings()
    
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        email: str = payload.get("email")
        name: str = payload.get("name")
        picture: str = payload.get("picture")
        
        if email is None:
            return None
        
        return TokenData(email=email, name=name, picture=picture)
    
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserInfo:
    """
    Dependency to get the current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials
    
    Returns:
        UserInfo object with user details
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    return UserInfo(
        email=token_data.email,
        name=token_data.name,
        picture=token_data.picture
    )


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[UserInfo]:
    """
    Dependency to optionally get the current user (doesn't require auth)
    
    Returns:
        UserInfo if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        token_data = verify_token(credentials.credentials)
        if token_data:
            return UserInfo(
                email=token_data.email,
                name=token_data.name,
                picture=token_data.picture
            )
    except Exception:
        pass
    
    return None
