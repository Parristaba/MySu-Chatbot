import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModel, AutoTokenizer
import json
from sklearn.model_selection import train_test_split
from tqdm import tqdm

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MAX_LEN = 128
BATCH_SIZE = 32
EPOCHS = 4
LR = 2e-5
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---- Dataset ---- #
class PairDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.pairs = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        item = self.pairs[idx]
        q1 = item["query1"]
        q2 = item["query2"]
        label = item["label"]

        tok_q1 = self.tokenizer(q1, truncation=True, padding='max_length', max_length=MAX_LEN, return_tensors="pt")
        tok_q2 = self.tokenizer(q2, truncation=True, padding='max_length', max_length=MAX_LEN, return_tensors="pt")

        return {
            "input_ids1": tok_q1["input_ids"].squeeze(),
            "attention_mask1": tok_q1["attention_mask"].squeeze(),
            "input_ids2": tok_q2["input_ids"].squeeze(),
            "attention_mask2": tok_q2["attention_mask"].squeeze(),
            "label": torch.tensor(label, dtype=torch.float)
        }

# ---- Siamese Encoder ---- #
class SiameseBERT(nn.Module):
    def __init__(self):
        super(SiameseBERT, self).__init__()
        self.encoder = AutoModel.from_pretrained(MODEL_NAME)

    def encode(self, input_ids, attention_mask):
        output = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        return output.last_hidden_state[:, 0, :]  # CLS token

    def forward(self, input_ids1, attention_mask1, input_ids2, attention_mask2):
        emb1 = self.encode(input_ids1, attention_mask1)
        emb2 = self.encode(input_ids2, attention_mask2)
        return emb1, emb2

# ---- Contrastive Loss ---- #
class ContrastiveLoss(nn.Module):
    def __init__(self, margin=0.5):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, emb1, emb2, labels):
        cos_sim = nn.functional.cosine_similarity(emb1, emb2)
        pos_loss = labels * (1 - cos_sim)
        neg_loss = (1 - labels) * torch.clamp(cos_sim - self.margin, min=0)
        return (pos_loss + neg_loss).mean()

# ---- Load Dataset ---- #
def load_dataset(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    return data

# ---- Training ---- #
def train(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for batch in tqdm(loader, desc="Training"):
        optimizer.zero_grad()

        input_ids1 = batch["input_ids1"].to(DEVICE)
        input_ids2 = batch["input_ids2"].to(DEVICE)
        attention_mask1 = batch["attention_mask1"].to(DEVICE)
        attention_mask2 = batch["attention_mask2"].to(DEVICE)
        labels = batch["label"].to(DEVICE)

        emb1, emb2 = model(input_ids1, attention_mask1, input_ids2, attention_mask2)
        loss = criterion(emb1, emb2, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

# ---- Save Model ---- #
def save_model(model, tokenizer, path=r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Contrastive_Model"):
    model.encoder.save_pretrained(path)
    tokenizer.save_pretrained(path)

# ---- Main ---- #
def main():
    data = load_dataset(r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Dataset\contrastive_pairs_dataset.jsonl")
    train_data, val_data = train_test_split(data, test_size=0.1, random_state=42)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train_dataset = PairDataset(train_data, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = SiameseBERT().to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    criterion = ContrastiveLoss()

    for epoch in range(EPOCHS):
        loss = train(model, train_loader, optimizer, criterion)
        print(f"Epoch {epoch+1} Loss: {loss:.4f}")

    save_model(model, tokenizer)
    print("✅ Model saved at: contrastive_model")

if __name__ == "__main__":
    main()
