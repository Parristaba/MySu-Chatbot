# RagModule.py

from typing import List
from Web_Application.Models.UserQueryHandled import UserQueryHandled
from Web_Application.OrchestratorModule.Orchestrator import Orchestrator
from Web_Application.Helper_Modules.SimilaritySearch.similarity_search import search_similar_content


class RAGBlock:
    """
    RAGBlock class handles the retrieval-augmented generation (RAG) process.
    It processes user queries, performs similarity searches, and routes the results
    based on the intent (e.g., announcement or document). It also maps similarity scores
    to data statuses for downstream processing.
    """

    # TODO: Decide if legacy API calls should be retained or removed.
    # These endpoints are placeholders for potential API integrations.
    ANNOUNCEMENT_SEARCH_ENDPOINT = ""  # Replace with actual endpoint if needed
    DOCUMENT_SEARCH_ENDPOINT = ""  # Replace with actual endpoint if needed

    @staticmethod
    def HandleParsedQuery(Handled_UserQuery: UserQueryHandled):
        """
        Processes a parsed user query and determines the appropriate action:
        - Performs a similarity search using the pruned query string.
        - Routes the query based on its intent (announcement or document).
        - Updates the Handled_UserQuery object with retrieved data and forwards it to the orchestrator.
    
        Args:
            Handled_UserQuery (UserQueryHandled): The parsed user query object containing
            the pruned query string, intent, and other metadata.
    
        Returns:
            Result of the HandleAction function after processing the query.
        """
    
        # Extract the pruned query string and intent from the user query object
        query_pruned = Handled_UserQuery.pruned_query
        intent = Handled_UserQuery.intent  # Access the 'intent' attribute directly
    
        # Handle queries with intent "announcement"
        if intent == "announcement":
            # Perform similarity search for announcements
            results = search_similar_content(query=query_pruned, is_document=False, k=1)
        elif intent == "document":
            # Perform similarity search for documents
            results = search_similar_content(query=query_pruned, is_document=True, k=1)
        else:
            # Handle unknown or unsupported intents
            return {"response": "Unknown intent"}
    
        # Ensure results are not empty
        if results:
            similarity_score, data_id = results[0]  # Extract the top result
        else:
            similarity_score, data_id = None, None  # Handle case where no results are found
    
        # Update the user query object with retrieved data and similarity score
        Handled_UserQuery.retrieved_data_id = data_id
        Handled_UserQuery.similarity_score = similarity_score
        Handled_UserQuery.data_status = RAGBlock.map_similarity_to_data_status(similarity_score)
    
        # Forward the updated query object to the orchestrator for further processing
        return Orchestrator.HandleAction(Handled_UserQuery)

    @staticmethod
    def map_similarity_to_data_status(score: float) -> str:
        """
        Maps a similarity score to a data status label, which is used in prompt generation.

        Args:
            score (float): The similarity score obtained from the search.

        Returns:
            str: A label indicating the quality of the similarity score:
                 - "null" if the score is None.
                 - "confident" if the score is less than 2.0.
                 - "flawed" if the score is greater than or equal to 2.0.
        """
        if score is None:
            return "null"
        elif score >= 2.0:
            return "flawed"
        else:
            return "confident"
        