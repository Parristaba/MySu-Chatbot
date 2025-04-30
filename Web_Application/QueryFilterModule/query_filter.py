import requests
from Models import UserQuery
from OrchestratorModule import Orchestrator  
from NluModule import NLU_get_intend  

# This is the endpoint we will use to determine if the user query is relevant or not. 
"""
The endpoint should accept a POST request with a JSON body containing the user query text.
Relevant -> {"relevant": true}
Not Relevant -> {"relevant": false}

The model will probably be connected through a FastAPI endpoint. Other frameworks can be used as well.
"""
QUERY_RELEVANCE_ENDPOINT = ""

# New function to replace the API call
def checkRelevance(query_text: str) -> str:
    """
    Simulates the relevance-checking logic.
    Returns "School Related" if relevant, otherwise "Other".
    """
    # Replace this logic with the actual implementation
    if "school" in query_text.lower():
        return "School Related"
    return "Other"

class QueryFilter:

    @staticmethod
    def process_query(user_query: UserQuery):
        """
        Determines if the query is relevant or not and routes it accordingly.
        - Uses `checkRelevance` to determine relevance.
        - If relevant, calls `NLU_get_intend(user_query)`.
        - If not relevant, calls `handle_non_relevant_query(user_query)` inside Orchestrator.
        """

        # TODO: Implement regex filtering if needed. For now, the accuracy of the model seems to be enough.

        # Legacy API call (commented out)
        """
        try:
            response = requests.post(QUERY_RELEVANCE_ENDPOINT, json={"query_text": user_query.query_text})
            if response.status_code == 200:
                is_relevant = response.json().get("Relevannce") == "School Related"
            else:
                is_relevant = False  
        except requests.RequestException:
            is_relevant = False  
        """

        # New logic using the `checkRelevance` function
        # TODO: Implement the checkRelevance function to call the actual model
        is_relevant = checkRelevance(user_query.query_text) == "School Related"

        if is_relevant:
            return NLU_get_intend(user_query) 
        else:
            return Orchestrator.handle_non_relevant_query(user_query)