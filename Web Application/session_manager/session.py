import time
import uuid
from typing import Optional
from .models import UserSession, UserQuery
from config import redis_client

SESSION_EXPIRY = 1800  # 30 minutes expiry

class SessionManager:

    @staticmethod
    def create_update_session(session_id: Optional[str], query_text: str) -> str:
        """
        Creates a new session or updates an existing session in Redis.
        """
        if session_id and redis_client.exists(session_id):
            # Extend session expiry
            redis_client.expire(session_id, SESSION_EXPIRY)
            session_data = redis_client.hgetall(session_id)
            session_data["query_list"].append(query_text)
        else:
            # Create a new session
            session_id = str(uuid.uuid4())
            session_data = {"query_list": [query_text], "expiry_time": int(time.time()) + SESSION_EXPIRY}

        # Store session data in Redis
        redis_client.hset(session_id, mapping=session_data)
        return session_id

    @staticmethod
    def get_session(session_id: str) -> Optional[UserSession]:
        """
        Retrieves session data from Redis.
        """
        if not redis_client.exists(session_id):
            return None
        session_data = redis_client.hgetall(session_id)
        return UserSession(**session_data)

    @staticmethod
    def delete_session(session_id: str):
        """
        Deletes a session from Redis.
        """
        redis_client.delete(session_id)
