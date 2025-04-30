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
                "You are an official assistant for Sabancı University. Respond clearly and formally.\n"
                "Rules:\n"
                "- Do not use or reference any prior knowledge.\n"
                "- Never include <think> or internal reasoning.\n"
                "- ONLY use the provided document for the answer.\n"
                "- Include and cite the document hyperlink.\n"
                "- Never repeat full paragraphs.\n"
                "- Limit your answer to 10 lines or less.\n"
                "- Do not speculate."
            )
        else:
            system_instructions = (
                "You are an official assistant for Sabancı University. Respond clearly and formally.\n"
                "Rules:\n"
                "- Never include <think> or internal reasoning.\n"
                "- ONLY use the retrieved announcement.\n"
                "- Mention that announcements may change.\n"
                "- Limit answer to 10 lines.\n"
                "- Do not speculate.\n"
                "- Cite information clearly but concisely."
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
                f"Respond politely in one line. Acknowledge greeting or thanks.")

    def _generate_followup_prompt(self, system_instructions: str) -> str:
        return (f"{system_instructions}\n\n"
                f"User query: {self.query}\n\n"
                f"Respond based on the previously retrieved document or announcement. Keep it formal, brief, and avoid speculation.")

    def _generate_announcement_prompt(self, system_instructions: str) -> str:
        if self.data_status == "confident":
            retrieval_info = f"### Announcement Start ###\n{self.retrieved_document}\n### Announcement End ###"
            instruction = "Respond using only the announcement above. Remind the user to verify from official sources."
        elif self.data_status == "mediocre":
            retrieval_info = f"### Possibly Incomplete Announcement ###\n{self.retrieved_document}\n### End ###"
            instruction = "Content may be partial. Use only what's given and suggest the user check the official page."
        elif self.data_status == "flawed":
            retrieval_info = f"### Flawed Content Warning ###\n{self.retrieved_document}\n### End ###"
            instruction = "This content may be unreliable. Warn the user and refer them to official channels."
        else:
            retrieval_info = "No relevant announcement found."
            instruction = "Politely inform the user no relevant announcement could be retrieved."

        return (f"{system_instructions}\n\n"
                f"{retrieval_info}\n\n"
                f"User query: {self.query}\n\n"
                f"{instruction}")

    def _generate_document_prompt(self, system_instructions: str) -> str:
        if not self.retrieved_data_id or self.retrieved_data_id not in self.metadata:
            return f"{system_instructions}\n\nDocument not found.\nUser query: {self.query}"

        chunks = [entry for entry in self.metadata.values() if entry.get("doc_id") == self.retrieved_data_id]
        chunks = sorted(chunks, key=lambda x: x["chunk_index"])

        if not chunks:
            return f"{system_instructions}\n\nNo document chunks available.\nUser query: {self.query}"

        full_doc_text = "\n\n".join(chunk["chunk_text"] for chunk in chunks)
        title = chunks[0].get("title", "")
        hyperlink = chunks[0].get("hyperlink", "")

        doc_context = f"### Begin Document: {title} ###\n{full_doc_text}\n### End Document ###"

        instruction = (
            f"Based ONLY on the document above, answer the user's query. Keep your reply under 10 lines.\n"
            f"Do not speculate or hallucinate. Always cite this hyperlink: {hyperlink}"
        )

        return (f"{system_instructions}\n\n"
                f"{doc_context}\n\n"
                f"User query: {self.query}\n\n"
                f"{instruction}")