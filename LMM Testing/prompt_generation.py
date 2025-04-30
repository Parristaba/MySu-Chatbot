import json
import os
from typing import Optional

class PromptGenerator:
    def __init__(
        self,
        type: str,
        query: str,
        retrieved_document: Optional[str] = None,
        data_status: Optional[str] = None,
        retrieved_data_id: Optional[str] = None,
        document_metadata_path: Optional[str] = None
    ):
        self.type = type
        self.query = query
        self.retrieved_document = retrieved_document
        self.data_status = data_status
        self.retrieved_data_id = retrieved_data_id
        self.metadata_path = document_metadata_path
        self.metadata = self._load_metadata() if document_metadata_path else {}

    def _load_metadata(self):
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_prompt(self) -> str:
        if self.type == "document":
            system_instructions = (
                "You are an official assistant for Sabancı University. Maintain a formal, precise, and polite tone.\n"
                "When answering:\n"
                "- Use the retrieved documents if available.\n"
                "- If no document is found, state it clearly and politely.\n"
                "- If a document is marked as flawed or outdated, clearly warn the user.\n"
                "- Always cite information if possible.\n"
                "- Respond with a concise and direct answer to the user's query.\n"
                "- Summarize or extract the relevant points.\n"
                "- Do not explain your reasoning or thought process. Provide the final answer immediately.\n"
                "- Always include the document hyperlink in your response."
            )
        else:
            system_instructions = (
                "You are an official assistant for Sabancı University. Maintain a formal, precise, and polite tone.\n"
                "When answering:\n"
                "- Use the retrieved documents if available.\n"
                "- If no document is found, state it clearly and politely.\n"
                "- If a document is marked as flawed or outdated, clearly warn the user.\n"
                "- Always cite information if possible.\n"
                "- Respond with a concise and direct answer to the user's query, without copying the full announcement unless explicitly requested.\n"
                "- Summarize or extract the relevant points rather than repeating formal memos in full.\n"
                "- Do not explain your reasoning or thought process. Provide the final answer immediately.\n"
                "- Remind the user that announcements may change and they should double-check them if needed."
            )

        if self.type == "greeting" or self.type == "goodbye":
            return self._generate_greeting_prompt(system_instructions)
        elif self.type == "followup":
            return self._generate_followup_prompt(system_instructions)
        elif self.type == "announcement":
            return self._generate_announcement_prompt(system_instructions)
        elif self.type == "document":
            return self._generate_document_prompt(system_instructions)
        else:
            return f"{system_instructions}\nUser query: {self.query}\nRespond appropriately."

    def _generate_greeting_prompt(self, system_instructions: str) -> str:
        return (f"{system_instructions}\n\n"
                f"User message: {self.query}\n\n"
                f"Respond politely and briefly in one sentence, acknowledging the greeting or gratitude.")

    def _generate_followup_prompt(self, system_instructions: str) -> str:
        # === TODO: Add document/announcement resolution logic using retrieved_data_id ===
        return (f"{system_instructions}\n\n"
                f"User query: {self.query}\n\n"
                f"Answer based on the previous document or announcement retrieved. Keep the answer short, relevant, and formal.")

    def _generate_announcement_prompt(self, system_instructions: str) -> str:
        if self.data_status == "confident":
            retrieval_info = (f"Here is the confidently retrieved information:\n{self.retrieved_document}\n")
            instruction = "Answer the user's query accurately and concisely based on the provided document. Reminder: Always advise the user to double-check announcements if needed."
        elif self.data_status == "mediocre":
            retrieval_info = (f"Here is the information found, but it might be partially incomplete:\n{self.retrieved_document}\n")
            instruction = "Answer the user's query, informing them that the information may not be fully complete. Reminder: Announcements may change, and users should double-check."
        elif self.data_status == "flawed":
            retrieval_info = (f"Warning: The following information might be flawed:\n{self.retrieved_document}\n")
            instruction = "Caution the user that the information might not be reliable. Suggest checking the announcement manually."
        else:
            retrieval_info = "We could not retrieve any relevant document."
            instruction = "Inform the user politely that no relevant information was found, while remaining concise."

        return (f"{system_instructions}\n\n"
                f"[Current Interaction]\n{retrieval_info}\n\n"
                f"User query: {self.query}\n\n"
                f"{instruction}")

    def _generate_document_prompt(self, system_instructions: str) -> str:
        if not self.retrieved_data_id or self.retrieved_data_id not in self.metadata:
            return f"{system_instructions}\n\nWe could not retrieve any relevant document.\nUser query: {self.query}"

        chunks = [entry for entry in self.metadata.values()
                  if entry.get("doc_id") == self.retrieved_data_id]
        chunks = sorted(chunks, key=lambda x: x["chunk_index"])

        if not chunks:
            return f"{system_instructions}\n\nNo valid document chunks found.\nUser query: {self.query}"

        full_doc_text = "\n\n".join([chunk["chunk_text"] for chunk in chunks])
        title = chunks[0].get("title", "")
        hyperlink = chunks[0].get("hyperlink", "")

        doc_header = f"Document Title: {title}\nHyperlink: {hyperlink}\n"
        retrieval_info = f"{doc_header}\nFull Document:\n{full_doc_text}"

        instruction = ("Answer the user's query based on the full document below."
                       " Provide a concise, formal response. The user should also be directed to the document hyperlink for more details:"
                       f" {hyperlink}")

        return (f"{system_instructions}\n\n"
                f"[Current Interaction]\n{retrieval_info}\n\n"
                f"User query: {self.query}\n\n"
                f"{instruction}")
