from datetime import datetime
from typing import List, Dict

def build_markdown_report(sector: str, analysis_text: str, context_items: List[Dict]) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Structured markdown report
    md = f"# Trade Opportunities Report — {sector.capitalize()} sector (India)\n\n"
    md += f"**Generated:** {now}\n\n"
    md += "## Executive summary\n\n"
    md += f"{analysis_text.strip()}\n\n"
    md += "## Context snippets\n\n"
    for item in context_items[:15]:
        md += f"- **Source:** {item.get('source', 'unknown')}\n  - {item.get('excerpt', '')}\n"
    md += "\n---\n"
    md += "## Actionable strategies\n\n"
    md += "- **Short term:** Focus on liquid opportunities with clear catalysts, risk-managed entries, and tight exits.\n"
    md += "- **Mid term:** Accumulate high-conviction plays aligned with regulatory clarity and macro tailwinds.\n"
    md += "- **Risk management:** Define position sizing, stop-loss discipline, and scenario planning.\n\n"
    md += "## Disclaimers\n\n"
    md += "- **Note:** This report is informational and not investment advice.\n"
    md += "- **Data freshness:** Web context may be incomplete; verify with official sources.\n"

    return md
