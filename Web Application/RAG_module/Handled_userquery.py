from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Handled_UserQuery(BaseModel):
    type: str  # "announcement" or "document"
    entities_concat: str  # Concatenated entity string
    user_query: str  # Original query text
    date: datetime = datetime.utcnow()  # Timestamp of processing
    entities_encoded: Optional[List[float]] = None  # TODO: Encoding (Pinecone)
    retrieved_data: Optional[str] = None  # TODO: Retrieved data
    similarity_score: Optional[float] = None  # TODO: Similarity score
