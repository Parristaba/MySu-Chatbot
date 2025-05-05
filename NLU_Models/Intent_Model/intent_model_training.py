import os
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizer, DistilBertModel, AdamW, DistilBertConfig
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Custom Dataset
class IntentDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        query = self.data[idx]["text"]
        label_str = self.data[idx]["label"]
        label_map = {"announcement": 0, "document": 1}
        label = label_map[label_str]

        encoded = self.tokenizer(
            query,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        input_ids = encoded["input_ids"].squeeze()
        attention_mask = encoded["attention_mask"].squeeze()

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "label": torch.tensor(label, dtype=torch.long)
        }


# Model Definition
class IntentClassificationModel(nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.distilbert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.classifier = nn.Linear(self.distilbert.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.distilbert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_output)

# Load .jsonl data
def load_jsonl(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

# Training
def train_model(model, data_loader, optimizer, device, epochs=4):
    model.train()
    criterion = nn.CrossEntropyLoss()
    for epoch in range(epochs):
        total_loss = 0
        for batch in data_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss / len(data_loader):.4f}")

# Evaluation
def evaluate_model(model, data_loader, device):
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids, attention_mask)
            predictions = torch.argmax(outputs, dim=1)
            all_preds.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    print("\nClassification Report:\n")
    print(classification_report(
        all_labels,
        all_preds,
        target_names=["announcement", "document"]
    ))

# Save model & tokenizer
def save_model(model, tokenizer, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(save_dir, "pytorch_model.bin"))
    tokenizer.save_pretrained(save_dir)
    config = DistilBertConfig.from_pretrained("distilbert-base-uncased")
    config.num_labels = 2
    with open(os.path.join(save_dir, "config.json"), "w") as f:
        f.write(config.to_json_string())

# Main Function
def main():
    dataset_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Dataset\intent_dataset.jsonl"  # unified dataset
    save_dir = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Final_Model"  # directory to save the model

    batch_size = 32
    learning_rate = 2e-5
    epochs = 4
    max_length = 128
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Using device: {device}")

    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    data = load_jsonl(dataset_path)

    labels = [item["label"] for item in data]
    train_data, test_data = train_test_split(data, test_size=0.2, stratify=labels, random_state=42)
    train_dataset = IntentDataset(train_data, tokenizer, max_length)
    test_dataset = IntentDataset(test_data, tokenizer, max_length)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    model = IntentClassificationModel(num_labels=2).to(device)
    optimizer = AdamW(model.parameters(), lr=learning_rate)

    print("🧠 Starting training...")
    train_model(model, train_loader, optimizer, device, epochs)

    print("\n📊 Evaluating on test set...")
    evaluate_model(model, test_loader, device)

    save_model(model, tokenizer, save_dir)
    print(f"\n✅ Model saved to {save_dir}")

if __name__ == "__main__":
    main()

