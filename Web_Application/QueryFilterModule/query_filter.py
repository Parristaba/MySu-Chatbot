from Web_Application.Models import UserQuery  # Importing the UserQuery model for query representation
from Web_Application.OrchestratorModule.Orchestrator import Orchestrator  # Importing the Orchestrator for handling non-relevant queries
from Web_Application.NluModule.NLU_Module import  NLU  # Importing the NLU module to determine the intent of relevant queries
from Web_Application.Helper_Modules.RelevanceFilter.check_relevance import checkRelevance  # Importing the relevance checking function


# Placeholder for the endpoint used to determine if a user query is relevant or not.
"""
The endpoint should accept a POST request with a JSON body containing the user query text.
Expected responses:
    - Relevant: {"relevant": true}
    - Not Relevant: {"relevant": false}

This endpoint is expected to be implemented using a FastAPI service or another framework.
"""
QUERY_RELEVANCE_ENDPOINT = ""


class QueryFilter:
    """
    A class responsible for filtering and routing user queries based on their relevance.
    """

    @staticmethod
    def process_query(user_query: UserQuery):
        """
        Processes a user query to determine its relevance and routes it accordingly.

        Workflow:
        - Uses `checkRelevance` to determine if the query is relevant.
        - If School Related, calls `NLU_get_intend(user_query)` to determine the intent.
        - If Other, calls `handle_non_relevant_query(user_query)` in the Orchestrator.
        - If greeting, calls `handle_greeting(user_query)` in the Orchestrator.

        Args:
            user_query (UserQuery): The user's query object.

        Returns:
            The result of either the NLU intent determination or the Orchestrator's handling of non-relevant queries.
        """

        # TODO: Implement regex filtering if additional pre-processing is required.
        # For now, the accuracy of the model is assumed to be sufficient.

    
        user_query_text = user_query.query_text
        predicted_label, confidence = checkRelevance(user_query_text)

        print(f"[DEBUG] Predicted Label: {predicted_label}, Confidence: {confidence}")
        

        if predicted_label == "Non-School":
            # If the query is not relevant, handle it using the Orchestrator
            print(f"[DEBUG] Entering HandleNonRelevantQuery with query: {user_query_text}")
            return Orchestrator.handle_non_relevant_query(user_query)
        elif predicted_label == "Greeting":
            intent = "greeting"
            print(f"[DEBUG] Entering HandleNonActionIntend with intent: {intent}")
            # If the query is a greeting, handle it using the Orchestrator
            return Orchestrator.HandleNonActionIntend(intent, user_query)
        else:
            # If the query is relevant, determine its intent using NLU
            print(f"[DEBUG] Entering NLU_get_intend with query: {user_query_text}")
            return NLU.NLU_get_intend(user_query)
        