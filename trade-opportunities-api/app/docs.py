from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Health check")
async def health():
    return {"status": "ok"}

@router.get("/", summary="API home")
async def home():
    return {
        "name": "Trade Opportunities API",
        "endpoints": ["/analyze/{sector}", "/login", "/health"],
        "docs": "/docs"
    }
