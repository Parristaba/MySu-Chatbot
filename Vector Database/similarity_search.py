# search_engine.py

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# === CONFIGURATION ===
FAISS_INDEX_FILE = "C:/Users/kagan_ntaijui/Desktop/MySu Chatbot Repo/MySu-Chatbot/Vector Database/faiss_announcements.index"
METADATA_FILE = "MySu-Chatbot/Vector Database/metadata_announcements.json"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5  # Default number of results

# === STEP 1: Initialization (Run Once) ===
print("[Search Engine] Initializing model, FAISS index, and metadata...")

# Load FAISS index
index = faiss.read_index(FAISS_INDEX_FILE)

# Load metadata
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load Sentence-BERT model
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

print("[Search Engine] Initialization complete.")

# === STEP 2: Search Function ===
def search_announcements(user_query, top_k=TOP_K):
    """
    Search similar announcements given a user query.
    
    Args:
        user_query (str): Text input from the user.
        top_k (int): Number of top results to return.
    
    Returns:
        list: List of dictionaries with announcement info.
    """
    # Embed the user query
    query_vector = model.encode([user_query])
    query_vector = np.array(query_vector).astype("float32")

    # Search the FAISS index
    distances, indices = index.search(query_vector, top_k)

    # Collect results
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        announcement_info = metadata.get(str(idx), {})
        result = {
            "id": announcement_info.get("id", ""),
            "title": announcement_info.get("title", ""),
            "date": announcement_info.get("date", ""),
            "source": announcement_info.get("source", ""),
            "score": float(dist)
        }
        results.append(result)

    return results
