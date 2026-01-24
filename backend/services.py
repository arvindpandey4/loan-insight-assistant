from fastapi import APIRouter, UploadFile, File, HTTPException
from .models import QueryRequest, QueryResponse, HealthResponse, UploadResponse
from .api import loan_api
import shutil
import os
from pathlib import Path

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", version="1.0.0")

@router.post("/query-loan-insights", response_model=QueryResponse)
async def query_insights(request: QueryRequest):
    try:
        agent_response = loan_api.get_insights(request.query)
        
        # convert agent response (FinalResponseSchema) to API response (QueryResponse)
        # we dump the Pydantic model to a dict to easily map fields
        response_data = agent_response.model_dump()
        
        return QueryResponse(
            answer=agent_response.summary,
            method_used="Agentic RAG",
            intent=agent_response.intent,
            evidence_points=agent_response.evidence_points,
            risk_notes=agent_response.risk_notes,
            compliance_disclaimer=agent_response.compliance_disclaimer,
            structured_data=[case.model_dump() for case in (agent_response.structured_data or [])]
        )
    except Exception as e:
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
