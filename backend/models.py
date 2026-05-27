from pydantic import BaseModel

from typing import List, Optional


# ==================================================
# STATUTE CITATION
# ==================================================

class StatuteCitation(BaseModel):

    section_number: str

    act: str

    text: str

    similarity_score: float


# ==================================================
# LEGAL RESPONSE
# ==================================================

class LegalResponse(BaseModel):

    summary: str

    confidence_score: float

    cited_statutes: List[StatuteCitation]

    caveat: Optional[str] = None