from pydantic import BaseModel
from typing import List, Optional

class UserSession(BaseModel):
    session_id: str
    query_list: List[str] = []
    expiry_time: int  # Time-to-Live (TTL) in seconds

class UserQuery(BaseModel):
    session_id: str
    query_text: str
