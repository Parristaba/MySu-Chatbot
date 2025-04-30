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
    
    def get_past_interactions(self) -> List[UserQueryHandled]:
        """Returns the last two handled queries."""
        return self.handled_query_list[-2:] if len(self.handled_query_list) >= 2 else self.handled_query_list[:]
    
    def update_past_interactions(self, handled_query: UserQueryHandled):
        """Updates the session with the current handled query."""
        if len(self.handled_query_list) >= 2:
            self.handled_query_list.pop(0)
        self.handled_query_list.append(handled_query)