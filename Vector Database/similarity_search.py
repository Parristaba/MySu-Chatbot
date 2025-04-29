
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from functools import lru_cache

# === CONFIGURATION ===
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

ANNOUNCEMENTS_FOLDER = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Announcements"
DOCUMENTS_FOLDER = "C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Documents"


@lru_cache(maxsize=1)
def load_model():
    print("[1/5] Loading Sentence-BERT model...")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def load_faiss_and_metadata(folder, faiss_name, metadata_name):
    index_path = os.path.join(folder, faiss_name)
    metadata_path = os.path.join(folder, metadata_name)

    index = faiss.read_index(index_path)
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata


# TODO: This should return similarity score and document_id, rather than the whole object.
def search_similar_content(query: str, is_document: bool, k: int = 1):
    """
    Searches either the documents or announcements index based on the flag.
    Args:
        query (str): the user's search query
        is_document (bool): True if searching documents, False for announcements
        k (int): number of top results to return

    Returns:
        List of top-k matching metadata entries
    """
    model = load_model()

    if is_document:
        folder = DOCUMENTS_FOLDER
        faiss_name = "faiss_documents.index"
        metadata_name = "metadata_documents.json"
    else:
        folder = ANNOUNCEMENTS_FOLDER
        faiss_name = "faiss_announcements.index"
        metadata_name = "metadata_announcements.json"

    index, metadata = load_faiss_and_metadata(folder, faiss_name, metadata_name)

    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        if str(idx) in metadata:
            results.append(metadata[str(idx)])

    return results

