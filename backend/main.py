from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

from fastapi import FastAPI
from services import router
from middleware import setup_middleware
from api import loan_api
from auth.google_oauth import router as auth_router
from database.connection import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="Loan Insight Assistant API",
    description="API for intelligent loan data search and analysis using RAG",
    version="1.0.0"
)

#setup middleware (CORS, Logging)
setup_middleware(app)

#api routes
app.include_router(router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    #initialize MongoDB
    await connect_to_mongo()
    
    #initialize the RAG system on startup
    try:
        loan_api.initialize()
    except Exception as e:
        print(f"Warning: RAG system could not be initialized at startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
