import json
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# Path to your model (update this to your trained contrastive model directory)
MODEL_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Contrastive_Model"
DATASET_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\embedding_queries.json"
OUTPUT_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\intent_query_embeddings.pt"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModel.from_pretrained(MODEL_PATH).to(DEVICE)
model.eval()

# Mean Pooling Function
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # (batch_size, seq_len, hidden_size)
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return (token_embeddings * input_mask_expanded).sum(1) / input_mask_expanded.sum(1)

# Load queries
queries = []
labels = []

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)  # Load the entire JSON array
    for item in data:
        queries.append(item["text"])
        labels.append(item["label"])

# Embed queries in batches
batch_size = 32
embeddings = []

for i in tqdm(range(0, len(queries), batch_size), desc="Embedding queries"):
    batch_texts = queries[i:i+batch_size]
    encoded = tokenizer(batch_texts, padding=True, truncation=True, max_length=128, return_tensors="pt").to(DEVICE)
    
    with torch.no_grad():
        model_output = model(**encoded)
    
    pooled = mean_pooling(model_output, encoded["attention_mask"])
    embeddings.append(pooled.cpu())

# Stack and save
embeddings_tensor = torch.cat(embeddings, dim=0)
labels_tensor = torch.tensor([0 if l == "announcement" else 1 for l in labels], dtype=torch.long)

torch.save({
    "embeddings": embeddings_tensor,
    "labels": labels_tensor,
    "texts": queries
}, OUTPUT_PATH)

print(f"✅ Saved {len(queries)} embeddings to: {OUTPUT_PATH}")
