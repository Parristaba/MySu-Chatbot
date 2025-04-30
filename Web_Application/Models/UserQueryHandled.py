from pydantic import BaseModel
from typing import List, Optional

class UserQueryHandled(BaseModel):
    """
    A Pydantic model representing a processed or handled user query in the chatbot system.

    Attributes:
        type (str): The type of query, e.g., 'document', 'announcement', 'greeting', or 'follow-up'.
        pruned_query (str): A simplified or cleaned version of the user's original query.
        user_query (str): The original query text from the user.
        user_id (Optional[str]): An optional identifier for the user, used to retrieve session data.
        retrieved_data_id (Optional[str]): An optional identifier for the data retrieved in response to the query.
        similarity_score (Optional[float]): An optional score indicating the similarity of the query to retrieved data.
        data_status (Optional[str]): An optional status of the retrieved data, e.g., 'processed' or 'pending'.
    """
    type: str  # The type of query, e.g., 'document', 'announcement', 'greeting', or 'follow-up'
    pruned_query: str  # A simplified or cleaned version of the user's original query
    user_query: str  # The original query text from the user
    user_id: Optional[str] = None  # Optional user ID to retrieve session data
    retrieved_data_id: Optional[str] = None  # Optional ID for the data retrieved in response to the query
    similarity_score: Optional[float] = None  # Optional similarity score for the query and retrieved data
    data_status: Optional[str] = None  # Optional status of the retrieved data

    # Note: The `RetrievedData` object was removed to avoid circular references and reduce memory usage.
    # If needed, this can be referenced or reintroduced later.
    # retrieved_data: Optional['RetrievedData'] = None

    # Note: Encoding and similarity search are handled in the same module to avoid loading the model multiple times.
    # This approach optimizes memory usage and avoids serializing the entire object.
    # query_encoded: Optional[List[float]] = None