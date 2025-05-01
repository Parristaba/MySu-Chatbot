# OrchestratorModule.py

from Models import UserQuery, UserQueryHandled
from SessionManager import SessionManager
from Models.LLMInfo import LLMInfo
from LLM.Zephyr import BuildResponsesAction, BuildResponsesFollowUp, BuildResponsesNonAction
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
        session = SessionManager.get_session(user_query.session_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}
    
        if intent in ["greeting", "goodbye"]:
            payload = {
                "type": intent,
                "query": user_query.query_text
            }
            response = BuildResponsesNonAction(query=payload["query"], type=payload["type"])
    
            # --- Legacy API usage (if re-enabled) ---
            # endpoint = Orchestrator.LLM_GREETING_ENDPOINT
            # try:
            #     response = requests.post(endpoint, json=payload)
            #     return response.json() if response.status_code == 200 else {"response": "Fallback response"}
            # except Exception as e:
            #     print(f"LLM call error: {e}")
            #     return {"response": "Fallback response"}
    
        elif intent == "follow-up":
            past_handled_queries = session.get_past_interactions()
            if not past_handled_queries:
                return {"response": "No past interactions found for follow-up."}
    
            # Use the last handled query for follow-up
            last_handled_query = past_handled_queries[-1]
            last_llm_info = LLMInfo.from_handled_query(last_handled_query)
    
            response = BuildResponsesFollowUp(
                type=last_llm_info.type,
                query=last_llm_info.query,
                retrieved_data_id=last_llm_info.retrieved_data_id,
                data_status=last_llm_info.data_status
            )
    
            # --- Legacy API usage (if re-enabled) ---
            # endpoint = Orchestrator.LLM_FOLLOWUP_ENDPOINT
            # payload = {
            #     "type": "follow-up",
            #     "query": user_query.query_text,
            #     "retrieved_data_id": last_llm_info.retrieved_data_id,
            #     "data_status": last_llm_info.data_status
            # }
            # try:
            #     response = requests.post(endpoint, json=payload)
            #     return response.json() if response.status_code == 200 else {"response": "Fallback response"}
            # except Exception as e:
            #     print(f"LLM call error: {e}")
            #     return {"response": "Fallback response"}
    
        else:
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
        session = SessionManager.get_session(handled_query.user_id)
        if not session:
            return {"response": "Session expired or invalid. Please try again."}
    
        # Use the current handled query for action-based response
        current_llm_info = LLMInfo.from_handled_query(handled_query)
    
        response = BuildResponsesAction(
            type=current_llm_info.type,
            query=current_llm_info.query,
            retrieved_data_id=current_llm_info.retrieved_data_id,
            data_status=current_llm_info.data_status
        )
    
        # --- Legacy API usage (if re-enabled) ---
        # endpoint = Orchestrator.LLM_ACTION_ENDPOINT
        # payload = {
        #     "type": current_llm_info.type,
        #     "query": current_llm_info.query,
        #     "retrieved_data_id": current_llm_info.retrieved_data_id,
        #     "data_status": current_llm_info.data_status
        # }
        # try:
        #     response = requests.post(endpoint, json=payload)
        #     return response.json() if response.status_code == 200 else {"response": "Fallback response"}
        # except Exception as e:
        #     print(f"LLM call error: {e}")
        #     return {"response": "Fallback response"}
    
        # Update the session with the current query
        session.update_past_interactions(handled_query)
        SessionManager.save_session(session)
    
        return response