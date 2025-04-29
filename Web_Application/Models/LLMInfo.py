from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Models/LLMInfo.py

from pydantic import BaseModel
from typing import Optional
from Models.UserQueryHandled import UserQueryHandled

class LLMInfo(BaseModel):
    query: str
    type: str  # 'announcement', 'document', 'greeting', 'followup'
    data_status: Optional[str] = None
    retrieved_data_id: Optional[str] = None


    @staticmethod
    def from_handled_query(handled_query: UserQueryHandled):
        """
        Converts a UserQueryHandled into an LLMInfo object.
        Automatically uses retrieved_data if available.
        """

        return LLMInfo(
            query=handled_query.user_query,
            type=handled_query.type,
            data_status=handled_query.data_status,
            retrieved_data_id=handled_query.retrieved_data_id

        )
