# vector_index_builder.py

import os
import re
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# === CONFIGURATION ===
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 300
STRIDE = 200


def load_model():
    print("[0/6] Loading Sentence-BERT model...")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_announcements(model, input_path, output_folder):
    print("\n📢 Embedding Announcements...")

    with open(input_path, "r", encoding="utf-8") as f:
        announcements = json.load(f)

    print(f"Loaded {len(announcements)} announcements.")
    texts = [item["content"] for item in announcements]

    print("[1/6] Encoding...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=16)
    embeddings = np.array(embeddings).astype("float32")

    print("[2/6] Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs(output_folder, exist_ok=True)
    faiss_path = os.path.join(output_folder, "faiss_announcements.index")
    faiss.write_index(index, faiss_path)

    print(f"[3/6] FAISS index saved to: {faiss_path}")

    metadata = {}
    for idx, item in enumerate(announcements):
        metadata[idx] = {
            "id": item.get("id", ""),
            "title": item.get("title", "")
        }

    metadata_path = os.path.join(output_folder, "metadata_announcements.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"[4/6] Metadata saved to: {metadata_path}")
    print("✅ Announcements embedding complete.\n")


def embed_documents(model, input_folder, output_folder):
    print("\n📄 Embedding Documents...")

    os.makedirs(output_folder, exist_ok=True)

    all_chunks = []
    chunk_metadata = {}
    chunk_id = 0

    def extract_metadata(header_lines):
        meta = {}
        for line in header_lines:
            if "ID:" in line:
                meta["id"] = line.split("ID:")[1].strip()
            elif "Title:" in line:
                meta["title"] = line.split("Title:")[1].strip()
            elif "Hyperlink:" in line:
                meta["hyperlink"] = line.split("Hyperlink:")[1].strip()
        return meta

    print("[1/6] Reading and chunking...")
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.endswith(".txt"):
            with open(os.path.join(input_folder, file_name), "r", encoding="utf-8") as f:
                lines = f.readlines()

            header_lines = [line for line in lines if line.startswith("#")]
            body_lines = [line.strip() for line in lines if not line.startswith("#") and not line.startswith("-")]
            full_text = " ".join(body_lines)
            words = full_text.split()

            doc_meta = extract_metadata(header_lines)
            doc_id = doc_meta.get("id", file_name)

            for start in range(0, len(words), STRIDE):
                end = start + CHUNK_SIZE
                chunk_words = words[start:end]
                if not chunk_words:
                    continue

                chunk_text = " ".join(chunk_words)
                all_chunks.append(chunk_text)
                chunk_metadata[chunk_id] = {
                    "doc_id": doc_id,
                    "title": doc_meta.get("title", ""),
                    "hyperlink": doc_meta.get("hyperlink", ""),
                    "chunk_index": start // STRIDE,
                    "chunk_text": chunk_text
                }
                chunk_id += 1

    print(f"Prepared {len(all_chunks)} chunks from {len(os.listdir(input_folder))} documents.")

    print("[2/6] Encoding chunks...")
    embeddings = model.encode(all_chunks, show_progress_bar=True, batch_size=16)
    embeddings = np.array(embeddings).astype("float32")

    print("[3/6] Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss_path = os.path.join(output_folder, "faiss_documents.index")
    faiss.write_index(index, faiss_path)
    print(f"[4/6] FAISS index saved to: {faiss_path}")

    metadata_path = os.path.join(output_folder, "metadata_documents.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunk_metadata, f, indent=2, ensure_ascii=False)

    print(f"[5/6] Metadata saved to: {metadata_path}")
    print("✅ Documents embedding complete.\n")


# === ENTRYPOINT EXAMPLE ===
if __name__ == "__main__":
    model = load_model()

    embed_announcements(
        model=model,
        input_path="C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Datasets/announcements.json",
        output_folder="C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Announcements"
    )


    embed_documents(
        model=model,
        input_folder="C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Datasets/Documents",
        output_folder="C:/Users/kagan_ntaijui/Desktop/MySu-Chatbot/Vector Database/Embeddings/Documents"
    )
