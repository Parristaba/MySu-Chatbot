from fastapi import FastAPI, HTTPException
from session_manager.session import SessionManager
from session_manager.models import UserQuery

app = FastAPI()

@app.post("/session/")
def create_session(user_query: UserQuery):
    """
    Creates or updates a session with a new user query.
    """
    session_id = SessionManager.create_update_session(user_query.session_id, user_query.query_text)
    return {"session_id": session_id}

@app.get("/session/{session_id}")
def get_session(session_id: str):
    """
    Retrieves session details.
    """
    session_data = SessionManager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_data

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """
    Deletes an active session.
    """
    SessionManager.delete_session(session_id)
    return {"message": "Session deleted successfully"}
