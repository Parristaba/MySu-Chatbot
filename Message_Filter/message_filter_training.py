import json
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import os

# File paths
non_school_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Message Filter\Training Data\Non_School_Related_Queries.json"
school_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Message Filter\Training Data\School_Related_Queries.json"
greeting_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Message Filter\Training Data\Greeting_Queries.json"

# Load datasets
with open(non_school_path, 'r', encoding='utf-8') as f:
    non_school_data = json.load(f)
with open(school_path, 'r', encoding='utf-8') as f:
    school_data = json.load(f)
with open(greeting_path, 'r', encoding='utf-8') as f:
    greeting_data = json.load(f)

# Map labels to integer classes
label_map = {
    "Non-School": 0,
    "School": 1,
    "Greeting": 2
}

# Prepare combined dataset
data = []
for item in non_school_data:
    data.append({"text": item["Query"], "label": label_map["Non-School"]})
for item in school_data:
    data.append({"text": item["Query"], "label": label_map["School"]})
for item in greeting_data:
    data.append({"text": item["Query"], "label": label_map["Greeting"]})

# Split into train and test
texts = [x["text"] for x in data]
labels = [x["label"] for x in data]

train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts,
    labels,
    test_size=0.1,
    random_state=42,
    stratify=labels
)

# Load tokenizer and tokenize
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

# Build HuggingFace Dataset
train_dataset = Dataset.from_dict({**train_encodings, "labels": train_labels})
test_dataset = Dataset.from_dict({**test_encodings, "labels": test_labels})

# Load model with 3 output classes
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Training config
training_args = TrainingArguments(
    output_dir="MySu-Chatbot/Message Filter/checkpoints_3class",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    logging_dir="MySu-Chatbot/Message Filter/logs_3class",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
    report_to="none"
)

# Metric function
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    return {"accuracy": (preds == labels).astype(float).mean().item()}

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Train
trainer.train()

# Evaluate
predictions = trainer.predict(test_dataset)
preds = predictions.predictions.argmax(-1)

print("Classification Report:")
print(classification_report(test_labels, preds, target_names=["Non-School", "School", "Greeting"]))
print("Confusion Matrix:")
print(confusion_matrix(test_labels, preds))

# Save model
# Save model
save_dir = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Message Filter\Filter Model"
os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)

print(f"Training complete. 3-class filter model saved to {save_dir}.")
