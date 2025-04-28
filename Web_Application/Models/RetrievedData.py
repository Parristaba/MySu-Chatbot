from pydantic import BaseModel
from typing import Optional

class RetrievedData(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    date: Optional[str] = None
    source: Optional[str] = None
    content: Optional[str] = None

