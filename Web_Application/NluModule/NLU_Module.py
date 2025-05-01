import requests
from Models import UserQuery  # Represents the user's query in the chatbot system
from OrchestratorModule import Orchestrator  # Handles non-actionable intents
from RagModule import HandleParsedQuery  # Handles retrieval-augmented generation (RAG) queries
from Models.UserQueryHandled import UserQueryHandled  # Represents a processed user query
from NluModule import determineIntent  # Function to determine the intent of a user query

# TODO: Define the `determineIntent` function in a separate module or import it from an existing one.
# TODO: Define the `pruneQuery` function in a separate module or import it from an existing one.

from NLU import pruneQuery  # Function to prune the user query for RAG retrieval

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

        # New logic using the `determineIntent` function
        intent = determineIntent(user_query.query_text)

        if intent == "document":
            return NLU.HandleDocumentModule(user_query, intent)
        elif intent == "announcement":
            return NLU.HandleAnnouncementModule(user_query, intent)
        elif intent in ["follow-up"]:
            return Orchestrator.HandleNonActionIntend(intent, user_query)
        else:
            # Handle unknown intents by routing them to the Orchestrator with "unknown" intent
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

        # TODO: Define an endpoint for this or import the function directly
        pruned = pruneQuery(user_query.query_text)

        handled_user_query = UserQueryHandled(
            text=user_query.query_text,
            query_pruned=pruned,
            user_id=user_query.session_id,
            intent=intent
        )

        return HandleParsedQuery(handled_user_query)

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

        # TODO: Define an endpoint for this or import the function directly
        pruned = pruneQuery(user_query.query_text)

        handled_user_query = UserQueryHandled(
            text=user_query.query_text,
            query_pruned=pruned,
            user_id=user_query.session_id,
            intent=intent
        )

        return HandleParsedQuery(handled_user_query)