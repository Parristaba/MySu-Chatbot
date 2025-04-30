# OrchestratorModule.py

from Models import UserQuery, UserQueryHandled
from SessionManager import SessionManager
from Models.LLMInfo import LLMInfo
from LLMResponseBuilder import (  # Assuming these functions live in this module
    BuildResponsesAction,
    BuildResponsesFollowUp,
    BuildResponsesNonAction
)
# import requests  # Legacy API support, if endpoints are used again

class Orchestrator:
    """
    The Orchestrator class is responsible for managing user queries and routing them
    to the appropriate handlers. It supports both action-based queries (e.g., announcements/documents)
    and non-action queries (e.g., greetings, follow-ups). It also integrates with session management
    and response building mechanisms.

    Note: Legacy API endpoints are currently disabled but can be re-enabled if needed.
    """

    # Placeholder for potential API endpoints (currently unused)
    LLM_GREETING_ENDPOINT = ""  # Endpoint for greeting-related queries
    LLM_FOLLOWUP_ENDPOINT = ""  # Endpoint for follow-up queries
    LLM_ACTION_ENDPOINT = ""    # Endpoint for action-based queries

    @staticmethod
    def handle_non_relevant_query(user_query: UserQuery):
        """
        Handles queries that are not relevant to the chatbot's scope.
        These queries are processed locally without involving the LLM.

        Args:
            user_query (UserQuery): The user query object containing query details.

        Returns:
            dict: A response indicating the query is out of scope.
        """
        return {
            "response": "Sorry, I can only assist with Sabancı University-related topics. Please ask a school-related question!"
        }

    @staticmethod
    def HandleNonActionIntend(intent: str, user_query: UserQuery):
        """
        Handles non-action user queries such as greetings or follow-ups.
        Determines the intent and uses local response builders to generate responses.

        Args:
            intent (str): The intent of the user query (e.g., "greeting", "follow-up").
            user_query (UserQuery): The user query object containing query details.

        Returns:
            dict: The generated response based on the intent.
        """
        # Retrieve the session associated with the user's query
        session = SessionManager.get_session(user_query.session_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}

        # Handle greeting or goodbye intents
        if intent in ["greeting", "goodbye"]:
            payload = {
                "type": intent,
                "query": user_query.query_text
            }

            # Use local response builder to generate the response
            response = BuildResponsesNonAction(query=payload["query"], type=payload["type"])

            # --- Legacy API usage (if re-enabled) ---
            # endpoint = Orchestrator.LLM_GREETING_ENDPOINT
            # try:
            #     response = requests.post(endpoint, json=payload)
            #     return response.json() if response.status_code == 200 else fallback_response
            # except Exception as e:
            #     print(f"LLM call error: {e}")
            #     return fallback_response

        # Handle follow-up intents
        elif intent == "follow-up":
            # Retrieve past interactions from the session
            past_handled_queries = session.get_past_interactions()
            past_llm_infos = [LLMInfo.from_handled_query(past) for past in past_handled_queries]

            # Use local response builder to generate the follow-up response
            response = BuildResponsesFollowUp(
                query=user_query.query_text,
                past_interactions=[info.dict() for info in past_llm_infos],
            )

            # --- Legacy API usage (if re-enabled) ---
            # endpoint = Orchestrator.LLM_FOLLOWUP_ENDPOINT
            # payload = {
            #     "type": "follow-up",
            #     "query": user_query.query_text,
            #     "past_interactions": [info.dict() for info in past_llm_infos]
            # }
            # try:
            #     response = requests.post(endpoint, json=payload)
            #     return response.json() if response.status_code == 200 else fallback_response
            # except Exception as e:
            #     print(f"LLM call error: {e}")
            #     return fallback_response

        # Handle unknown intents (fallback case)
        else:
            # TODO: Define behavior for unknown intents if necessary.
            # Currently, this returns an empty response.
            response = ""

        return response

    @staticmethod
    def HandleAction(handled_query: UserQueryHandled):
        """
        Handles action-based queries such as announcements or documents.
        Uses the LLMInfo structure to build responses and integrates with session management.

        Args:
            handled_query (UserQueryHandled): The processed user query object containing
            details about the query and its intent.

        Returns:
            dict: The generated response for the action-based query.
        """
        # Retrieve the session associated with the user's query
        session = SessionManager.get_session(handled_query.user_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}

        # Retrieve past interactions from the session
        past_handled_queries = session.get_past_interactions()
        past_llm_infos = [LLMInfo.from_handled_query(past) for past in past_handled_queries]
        current_llm_info = LLMInfo.from_handled_query(handled_query)

        # Use local response builder to generate the action-based response
        response = BuildResponsesAction(
            current_interaction=current_llm_info.dict(),
            past_interactions=[info.dict() for info in past_llm_infos]
        )

        # --- Legacy API usage (if re-enabled) ---
        # endpoint = Orchestrator.LLM_ACTION_ENDPOINT
        # payload = {
        #     "current_interaction": current_llm_info.dict(),
        #     "past_interactions": [info.dict() for info in past_llm_infos]
        # }
        # try:
        #     response = requests.post(endpoint, json=payload)
        #     llm_response = response.json() if response.status_code == 200 else fallback_response
        # except Exception as e:
        #     print(f"LLM call error: {e}")
        #     llm_response = fallback_response

        # Update the session with the current query
        session.update_past_interactions(handled_query)

        # Save the updated session state
        SessionManager.save_session(session)

        return response