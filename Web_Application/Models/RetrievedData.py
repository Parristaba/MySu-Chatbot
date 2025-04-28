# Models/RetrievedData.py

from pydantic import BaseModel

class RetrievedData(BaseModel):
    id: str
    title: str
    date: str
    source: str
    content: str
