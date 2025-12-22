import time
from typing import Optional

from fastapi import FastAPI, Path, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .auth import create_jwt, verify_jwt, start_session, touch_session
from .rate_limit import check_rate_limit
from .models import MarkdownReport, AnalyzeSectorParams
from .collectors.search import fetch_sector_news
from .collectors.normalize import normalize_news_items
from .analysis.gemini import GeminiClient
from .utils.markdown import build_markdown_report
from .utils.logging import get_logger
from .docs import router as docs_router

logger = get_logger("trade-opportunities")

app = FastAPI(
    title=settings.app_name,
    description="Analyze Indian market sectors and generate structured Markdown trade opportunity reports.",
    version="1.0.0",
)

# CORS (adjust for your client origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.env == "dev" else ["https://yourclient.example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount docs endpoints
app.include_router(docs_router)

def get_auth_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract and verify JWT from Authorization header: `Bearer <token>`
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    user_id = verify_jwt(token)
    return user_id

@app.post("/login", summary="Simple login to obtain JWT", tags=["auth"])
async def login(user_id: str):
    """
    Simple endpoint to generate a JWT for a given user_id.
    In production, validate credentials properly.
    """
    token = create_jwt(user_id)
    session_id = start_session(user_id)
    return {"token": token, "session_id": session_id, "expires_in_seconds": settings.session_ttl_seconds}

@app.get(
    "/analyze/{sector}",
    response_model=MarkdownReport,
    summary="Analyze sector and return a structured Markdown report",
    tags=["analysis"]
)
async def analyze_sector(
    sector: str = Path(..., min_length=3, max_length=50, description="Sector name"),
    user_id: str = Depends(get_auth_user),
    session_id: Optional[str] = Header(None, description="Session ID returned from /login")
):
    # Input validation through Pydantic model
    try:
        params = AnalyzeSectorParams(sector=sector.lower().strip())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    # Basic session tracking
    if session_id:
        touch_session(session_id)

    # Rate limiting per user or session
    rate_key = session_id or user_id
    remaining, window = check_rate_limit(rate_key)
    logger.info(f"Rate limit check for {rate_key}: remaining={remaining}/{window}s")

    # Data collection layer
    try:
        raw_items = await fetch_sector_news(params.sector)
        normalized_items = normalize_news_items(raw_items)
    except Exception as e:
        logger.exception("Error collecting data")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Data collection failed: {str(e)}")

    # AI analysis layer (Gemini)
    if not settings.google_api_key.get_secret_value():
        # If no key, provide a graceful fallback
        analysis_text = (
            "Gemini API key not configured. Fallback summary:\n"
            f"- The {params.sector} sector in India shows mixed signals.\n"
            "- Validate demand drivers, export trends, and regulatory updates.\n"
            "- Consider a basket approach with risk-managed entries.\n"
        )
    else:
        try:
            gemini = GeminiClient(
                api_key=settings.google_api_key.get_secret_value(),
                model=settings.gemini_model
            )
            analysis_text = await gemini.analyze(params.sector, normalized_items)
        except Exception as e:
            logger.exception("Gemini analysis error")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"AI analysis failed: {str(e)}")

    # Markdown generation
    md = build_markdown_report(params.sector, analysis_text, normalized_items)

    # Final response
    return MarkdownReport(sector=params.sector, markdown=md)

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.exception("Unhandled error")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
