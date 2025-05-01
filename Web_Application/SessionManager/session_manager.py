import time
import uuid
from fastapi import Request, Response  
from config import redis_client
from typing import Optional
from datetime import datetime
from Web_Application.QueryFilterModule import process_query
from Web_Application.Models.UserQuery import UserQuery
from Web_Application.Models.UserSession import UserSession 


SESSION_EXPIRY = 900  
COOKIE_NAME = "su_session_id"

class SessionManager:

    ''''
    This class is responsible for handling user sessions and messages.

    get_or_create_session: Retrieves or creates a session for a user based on cookies.
    on_message_activity: Handles user message activity.
    get_session: Retrieves session data from Redis.
    delete_session: Deletes a session from Redis.

    A cookie is set in the response to store the session ID.
    The session data is stored in Redis with the following fields:
    - query_list: List of UserQuery objects as dictionaries.
    - expiry_time: Expiration time in seconds.
    - last_active: Timestamp of the last activity.
    '''

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
            "query_list": str([]),  
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
        This is the main entry point for processing user queries.

        Handles user message activity:
        - Retrieves or creates a session based on cookies.
        - Creates a UserQuery object.
        - Sends the UserQuery object to the QueryFilterModule.
        
        IMPORTANT:
        - We do not save the query into the session here anymore.
        - Only fully processed HandledUserQuery objects will be saved later after LLM call.
        """
        session_id = SessionManager.get_or_create_session(request, response)

        # Step 1: Create the basic UserQuery object
        user_query = UserQuery(
            session_id=session_id,
            query_text=query_text,
            timestamp=datetime.utcnow()
        )

        # Step 2: Update only last_active in session
        session_data = redis_client.hgetall(session_id)
        session_data["last_active"] = int(time.time())
        redis_client.hset(session_id, mapping=session_data)

        # Step 3: Pass UserQuery forward for processing
        return process_query(user_query)

    

    # This is an old method that is not used anymore.
    # It is kept here for reference and future use if needed.
    """
    @staticmethod
    def get_session(session_id: str) -> Optional[UserSession]:
        """"""
        Retrieves session data from Redis.

        This will mainly be used by the Orchestrator to retrieve the session data during LLM feeding.
        """""""
        if not redis_client.exists(session_id):
            return None

        session_data = redis_client.hgetall(session_id)
        return UserSession(
            session_id=session_id,
            query_list=eval(session_data.get("query_list", "[]")),
            last_active=int(session_data["last_active"])
        )
    """

    # This method is not used, but kept for future use if needed.
    # Note that deletions are handled by the Redis expiration mechanism.
    @staticmethod
    def delete_session(session_id: str):
        """
        Deletes a session from Redis.

        For now, it has no use for the current implementation since redis_client.expire is used to manage session expiration.
        """
        redis_client.delete(session_id)
