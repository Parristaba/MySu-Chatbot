
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from functools import lru_cache

# === CONFIGURATION ===
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

ANNOUNCEMENTS_FOLDER = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Vector_Database\Embeddings\Announcements"
DOCUMENTS_FOLDER = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Vector_Database\Embeddings\Documents"


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


def search_similar_content(query: str, is_document: bool, k: int = 1):
    """
    Searches either the documents or announcements index based on the flag.
    Args:
        query (str): the user's search query
        is_document (bool): True if searching documents, False for announcements
        k (int): number of top results to return

    Returns:
        List of tuples containing:
            - similarity score (float)
            - document ID (str) or announcement ID (str)
    """
    model = load_model()

    if is_document:
        folder = DOCUMENTS_FOLDER
        faiss_name = "faiss_documents.index"
        metadata_name = "metadata_documents.json"
        id_key = "doc_id"  # Key for document IDs in metadata
    else:
        folder = ANNOUNCEMENTS_FOLDER
        faiss_name = "faiss_announcements.index"
        metadata_name = "metadata_announcements.json"
        id_key = "id"  # Key for announcement IDs in metadata

    index, metadata = load_faiss_and_metadata(folder, faiss_name, metadata_name)

    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    distances, indices = index.search(query_vec, k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if str(idx) in metadata:
            # Extract the ID based on the key (doc_id or id)
            item_id = metadata[str(idx)].get(id_key)
            if item_id:  # Ensure the ID exists in the metadata
                results.append((dist, item_id))

    print(f"[DEBUG] Found the following results for query '{query}':")
    print(f"[DEBUG] Distances: {distances[0]}")
    print(f"[DEBUG] Title from Metadata: {metadata.get(str(idx), {}).get('title', 'N/A')}")

    return results

