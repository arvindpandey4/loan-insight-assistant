import httpx
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from urllib.parse import urlencode

from .config import get_auth_settings
from .jwt_handler import create_access_token, get_current_user
from database import UserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class TokenResponse(BaseModel):
    """Response model for token endpoint"""
    access_token: str
    token_type: str = "bearer"
    user: dict


class GoogleTokenRequest(BaseModel):
    """Request model for exchanging Google auth code"""
    code: str
    redirect_uri: Optional[str] = None


@router.get("/google/login")
async def google_login():
    """
    Initiate Google OAuth login flow
    
    Redirects user to Google's OAuth consent screen
    """
    settings = get_auth_settings()
    
    if not settings.google_client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth not configured"
        )
    
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@router.get("/google/callback")
async def google_callback(code: str, error: Optional[str] = None):
    """
    Handle Google OAuth callback
    
    Exchanges authorization code for tokens and creates JWT
    """
    settings = get_auth_settings()
    
    if error:
        # Redirect to frontend with error
        return RedirectResponse(
            url=f"{settings.frontend_url}/login?error={error}"
        )
    
    try:
        # Exchange authorization code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.google_redirect_uri
                }
            )
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange authorization code"
                )
            
            token_data = token_response.json()
            google_access_token = token_data.get("access_token")
            
            # Get user info from Google
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {google_access_token}"}
            )
            
            if userinfo_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info from Google"
                )
            
            user_info = userinfo_response.json()
        
        # Find or create user in database
        user, is_new = await UserRepository.find_or_create_google_user(
            email=user_info.get("email"),
            name=user_info.get("name"),
            google_id=user_info.get("id"),
            picture=user_info.get("picture")
        )
        
        if is_new:
            print(f"[NEW USER] Created new user: {user.email}")
        else:
            print(f"[LOGIN] User logged in: {user.email}")
        
        # Create our own JWT token with user database ID
        jwt_token = create_access_token({
            "user_id": user.id,
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "google_id": user_info.get("id")
        })
        
        # Redirect to frontend with token
        return RedirectResponse(
            url=f"{settings.frontend_url}/auth/callback?token={jwt_token}"
        )
    
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error communicating with Google: {str(e)}"
        )


@router.post("/google/token", response_model=TokenResponse)
async def google_token_exchange(request: GoogleTokenRequest):
    """
    Exchange Google authorization code for JWT token
    
    Alternative to callback - for SPA/frontend direct integration
    """
    settings = get_auth_settings()
    
    redirect_uri = request.redirect_uri or settings.google_redirect_uri
    
    try:
        async with httpx.AsyncClient() as client:
            # Exchange code for Google tokens
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "code": request.code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri
                }
            )
            
            if token_response.status_code != 200:
                error_detail = token_response.json().get("error_description", "Token exchange failed")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_detail
                )
            
            token_data = token_response.json()
            google_access_token = token_data.get("access_token")
            
            # Get user info
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {google_access_token}"}
            )
            
            if userinfo_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to get user info"
                )
            
            user_info = userinfo_response.json()
        
        # Find or create user in database
        user, is_new = await UserRepository.find_or_create_google_user(
            email=user_info.get("email"),
            name=user_info.get("name"),
            google_id=user_info.get("id"),
            picture=user_info.get("picture")
        )
        
        if is_new:
            print(f"[NEW USER] Created new user: {user.email}")
        else:
            print(f"[LOGIN] User logged in: {user.email}")
        
        # Create JWT with user database ID
        jwt_token = create_access_token({
            "user_id": user.id,
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "google_id": user_info.get("id")
        })
        
        return TokenResponse(
            access_token=jwt_token,
            user={
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "picture": user_info.get("picture")
            }
        )
    
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error communicating with Google: {str(e)}"
        )


@router.get("/me")
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    return {
        "email": current_user.email,
        "name": current_user.name,
        "picture": current_user.picture
    }
