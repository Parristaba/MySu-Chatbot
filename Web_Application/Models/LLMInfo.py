from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LLMInfo(BaseModel):
    query: str
    retrieved_document: Optional[str] = None
    past_queries: List[str] = []
    time_status: Optional[datetime] = None
    data_status: Optional[str] = None
    instructions: str
