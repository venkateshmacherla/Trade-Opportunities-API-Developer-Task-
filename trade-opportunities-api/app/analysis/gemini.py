import httpx
from typing import List
from ..config import settings

class GeminiClient:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.endpoint = settings.google_api_endpoint.format(model=model)

    async def analyze(self, sector: str, context_items: List[dict]) -> str:
        """
        Calls Gemini's generateContent endpoint with news context to produce insights.
        Returns a plain text analysis that we will format into Markdown in a separate step.
        """
        prompt = (
            f"You are an expert market analyst for India. Analyze the '{sector}' sector using "
            f"the following recent context snippets. Identify trade opportunities, risks, "
            f"regulatory notes, key players, macro signals, and actionable strategies for short- and mid-term.\n\n"
            f"Context:\n"
        )
        for item in context_items:
            prompt += f"- [{item.get('source')}] {item.get('excerpt')}\n"
        prompt += "\nProduce concise, current insights. Avoid hallucinations; if data seems sparse, state assumptions clearly."

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": settings.google_api_key.get_secret_value()
        }

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(self.endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        # Extract text from Gemini response
        try:
            candidates = data.get("candidates", [])
            text = candidates[0]["content"]["parts"][0]["text"]
        except Exception:
            text = "Unable to parse Gemini response. Check API key, model, and payload."

        return text
