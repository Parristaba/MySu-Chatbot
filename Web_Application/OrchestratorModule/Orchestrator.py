from Models import LLMInfo, UserQuery, UserQueryHandled
from SessionManagerModule import SessionManager
from context_manager import ContextManager #TODO: not implemented yet

class Orchestrator:

    @staticmethod
    def handle_non_relevant_query(user_query: UserQuery):
        """
        Handles irrelevant queries.
        Returns an LLMInfo object with only instructions filled.
        """
        return LLMInfo(
            query=user_query.query_text,
            instructions="This question is not within the scope of the university chatbot. Please respond politely that you cannot help with this topic."
        )

    @staticmethod
    def HandleNonActionIntend(intent: str, user_query: UserQuery):
        """
        Handles generic user messages (greetings, thank yous, etc.).
        Returns LLMInfo with only past queries included.
        """
        session = SessionManager.get_session(user_query.session_id)
        past_queries = [q['query_text'] for q in session.query_list] if session else []

        return LLMInfo(
            query=user_query.query_text,
            past_queries=past_queries,
            instructions=""  # TODO: Implement a way to get the instructions for the query based on types
        )

    @staticmethod
    def HandleAction(handled_query: UserQueryHandled):  # Fixed parameter type
        """
        Handles action-based queries (e.g., document or announcement).
        Returns a context-aware LLMInfo object and sends it to the Context Manager.
        """
        session = SessionManager.get_session(handled_query.user_id)  # Fixed to use user_id from UserQueryHandled
        past_queries = [q['query_text'] for q in session.query_list] if session else []

        # Determine data status based on similarity score
        data_status = ""
        if handled_query.similarity_score < 0.3:
            data_status = "Null"
        elif handled_query.similarity_score < 0.6:
            data_status = "Flawed"
        else:
            data_status = "Correct"

        llm_info = LLMInfo(
            query=handled_query.text,  # Fixed to use the text attribute from UserQueryHandled
            retrieved_document=handled_query.retrieved_data,
            past_queries=past_queries,
            time_status="NULL",  # TODO: Implement a way to get the time status of the query
            data_status=data_status,
            instructions="",  # TODO: Add appropriate instructions
        )

        return ContextManager.fill_intend(llm_info)
    
