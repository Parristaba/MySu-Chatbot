from pydantic import BaseModel
from typing import List, Optional


class UserQueryHandled(BaseModel):
    type: str # 'document', 'announcement', 'greeter', 'ambiguous'
    entities: List[str]
    entities_concat: Optional[str] = None 
    user_query: str  
    user_id: Optional[str] = None
    entities_encoded: Optional[List[float]] = None  # TODO: Encoding (Pinecone)
    retrieved_data: Optional[str] = None  # TODO: Retrieved data
    similarity_score: Optional[float] = None  # TODO: Similarity score
