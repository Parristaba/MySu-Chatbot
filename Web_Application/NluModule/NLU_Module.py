import requests
from Models import UserQuery
from OrchestratorModule import Orchestrator  # Orchestrator module
from RagModule import HandleParsedQuery  # RAG Block
from Models.UserQueryHandled import UserQueryHandled


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
        Calls the intent model API and determines how to process the query.
        Routes based on intent:
        - document ➔ HandleDocumentModule
        - announcement ➔ HandleAnnouncementModule
        - greeting, goodbye, follow-up ➔ Orchestrator.HandleNonActionIntend
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

        if intent == "document":
            return NLU.HandleDocumentModule(user_query, intent)
        elif intent == "announcement":
            return NLU.HandleAnnouncementModule(user_query, intent)
        elif intent in ["greeting", "goodbye", "follow-up"]:
            return Orchestrator.HandleNonActionIntend(intent, user_query)
        else:
            # ❗ For now, we do not have a fallback for unknown intents.
            # Maybe we can add a intentt called "fallback" in the model and handle it here.
            # For now, we will just call the HandleNonActionIntend function with "unknown" intent.
            return Orchestrator.HandleNonActionIntend("unknown", user_query)


    @staticmethod
    def HandleDocumentModule(user_query: UserQuery, intent: str):
        """
        Processes document-type user queries by pruning the query instead of using NER.
        Constructs a UserQueryHandled object with pruned query for RAG retrieval.
        """

        # TODO: Define a endpoint for this, or import the function directly
        pruned = prune_query(user_query.query_text)

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
        pruned = prune_query(user_query.query_text)

        handled_user_query = UserQueryHandled(
            text=user_query.query_text,
            query_pruned=pruned,
            user_id=user_query.session_id,
            intent=intent
        )

        return HandleParsedQuery(handled_user_query)