import time
import uuid
import json
from fastapi import Request, Response
from config import redis_client
from typing import Optional
from datetime import datetime
from Web_Application.QueryFilterModule import process_query
from Web_Application.Models.UserQuery import UserQuery
from Web_Application.Models.UserSession import UserSession
from Web_Application.Models.UserQueryHandled import UserQueryHandled


SESSION_EXPIRY = 900
COOKIE_NAME = "su_session_id"


class SessionManager:
    """
    Handles user session creation, retrieval, updating, and deletion using Redis.
    Stores the entire UserSession model as a JSON object in Redis.
    """

    @staticmethod
    def get_or_create_session(request: Request, response: Response) -> str:
        """
        Retrieves or creates a session based on cookies.
        Stores a full UserSession object in Redis as JSON.
        """
        session_id = request.cookies.get(COOKIE_NAME)

        if session_id and redis_client.exists(session_id):
            # Extend expiration
            redis_client.expire(session_id, SESSION_EXPIRY)
            return session_id

        # Create new session
        session_id = str(uuid.uuid4())
        session = UserSession(session_id=session_id)

        redis_client.set(session_id, json.dumps(session.dict(), default=str))
        redis_client.expire(session_id, SESSION_EXPIRY)

        # Set session ID in cookie
        response.set_cookie(
            key=COOKIE_NAME,
            value=session_id,
            max_age=SESSION_EXPIRY,
            httponly=True,
            secure=True
        )

        return session_id

    @staticmethod
    def on_message_activity(request: Request, response: Response, query_text: str) -> str:
        """
        Main entry for handling incoming messages.
        - Retrieves or creates a session
        - Updates last_active
        - Creates UserQuery
        - Forwards it for processing
        """
        session_id = SessionManager.get_or_create_session(request, response)

        # Fetch session from Redis
        session = SessionManager.get_session(session_id)
        if session is None:
            session = UserSession(session_id=session_id)

        # Update last_active
        session.last_active = datetime.utcnow()
        SessionManager.save_session(session)

        # Build user query and forward it
        user_query = UserQuery(
            session_id=session_id,
            query_text=query_text,
            timestamp=datetime.utcnow()
        )
        return process_query(user_query)

    @staticmethod
    def get_session(session_id: str) -> Optional[UserSession]:
        """
        Retrieves the full UserSession from Redis.
        """
        raw_data = redis_client.get(session_id)
        if not raw_data:
            return None

        try:
            data = json.loads(raw_data)
            # Convert handled_query_list items into actual objects
            data["handled_query_list"] = [
                UserQueryHandled(**item) for item in data.get("handled_query_list", [])
            ]
            data["last_active"] = datetime.fromisoformat(data["last_active"])
            return UserSession(**data)
        except Exception as e:
            print(f"Error parsing session from Redis: {e}")
            return None

    @staticmethod
    def save_session(session: UserSession):
        """
        Saves the entire session model into Redis as JSON.
        """
        try:
            # Serialize to JSON and save
            redis_client.set(session.session_id, json.dumps(session.dict(), default=str))
            redis_client.expire(session.session_id, session.expiry_time)
        except Exception as e:
            print(f"Error saving session to Redis: {e}")

    @staticmethod
    def delete_session(session_id: str):
        """
        Deletes a session from Redis.
        """
        redis_client.delete(session_id)
