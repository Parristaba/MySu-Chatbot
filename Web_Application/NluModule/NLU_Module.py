import requests
from Web_Application.Models import UserQuery  # Represents the user's query in the chatbot system
from Web_Application.OrchestratorModule.Orchestrator import Orchestrator  # Handles non-actionable intents
from Web_Application.RagModule.RAG_module import RAGBlock  # Handles retrieval-augmented generation (RAG) queries
from Web_Application.Models.UserQueryHandled import UserQueryHandled  # Represents a processed user query
from Web_Application.Helper_Modules.IntentDetection.check_intent import determineIntent  # Function to determine the intent of a user query
from Web_Application.Helper_Modules.QueryPruning.query_pruning import prune_query  # Function to prune the user query


"""
Endpoints for intent and NER models.

Currently, separate endpoints are defined for each model. 
These can be combined into a single endpoint with a flag for better efficiency.
"""
INTENT_MODEL_ENDPOINT = ""  # Endpoint for determining the intent of a query
ANNOUNCEMENT_NER_ENDPOINT = ""  # Endpoint for extracting named entities from announcement queries
DOCUMENT_NER_ENDPOINT = ""  # Endpoint for extracting named entities from document queries

class NLU:
    """
    A class responsible for determining the intent of user queries and routing them to the appropriate modules.
    """

    @staticmethod
    def NLU_get_intend(user_query: UserQuery):
        """
        Determines the intent of the query and processes it accordingly.

        Routes based on intent:
        - "document" ➔ HandleDocumentModule
        - "announcement" ➔ HandleAnnouncementModule
        - "follow-up" ➔ Orchestrator.HandleNonActionIntend
        - Unknown intents ➔ Orchestrator.HandleNonActionIntend with "unknown" intent

        Args:
            user_query (UserQuery): The user's query object.

        Returns:
            The result of the appropriate handler based on the determined intent.
        """

        # Legacy API call for intent determination (commented out for reference)
        """
        try:
            response = requests.post(INTENT_MODEL_ENDPOINT, json={"query_text": user_query.query_text})
            if response.status_code == 200:
                intent = response.json().get("intent", None)
            else:
                intent = None
        except requests.RequestException:
            intent = None
            # TODO: Log error if necessary
        """
        
        intent_tuple = determineIntent(user_query.query_text)
        intent = intent_tuple[0]  # Extract the intent string
        print(f"[DEBUG] Determined Intent: {intent}")
        
        if intent == "document":
            print(f"[DEBUG] Entering HandleDocumentModule with intent: {intent}")
            return NLU.HandleDocumentModule(user_query, intent)
        elif intent == "announcement":
            print(f"[DEBUG] Entering HandleAnnouncementModule with intent: {intent}")
            return NLU.HandleAnnouncementModule(user_query, intent)
        elif intent in ["follow-up"]:
            print(f"[DEBUG] Entering HandleNonActionIntend with intent: {intent}")
            return Orchestrator.HandleNonActionIntend(intent, user_query)
        else:
            print(f"[DEBUG] Unknown intent: {intent}. Routing to Orchestrator.")
            return Orchestrator.HandleNonActionIntend("unknown", user_query)

    @staticmethod
    def HandleDocumentModule(user_query: UserQuery, intent: str):
        """
        Processes document-type user queries by pruning the query instead of using NER.

        Constructs a `UserQueryHandled` object with the pruned query for RAG retrieval.

        Args:
            user_query (UserQuery): The user's query object.
            intent (str): The determined intent of the query.

        Returns:
            The result of the RAG retrieval process.
        """

        pruned = prune_query(user_query.query_text)

        print(f"[DEBUG] Pruned Query: {pruned}")
        print(f"[DEBUG] User ID: {user_query.session_id}")
        print(f"[DEBUG] Original Query: {user_query.query_text}")
        print(f"[DEBUG] Intent: {intent}")


        handled_user_query = UserQueryHandled(
            user_query=user_query.query_text,
            pruned_query=pruned,
            user_id=user_query.session_id,
            intent=intent
        )

        return RAGBlock.HandleParsedQuery(handled_user_query)

    @staticmethod
    def HandleAnnouncementModule(user_query: UserQuery, intent: str):
        """
        Processes announcement-type user queries by pruning the query instead of using NER.

        Constructs a `UserQueryHandled` object with the pruned query for RAG retrieval.

        Args:
            user_query (UserQuery): The user's query object.
            intent (str): The determined intent of the query.

        Returns:
            The result of the RAG retrieval process.
        """
        
        pruned = prune_query(user_query.query_text)

        print(f"[DEBUG] Pruned Query: {pruned}")
        print(f"[DEBUG] User ID: {user_query.session_id}")
        print(f"[DEBUG] Original Query: {user_query.query_text}")
        print(f"[DEBUG] Intent: {intent}")

        handled_user_query = UserQueryHandled(
            user_query=user_query.query_text,
            pruned_query=pruned,
            user_id=user_query.session_id,
            intent=intent
        )

        return RAGBlock.HandleParsedQuery(handled_user_query)