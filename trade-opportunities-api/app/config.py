import os
from pydantic import BaseModel, Field, SecretStr
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    app_name: str = "Trade Opportunities API"
    env: str = os.getenv("ENV", "dev")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8080"))
    jwt_secret: SecretStr = SecretStr(os.getenv("JWT_SECRET", "change-this-dev-secret"))
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "30"))  # per window
    rate_limit_window_seconds: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    session_ttl_seconds: int = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
    # External APIs
    duckduckgo_api: str = os.getenv("DUCKDUCKGO_API", "https://duckduckgo.com/?q={query}&ia=news")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    google_api_key: SecretStr = SecretStr(os.getenv("GOOGLE_API_KEY", ""))  # for Gemini
    google_api_endpoint: str = os.getenv("GOOGLE_API_ENDPOINT", "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent")

settings = Settings()
