import requests
from .models import UserQuery
from orchestrator import Orchestrator  # Assuming this is the correct module import
from nlu import NLU_get_intend  # Assuming this is the correct function import

# Basarim halledersin
QUERY_RELEVANCE_ENDPOINT = ""

class QueryFilter:

    @staticmethod
    def process_query(user_query: UserQuery):
        """
        Determines if the query is relevant or not and routes it accordingly.
        - Sends a request to the relevance-checking endpoint.
        - If relevant, calls `NLU_get_intend(user_query)`.
        - If not relevant, calls `handle_non_relevant_query(user_query)` inside Orchestrator.
        """

        # TODO: Implement regex filtering if necessary, sanmam ama olabilir


        # Model endpointinden duzgun bool donmesi lazim burayi bi checkleriz
        try:
            response = requests.post(QUERY_RELEVANCE_ENDPOINT, json={"query_text": user_query.query_text})
            if response.status_code == 200:
                is_relevant = response.json().get("relevant", False)
            else:
                is_relevant = False  
        except requests.RequestException:
            is_relevant = False  

       
        if is_relevant:
            return NLU_get_intend(user_query) 
        else:
            return Orchestrator.handle_non_relevant_query(user_query) 
