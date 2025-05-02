from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Web_Application.SessionManager.session_manager import SessionManager

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
    """
    Endpoint to support Bot Framework messages.
    Extracts `text` and `from.id` from standard Bot Framework Activity payload.
    Uses `from.id` as session ID to track user state.
    """
    activity = await request.json()

    # Extract user message text and user ID
    user_text = activity.get("text", "")
    session_id = activity.get("from", {}).get("id")

    if not user_text or not session_id:
        return {"type": "message", "text": "Missing user ID or message."}

    # Process message using chatbot logic with external session ID
    chatbot_response = SessionManager.on_message_activity(
        request=request,
        response=response,
        query_text=user_text,
        external_session_id=session_id
    )

    # Return response in Bot Framework format
    return {
        "type": "message",
        "text": chatbot_response
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Web_Application.main:app", host="127.0.0.1", port=8000, reload=True)


