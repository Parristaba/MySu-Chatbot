from Models import LLMInfo, UserQuery, UserQueryHandled
from SessionManagerModule import SessionManager
from context_manager import ContextManager  # TODO: not implemented yet


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

        # Tailored instructions based on intent
        if intent in ["thanks", "goodbye"]:
            instructions = "Politely acknowledge the user's gratitude or bid them farewell."
        elif intent in ["hello", "hi"]:
            instructions = "Greet the user warmly and ask how you can assist them."
        else:
            instructions = (
                "This is a generic user message. "
                f"If it is a follow-up question, reference the last query: '{past_queries[-1]}' and respond accordingly. "
                "If not, respond politely."
            )

        return LLMInfo(
            query=user_query.query_text,
            past_queries=past_queries,
            instructions=instructions,
        )

    @staticmethod
    def HandleAction(handled_query: UserQueryHandled):
        """
        Handles action-based queries (e.g., document or announcement).
        Returns a context-aware LLMInfo object and sends it to the Context Manager.
        """
        session = SessionManager.get_session(handled_query.user_id)  # Retrieve session data
        past_queries = [q['query_text'] for q in session.query_list] if session else []

        # Determine data status based on similarity score
        data_status = ""
        instructions = ""

        if not handled_query.retrieved_data:  # No match found in RAG block
            data_status = "No Match"
            instructions = (
                "No relevant data was found for the user's query. "
                "Politely inform the user that no matching documents or announcements were found. "
                "Encourage them to rephrase their query or provide more details."
            )
        elif handled_query.similarity_score < 0.3:  # Very low similarity
            data_status = "Null"
            instructions = (
                "The retrieved data is not relevant to the user's query. "
                "Politely inform the user that no useful information was found. "
                "Suggest they try rephrasing their query or ask a different question."
            )
        elif handled_query.similarity_score < 0.6:  # Moderate similarity
            data_status = "Flawed"
            instructions = (
                "The retrieved data may only partially match the user's query. "
                "Inform the user that the results might not be fully accurate. "
                "Encourage them to review the information carefully or provide more specific details."
            )
        else:  # High similarity
            data_status = "Correct"
            instructions = (
                "The retrieved data is relevant to the user's query. "
                "Provide the information confidently and ask if further assistance is needed."
            )

        # Construct the LLMInfo object
        llm_info = LLMInfo(
            query=handled_query.text,  # Use the text attribute from UserQueryHandled
            retrieved_document=handled_query.retrieved_data,
            past_queries=past_queries,
            time_status="NULL",  # TODO: Implement a way to get the time status of the query
            data_status=data_status,
            instructions=instructions,
        )

        # Pass the LLMInfo object to the Context Manager
        return ContextManager.pass_data_to_LLM(llm_info)