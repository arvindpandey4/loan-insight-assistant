import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Tuple

# Add the project root to sys.path to import rag modules
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agent_system.orchestrator import AgentOrchestrator
from agent_system.schemas import UserQueryInput

class LoanInsightAPI:
    def __init__(self):
        self.orchestrator = None
        self.is_initialized = False

    def initialize(self):
        """Initialize the RAG system"""
        try:
            api_key = os.getenv("GROQ_API_KEY")
            
            #setup the system using AgentOrchestrator
            self.orchestrator = AgentOrchestrator()
            self.is_initialized = True
            print("[OK] LoanInsightAPI initialized successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize LoanInsightAPI: {str(e)}")
            raise e

    def get_insights(self, query: str) -> Tuple[str, str]:
        """Process a query and return insights"""
        if not self.is_initialized:
            self.initialize()
        
        
        #use the orchestrator pipeline
        response_schema = self.orchestrator.pydantic_ai_pipeline(
            UserQueryInput(query_text=query)
        )
        
        return response_schema

    def process_upload(self, file_path: str) -> int:
        """Process an uploaded CSV file (Stub for now)"""
        #in a real scenario, this would trigger the pipeline_orchestrator
        #or update the current dataframe and FAISS index.
        df = pd.read_csv(file_path)
        return len(df)

#global API instance
loan_api = LoanInsightAPI()
