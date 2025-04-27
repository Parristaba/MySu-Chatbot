# Import libraries
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# === CONFIGURATION ===
ANNOUNCEMENTS_FILE = "MySu-Chatbot/Vector Database/announcements.json"  # Your announcements file
FAISS_INDEX_FILE = "MySu-Chatbot/Vector Database/faiss_announcements.index"  # FAISS index output file
METADATA_FILE = "MySu-Chatbot/Vector Database/metadata_announcements.json"  # Metadata (mapping) output file

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# === STEP 1: Load Announcements JSON ===
print("[1/5] Loading announcements...")
with open(ANNOUNCEMENTS_FILE, "r", encoding="utf-8") as f:
    announcements = json.load(f)

print(f"Loaded {len(announcements)} announcements.")

# === STEP 2: Load Sentence-BERT Model ===
print("[2/5] Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# === STEP 3: Encode Announcements ===
print("[3/5] Encoding announcements...")
texts = [item["content"] for item in announcements]

# Batch encoding with progress bar
embeddings = model.encode(texts, show_progress_bar=True, batch_size=16)
embeddings = np.array(embeddings).astype("float32")  # FAISS needs float32

print(f"Embeddings shape: {embeddings.shape}")

# === STEP 4: Build FAISS Index ===
print("[4/5] Building FAISS index...")
dimension = embeddings.shape[1]  # Embedding dimension (e.g., 384)
index = faiss.IndexFlatL2(dimension)  # L2 distance (cosine similarity alternative)

index.add(embeddings)  # Add all vectors
print(f"Total vectors indexed: {index.ntotal}")

# Save the FAISS index
faiss.write_index(index, FAISS_INDEX_FILE)
print(f"FAISS index saved to {FAISS_INDEX_FILE}")

# === STEP 5: Save Metadata (ID-Title Mapping) ===
print("[5/5] Saving metadata...")
metadata = {}

for idx, item in enumerate(announcements):
    metadata[idx] = {
        "id": item.get("id", ""),
        "title": item.get("title", ""),
        "date": item.get("date", ""),
        "source": item.get("source", "")
    }

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"Metadata saved to {METADATA_FILE}")

# DONE
print("\n✅ Announcements embedding and FAISS index creation complete!")
