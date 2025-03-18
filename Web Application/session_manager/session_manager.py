import time
import uuid
from fastapi import Request, Response
from .models import UserSession, UserQuery
from config import redis_client
from typing import Optional
from datetime import datetime
from query_filter import CheckQueryRelevance  # Might change the name based on the module name

SESSION_EXPIRY = 900  # 15 minutes expiry
COOKIE_NAME = "su_session_id"

class SessionManager:

    # So, in here, the api/message first calls the get_or_create_session method to handle user session.
    # Then, it calls the on_message_activity method to handle user message activity.
    # This utilizes cookies (anonymous session) to store user data and queries.
    @staticmethod
    def get_or_create_session(request: Request, response: Response) -> str:
        """
        Retrieves or creates a session for a user based on cookies.
        - If a valid session cookie exists, return that session.
        - Otherwise, create a new session and set a cookie in the response.
        """
        session_id = request.cookies.get(COOKIE_NAME)

        if session_id and redis_client.exists(session_id):
            # Extend session expiration
            redis_client.expire(session_id, SESSION_EXPIRY)
            return session_id

        # If no valid session found, create a new one
        session_id = str(uuid.uuid4())
        redis_client.hset(session_id, mapping={
            "query_list": str([]),  # Store as string for Redis compatibility
            "expiry_time": int(time.time()) + SESSION_EXPIRY,
            "last_active": int(time.time())
        })
        redis_client.expire(session_id, SESSION_EXPIRY)

        # Set cookie in response
        response.set_cookie(key=COOKIE_NAME, value=session_id, max_age=SESSION_EXPIRY, httponly=True, secure=True)

        return session_id

    @staticmethod
    def on_message_activity(request: Request, response: Response, query_text: str) -> str:
        """
        Handles user message activity.
        - Retrieves or creates a session based on cookies.
        - Updates session with latest query as a UserQuery object.
        - Passes the UserQuery object to CheckQueryRelevance.
        """
        session_id = SessionManager.get_or_create_session(request, response)

        # Create UserQuery object
        user_query = UserQuery(session_id=session_id, query_text=query_text, timestamp=datetime.utcnow())

        # Retrieve session data
        session_data = redis_client.hgetall(session_id)
        existing_queries = eval(session_data.get("query_list", "[]"))

        # Append the new UserQuery object
        existing_queries.append(user_query.dict())  # Store as dict for Redis compatibility

        # Update session in Redis
        session_data["query_list"] = str(existing_queries)  # Convert list of dicts to string
        session_data["last_active"] = int(time.time())  # Update timestamp
        redis_client.hset(session_id, mapping=session_data)

        # Send UserQuery object for further processing
        return CheckQueryRelevance.process_query(user_query, session_id)
    
    @staticmethod
    def get_session(session_id: str) -> Optional[UserSession]:
        """
        Retrieves session data from Redis.
        """
        if not redis_client.exists(session_id):
            return None

        session_data = redis_client.hgetall(session_id)
        return UserSession(
            session_id=session_id,
            query_list=eval(session_data.get("query_list", "[]")),
            last_active=int(session_data["last_active"])
        )

    @staticmethod
    def delete_session(session_id: str):
        """
        Deletes a session from Redis.
        """
        redis_client.delete(session_id)
