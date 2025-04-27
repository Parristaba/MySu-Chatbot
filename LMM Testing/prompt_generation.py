import json
from typing import List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel

# LLMInfo Class
class LLMInfo(BaseModel):
    type: str  # announcement, document, greeting, followup, etc.
    query: str
    retrieved_document: Optional[str] = None
    past_interactions: List[Tuple[str, Optional[str]]] = []  # (past_query, past_retrieved_doc)
    time_status: Optional[datetime] = None
    data_status: Optional[str] = None  # confident, mediocre, flawed, null

# Prompt Generation Logic
class PromptGenerator:
    def __init__(self, llm_info: LLMInfo):
        self.llm_info = llm_info

    def generate_prompt(self) -> str:
        # Step 1: System Instructions
        system_instructions = (
            "You are an official assistant for Sabancı University. Maintain a formal, precise, and polite tone.\n"
            "When answering:\n"
            "- Use the retrieved documents if available.\n"
            "- If no document is found, state it clearly and politely.\n"
            "- If multiple documents exist, prioritize the most recent and relevant.\n"
            "- If a document is marked as flawed or outdated, clearly warn the user.\n"
            "- Only use past interactions if they are directly relevant to the current user query.\n"
            "- If past information is irrelevant, ignore it.\n"
            "- Always cite information if possible.\n"
            "- Respond with a concise and direct answer to the user's query, without copying the full announcement unless explicitly requested.\n"
            "- Summarize or extract the relevant points rather than repeating formal memos in full.\n"
            "- Do not explain your reasoning or thought process. Provide the final answer immediately."
        )

        # Step 2: Context from past interactions
        context = self._build_context()

        # Step 3: Handling different types
        if self.llm_info.type == "greeting":
            return self._generate_greeting_prompt(system_instructions)

        if self.llm_info.type == "followup":
            return self._generate_followup_prompt(system_instructions, context)

        if self.llm_info.type in ["announcement", "document"]:
            return self._generate_retrieval_prompt(system_instructions, context)

        # Default fallback
        return f"{system_instructions}\nUser query: {self.llm_info.query}\nRespond appropriately."

    def _build_context(self) -> str:
        if not self.llm_info.past_interactions:
            return ""

        context_blocks = []
        # Use last 2 interactions
        for past_query, past_doc in self.llm_info.past_interactions[-2:]:
            past_info = f"User asked: {past_query}\nRetrieved document: {past_doc or 'No document retrieved.'}"
            context_blocks.append(past_info)

        return "\n\n".join(context_blocks)

    def _generate_greeting_prompt(self, system_instructions: str) -> str:
        return (f"{system_instructions}\n\n"
                f"User message: {self.llm_info.query}\n\n"
                f"Respond warmly and casually, maintaining a formal but friendly tone. Keep the response short and appreciative.")

    def _generate_followup_prompt(self, system_instructions: str, context: str) -> str:
        base = (f"{system_instructions}\n\n"
                f"[Past Interactions]\n{context}\n\n"
                f"[Current Interaction]\nUser query: {self.llm_info.query}\n\n"
                f"Answer based on the context, prioritizing relevance. Keep the response concise and to the point.")
        return base

    def _generate_retrieval_prompt(self, system_instructions: str, context: str) -> str:
        if self.llm_info.data_status == "confident":
            retrieval_info = (f"Here is the confidently retrieved information:\n{self.llm_info.retrieved_document}\n")
            instruction = "Answer the user's query accurately and concisely based on the provided document."
        elif self.llm_info.data_status == "mediocre":
            retrieval_info = (f"Here is the information found, but it might be partially incomplete:\n{self.llm_info.retrieved_document}\n")
            instruction = "Answer the user's query, informing them that the information may not be fully complete. Keep the response focused."
        elif self.llm_info.data_status == "flawed":
            retrieval_info = (f"Warning: The following information might be flawed:\n{self.llm_info.retrieved_document}\n")
            instruction = "Caution the user that the information might not be reliable. Maintain a formal tone and be brief."
        else:  # null case
            retrieval_info = "We could not retrieve any relevant document."
            instruction = "Inform the user politely that no relevant information was found, while remaining concise."

        base = (f"{system_instructions}\n\n"
                f"[Past Interactions]\n{context}\n\n"
                f"[Current Interaction]\n{retrieval_info}\n\n"
                f"User query: {self.llm_info.query}\n\n"
                f"{instruction}")
        return base