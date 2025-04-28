# OrchestratorModule.py

from Models import UserQuery, UserQueryHandled
from SessionManager import SessionManager
import requests
from Models.LLMInfo import LLMInfo

class Orchestrator:

    LLM_GREETING_ENDPOINT = ""  # To be filled later
    LLM_FOLLOWUP_ENDPOINT = ""  # To be filled later
    LLM_ACTION_ENDPOINT = ""  # To be filled later

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
        Decides based on intent and sends to the proper LLM endpoint.
        """
        session = SessionManager.get_session(user_query.session_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}

        if intent in ["greeting", "goodbye"]:
            # GREETING / GOODBYE: Simple payload
            payload = {
                "type": intent,
                "query": user_query.query_text
            }

            endpoint = Orchestrator.LLM_GREETING_ENDPOINT

        elif intent == "follow-up":
            # FOLLOW-UP: Need past handled queries too
            past_handled_queries = session.handled_query_list[-2:] if session.handled_query_list else []
            past_llm_infos = [LLMInfo.from_handled_query(past) for past in past_handled_queries]

            payload = {
                "type": intent,
                "query": user_query.query_text,
                "past_interactions": [info.dict() for info in past_llm_infos]
            }

            endpoint = Orchestrator.LLM_FOLLOWUP_ENDPOINT

        else:
            # Fallback in case of unknown intent (should not happen)
            payload = {
                "type": intent,
                "query": user_query.query_text
            }
            endpoint = Orchestrator.LLM_GREETING_ENDPOINT  # Fallback to basic endpoint

        # Send the payload
        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"response": "Sorry, an error occurred while processing your request."}
        except Exception as e:
            print(f"Error during LLM call: {e}")
            return {"response": "Sorry, an internal error occurred."}

    @staticmethod
    def HandleAction(handled_query: UserQueryHandled):
        """
        Handles action-based queries (announcement/document).
        Prepares a structured payload and sends to LLM action endpoint.
        """
        # Step 1: Fetch the user's session
        session = SessionManager.get_session(handled_query.user_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}

        # Step 2: Convert past handled queries to LLMInfo (use only last 2)
        past_handled_queries = session.handled_query_list[-2:] if session.handled_query_list else []
        past_llm_infos = [LLMInfo.from_handled_query(past) for past in past_handled_queries]

        # Step 3: Convert current handled query to LLMInfo
        current_llm_info = LLMInfo.from_handled_query(handled_query)

        # Step 4: Build the payload
        payload = {
            "current_interaction": current_llm_info.dict(),
            "past_interactions": [info.dict() for info in past_llm_infos]
        }

        # Step 5: Send the payload to LLM action endpoint
        try:
            response = requests.post(Orchestrator.LLM_ACTION_ENDPOINT, json=payload)
            if response.status_code == 200:
                llm_response = response.json()
            else:
                llm_response = {"response": "Sorry, an error occurred while processing your request."}
        except Exception as e:
            print(f"Error during LLM call: {e}")
            llm_response = {"response": "Sorry, an internal error occurred."}

        # Step 6: Update session memory (keep max 2 past handled queries)
        if len(session.handled_query_list) >= 2:
            session.handled_query_list.pop(0)  # Remove oldest query

        session.handled_query_list.append(handled_query)

        # Step 7: Save updated session back to Redis
        SessionManager.save_session(session)

        return llm_response
