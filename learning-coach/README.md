# Personalized Learning Coach — AI SaaS Platform

An intelligent adaptive learning platform powered by 7 MCP tools, context-aware AI chatbot, and premium SaaS UI.

## Architecture

```
learning-coach/
├── backend/          # FastAPI + 7 MCP Tools
│   ├── app/
│   │   ├── mcp/      # 7 MCP Tool modules
│   │   ├── api/      # REST API routes
│   │   └── core/     # Config, DB, LLM
│   └── main.py
├── frontend/         # React + Tailwind + Framer Motion
│   └── src/
│       ├── pages/    # Landing, Dashboard, Learn, Analytics
│       └── components/ # Navbar, ChatBot, ApiKeyModal
└── data/             # Sample dataset CSV
```

## 7 MCP Tools

| # | Tool | Purpose |
|---|------|---------|
| 1 | Knowledge Graph Engine | Topic relationships & learning paths |
| 2 | Learner Profiling Agent | Track accuracy, time, user state |
| 3 | Adaptive Difficulty Engine | Dynamic difficulty adjustment |
| 4 | Question Generator | LLM-powered question generation |
| 5 | Explanation Generator | Multi-level explanations |
| 6 | Vector Memory (RAG) | FAISS-based learning history |
| 7 | Progress Analytics Engine | Mastery, engagement, insights |

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys (optional - demo mode works without)

uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:3000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/generate-question | Generate adaptive question |
| POST | /api/submit-answer | Submit answer + get feedback |
| GET | /api/explanation | Get concept explanation |
| GET | /api/progress/{user_id} | Get user progress |
| GET | /api/analytics/{user_id} | Get full analytics |
| GET | /api/learning-path/{user_id} | Get learning path |
| POST | /api/chat | Chat with AI tutor |
| POST | /api/upload/dataset | Upload CSV question bank |
| GET | /api/topics | Get all topics |

## API Key Setup

1. Click "Demo Mode" button in the navbar
2. Enter your OpenAI (`sk-...`) or Gemini (`AIza...`) API key
3. Click "Connect API" — the key is stored locally and sent as a header

**Demo mode** works fully without any API key using the built-in question bank.

## CSV Upload Format

```csv
topic,difficulty,question,option_a,option_b,option_c,correct_answer,explanation
Algorithms,3,What is O(log n)?,Linear,Logarithmic,Quadratic,Logarithmic,Logarithmic complexity...
```

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion, Recharts
- **Backend**: FastAPI, Python 3.11+
- **AI**: LangChain, OpenAI / Gemini
- **Vector DB**: FAISS (with ChromaDB option)
- **Graph**: NetworkX
- **Database**: MongoDB (with in-memory fallback)
