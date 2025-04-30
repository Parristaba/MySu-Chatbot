from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from Web_Application.Models.UserQuery import UserQuery
from Web_Application.Models.UserQueryHandled import UserQueryHandled

class UserSession(BaseModel):
    """
    A Pydantic model representing a user's session in the chatbot system.

    Attributes:
        session_id (str): A unique identifier for the session.
        user_id (Optional[str]): An optional identifier for the user associated with the session.
        handled_query_list (List[UserQueryHandled]): A list of handled queries representing the conversation history.
        last_active (datetime): The timestamp of the last activity in the session. Defaults to the current UTC time.
        expiry_time (int): The session expiry time in seconds. Defaults to 900 seconds (15 minutes).
    """
    session_id: str  # Unique identifier for the session
    user_id: Optional[str] = None  # Optional user ID associated with the session
    handled_query_list: List['UserQueryHandled'] = []  # Full memory of the conversation
    last_active: datetime = Field(default_factory=datetime.utcnow)  # Timestamp of the last activity
    expiry_time: int = 900  # Session expiry time in seconds (default: 15 minutes)

    def add_query(self, query_text: str):
        """
        Adds a new query to the session and updates the last active timestamp.

        Args:
            query_text (str): The text of the user's query.
        """
        self.query_list.append(UserQuery(session_id=self.session_id, query_text=query_text))
        self.last_active = datetime.utcnow()  # Update the last active timestamp

    def is_expired(self) -> bool:
        """
        Checks if the session has expired based on the expiry time.

        Returns:
            bool: True if the session has expired, False otherwise.
        """
        return (datetime.utcnow() - self.last_active).total_seconds() > self.expiry_time

    def get_session(self, session_id: str) -> Optional['UserSession']:
        """
        Retrieves the session by its session ID.

        Args:
            session_id (str): The session ID to search for.

        Returns:
            Optional[UserSession]: The session if the ID matches, otherwise None.
        """
        if self.session_id == session_id:
            return self
        return None

    def get_past_interactions(self) -> List[UserQueryHandled]:
        """
        Retrieves the last two handled queries from the session.

        Returns:
            List[UserQueryHandled]: A list of the last two handled queries, or fewer if less than two exist.
        """
        return self.handled_query_list[-2:] if len(self.handled_query_list) >= 2 else self.handled_query_list[:]

    def update_past_interactions(self, handled_query: UserQueryHandled):
        """
        Updates the session with a new handled query. Maintains a maximum of two past interactions.

        Args:
            handled_query (UserQueryHandled): The handled query to add to the session.
        """
        if len(self.handled_query_list) >= 2:
            self.handled_query_list.pop(0)  # Remove the oldest query to maintain a maximum of two
        self.handled_query_list.append(handled_query)  # Add the new handled query