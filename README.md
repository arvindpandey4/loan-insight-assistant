# 🏦 Loan Insight Assistant - AI-Powered RAG System

An intelligent loan analysis assistant powered by **Retrieval-Augmented Generation (RAG)**, **Golden Knowledge Base**, and **Conversational AI**. Get instant insights into loan approvals, rejections, and risk factors with a beautiful, modern interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![React](https://img.shields.io/badge/react-18.0+-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)

---

## ✨ Features

### 🤖 **Conversational AI Assistant**
- **Real-time chat interface** with message history
- **Context-aware responses** using conversation history
- **Golden Knowledge Base** for instant, curated answers
- **RAG-powered insights** from historical loan data

### 📊 **Comprehensive Analytics**
- Interactive dashboards with real-time statistics
- Loan approval/rejection trends
- CIBIL score analysis
- Income range breakdowns
- **Exportable reports** (CSV format)

### 🔐 **Secure Authentication**
- Google OAuth 2.0 integration
- JWT-based session management
- Protected routes and user-specific history

### 🎯 **Smart Features**
- **Golden KB Fast-Track**: Instant answers for common queries (no RAG needed)
- **Hallucination Prevention**: Conversational query detection
- **Evidence-Based Responses**: Clear explanations with risk factors
- **Compliance-Safe**: Educational insights only, no approval decisions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB (local or Atlas)
- Docker & Docker Compose (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/BridgeLabz_Loan_RAG.git
cd BridgeLabz_Loan_RAG/Loan_Insight_Assistant_RAG
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Frontend URL
FRONTEND_URL=http://localhost:5173

# MongoDB
MONGO_URI=mongodb://localhost:27017/loan_insights
# Or use MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Groq API Key (for LLM)
GROQ_API_KEY=your-groq-api-key
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

This will start:
- Backend API on port 8000
- Frontend on port 5173
- MongoDB on port 27017

---

## 📁 Project Structure

```
Loan_Insight_Assistant_RAG/
├── backend/
│   ├── agent_system/          # AI Agent orchestration
│   │   ├── agents/            # Query & Explanation agents
│   │   ├── golden_kb.json     # Curated knowledge base
│   │   ├── golden_kb_handler.py
│   │   ├── orchestrator.py    # Main pipeline
│   │   └── schemas.py         # Pydantic models
│   ├── auth/                  # OAuth & JWT
│   ├── database/              # MongoDB models
│   ├── rag/                   # RAG components
│   ├── api.py                 # Core API logic
│   ├── main.py                # FastAPI app
│   ├── services.py            # API routes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConversationalChat.jsx  # Chat interface
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── loanInsightsApi.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── .env
├── docker-compose.yml
├── API_DOCS.md
└── README.md
```

---

## 🎨 Key Components

### Backend Architecture

#### **1. Agent System**
- **Query Understanding Agent**: Detects user intent and extracts filters
- **Retrieval System**: FAISS-powered vector search
- **Explanation Agent**: Generates compliance-safe explanations
- **Orchestrator**: Manages the entire pipeline

#### **2. Golden Knowledge Base**
- 10+ curated Q&A pairs
- Instant responses for common queries
- Semantic similarity matching
- Categories: CIBIL scores, DTI ratios, rejection reasons, etc.

#### **3. RAG Pipeline**
- LangChain integration
- FAISS vector store
- FastEmbed embeddings
- Top-k retrieval with scoring

### Frontend Architecture

#### **1. Conversational Chat**
- Real-time message streaming
- Conversation history management
- Golden KB indicators (✨ sparkle badge)
- Evidence points and risk notes display

#### **2. Analytics Dashboard**
- Recharts visualizations
- Real-time data fetching
- CSV export functionality
- Responsive design

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Secret | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT signing | Yes |
| `MONGO_URI` | MongoDB connection string | Yes |
| `GROQ_API_KEY` | Groq LLM API key | Yes |
| `FRONTEND_URL` | Frontend URL for CORS | Yes |

### Golden KB Customization

Edit `backend/agent_system/golden_kb.json` to add/modify curated answers:

```json
{
  "id": "your_topic",
  "questions": ["question 1", "question 2"],
  "answer": "Your curated answer here",
  "category": "category_name"
}
```

---

## 📊 API Endpoints

See [API_DOCS.md](./API_DOCS.md) for complete API documentation.

**Key Endpoints:**
- `POST /query-loan-insights` - Conversational AI queries
- `GET /dashboard-stats` - Dashboard statistics
- `GET /analytics/*` - Analytics data
- `GET /history` - User query history
- `POST /upload-loan-data` - Upload CSV data

---

## 🚢 Deployment

### Railway (Backend)
1. Create new project on Railway
2. Connect GitHub repository
3. Add environment variables
4. Deploy from `backend` directory

### Vercel (Frontend)
1. Import project from GitHub
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_BASE_URL=https://your-railway-app.railway.app`
4. Deploy

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **LangChain** - RAG orchestration
- **Groq** - Fast LLM inference
- **FAISS** - Vector similarity search
- **React** - Frontend framework
- **Recharts** - Data visualization

---

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Email: support@loaninsights.com

---

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] Fine-tuned domain-specific LLM
- [ ] Advanced analytics (ML predictions)

---

**Made with ❤️ by the BridgeLabz Team**
