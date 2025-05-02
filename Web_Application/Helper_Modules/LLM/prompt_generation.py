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
        """Generate appropriate prompt based on the type"""
        if self.type == "greeting" or self.type == "goodbye":
            return self._generate_casual_interaction_prompt()
        elif self.type == "followup":
            return self._generate_followup_prompt()
        elif self.type == "announcement":
            return self._generate_announcement_prompt()
        elif self.type == "document":
            return self._generate_document_prompt()
        else:
            return (f"You are a helpful assistant for Sabancı University.\n\n"
                   f"USER: {self.query}\n\n"
                   f"ASSISTANT: ")
    
    def _generate_casual_interaction_prompt(self) -> str:
        return (f"You are a helpful assistant for Sabancı University.\n\n"
                f"USER: {self.query}\n\n"
                f"Respond naturally but briefly to this casual interaction (greeting, thanks, or goodbye). "
                f"Keep your response to exactly 1 sentence. "
                f"Do not make up sample conversations or generate additional hypothetical exchanges.\n\n"
                f"ASSISTANT: ")
    
    def _generate_followup_prompt(self) -> str:
        return (f"You are a helpful assistant for Sabancı University. Respond to follow-up questions.\n\n"
                f"USER: {self.query}\n\n"
                f"ASSISTANT: ")
    
    def _generate_announcement_prompt(self) -> str:
        # Debug: show the received ID
        print(f"[DEBUG] Looking for announcement ID: {self.retrieved_data_id}")

        # Load full announcements database
        announcements_db_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Vector Database\Datasets\announcements.json"
        try:
            with open(announcements_db_path, "r", encoding="utf-8") as f:
                announcements_db = json.load(f)
            print(f"[DEBUG] Loaded {len(announcements_db)} announcements from JSON.")
        except Exception as e:
            print(f"[ERROR] Failed to load announcements.json: {e}")
            return (f"You are a helpful assistant for Sabancı University.\n\n"
                    f"USER: {self.query}\n\n"
                    f"ASSISTANT: I could not access the announcements database. Please try again later.")

        # Find matching announcement content
        match = next((a for a in announcements_db if a.get("id") == self.retrieved_data_id), None)

        if not match:
            print("[WARNING] Announcement not found in the JSON file.")
            retrieval_info = "No relevant announcement found."
            instruction = "Inform the user no matching announcement was found."
        else:
            title = match.get("title", "No title")
            content = match.get("content", "[No content]")

            print(f"[DEBUG] Matched announcement title: {title}")
            print(f"[DEBUG] Matched content (first 100 chars): {content[:100]}")

            if self.data_status == "confident":
                retrieval_info = f"ANNOUNCEMENT:\n{title}\n\n{content}"
                instruction = "Use only this announcement to answer. Write a 2-3 sentence summary."
            elif self.data_status == "mediocre":
                retrieval_info = f"POSSIBLY INCOMPLETE ANNOUNCEMENT:\n{title}\n\n{content}"
                instruction = "This announcement may be incomplete. Write a careful 2-3 sentence summary."
            elif self.data_status == "flawed":
                retrieval_info = f"UNRELIABLE ANNOUNCEMENT:\n{title}\n\n{content}"
                instruction = "This may be unreliable. Write a 2-3 sentence summary with appropriate caution."
            else:
                retrieval_info = "No relevant announcement found."
                instruction = "Inform the user no matching announcement was found."


        return (f"You are a helpful assistant for Sabancı University.\n\n"
                f"{retrieval_info}\n\n"
                f"USER: {self.query}\n\n"
                f"{instruction} End with a reminder that announcements may change.\n\n"
                f"ASSISTANT: ")



    
    def _generate_document_prompt(self) -> str:
        if not self.retrieved_data_id or not any(
            entry.get("doc_id") == self.retrieved_data_id for entry in self.metadata.values()
        ):
            return (f"You are a helpful assistant for Sabancı University.\n\n"
                    f"USER: {self.query}\n\n"
                    f"ASSISTANT: I could not find any document related to your query. Please try rewording your question or ask about something else.")
            
        chunks = [entry for entry in self.metadata.values() if entry.get("doc_id") == self.retrieved_data_id]
        chunks = sorted(chunks, key=lambda x: x["chunk_index"])
        
        if not chunks:
            return (f"You are a helpful assistant for Sabancı University.\n\n"
                    f"USER: {self.query}\n\n"
                    f"ASSISTANT: I could not find any relevant document chunks. Please try asking a different question.")
            
        # Extract document information
        full_doc_text = "\n\n".join(chunk["chunk_text"] for chunk in chunks)
        title = chunks[0].get("title", "Sabancı University Document")
        hyperlink = chunks[0].get("hyperlink", "")
        
        # Create a simplified prompt with clear instructions
        prompt = (
            f"You are a helpful assistant for Sabancı University.\n\n"
            f"DOCUMENT: {title}\n\n{full_doc_text}\n\n"
            f"USER: {self.query}\n\n"
            f"Write exactly 4-5 sentences summarizing the key information from the document that answers the question. "
            f"Do not include any URLs or hyperlinks in your response as these will be added automatically.\n\n"
            f"ASSISTANT: "
        )
        
        return prompt