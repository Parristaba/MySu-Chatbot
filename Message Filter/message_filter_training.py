import json
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# File paths
non_school_path = "MySu-Chatbot/Message Filter/Non_School_Related_Queries.json"
school_path = "MySu-Chatbot/Message Filter/School_Related_Queries.json"

# Load datasets
with open(non_school_path, 'r', encoding='utf-8') as f:
    non_school_data = json.load(f)

with open(school_path, 'r', encoding='utf-8') as f:
    school_data = json.load(f)

# Prepare combined dataset
data = []
for item in non_school_data:
    data.append({"text": item["Query"], "Relevance": 0})  # Other => 0
for item in school_data:
    data.append({"text": item["Query"], "Relevance": 1})  # School Related => 1

# Split into train and test
train_texts, test_texts, train_labels, test_labels = train_test_split(
    [x["text"] for x in data],
    [x["Relevance"] for x in data],  # Use "Relevance" instead of "label"
    test_size=0.1,
    random_state=42,
    stratify=[x["Relevance"] for x in data]  # Use "Relevance" here as well
)

# Load tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

# Tokenize
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

# Prepare datasets
train_dataset = Dataset.from_dict({**train_encodings, "labels": train_labels})
test_dataset = Dataset.from_dict({**test_encodings, "labels": test_labels})

# Load model
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# Move model to GPU if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

# Training arguments
training_args = TrainingArguments(
    output_dir="MySu-Chatbot/Message Filter/checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    logging_dir="MySu-Chatbot/Message Filter/logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
    report_to="none"
)

# Compute metrics
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    return {"accuracy": (preds == labels).astype(float).mean().item()}

# Trainer
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
print(classification_report(test_labels, preds))
print("Confusion Matrix:")
print(confusion_matrix(test_labels, preds))

# Save the fine-tuned model
model.save_pretrained("MySu-Chatbot/Message Filter/distilbert_message_filter")
tokenizer.save_pretrained("MySu-Chatbot/Message Filter/distilbert_message_filter")

print("Training complete. Model saved.")