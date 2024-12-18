import os
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import DistilBertTokenizer, DistilBertModel, AdamW, DistilBertConfig

# Custom Dataset for Intent Classification
class IntentDataset(Dataset):
    """
    A custom PyTorch Dataset class to handle the intent classification task.

    Attributes:
        data (list): List of data points where each contains 'Query' and 'Intent'.
        tokenizer: DistilBERT tokenizer to preprocess text queries.
        max_length (int): Maximum length of tokenized sequences for padding/truncation.
    """
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        """Returns the total number of samples in the dataset."""
        return len(self.data)

    def __getitem__(self, idx):
        """
        Retrieves a single data point and tokenizes the 'Query' text.

        Args:
            idx (int): Index of the data sample.

        Returns:
            dict: Contains input IDs, attention masks, and label tensor.
        """
        query = self.data[idx]["Query"]
        # Convert 'Intent' field to binary label: 0 for 'Announcements', 1 for 'Documents'
        label = 0 if self.data[idx]["Intent"] == "Announcements" else 1

        # Tokenize the query and return input IDs and attention masks
        encoded = self.tokenizer(query, truncation=True, padding='max_length',
                                 max_length=self.max_length, return_tensors='pt')
        input_ids = encoded["input_ids"].squeeze()
        attention_mask = encoded["attention_mask"].squeeze()

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "label": torch.tensor(label, dtype=torch.long)
        }

# Intent Classification Model
class IntentClassificationModel(nn.Module):
    """
    A DistilBERT-based model for intent classification.

    Attributes:
        distilbert: Pretrained DistilBERT model for feature extraction.
        fc: Fully connected layer for classification.
        softmax: LogSoftmax activation for multi-class classification.
    """
    def __init__(self, num_labels):
        super(IntentClassificationModel, self).__init__()
        self.distilbert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.fc = nn.Linear(self.distilbert.config.hidden_size, num_labels)
        self.softmax = nn.LogSoftmax(dim=1)  # Apply log softmax for output logits

    def forward(self, input_ids, attention_mask):
        """
        Defines the forward pass for the model.

        Args:
            input_ids: Tensor of tokenized input IDs.
            attention_mask: Tensor of attention masks for the input.

        Returns:
            Tensor: Logits for each class after applying log softmax.
        """
        # Extract features from the DistilBERT model
        outputs = self.distilbert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]  # CLS token representation
        logits = self.fc(cls_output)  # Pass through the fully connected layer
        return self.softmax(logits)

# Load Data from JSON Files
def load_data(announcement_file, document_file):
    """
    Loads and combines data from announcement and document JSON files.

    Args:
        announcement_file (str): Path to the announcements data file.
        document_file (str): Path to the documents data file.

    Returns:
        list: Combined list of data points containing 'Query' and 'Intent'.
    """
    with open(announcement_file, 'r') as f:
        announcements = json.load(f)
    with open(document_file, 'r') as f:
        documents = json.load(f)

    # Combine announcements and documents into a single dataset
    combined_data = announcements + documents
    return combined_data

# Training Function
def train_model(model, data_loader, optimizer, device, epochs=6):
    """
    Trains the intent classification model using the provided dataset.

    Args:
        model: The intent classification model.
        data_loader: DataLoader for the training dataset.
        optimizer: Optimizer for model parameters.
        device: Device (CPU or GPU) to run the training on.
        epochs (int): Number of training epochs.

    Returns:
        None
    """
    model.train()
    criterion = nn.NLLLoss()  # Negative Log Likelihood Loss for classification tasks

    for epoch in range(epochs):
        total_loss = 0  # Track total loss for the epoch
        for batch in data_loader:
            # Move batch data to the appropriate device
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            # Zero the gradients, perform forward pass, compute loss, and update weights
            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
        
        # Print average loss per epoch
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(data_loader):.4f}")

# Evaluation Function
def evaluate_model(model, data_loader, device):
    """
    Evaluates the model's performance on the test dataset.

    Args:
        model: The trained intent classification model.
        data_loader: DataLoader for the test dataset.
        device: Device (CPU or GPU) to run the evaluation on.

    Returns:
        float: Test accuracy of the model.
    """
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():  # Disable gradient calculations during evaluation
        for batch in data_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            # Get predictions and calculate accuracy
            outputs = model(input_ids, attention_mask)
            predictions = torch.argmax(outputs, dim=1)
            correct += (predictions == labels).sum().item()
            total += labels.size(0)

    accuracy = correct / total
    print(f"Test Accuracy: {accuracy:.4f}")
    return accuracy

# Save Model and Tokenizer
def save_model(model, tokenizer, save_dir):
    """
    Saves the trained model, tokenizer, and configuration to a specified directory.

    Args:
        model: The trained intent classification model.
        tokenizer: The tokenizer used for preprocessing.
        save_dir (str): Directory to save the model and tokenizer.

    Returns:
        None
    """
    os.makedirs(save_dir, exist_ok=True)

    # Save the model's parameters (weights)
    model_save_path = os.path.join(save_dir, "pytorch_model.bin")
    torch.save(model.state_dict(), model_save_path)
    print(f"Model saved to {model_save_path}")

    # Save the tokenizer
    tokenizer_save_path = os.path.join(save_dir, "tokenizer")
    tokenizer.save_pretrained(tokenizer_save_path)
    print(f"Tokenizer saved to {tokenizer_save_path}")

    # Save the model configuration
    config = DistilBertConfig.from_pretrained("distilbert-base-uncased")
    config.num_labels = 2  # Update for binary classification
    config_save_path = os.path.join(save_dir, "config.json")
    config.save_pretrained(config_save_path)
    print(f"Config saved to {config_save_path}")

# Main Function
def main():
    """
    Main function to execute the training and evaluation pipeline for intent classification.
    """
    # Paths for data and model saving
    announcement_file = "Data Generation/Generated Data/generated_announcements.json"
    document_file = "Data Generation/Generated Data/generated_documents.json"
    save_dir = "ML Models/Intent Model/DistilBert Trained"

    # Hyperparameters
    batch_size = 32
    learning_rate = 2e-5
    epochs = 1
    max_length = 128

    # Device setup: Use GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load and preprocess data
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    data = load_data(announcement_file, document_file)
    dataset = IntentDataset(data, tokenizer, max_length)

    # Train-test split
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    # Model and optimizer setup
    model = IntentClassificationModel(num_labels=2).to(device)
    optimizer = AdamW(model.parameters(), lr=learning_rate)

    # Train the model
    print("Starting Training...")
    train_model(model, train_loader, optimizer, device, epochs)

    # Evaluate the model
    print("Evaluating on Test Data...")
    accuracy = evaluate_model(model, test_loader, device)

    # Save the model and tokenizer
    save_model(model, tokenizer, save_dir)

if __name__ == "__main__":
    main()
