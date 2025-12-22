from pydantic import BaseModel, Field, constr

ValidSector = constr(strip_whitespace=True, to_lower=True, min_length=3, max_length=50)

class AnalyzeSectorParams(BaseModel):
    sector: ValidSector = Field(..., description="Sector name like 'pharmaceuticals', 'technology', 'agriculture'")

class MarkdownReport(BaseModel):
    sector: str
    markdown: str
