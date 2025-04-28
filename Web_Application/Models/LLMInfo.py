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
    retrieved_document_head: Optional[str] = None
    retrieved_document_body: Optional[str] = None

    @staticmethod
    def from_handled_query(handled_query: UserQueryHandled):
        """
        Converts a UserQueryHandled into an LLMInfo object.
        Automatically uses retrieved_data if available.
        """
        retrieved = handled_query.retrieved_data  # Shorten the access

        return LLMInfo(
            query=handled_query.user_query,
            type=handled_query.type,
            data_status=handled_query.data_status,
            retrieved_document_head=retrieved.title if retrieved else None,
            retrieved_document_body=retrieved.content if retrieved else None
        )
