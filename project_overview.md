# Qontint - Project Overview

## 💻 Programming Languages & Technologies Used

### Frontend (User Interface)
* **TypeScript / TSX:** The primary language for the frontend, providing strong typing for React components.
* **HTML/CSS:** Used for structuring and styling the web application, heavily utilizing **Tailwind CSS** for utility-first styling.
* **JavaScript:** Used in configuration files (like Vite) and underlying Node.js build tools.
* *Frameworks/Libraries:* React, Vite, TanStack Router.

### Backend (Server, API & Machine Learning)
* **Python (3.10+):** The core language for the backend, handling API requests, data processing, machine learning, and natural language processing.
* *Frameworks/Libraries:* FastAPI, SQLAlchemy, Uvicorn, spaCy (NLP), NetworkX (Graphs), XGBoost (ML), Playwright, BeautifulSoup, httpx.

### Infrastructure & Database
* **PostgreSQL / Relational SQL:** For relational data storage (managed via SQLAlchemy).
* **Neo4j:** For extensible graph storage.
* **Redis:** Used for caching.
* **Batch / Shell Scripting:** Used for automation scripts (e.g., `start.bat`).

---

## 🚀 Key Features

1. **SERP Collection (Search Engine Results Page):** Real-time scraping from DuckDuckGo or Ahrefs, with a Playwright fallback mechanism to handle complex, JavaScript-rendered websites.
2. **Entity Extraction (NLP):** An advanced Natural Language Processing pipeline that reads content and identifies core concepts, topics, and relationships.
3. **Knowledge Graph & Authority Scoring:** Uses NetworkX to build an Entity Knowledge Graph and calculates entity authority using PageRank algorithms.
4. **Ranking Prediction Engine:** Integrates an XGBoost Machine Learning model to evaluate a user's draft content against top competitors and estimate its Google search position.
5. **Multi-Vertical SLMs (Small Language Models):** Features industry-specific language models and patterns tailored for SaaS, Mortgage, Healthcare, Finance, Legal, and Insurance sectors.
6. **YouTube Prediction:** Optimization scoring for video titles, transcripts, and tags to predict performance on YouTube.
7. **LLM Engine Integration:** Primary integration with the Claude API for AI generation, with an Ollama fallback.
8. **Real-time Pipeline Analysis:** A dynamic dashboard providing live analysis, ranking predictions, and entity authority visualizations based on user input.
