import sys
import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


sys.path.append("/Users/ravdeepsingh/Desktop/Loan_Insight_Assistant_RAG")

from backend.main import app
from agent_system.schemas import FinalResponseSchema, IntentType, ComplianceTone

class TestBackendIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("backend.api.AgentOrchestrator")
    def test_query_loan_insights_success(self, MockOrchestrator):
        mock_instance = MockOrchestrator.return_value
        
        mock_response = FinalResponseSchema(
            query="Why was loan 123 rejected?",
            intent=IntentType.WHY_REJECTED,
            retrieved_case_count=3,
            summary="Loan 123 was rejected due to high DTI.",
            evidence_points=["Case A had DTI 0.5 and was rejected."],
            risk_notes=["High DTI is a major risk factor."],
            compliance_disclaimer="AI generated.",
            structured_data=[]
        )
        
        mock_instance.pydantic_ai_pipeline.return_value = mock_response

        response = self.client.post(
            "/query-loan-insights",
            json={"query": "Why was loan 123 rejected?"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["answer"], "Loan 123 was rejected due to high DTI.")
        self.assertEqual(data["method_used"], "Agentic RAG")
        self.assertEqual(data["intent"], "why_rejected")
        self.assertEqual(len(data["evidence_points"]), 1)
        self.assertEqual(data["risk_notes"][0], "High DTI is a major risk factor.")

        print("\n[SUCCESS] /query-loan-insights endpoint verified successfully.")

if __name__ == "__main__":
    unittest.main()
