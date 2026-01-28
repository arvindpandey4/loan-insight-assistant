# Loan Insight Assistant - API Documentation

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-railway-app.railway.app`

## Authentication
Most endpoints support optional authentication via JWT Bearer token.

```
Authorization: Bearer <your_jwt_token>
```

---

## Core Endpoints

### 1. Health Check
**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-28T17:21:00Z"
}
```

---

### 2. Query Loan Insights (Conversational AI)
**POST** `/query-loan-insights`

Submit a query to the AI assistant with optional conversation history.

**Request Body:**
```json
{
  "query": "What is a good CIBIL score?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help you?"
    }
  ]
}
```

**Response:**
```json
{
  "answer": "**CIBIL Score Guidelines:**\n\n✅ **750+** - Excellent...",
  "method_used": "Agentic RAG with Golden KB",
  "intent": "general",
  "evidence_points": [
    "✨ This is a curated answer from our Golden Knowledge Base"
  ],
  "risk_notes": [],
  "compliance_disclaimer": "This information is provided for educational purposes...",
  "structured_data": [],
  "source": "golden_kb",
  "timestamp": "2026-01-28T17:21:00Z"
}
```

**Source Types:**
- `golden_kb`: Answer from curated Golden Knowledge Base (instant, high-quality)
- `rag`: Answer from RAG retrieval (historical data analysis)

---

### 3. Dashboard Statistics
**GET** `/dashboard-stats`

Get aggregated statistics for the dashboard.

**Response:**
```json
{
  "total_loans": 9432,
  "approval_rate": 74.8,
  "avg_cibil": 720,
  "avg_loan_amount": 450000,
  "loan_status_distribution": [
    {
      "name": "Approved",
      "value": 7056,
      "color": "#10b981"
    },
    {
      "name": "Rejected",
      "value": 2376,
      "color": "#ef4444"
    }
  ],
  "loan_type_distribution": [
    {
      "name": "Home Loans",
      "value": 3542,
      "color": "#3b82f6"
    }
  ],
  "recent_applications": [
    {
      "id": "L12345",
      "applicant": "John Doe",
      "status": "Approved",
      "type": "Home Loan",
      "amount": 500000
    }
  ]
}
```

---

### 4. Upload Loan Data
**POST** `/upload-loan-data`

Upload CSV file with loan data.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (CSV file)

**Response:**
```json
{
  "message": "File uploaded successfully",
  "filename": "loans.csv",
  "records_processed": 1000,
  "timestamp": "2026-01-28T17:21:00Z"
}
```

---

## Analytics Endpoints

### 5. Loan Status Distribution
**GET** `/analytics/loan-status`

Get loan approval/rejection distribution.

**Response:**
```json
{
  "distribution": {
    "Approved": 7056,
    "Rejected": 2376
  }
}
```

---

### 6. Average CIBIL by Status
**GET** `/analytics/cibil-by-status`

Get average CIBIL scores by loan status.

**Response:**
```json
{
  "average_scores": {
    "Approved": 750.5,
    "Rejected": 620.3
  }
}
```

---

### 7. Rejections by Purpose
**GET** `/analytics/rejections-by-purpose`

Get rejection counts by loan purpose.

**Response:**
```json
{
  "rejections_by_purpose": {
    "Home Loan": 450,
    "Personal Loan": 320,
    "Auto Loan": 180
  }
}
```

---

## History Endpoints

### 8. Get User History
**GET** `/history`

Get query history for authenticated user (requires authentication).

**Query Parameters:**
- `page` (int, default: 1): Page number
- `limit` (int, default: 20, max: 100): Results per page
- `query_type` (optional): Filter by query type

**Response:**
```json
{
  "entries": [
    {
      "id": "hist_123",
      "query": "What is a good CIBIL score?",
      "response": "CIBIL Score Guidelines...",
      "query_type": "LOAN_ANALYSIS",
      "created_at": "2026-01-28T17:21:00Z",
      "metadata": {
        "intent": "general",
        "case_count": 0,
        "source": "golden_kb"
      }
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 20
}
```

---

### 9. Create History Entry
**POST** `/history`

Manually create a history entry (requires authentication).

**Request Body:**
```json
{
  "query": "Why was my loan rejected?",
  "response": "Based on analysis...",
  "query_type": "GENERAL",
  "metadata": {
    "custom_field": "value"
  }
}
```

---

### 10. Delete History Entry
**DELETE** `/history/{entry_id}`

Delete a specific history entry (requires authentication).

**Response:** `204 No Content`

---

### 11. Clear All History
**DELETE** `/history`

Clear all history for the current user (requires authentication).

**Response:**
```json
{
  "message": "Deleted 45 history entries"
}
```

---

## Authentication Endpoints

### 12. Google OAuth Login
**GET** `/auth/google/login`

Initiate Google OAuth flow.

**Response:** Redirects to Google OAuth consent screen

---

### 13. Google OAuth Callback
**GET** `/auth/google/callback`

Handle Google OAuth callback.

**Query Parameters:**
- `code`: OAuth authorization code

**Response:** Redirects to frontend with JWT token

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes:**
- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

---

## Golden Knowledge Base

The system includes a curated Golden Knowledge Base with instant answers for common queries:

**Covered Topics:**
- CIBIL score guidelines
- Loan rejection reasons
- DTI ratio calculations
- Approval factors
- Income requirements
- Documentation requirements
- Processing timelines
- Post-rejection strategies

**Benefits:**
- ⚡ Instant responses (no RAG retrieval needed)
- ✨ Expert-curated content
- 🎯 High accuracy
- 📚 Compliance-approved

---

## Rate Limiting

Currently no rate limiting is enforced. For production deployment, consider implementing rate limiting based on your requirements.

---

## Versioning

Current API Version: **v1.0.0**

The API follows semantic versioning. Breaking changes will result in a major version bump.
