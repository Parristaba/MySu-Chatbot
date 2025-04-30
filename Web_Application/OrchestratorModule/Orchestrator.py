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
    LLM_GREETING_ENDPOINT = ""  # To be filled later
    LLM_FOLLOWUP_ENDPOINT = ""  # To be filled later
    LLM_ACTION_ENDPOINT = ""    # To be filled later
    """

    @staticmethod
    def handle_non_relevant_query(user_query: UserQuery):
        """
        Handles irrelevant queries directly without calling LLM.
        """
        return {
            "response": "Sorry, I can only assist with Sabancı University-related topics. Please ask a school-related question!"
        }

    @staticmethod
    def HandleNonActionIntend(intent: str, user_query: UserQuery):
        """
        Handles non-action user messages like greetings or follow-ups.
        Decides based on intent and calls local builder instead of endpoint.
        """
        session = SessionManager.get_session(user_query.session_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}

        if intent in ["greeting", "goodbye"]:
            payload = {
                "type": intent,
                "query": user_query.query_text
            }

            # Local builder function replaces API call
            response = BuildResponsesNonAction(query=payload["query"], type=payload["type"])

            # --- Legacy API usage (if re-enabled) ---
            # endpoint = Orchestrator.LLM_GREETING_ENDPOINT
            # try:
            #     response = requests.post(endpoint, json=payload)
            #     return response.json() if response.status_code == 200 else fallback_response
            # except Exception as e:
            #     print(f"LLM call error: {e}")
            #     return fallback_response

        elif intent == "follow-up":
            past_handled_queries = session.get_past_interactions()
            past_llm_infos = [LLMInfo.from_handled_query(past) for past in past_handled_queries]

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

        else:
            # TODO: There will probably be no unknown intents aside from the fallback one.
            # So, we will leave this as an empty "response" for now.
            response = ""

        return response

    @staticmethod
    def HandleAction(handled_query: UserQueryHandled):
        """
        Handles action-based queries (announcement/document).
        Uses local response builder with LLMInfo structure.
        """
        session = SessionManager.get_session(handled_query.user_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}

        past_handled_queries = session.get_past_interactions()
        past_llm_infos = [LLMInfo.from_handled_query(past) for past in past_handled_queries]
        current_llm_info = LLMInfo.from_handled_query(handled_query)

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

        # Update session with current query
        session.update_past_interactions(handled_query)

        # Save session state
        SessionManager.save_session(session)

        return response
