import json
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from tqdm import tqdm

# Paths
model_path = "MySu-Chatbot/Message Filter/distilbert_message_filter"
test_data_path = "MySu-Chatbot\Message Filter\message_filter_test_set.json"
output_path = "MySu-Chatbot\Message Filter\message_filter_test_results.json"

# Load model and tokenizer
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model = DistilBertForSequenceClassification.from_pretrained(model_path).to(device)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)

# Load test data
with open(test_data_path, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

# Prepare output
predicted_data = []
true_count = 0
false_count = 0

print("Running predictions...")

for item in tqdm(test_data):
    text = item["query"]
    label = 1 if item["label"] == "School Related" else 0

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()

    match = prediction == label

    if match:
        true_count += 1
    else:
        false_count += 1

    predicted_data.append({
        "query": text,
        "true_label": item["label"],
        "predicted_label": "School Related" if prediction == 1 else "Other",
        "match": match
    })

# Save predictions
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(predicted_data, f, indent=4, ensure_ascii=False)

# Print results
print(f"True predictions: {true_count}")
print(f"False predictions: {false_count}")
print(f"Saved detailed predictions to {output_path}")