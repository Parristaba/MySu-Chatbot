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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Web_Application.main:app", host="127.0.0.1", port=8000, reload=True)


