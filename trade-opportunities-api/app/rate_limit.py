import time
from typing import Dict, Tuple
from fastapi import HTTPException, status
from .config import settings

# In-memory counter: {(user_id or session_id): [(timestamp1), (timestamp2), ...]}
RATE_BUCKETS: Dict[str, list] = {}

def check_rate_limit(key: str) -> Tuple[int, int]:
    """Returns remaining requests and window seconds."""
    now = time.time()
    window = settings.rate_limit_window_seconds
    max_req = settings.rate_limit_requests

    RATE_BUCKETS.setdefault(key, [])
    # Keep only timestamps within the window
    RATE_BUCKETS[key] = [ts for ts in RATE_BUCKETS[key] if now - ts < window]

    if len(RATE_BUCKETS[key]) >= max_req:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {int(window - (now - RATE_BUCKETS[key][0]))}s",
        )

    RATE_BUCKETS[key].append(now)
    remaining = max_req - len(RATE_BUCKETS[key])
    return remaining, window
