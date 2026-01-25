from fastapi.testclient import TestClient
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Create a TestClient
client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_dashboard_stats():
    # We can rely on the real implementation if the CSV exists, which it uses.
    response = client.get("/dashboard-stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_loans" in data
    assert "approval_rate" in data

def test_query_endpoint_validation():
    # Test valid payload with mocked backend
    # mocking loan_api.get_insights on the backend module
    with patch("services.loan_api") as mock_api:
        # Mock the return value of get_insights
        msg = MagicMock()
        msg.summary = "Test summary"
        msg.intent = "TEST_INTENT"
        msg.evidence_points = []
        msg.risk_notes = []
        msg.compliance_disclaimer = "Compliance"
        msg.structured_data = [] # empty list
        
        # We need to ensure the mock returns an object that has model_dump() method 
        # or services.py converts it. 
        # Wait, services.py calls agent_response.model_dump(). 
        # So our mock return must have a .model_dump() method.
        msg.model_dump.return_value = {
            "summary": "Test summary",
            "intent": "TEST_INTENT", 
            "evidence_points": [],
            "risk_notes": [],
            "compliance_disclaimer": "Compliance",
            "structured_data": []
        }
        
        mock_api.get_insights.return_value = msg

        response = client.post("/query-loan-insights", json={"query": "Test query"})
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Test summary"
