from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Optional
from .models import QueryRequest, QueryResponse, HealthResponse, UploadResponse, DashboardStatsResponse, LoanStatusDistributionResponse, AverageCIBILResponse, RejectionPurposeResponse
from .api import loan_api
from .analytics import analytics_service
from .auth.jwt_handler import get_current_user_optional, UserInfo
from .database import UserRepository, HistoryRepository
from .database.history_schema import HistoryEntryCreate, QueryType
import shutil
import os
from pathlib import Path

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", version="1.0.0")

@router.get("/dashboard-stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats():
    try:
        stats = loan_api.get_dashboard_stats()
        return DashboardStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard stats: {str(e)}")

@router.post("/query-loan-insights", response_model=QueryResponse)
async def query_insights(
    request: QueryRequest,
    current_user: Optional[UserInfo] = Depends(get_current_user_optional)
):
    try:
        # Pass conversation history to the orchestrator
        agent_response = loan_api.get_insights(
            request.query,
            conversation_context=request.conversation_history
        )
        
        # convert agent response (FinalResponseSchema) to API response (QueryResponse)
        # we dump the Pydantic model to a dict to easily map fields
        response_data = agent_response.model_dump()
        
        query_response = QueryResponse(
            answer=agent_response.summary,
            method_used="Agentic RAG with Golden KB",
            intent=agent_response.intent,
            evidence_points=agent_response.evidence_points,
            risk_notes=agent_response.risk_notes,
            compliance_disclaimer=agent_response.compliance_disclaimer,
            structured_data=[case.model_dump() for case in (agent_response.structured_data or [])],
            source=agent_response.source
        )
        
        # Save to history if user is authenticated
        if current_user:
            try:
                user = await UserRepository.get_user_by_email(current_user.email)
                if user:
                    await HistoryRepository.create_entry(
                        HistoryEntryCreate(
                            user_id=user.id,
                            query=request.query,
                            response=agent_response.summary,
                            query_type=QueryType.LOAN_ANALYSIS,
                            metadata={
                                "intent": agent_response.intent.value,
                                "case_count": agent_response.retrieved_case_count,
                                "source": agent_response.source
                            }
                        )
                    )
            except Exception as hist_err:
                # Don't fail the request if history save fails
                print(f"[WARN] Failed to save history: {hist_err}")
        
        return query_response
    except Exception as e:
        import traceback
        print(f"[ERROR] Query processing failed:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.post("/upload-loan-data", response_model=UploadResponse)
async def upload_data(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        records = loan_api.process_upload(str(file_path))
        
        return UploadResponse(
            message="File uploaded and processed successfully",
            filename=file.filename,
            records_processed=records
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@router.get("/analytics/loan-status", response_model=LoanStatusDistributionResponse)
async def get_loan_status_analytics():
    try:
        data = analytics_service.get_loan_status_distribution()
        return LoanStatusDistributionResponse(distribution=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching loan status analytics: {str(e)}")

@router.get("/analytics/cibil-by-status", response_model=AverageCIBILResponse)
async def get_cibil_analytics():
    try:
        data = analytics_service.get_avg_cibil_by_status()
        return AverageCIBILResponse(average_scores=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CIBIL analytics: {str(e)}")

@router.get("/analytics/rejections-by-purpose", response_model=RejectionPurposeResponse)
async def get_rejection_analytics():
    try:
        data = analytics_service.get_rejections_by_purpose()
        return RejectionPurposeResponse(rejections_by_purpose=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching rejection analytics: {str(e)}")
