import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List

# Add the project root to sys.path to import rag modules
# project_root is the directory containing 'agent_system', 'rag', etc.
# Since this file (api.py) is now in 'backend/', and 'agent_system' is in 'backend/agent_system',
# the project root is effectively the directory containing this file.

project_root = str(Path(__file__).parent)
parent_root = str(Path(__file__).parent.parent)

# Add parent directory (project root) first
if parent_root not in sys.path:
    sys.path.insert(0, parent_root)

# Add backend directory LAST (so it is at index 0)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
else:
    # If already in path, move to front
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

from agent_system.schemas import UserQueryInput

class LoanInsightAPI:
    def __init__(self):
        self.orchestrator = None
        self.is_initialized = False

    def initialize(self):
        """Initialize the RAG system"""
        try:
            # Lazy import to avoid heavy loading at module level
            from agent_system.orchestrator import AgentOrchestrator
            
            api_key = os.getenv("GROQ_API_KEY")
            
            #setup the system using AgentOrchestrator
            self.orchestrator = AgentOrchestrator()
            self.is_initialized = True
            print("[OK] LoanInsightAPI initialized successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize LoanInsightAPI: {str(e)}")
            raise e

    def get_insights(self, query: str, conversation_context: List[Dict[str, str]] = None):
        """Process a query and return insights with conversation support"""
        if not self.is_initialized:
            self.initialize()
        
        
        #use the orchestrator pipeline with conversation context
        response_schema = self.orchestrator.pydantic_ai_pipeline(
            UserQueryInput(query_text=query),
            conversation_context=conversation_context
        )
        
        return response_schema

    def process_upload(self, file_path: str) -> int:
        """Process an uploaded CSV file (Stub for now)"""
        #in a real scenario, this would trigger the pipeline_orchestrator
        #or update the current dataframe and FAISS index.
        df = pd.read_csv(file_path)
        return len(df)

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Calculate dashboard statistics from the CSV dataset"""
        try:
            # Path to the dataset - adjusting to the correct relative or absolute path
            # Path to the dataset - assuming it's in the same project root
            csv_path = Path(project_root) / "hdfc_loan_dataset_full_enriched - hdfc_loan_dataset_full_enriched.csv"
            
            if not csv_path.exists():
                print(f"[ERROR] CSV file not found at {csv_path}")
                # Fallback to empty stats
                return {
                    "total_loans": 0,
                    "approval_rate": 0.0,
                    "avg_cibil": 0.0,
                    "avg_loan_amount": 0.0,
                    "loan_status_distribution": [],
                    "loan_type_distribution": [],
                    "recent_applications": []
                }

            df = pd.read_csv(csv_path)
            
            # Simple aggregations
            total_loans = len(df)
            
            # Approval Rate
            approved_count = len(df[df['Loan_Status'] == 'Approved'])
            approval_rate = (approved_count / total_loans * 100) if total_loans > 0 else 0.0
            
            # Avg CIBIL
            avg_cibil = df['CIBIL_Score'].mean() if not df['CIBIL_Score'].empty else 0.0
            
            # Avg Loan Amount
            avg_loan_amount = df['Loan_Amount'].mean() if not df['Loan_Amount'].empty else 0.0

            # Loan Status Distribution
            status_counts = df['Loan_Status'].value_counts()
            status_dist = [
                {"name": status, "value": int(count), "color": "#10b981" if status == "Approved" else "#ef4444"}
                for status, count in status_counts.items()
            ]

            # Loan Type Distribution
            type_counts = df['Purpose_of_Loan'].value_counts()
            # Assigning some colors cyclically
            colors = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#6366f1"]
            type_dist = [
                {"name": loan_type, "value": int(count), "color": colors[i % len(colors)]}
                for i, (loan_type, count) in enumerate(type_counts.items())
            ]

            # Recent Applications (Just taking the top 5 rows as a proxy for 'recent' if no date provided, 
            # or we could assume the order in CSV implies recency)
            # The CSV has no obvious date column, so we'll take the first 5 rows.
            recent_apps = df.head(5).apply(lambda row: {
                "id": str(row.get('Loan_ID', '')),
                "applicant": str(row.get('Customer_Name', 'Unknown')),
                "amount": float(row.get('Loan_Amount', 0)),
                "status": str(row.get('Loan_Status', 'Pending')),
                "type": str(row.get('Purpose_of_Loan', 'Other'))
            }, axis=1).tolist()

            return {
                "total_loans": total_loans,
                "approval_rate": round(approval_rate, 1),
                "avg_cibil": round(avg_cibil, 0),
                "avg_loan_amount": round(avg_loan_amount, 2),
                "loan_status_distribution": status_dist,
                "loan_type_distribution": type_dist,
                "recent_applications": recent_apps
            }

        except Exception as e:
            print(f"[ERROR] Failed to calculate dashboard stats: {str(e)}")
            return {
                "total_loans": 0,
                "approval_rate": 0.0,
                "avg_cibil": 0.0,
                "avg_loan_amount": 0.0,
                "loan_status_distribution": [],
                "loan_type_distribution": [],
                "recent_applications": []
            }

#global API instance
loan_api = LoanInsightAPI()
