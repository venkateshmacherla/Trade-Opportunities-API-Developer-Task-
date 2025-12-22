import httpx
from typing import List, Dict
from urllib.parse import quote_plus

from ..config import settings

async def fetch_sector_news(sector: str) -> List[Dict]:
    """
    Fetch current market data/news headlines for the given sector.
    This uses a lightweight approach with DuckDuckGo's web interface.
    For production, replace with a proper news API.
    """
    query = quote_plus(f"{sector} sector India market news 2025")
    url = settings.duckduckgo_api.format(query=query)

    async with httpx.AsyncClient(timeout=15) as client:
        # We fetch the HTML, then do a naive parse looking for headlines.
        resp = await client.get(url)
        resp.raise_for_status()
        html = resp.text

    # Very naive parsing: collect "<a" lines with title-like text.
    # Replace with a real parser or official API for reliability.
    items: List[Dict] = []
    for line in html.splitlines():
        if "<a" in line and "news" in line.lower():
            # Simplistic extraction for demo purposes
            text = line.strip()
            items.append({"source": "duckduckgo", "raw": text})

    # Fallback if nothing found
    if not items:
        items.append({"source": "duckduckgo", "raw": f"No structured headlines found for {sector}. Consider using a news API."})

    return items
