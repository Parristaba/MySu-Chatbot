from pydantic import BaseModel
from typing import List, Optional

class ParsedQuery(BaseModel):
    text: str
    entities: List[str]  # Extracted entities from NER models
    user_id: Optional[str] = None
    intent: str  # Intent type (e.g., "announcement", "document", etc.)
