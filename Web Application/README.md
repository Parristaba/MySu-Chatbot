# MySu ChatBot

MySu ChatBot is an AI-powered chatbot designed to centralize and simplify access to Sabancı University's digital resources. The chatbot is built using **FastAPI**, ensuring a scalable and efficient backend.

---

## Installation
Before starting the application, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application
Start the FastAPI server using:

```bash
uvicorn main:app --reload
```

The API will be accessible at:

- **Swagger UI (for testing):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc API Docs:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Modules

### **1️⃣ Session Manager Module**
The **Session Manager Module** is responsible for handling user sessions. It ensures that user queries are linked to a session, allowing for context-aware interactions.

**🔹 Features:**
- Create, update, and delete user sessions.
- Store session data using **Redis** for efficient session management.
- Extend session expiration to maintain active conversations.

**🔹 API Endpoints:**

| Method  | Endpoint               | Description |
|---------|------------------------|-------------|
| `POST`  | `/session/`            | Create or update a user session |
| `GET`   | `/session/{session_id}` | Retrieve session details |
| `DELETE`| `/session/{session_id}` | Delete a user session |
