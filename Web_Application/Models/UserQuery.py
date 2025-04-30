from pydantic import BaseModel, Field  
from typing import List, Optional 
from datetime import datetime, timedelta

class UserQuery(BaseModel):
    """
    A Pydantic model representing a user's query in the chatbot system.

    Attributes:
        session_id (str): A unique identifier for the user's session.
        query_text (str): The text of the user's query.
        timestamp (datetime): The time when the query was made. Defaults to the current UTC time.
    """
    session_id: str  # Unique identifier for the session
    query_text: str  # The text of the user's query
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Timestamp of the query, defaults to current UTC time