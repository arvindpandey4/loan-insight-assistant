import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

# Add parent directory to path to access 'rag' and 'simple_qa'
sys.path.insert(0, str(Path(__file__).parents[1]))

from rag.embedding_generator import EmbeddingGenerator
from rag.langchain_Retriver import LoanRAGRetriever, LoanFAISSVectorStore, LoanEmbeddings
from rag.vector_store import FAISSVectorStore
from simple_qa import setup_system

from .schemas import RetrievedLoanCaseSchema

class RetrievalSystem:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RetrievalSystem, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self):
        if self.initialized:
            return

        print("[RetrievalSystem] Initializing RAG components...")
        # reusing simple_qa setup for consistency, ignoring the router
        _, self.df, self.retriever, _ = setup_system()
        self.initialized = True
        print("[RetrievalSystem] Initialization complete.")

    def retrieve_cases(self, query_text: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[RetrievedLoanCaseSchema]:
        if not self.initialized:
            self.initialize()
            
        # TODO: Implement filtering logic if supported by the underlying retriever or post-retrieval
        # Currently the existing retriever does not seem to support explicit filtering in the retrieve method
        # We will perform retrieval and then map to schema
        
        print(f"[RetrievalSystem] Searching for: {query_text} (top_k={top_k})")
        result = self.retriever.retrieve(query_text, k=top_k, return_score=True)
        
        mapped_results = []
        for doc, score in zip(result.documents, result.scores):
            # Parse metadata to schema
            meta = doc.metadata
            
            # Basic mapping - adjust keys based on actual dataframe columns
            mapped = RetrievedLoanCaseSchema(
                case_id=str(meta.get('index', 'unknown')), 
                customer_name=meta.get('Customer_Name'),
                loan_amount=float(meta.get('Loan_Amount', 0)) if meta.get('Loan_Amount') else None,
                approval_status=meta.get('Loan_Status'),
                similarity_score=float(score) if score is not None else 0.0,
                original_data=meta
            )
            mapped_results.append(mapped)
            
        return mapped_results

# Global instance
retrieval_system = RetrievalSystem()
