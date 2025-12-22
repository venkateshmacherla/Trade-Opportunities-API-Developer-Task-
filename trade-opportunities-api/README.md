# Trade Opportunities API

A FastAPI service that analyzes market data and returns structured Markdown trade opportunity reports for Indian sectors. Includes in-memory sessions, JWT auth, per-user rate limiting, web search data collection, and Gemini AI analysis.

## Features
- Single endpoint: `GET /analyze/{sector}` returning a Markdown report
- FastAPI with async I/O
- In-memory session tracking
- Simple JWT authentication
- Per-user/session rate limiting
- Web data collection (DuckDuckGo HTML method; swap for official news APIs)
- Gemini (Google) integration for analysis with graceful fallback
- Clean separation: collectors, analysis, utils, API layers
- Proper error handling, logging, and CORS
- OpenAPI docs at `/docs`

## Quick start

### 1) Prerequisites
- Python 3.10+
- A Google Generative Language API key (optional but recommended)

### 2) Setup
```bash
git clone <your-repo-url> trade-opportunities-api
cd trade-opportunities-api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
