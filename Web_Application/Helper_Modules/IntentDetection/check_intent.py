import torch
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# 🔄 New model path
model_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\NLU_Models\Intent_Model\Final_Model"

# 🔧 Load tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

# 🚀 Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# 🔁 Class label mapping
label_to_intent = {
    0: "announcement",
    1: "document"
}

def determineIntent(query_text):
    """
    Predict the intent label and confidence score for a given query.
    """
    inputs = tokenizer(query_text, truncation=True, padding="max_length", max_length=128, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
        confidence = F.softmax(logits, dim=1)[0][predicted_label].item()

    intent = label_to_intent.get(predicted_label, "unknown")
    return intent, confidence

# ▶ Example usage
if __name__ == "__main__":
    user_query = input("Enter a query: ")
    intent, confidence = determineIntent(user_query)
    print(f"Predicted Intent: {intent} (confidence: {confidence:.2f})")
