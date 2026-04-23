# Qontint — Semantic Authority OS

AI-powered system that predicts whether content will rank on Google before it is published.

## The Architecture
Qontint is designed around an **Intelligence Core**. It doesn't just guess keywords — it actually reads the SERP, builds an Entity Knowledge Graph, calculates PageRank for topics, and runs an XGBoost machine learning model to estimate position.

### Stack
- **Frontend**: React + Vite + Tailwind + TanStack Router
- **Backend**: FastAPI + SQLAlchemy + Uvicorn
- **Intelligence**: spaCy (NLP), NetworkX (Graphs), XGBoost (ML)
- **Scraping**: Playwright, httpx, BeautifulSoup
- **LLM Engine**: Claude API (primary), Ollama (fallback)
- **Extensible Storage**: Neo4j (graph), PostgreSQL (relational), Redis (cache)

---

## 🚀 How to Run Locally

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**

### 2. First Time Setup

You only need to install the dependencies once. Open a terminal and run:

**Backend Setup:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux

pip install -r requirements.txt
playwright install chromium
python -m spacy download en_core_web_sm
```

**Frontend Setup:**
```bash
cd frontend
npm install
```

### 3. Environment Variables (Optional but recommended)
Qontint comes with mock data to run immediately, but for real production data, add your keys to `backend/.env`:

- `ANTHROPIC_API_KEY`: Hook up Claude for AI generation
- `AHREFS_API_KEY`: Hook up Ahrefs for live SERP data
- `YOUTUBE_API_KEY`: Hook up YouTube ranking predictions

*(See `backend/.env` for all configuration options).*

### 4. Running the App
The absolute easiest way to start both the frontend and backend simultaneously is to double click the **`start.bat`** file in the root directory (Windows).

Alternatively, run them separately:

**Start Backend (Terminal 1):**
```bash
cd backend
# Make sure your venv is activated!
uvicorn app.main:app --reload --port 8000
```

**Start Frontend (Terminal 2):**
```bash
cd frontend
npm run dev -- --port 8081
```

Once running, the application is available at:
- Web App: **http://localhost:8081**
- API Docs: **http://localhost:8000/docs**

---

## 🛠 Features

1. **SERP Collection**: Real-time DuckDuckGo or Ahrefs scraping (with Playwright fallback for JS-rendered sites).
2. **Entity Extraction**: NLP pipeline identifies core concepts and relationships.
3. **Knowledge Graph**: NetworkX graph calculates entity authority via PageRank.
4. **Ranking Prediction**: XGBoost ML model evaluates your draft against top competitors.
5. **Multi-Vertical SLMs**: Includes industry-specific patterns for SaaS, Mortgage, Healthcare, Finance, Legal, and Insurance.
6. **YouTube Prediction**: Video title, transcript, and tag optimization scoring.
