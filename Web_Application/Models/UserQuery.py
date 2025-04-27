from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta

class UserQuery(BaseModel):
    session_id: str
    query_text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)