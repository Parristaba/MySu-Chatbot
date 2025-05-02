from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from Web_Application.Models.UserQueryHandled import UserQueryHandled



class LLMInfo(BaseModel):
    """
    A model representing information about a query handled by the system.
    
    Attributes:
        query (str): The original user query.
        type (str): The type of query, e.g., 'announcement', 'document', 'greeting', or 'followup'.
        data_status (Optional[str]): The status of the data retrieved for the query, if any.
        retrieved_data_id (Optional[str]): The ID of the retrieved data, if applicable.
    """
    query: str
    type: str  # 'announcement', 'document', 'greeting', 'followup'
    data_status: Optional[str] = None
    retrieved_data_id: Optional[str] = None

    @staticmethod
    def from_handled_query(handled_query: UserQueryHandled):
        """
        Converts a UserQueryHandled object into an LLMInfo object.
        
        Args:
            handled_query (UserQueryHandled): The handled query object containing details about the query.
        
        Returns:
            LLMInfo: An instance of LLMInfo populated with data from the handled query.
        """
        return LLMInfo(
            query=handled_query.user_query,
            type=handled_query.intent,
            data_status=handled_query.data_status,
            retrieved_data_id=handled_query.retrieved_data_id
        )