import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

# === Paths ===
model_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Contrastive_Aproach\Contrastive_Model"
embedding_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Contrastive_Aproach\intent_query_embeddings.pt"

# === Load model and tokenizer ===
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# === Load saved anchor embeddings ===
embedding_data = torch.load(embedding_path)
anchor_embeddings = embedding_data["embeddings"]  # (N, D)
anchor_labels = embedding_data["labels"]          # (N,)
anchor_texts = embedding_data["texts"]            # Optional: for inspection

# === Label index to string
label_to_intent = {
    0: "announcement",
    1: "document"
}

# === Mean pooling
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return (token_embeddings * mask_expanded).sum(1) / mask_expanded.sum(1)

# === Inference
def determineIntent(query_text):
    """
    Predict the intent by comparing the query to labeled anchor queries (contrastive search).
    Returns: (intent_label, similarity_score)
    """
    encoded = tokenizer(query_text, truncation=True, padding="max_length", max_length=128, return_tensors="pt").to(device)
    with torch.no_grad():
        output = model(**encoded)
        query_embedding = mean_pooling(output, encoded["attention_mask"])  # (1, D)

    # Compare to anchors (cosine similarity)
    similarities = F.cosine_similarity(query_embedding.cpu(), anchor_embeddings)  # (N,)
    best_idx = torch.argmax(similarities).item()
    predicted_label = anchor_labels[best_idx].item()
    similarity_score = similarities[best_idx].item()

    intent = label_to_intent.get(predicted_label, "unknown")
    return intent, similarity_score

# === Example usage
if __name__ == "__main__":
    user_query = input("Enter a query: ")
    intent, confidence = determineIntent(user_query)
    print(f"Predicted Intent: {intent} (confidence: {confidence:.2f})")
