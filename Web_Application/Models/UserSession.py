from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from Web_Application.Models.UserQueryHandled import UserQueryHandled

class UserSession(BaseModel):
    """
    A Pydantic model representing a user's session in the chatbot system.
    """

    session_id: str
    user_id: Optional[str] = None
    handled_query_list: List[UserQueryHandled] = Field(default_factory=list)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    expiry_time: int = 900

    def is_expired(self) -> bool:
        return (datetime.utcnow() - self.last_active).total_seconds() > self.expiry_time

    def get_session(self, session_id: str) -> Optional['UserSession']:
        return self if self.session_id == session_id else None

    def get_past_interactions(self) -> List[UserQueryHandled]:
        return self.handled_query_list[-2:] if len(self.handled_query_list) >= 2 else self.handled_query_list[:]

    def update_past_interactions(self, handled_query: UserQueryHandled):
        if len(self.handled_query_list) >= 2:
            self.handled_query_list.pop(0)
        self.handled_query_list.append(handled_query)
