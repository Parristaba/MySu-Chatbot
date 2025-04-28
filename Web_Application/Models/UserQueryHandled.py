from pydantic import BaseModel
from typing import List, Optional
from Models.RetrievedData import RetrievedData


class UserQueryHandled(BaseModel):
    type: str # 'document', 'announcement', 'greeter', 'ambiguous'
    entities: List[str]
    entities_concat: Optional[str] = None 
    user_query: str  
    user_id: Optional[str] = None
    entities_encoded: Optional[List[float]] = None 
    # An optional single retrieved data object
    retrieved_data: Optional['RetrievedData'] = None  # TODO: Retrieved data object
    similarity_score: Optional[float] = None  # TODO: Similarity score
    data_status: Optional[str] = None  # TODO: Data status
