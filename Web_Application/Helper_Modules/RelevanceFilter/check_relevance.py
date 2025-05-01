import torch
import torch.nn.functional as F
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Load model and tokenizer
model_path = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Message Filter\Filter Model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

# Label mapping
label_map = {
    0: "Non-School",
    1: "School",
    2: "Greeting"
}

def checkRelevance(query: str):
    """
    Classifies the relevance of a user query.

    Args:
        query (str): The input text query from the user.

    Returns:
        tuple[str, float]: A tuple containing:
            - Predicted class label (e.g., "School", "Greeting", "Non-School")
            - Confidence score for the prediction
    """
    inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
        confidence = F.softmax(logits, dim=1)[0][predicted_label].item()

    return label_map[predicted_label], confidence

# Example usage
if __name__ == "__main__":
    while True:
        user_query = input("\nEnter a query (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        label, score = checkRelevance(user_query)
        print(f"Predicted: {label} (confidence: {score:.2f})")