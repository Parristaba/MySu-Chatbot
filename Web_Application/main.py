from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Web_Application.SessionManager.session_manager import SessionManager
import uuid
import requests

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Allow Bot Framework or any front-end to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model to receive user message
class UserMessage(BaseModel):
    query: str

@app.post("/message")
async def message_endpoint(message: UserMessage, request: Request, response: Response):
    """
    Handles user messages sent to the chatbot.
    This is the main gateway endpoint for chatbot communication.
    """
    chatbot_response = SessionManager.on_message_activity(
        request=request,
        response=response,
        query_text=message.query
    )
    return {"response": chatbot_response}

@app.post("/botframework")
async def botframework_endpoint(request: Request, response: Response):
    activity = await request.json()
    user_text = activity.get("text", "")
    user_id = activity.get("from", {}).get("id")
    service_url = activity.get("serviceUrl")
    conversation_id = activity.get("conversation", {}).get("id")

    if not all([user_text, user_id, service_url, conversation_id]):
        return {"error": "Missing required fields"}

    # Call your core logic
    chatbot_response = SessionManager.on_message_activity(
        request=request,
        response=response,
        query_text=user_text,
        external_session_id=user_id
    )
    message_text = chatbot_response.get("response", "[Empty response]")

    # ✅ Send message to Bot Framework
    reply_payload = {
        "type": "message",
        "text": message_text,
        "from": {"id": "bot"},
        "recipient": {"id": user_id},
        "conversation": {"id": conversation_id},
        "id": str(uuid.uuid4())
    }

    reply_url = f"{service_url}/v3/conversations/{conversation_id}/activities"
    requests.post(reply_url, json=reply_payload)

    return {"status": "sent"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Web_Application.main:app", host="127.0.0.1", port=8000, reload=True)


