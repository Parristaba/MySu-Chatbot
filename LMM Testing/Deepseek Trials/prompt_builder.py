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
            return self._generate_document_prompt()
        elif self.type == "announcement":
            return self._generate_announcement_prompt()
        elif self.type == "followup":
            return self._generate_followup_prompt()
        elif self.type in ["greeting", "goodbye"]:
            return self._generate_greeting_prompt()
        else:
            return f"### Instruction:\nYou are an official assistant for Sabancı University. Respond clearly and formally.\nAnswer the following query using only the retrieved data.\nDO NOT include internal reasoning, thoughts, or prompt repeats. Limit to 5 sentences.\n### Query:\n{self.query}\n\n### Response:"

    def _generate_greeting_prompt(self) -> str:
        return (f"### Instruction:\nYou are an official assistant for Sabancı University. Respond to greetings or thanks in one polite sentence.\n"
                f"### Message:\n{self.query}\n\n"
                f"### Response:")

    def _generate_followup_prompt(self) -> str:
        return (f"### Instruction:\nYou are an official assistant for Sabancı University. Respond concisely using only the previously retrieved document or announcement.\nDO NOT include internal thoughts or previous instructions.\nLimit your response to 4–5 formal sentences.\n"
                f"### Query:\n{self.query}\n\n"
                f"### Response:")

    def _generate_announcement_prompt(self) -> str:
        if self.data_status == "confident":
            wrapper = f"### Retrieved Announcement\n{self.retrieved_document}"
        elif self.data_status == "mediocre":
            wrapper = f"### Possibly Incomplete Announcement\n{self.retrieved_document}"
        elif self.data_status == "flawed":
            wrapper = f"### Flawed Announcement (May be inaccurate)\n{self.retrieved_document}"
        else:
            wrapper = "### No relevant announcement could be found."

        return (f"### Instruction:\nYou are an official assistant for Sabancı University. Use the announcement below to answer the query.\nDO NOT speculate or repeat the content. Limit response to 5 sentences.\nRemind users announcements may change. Begin directly after '### Response:'.\n\n{wrapper}\n\n### Query:\n{self.query}\n\n### Response:")

    def _generate_document_prompt(self) -> str:
        if not self.retrieved_data_id or not any(
            entry.get("doc_id") == self.retrieved_data_id for entry in self.metadata.values()
        ):
            return f"### Instruction:\nNo matching document was found for this request.\n### Query:\n{self.query}\n\n### Response:"

        chunks = [entry for entry in self.metadata.values() if entry.get("doc_id") == self.retrieved_data_id]
        chunks = sorted(chunks, key=lambda x: x["chunk_index"])

        if not chunks:
            return f"### Instruction:\nNo chunks available for the matched document.\n### Query:\n{self.query}\n\n### Response:"

        full_doc_text = "\n\n".join(chunk["chunk_text"] for chunk in chunks)
        title = chunks[0].get("title", "")
        hyperlink = chunks[0].get("hyperlink", "")

        doc_section = f"### Document Title: {title}\n### Document URL: {hyperlink}\n\n{full_doc_text}"

        return (f"### Instruction:\nYou are an official assistant for Sabancı University. Use ONLY the document below to answer the query.\nDO NOT include any planning, internal monologue, or speculation.\nDO NOT repeat the document. Limit to 5 clear sentences. Always cite the document URL if relevant.\nBegin your response immediately after '### Response:'.\n"
                f"{doc_section}\n\n### Query:\n{self.query}\n\n### Response:")