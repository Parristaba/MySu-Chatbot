from Models import LLMInfo, UserQuery, UserQueryHandled  # Fixed import for UserQueryHandled
from SessionManager import SessionManager
from ContextManager import pass_data_to_LLM  

class Orchestrator:

    """
    Some of the prompts for the LLM are test prompts. We might need advanced prompt engineering in the future.
    """
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
            instructions = (
            "If this is a follow-up question, reference the last query: "
            f"'{past_queries[-1]}' and respond accordingly. "
            "If not, respond politely."
            ) # So, this might require some advanced prompt engineering in the future. An additional intent recognition such as 
            # 'greeting' or 'thank_you' might be needed to handle these cases better to differentiate between generic messages and greetings.
        )

    @staticmethod
    def HandleAction(handled_query: UserQueryHandled): 
        """
        Handles action-based queries (e.g., document or announcement).
        Returns a context-aware LLMInfo object and sends it to the Context Manager.
        """
        session = SessionManager.get_session(handled_query.user_id)  # Retrieve session data
        # Get the last two queries from the session
        past_queries = [q['query_text'] for q in session.query_list[-2]] if session else []
    
        # Determine data status based on similarity score
        data_status = ""
        instructions = ""
    
        if not handled_query.retrieved_data: 
            """
            This is the case where RAG block returns empty for the query. We might need to alter this part based on how we build the
            similarity search module and etc.

            Furthermore, we might merge this with the Null case, based on how well the LLM returns responses.
            """
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
    
        return pass_data_to_LLM(llm_info)
    
