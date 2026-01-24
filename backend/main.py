from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

from fastapi import FastAPI
from backend.services import router
from backend.middleware import setup_middleware
from backend.api import loan_api

app = FastAPI(
    title="Loan Insight Assistant API",
    description="API for intelligent loan data search and analysis using RAG",
    version="1.0.0"
)

#setup middleware (CORS, Logging)
setup_middleware(app)

#api routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    #initialize the RAG system on startup
    try:
        loan_api.initialize()
    except Exception as e:
        print(f"Warning: RAG system could not be initialized at startup: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
