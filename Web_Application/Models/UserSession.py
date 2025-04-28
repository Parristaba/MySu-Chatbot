from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from Web_Application.Models.UserQuery import UserQuery
from Web_Application.Models.UserQueryHandled import UserQueryHandled

class UserSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    handled_query_list: List['UserQueryHandled'] = []  # Full memory of conversation
    last_active: datetime = Field(default_factory=datetime.utcnow)
    expiry_time: int = 900

    def add_query(self, query_text: str):
        """Adds a new query and updates last active timestamp."""
        self.query_list.append(UserQuery(session_id=self.session_id, query_text=query_text))
        self.last_active = datetime.utcnow()

    def is_expired(self) -> bool:
        """Checks if the session has expired."""
        return (datetime.utcnow() - self.last_active).total_seconds() > self.expiry_time
    
    def get_session(self, session_id: str) -> Optional['UserSession']:
        """Retrieves the session by session ID."""
        if self.session_id == session_id:
            return self
        return None