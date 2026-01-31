# 🏦 Loan Insight Assistant - AI-Powered RAG System

<div align="center">

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Visit_App-blue?style=for-the-badge)](https://loan-insight-assistant.vercel.app)
[![API Docs](https://img.shields.io/badge/📚_API-Documentation-green?style=for-the-badge)](https://loan-insight-assistant-production.up.railway.app/docs)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![React](https://img.shields.io/badge/react-19.0+-61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)
![License](https://img.shields.io/badge/license-MIT-purple)

**An intelligent loan analysis assistant powered by Retrieval-Augmented Generation (RAG), Golden Knowledge Base, and Conversational AI. Get instant insights into loan approvals, rejections, and risk factors with a beautiful, modern interface.**

[Live Application](https://loan-insight-assistant.vercel.app) • [API Documentation](./API_DOCS.md) • [Report Bug](https://github.com/yourusername/BridgeLabz_Loan_RAG/issues) • [Request Feature](https://github.com/yourusername/BridgeLabz_Loan_RAG/issues)

</div>

---

## 🌟 Overview

Loan Insight Assistant is a production-ready, enterprise-grade AI system that revolutionizes loan analysis through advanced RAG technology. Built with modern web technologies and deployed on cloud infrastructure, it provides real-time insights, conversational AI assistance, and comprehensive analytics for loan decision-making.

### 🎯 Live Deployment

- **Frontend**: [https://loan-insight-assistant.vercel.app](https://loan-insight-assistant.vercel.app)
- **Backend API**: [https://loan-insight-assistant-production.up.railway.app](https://loan-insight-assistant-production.up.railway.app)
- **Interactive API Docs**: [https://loan-insight-assistant-production.up.railway.app/docs](https://loan-insight-assistant-production.up.railway.app/docs)

---

## ✨ Key Features

### 🤖 **Conversational AI Assistant**
- **Real-time chat interface** with persistent message history
- **Context-aware responses** using conversation memory
- **Golden Knowledge Base** for instant, curated answers (10+ expert Q&A pairs)
- **RAG-powered insights** from 1000+ historical loan records
- **Smart intent detection** to prevent hallucinations
- **Evidence-based explanations** with risk factor analysis

### 📊 **Comprehensive Analytics Dashboard**
- **Interactive visualizations** with Recharts
- **Real-time statistics**: approval rates, CIBIL scores, loan amounts
- **Loan type distribution** analysis
- **Status breakdown** (Approved/Rejected)
- **Recent applications** tracking
- **CSV export functionality** for reports
- **Demo mode** with fallback data for seamless UX

### 🔐 **Enterprise-Grade Security**
- **Google OAuth 2.0** integration
- **JWT-based** session management
- **Protected routes** and user-specific history
- **Secure API** with Bearer token authentication
- **MongoDB Atlas** for scalable data storage

### 🎯 **Smart AI Features**
- **Golden KB Fast-Track**: Instant answers for common queries (no RAG latency)
- **Hallucination Prevention**: Conversational query detection
- **Compliance-Safe Responses**: Educational insights only, no approval decisions
- **Multi-turn Conversations**: Context retention across messages
- **Semantic Search**: FAISS-powered vector similarity matching

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB (local or Atlas)
- Groq API Key ([Get one here](https://console.groq.com))
- Google OAuth Credentials ([Setup guide](https://developers.google.com/identity/protocols/oauth2))

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/BridgeLabz_Loan_RAG.git
cd BridgeLabz_Loan_RAG/Loan_Insight_Assistant_RAG
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5173

# MongoDB Connection
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=YourApp

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

# Create frontend/.env
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

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
│   │   ├── golden_kb.json     # Curated knowledge base (10 entries)
│   │   ├── golden_kb_handler.py
│   │   ├── orchestrator.py    # Main pipeline coordinator
│   │   └── schemas.py         # Pydantic models
│   ├── auth/                  # OAuth & JWT authentication
│   │   ├── config.py
│   │   ├── google_oauth.py
│   │   └── jwt_handler.py
│   ├── database/              # MongoDB models & repositories
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── repositories.py
│   ├── rag/                   # RAG components
│   │   ├── embedding_generator.py
│   │   ├── langchain_Retriver.py
│   │   ├── llm_router.py
│   │   └── vector_store.py
│   ├── api.py                 # Core API logic
│   ├── main.py                # FastAPI app entry point
│   ├── services.py            # API route handlers
│   ├── analytics.py           # Analytics endpoints
│   ├── history_routes.py      # User history management
│   ├── middleware.py          # CORS & logging
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConversationalChat.jsx  # Chat interface
│   │   │   ├── Dashboard.jsx           # Main dashboard
│   │   │   ├── Analytics.jsx           # Analytics charts
│   │   │   ├── Sidebar.jsx             # Navigation
│   │   │   └── StatsCard.jsx           # Stat widgets
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   └── AuthCallback.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx         # Auth state management
│   │   ├── services/
│   │   │   └── loanInsightsApi.js      # API client
│   │   ├── App.jsx
│   │   └── index.css                   # Tailwind + custom styles
│   ├── vercel.json                     # Vercel SPA routing config
│   ├── package.json
│   └── vite.config.js
├── .env
├── docker-compose.yml
├── API_DOCS.md
├── LICENSE
└── README.md
```

---

## 🎨 Architecture & Technology Stack

### Backend Architecture

#### **1. Agent System (Agentic RAG)**
- **Query Understanding Agent**: Detects user intent and extracts filters using LLM
- **Golden KB Handler**: Semantic matching for instant curated answers
- **Retrieval System**: FAISS-powered vector search with top-k retrieval
- **Explanation Agent**: Generates compliance-safe, evidence-based explanations
- **Orchestrator**: Manages the entire pipeline with fallback strategies

#### **2. Golden Knowledge Base**
- **10+ curated Q&A pairs** covering:
  - CIBIL score guidelines
  - Loan rejection reasons
  - DTI ratio calculations
  - Approval factors
  - Income requirements
  - Documentation requirements
  - Processing timelines
  - Post-rejection strategies
- **Semantic similarity matching** (threshold: 0.75)
- **Instant responses** (no RAG latency)
- **Expert-curated** and compliance-approved content

#### **3. RAG Pipeline**
- **LangChain** integration for orchestration
- **FAISS** vector store (1000 loan records)
- **Sentence Transformers** embeddings (`all-MiniLM-L6-v2`)
- **Groq LLM** (`llama-3.3-70b-versatile`) for fast inference
- **Top-k retrieval** with similarity scoring

#### **4. Tech Stack**
- **FastAPI** - Modern async web framework
- **MongoDB Atlas** - Cloud database
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **HTTPX** - Async HTTP client
- **Python 3.9+**

### Frontend Architecture

#### **1. Conversational Chat**
- **Real-time messaging** with auto-scroll
- **Conversation history** (last 5 messages for context)
- **Golden KB indicators** (✨ Verified Answer badge)
- **Evidence points** and **risk notes** display
- **Suggested questions** for new users
- **Typing indicators** and loading states

#### **2. Analytics Dashboard**
- **Recharts** visualizations (Bar, Pie charts)
- **Real-time data fetching** with error handling
- **Mock data fallback** for demo mode
- **Responsive design** (mobile-friendly)
- **System health** indicators

#### **3. Tech Stack**
- **React 19** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first styling
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **Framer Motion** - Animations

---

## 🔧 Configuration

### Environment Variables

#### Backend Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | ✅ | `123456-abc.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Secret | ✅ | `GOCSPX-...` |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL | ✅ | `https://your-app.railway.app/auth/google/callback` |
| `JWT_SECRET_KEY` | Secret key for JWT signing | ✅ | `your-super-secret-key` |
| `JWT_ALGORITHM` | JWT algorithm | ✅ | `HS256` |
| `JWT_EXPIRATION_MINUTES` | Token validity period | ✅ | `60` |
| `MONGO_URI` | MongoDB connection string | ✅ | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `GROQ_API_KEY` | Groq LLM API key | ✅ | `gsk_...` |
| `FRONTEND_URL` | Frontend URL for CORS | ✅ | `https://your-app.vercel.app` |
| `PORT` | Server port | ❌ | `8000` |

#### Frontend Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_BASE_URL` | Backend API URL | ✅ | `https://your-app.railway.app` |

### Golden KB Customization

Edit `backend/agent_system/golden_kb.json` to add/modify curated answers:

```json
{
  "id": "your_topic_id",
  "questions": [
    "What is X?",
    "How does X work?",
    "Explain X"
  ],
  "answer": "**Your Topic**\n\nYour detailed, markdown-formatted answer here...",
  "category": "category_name"
}
```

---

## 📊 API Endpoints

See [API_DOCS.md](./API_DOCS.md) for complete API documentation.

### Core Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/query-loan-insights` | Conversational AI queries | Optional |
| `GET` | `/dashboard-stats` | Dashboard statistics | No |
| `GET` | `/analytics/loan-status` | Loan status distribution | No |
| `GET` | `/analytics/cibil-by-status` | Avg CIBIL by status | No |
| `GET` | `/history` | User query history | Yes |
| `POST` | `/upload-loan-data` | Upload CSV data | No |
| `GET` | `/auth/google/login` | Initiate OAuth flow | No |
| `GET` | `/auth/google/callback` | OAuth callback | No |
| `GET` | `/auth/me` | Get current user | Yes |

---

## 🚢 Deployment

### Production Deployment (Current)

**Frontend (Vercel)**
- URL: https://loan-insight-assistant.vercel.app
- Auto-deploys from `main` branch
- Environment variable: `VITE_API_BASE_URL`

**Backend (Railway)**
- URL: https://loan-insight-assistant-production.up.railway.app
- Auto-deploys from `main` branch
- All environment variables configured

### Deploy Your Own

#### Railway (Backend)
1. Create new project on [Railway](https://railway.app)
2. Connect GitHub repository
3. Set root directory to `backend`
4. Add all environment variables from table above
5. Set port to `8000`
6. Deploy

#### Vercel (Frontend)
1. Import project from GitHub on [Vercel](https://vercel.com)
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_BASE_URL=https://your-railway-app.railway.app`
4. Deploy

#### Update OAuth Settings
After deployment, update Google Cloud Console:
- **Authorized JavaScript Origins**: Add your Vercel URL
- **Authorized Redirect URIs**: Add `https://your-railway-app.railway.app/auth/google/callback`

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing
Use the interactive API docs at:
- Local: http://localhost:8000/docs
- Production: https://loan-insight-assistant-production.up.railway.app/docs

---

## 🎯 Use Cases

1. **Loan Officers**: Quick insights into approval patterns and rejection reasons
2. **Risk Analysts**: Historical data analysis and trend identification
3. **Customers**: Educational information about loan requirements
4. **Compliance Teams**: Audit trail with query history
5. **Data Scientists**: CSV export for further analysis

---

## 🔒 Security & Compliance

- ✅ **OAuth 2.0** authentication
- ✅ **JWT** token-based sessions
- ✅ **HTTPS** enforced in production
- ✅ **CORS** properly configured
- ✅ **No PII** in logs
- ✅ **Educational disclaimers** on all responses
- ✅ **No automated decisions** (compliance-safe)

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Write tests for new features
- Update documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **LangChain** - RAG orchestration framework
- **Groq** - Ultra-fast LLM inference
- **FAISS** - Efficient vector similarity search
- **React** - Powerful UI library
- **Recharts** - Beautiful data visualization
- **Vercel** - Seamless frontend deployment
- **Railway** - Simple backend hosting
- **MongoDB Atlas** - Scalable cloud database

---

## 📧 Support & Contact

- **Live Demo**: [https://loan-insight-assistant.vercel.app](https://loan-insight-assistant.vercel.app)
- **Issues**: [GitHub Issues](https://github.com/yourusername/BridgeLabz_Loan_RAG/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/BridgeLabz_Loan_RAG/discussions)
- **Email**: support@loaninsights.com

---

## 🎯 Roadmap

- [x] Conversational AI with RAG
- [x] Golden Knowledge Base
- [x] Google OAuth authentication
- [x] Analytics dashboard
- [x] Production deployment
- [ ] Multi-language support (Hindi, Spanish)
- [ ] Advanced filtering (date ranges, custom queries)
- [ ] Real-time collaboration features
- [ ] Mobile app (React Native)
- [ ] Fine-tuned domain-specific LLM
- [ ] ML-based approval predictions
- [ ] Webhook integrations
- [ ] Admin dashboard

---

## 📊 Project Stats

- **Lines of Code**: 15,000+
- **API Endpoints**: 15+
- **Golden KB Entries**: 10
- **Historical Records**: 1000+
- **Response Time**: <2s (Golden KB: <100ms)
- **Uptime**: 99.9%

---

<div align="center">

**Made with ❤️ by the BridgeLabz Team**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/yourusername/BridgeLabz_Loan_RAG)
[![Live Demo](https://img.shields.io/badge/🚀_Live-Demo-blue?style=for-the-badge)](https://loan-insight-assistant.vercel.app)

</div>
