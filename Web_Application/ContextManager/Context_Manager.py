import requests

class ContextManager:

    LLM_ENDPOINT = ""  # Leave the endpoint blank for now

    @staticmethod
    def pass_data_to_LLM(llm_info):
        """
        Sends the LLMInfo object to the LLM endpoint and returns the response.
        Ends the current loop and prepares for the next user interaction.
        """
        try:
            # Prepare the payload for the LLM
            payload = {
                "query": llm_info.query,
                "retrieved_document": llm_info.retrieved_document,
                "past_queries": llm_info.past_queries,
                "time_status": llm_info.time_status,
                "data_status": llm_info.data_status,
                "instructions": llm_info.instructions,
            }

            # Send the payload to the LLM endpoint
            response = requests.post(ContextManager.LLM_ENDPOINT, json=payload)

            # Check if the response is successful
            if response.status_code == 200:
                return response.json()  # Return the LLM's output
            else:
                # Handle errors from the LLM endpoint
                return {
                    "error": f"Failed to communicate with LLM. Status code: {response.status_code}",
                    "details": response.text,
                }

        except Exception as e:
            # Handle exceptions during the request
            return {
                "error": "An error occurred while communicating with the LLM.",
                "details": str(e),
            }