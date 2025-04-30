import requests
from Models import UserQuery
from OrchestratorModule import Orchestrator  # Orchestrator module
from RagModule import HandleParsedQuery  # RAG Block
from Models.UserQueryHandled import UserQueryHandled


# TODO: Define determineIntent function in a separate module or import it from an existing one.
# TODO: Define pruneQuery function in a separate module or import it from an existing one.



"""
These enpoints will be defined later.

As of now, they are seperate endpoints for each model. But they can be combined into a single endpoint as well with a flag.
"""
INTENT_MODEL_ENDPOINT = ""
ANNOUNCEMENT_NER_ENDPOINT = ""
DOCUMENT_NER_ENDPOINT = ""

class NLU:

    @staticmethod
    def NLU_get_intend(user_query: UserQuery):
        """
        Determines the intent of the query and processes it accordingly.
        Routes based on intent:
        - document ➔ HandleDocumentModule
        - announcement ➔ HandleAnnouncementModule
        - greeting, goodbye, follow-up ➔ Orchestrator.HandleNonActionIntend
        """

        # Legacy API call (commented out)
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

        # New logic using the `determine_intent` function
        intent = determineIntent(user_query.query_text)

        if intent == "document":
            return NLU.HandleDocumentModule(user_query, intent)
        elif intent == "announcement":
            return NLU.HandleAnnouncementModule(user_query, intent)
        elif intent in ["greeting", "goodbye", "follow-up"]:
            return Orchestrator.HandleNonActionIntend(intent, user_query)
        else:
            # ❗ For now, we do not have a fallback for unknown intents.
            # Maybe we can add an intent called "fallback" in the model and handle it here.
            # For now, we will just call the HandleNonActionIntend function with "unknown" intent.
            return Orchestrator.HandleNonActionIntend("unknown", user_query)
        
    @staticmethod
    def HandleDocumentModule(user_query: UserQuery, intent: str):
        """
        Processes document-type user queries by pruning the query instead of using NER.
        Constructs a UserQueryHandled object with pruned query for RAG retrieval.
        """

        # TODO: Define a endpoint for this, or import the function directly
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
        Constructs a UserQueryHandled object with pruned query for RAG retrieval.
        """

        # TODO: Define a endpoint for this, or import the function directly
        pruned = pruneQuery(user_query.query_text)

        handled_user_query = UserQueryHandled(
            text=user_query.query_text,
            query_pruned=pruned,
            user_id=user_query.session_id,
            intent=intent
        )

        return HandleParsedQuery(handled_user_query)