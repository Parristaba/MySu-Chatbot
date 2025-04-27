import request
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
        - If intent is 'document', calls HandleDocumentModule.
        - If intent is 'announcement', calls HandleAnnouncementModule.
        - Otherwise, calls Orchestrator.HandleNonActionIntend with the returned intent.
        """
        try:
            response = requests.post(INTENT_MODEL_ENDPOINT, json={"query_text": user_query.query_text})
            if response.status_code == 200:
                intent = response.json().get("intent", "ambiguous")
            else:
                intent = "ambiguous"
        except requests.RequestException:
            intent = "ambiguous"
            # TODO: Log error, might want to return the user a proper error message

        if intent == "document":
            return NLU.HandleDocumentModule(user_query, intent)
        elif intent == "announcement":
            return NLU.HandleAnnouncementModule(user_query, intent)
        else:
            return Orchestrator.HandleNonActionIntend(intent, user_query)


    @staticmethod
    def HandleDocumentModule(user_query: UserQuery, intent: str):
        """
        Calls the Document NER model and processes the extracted entities.
        - Constructs a UserQueryHandled object.
        - Sends it to RAG's HandleParsedQuery function.
        """
        try:
            response = requests.post(DOCUMENT_NER_ENDPOINT, json={"query_text": user_query.query_text})
            entities = response.json().get("entities", [])
        except requests.RequestException:
            entities = []
    
        handled_user_query = UserQueryHandled(
            text=user_query.query_text,
            entities=entities,
            user_id=user_query.session_id,  # Assuming session_id is unique to user
            intent=intent
        )
    
        return HandleParsedQuery(handled_user_query)
    
    
    @staticmethod
    def HandleAnnouncementModule(user_query: UserQuery, intent: str):
        """
        Calls the Announcement NER model and processes the extracted entities.
        - Constructs a UserQueryHandled object.
        - Sends it to RAG's HandleParsedQuery function.
        """
        try:
            response = requests.post(ANNOUNCEMENT_NER_ENDPOINT, json={"query_text": user_query.query_text})
            entities = response.json().get("entities", [])
        except requests.RequestException:
            entities = []
    
        handled_user_query = UserQueryHandled(
            text=user_query.query_text,
            entities=entities,
            user_id=user_query.session_id,
            intent=intent
        )
    
        return HandleParsedQuery(handled_user_query)
