import requests
from Models import UserQuery  # Importing the UserQuery model for query representation
from OrchestratorModule import Orchestrator  # Importing the Orchestrator for handling non-relevant queries
from NluModule import NLU_get_intend  # Importing the NLU module to determine the intent of relevant queries

# TODO: Implement and import the checkRelevance function from the ML model.

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
        - If relevant, calls `NLU_get_intend(user_query)` to determine the intent.
        - If not relevant, calls `handle_non_relevant_query(user_query)` in the Orchestrator.

        Args:
            user_query (UserQuery): The user's query object.

        Returns:
            The result of either the NLU intent determination or the Orchestrator's handling of non-relevant queries.
        """

        # TODO: Implement regex filtering if additional pre-processing is required.
        # For now, the accuracy of the model is assumed to be sufficient.

        # Legacy API call for relevance checking (commented out for reference)
        """
        try:
            response = requests.post(QUERY_RELEVANCE_ENDPOINT, json={"query_text": user_query.query_text})
            if response.status_code == 200:
                is_relevant = response.json().get("relevant") == True
            else:
                is_relevant = False  
        except requests.RequestException:
            is_relevant = False  
        """

        # New logic using the `checkRelevance` function
        # Replace `checkRelevance` with the actual model call when ready
        is_relevant = checkRelevance(user_query.query_text) == "School Related"

        if is_relevant:
            return NLU_get_intend(user_query)  # Process relevant queries to determine intent
        else:
            return Orchestrator.handle_non_relevant_query(user_query)  # Handle non-relevant queries