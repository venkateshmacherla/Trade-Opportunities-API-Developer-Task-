from typing import List, Dict

def normalize_news_items(items: List[Dict]) -> List[Dict]:
    """
    Clean and shape news items into a consistent structure.
    """
    normalized = []
    for i, item in enumerate(items):
        raw = item.get("raw", "")
        # Trim, remove tags crudely, and keep short excerpts
        text = (
            raw.replace("<a", "")
               .replace("</a>", "")
               .replace("<b>", "")
               .replace("</b>", "")
               .replace("<br>", " ")
               .strip()
        )
        normalized.append({
            "id": i + 1,
            "source": item.get("source", "unknown"),
            "excerpt": text[:500]
        })
    return normalized
