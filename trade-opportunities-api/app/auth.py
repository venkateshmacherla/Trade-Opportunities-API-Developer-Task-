import time
from typing import Optional, Dict
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from .config import settings

# In-memory sessions {session_id: {user_id, created_at, last_seen}}
SESSIONS: Dict[str, Dict] = {}

class AuthPayload(BaseModel):
    user_id: str

def create_jwt(user_id: str) -> str:
    now = int(time.time())
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + settings.session_ttl_seconds,
    }
    token = jwt.encode(payload, settings.jwt_secret.get_secret_value(), algorithm=settings.jwt_alg)
    return token

def verify_jwt(token: str) -> str:
    try:
        decoded = jwt.decode(token, settings.jwt_secret.get_secret_value(), algorithms=[settings.jwt_alg])
        return decoded.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def start_session(user_id: str) -> str:
    session_id = f"{user_id}:{int(time.time())}"
    SESSIONS[session_id] = {"user_id": user_id, "created_at": time.time(), "last_seen": time.time()}
    return session_id

def touch_session(session_id: str) -> None:
    sess = SESSIONS.get(session_id)
    if sess:
        sess["last_seen"] = time.time()

def get_session(session_id: str) -> Optional[Dict]:
    return SESSIONS.get(session_id)
