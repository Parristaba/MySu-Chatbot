from pydantic import BaseModel
from typing import List, Optional


class UserQueryHandled(BaseModel):
    type: str # 'document', 'announcement', 'greeter', 'ambiguous'
    pruned_query: str  # The pruned version of the user query
    user_query: str  
    user_id: Optional[str] = None
    query_encoded: Optional[List[float]] = None
    # An optional single retrieved data object
    # TODO: Rather than using this, we can use the ID's of the retrieved data objects.
    # This way we can save memory and avoid having to serialize the whole object.
    # retrieved_data: Optional['RetrievedData'] = None #
    retrieved_data_id: Optional[str] = None
    similarity_score: Optional[float] = None
    data_status: Optional[str] = None
