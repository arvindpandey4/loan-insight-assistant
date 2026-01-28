from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel

from auth.jwt_handler import get_current_user, UserInfo
from database import HistoryRepository
from database.history_schema import (
    HistoryEntryCreate, 
    HistoryEntryResponse, 
    QueryType
)

router = APIRouter(prefix="/history", tags=["History"])


class HistoryListResponse(BaseModel):
    """Response model for history list"""
    entries: List[HistoryEntryResponse]
    total: int
    page: int
    limit: int


class CreateHistoryRequest(BaseModel):
    """Request model for creating history entry"""
    query: str
    response: str
    query_type: QueryType = QueryType.GENERAL
    metadata: Optional[dict] = None


@router.get("", response_model=HistoryListResponse)
async def get_history(
    current_user: UserInfo = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    query_type: Optional[QueryType] = None
):
    """
    Get user's query history
    
    - Supports pagination with page and limit
    - Can filter by query_type
    """
    skip = (page - 1) * limit
    
    # Get user_id from token (we need to fetch user from DB by email)
    from database import UserRepository
    user = await UserRepository.get_user_by_email(current_user.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    entries = await HistoryRepository.get_user_history(
        user_id=user.id,
        limit=limit,
        skip=skip,
        query_type=query_type
    )
    
    total = await HistoryRepository.get_user_history_count(user.id)
    
    return HistoryListResponse(
        entries=[
            HistoryEntryResponse(
                id=entry.id,
                query=entry.query,
                response=entry.response,
                query_type=entry.query_type,
                created_at=entry.created_at,
                metadata=entry.metadata
            )
            for entry in entries
        ],
        total=total,
        page=page,
        limit=limit
    )


@router.post("", response_model=HistoryEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_history_entry(
    request: CreateHistoryRequest,
    current_user: UserInfo = Depends(get_current_user)
):
    """
    Create a new history entry
    """
    from database import UserRepository
    user = await UserRepository.get_user_by_email(current_user.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    entry = await HistoryRepository.create_entry(
        HistoryEntryCreate(
            user_id=user.id,
            query=request.query,
            response=request.response,
            query_type=request.query_type,
            metadata=request.metadata
        )
    )
    
    return HistoryEntryResponse(
        id=entry.id,
        query=entry.query,
        response=entry.response,
        query_type=entry.query_type,
        created_at=entry.created_at,
        metadata=entry.metadata
    )


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history_entry(
    entry_id: str,
    current_user: UserInfo = Depends(get_current_user)
):
    """
    Delete a specific history entry
    """
    from database import UserRepository
    user = await UserRepository.get_user_by_email(current_user.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    deleted = await HistoryRepository.delete_entry(entry_id, user.id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History entry not found"
        )


@router.delete("", status_code=status.HTTP_200_OK)
async def clear_history(
    current_user: UserInfo = Depends(get_current_user)
):
    """
    Clear all history for the current user
    """
    from database import UserRepository
    user = await UserRepository.get_user_by_email(current_user.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    deleted_count = await HistoryRepository.delete_user_history(user.id)
    
    return {"message": f"Deleted {deleted_count} history entries"}
