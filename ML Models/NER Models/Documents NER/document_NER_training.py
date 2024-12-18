import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import T5Tokenizer, T5ForConditionalGeneration, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
import json
import os
import re

class AnnouncementDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=128):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        
        self.tokenizer = tokenizer
        self.max_length = max_length
        self._preprocess_data()
    
    def _preprocess_data(self):
        cleaned_data = []
        for entry in self.data:
            query = entry.get('Query', '').strip()
            if query:
                entities = entry.get('Entities', [])
                entity_str = ', '.join(entities) if entities else 'None'  # Join entities with a comma
                cleaned_data.append({
                    'Query': query,
                    'Entities': entity_str
                })
        self.data = cleaned_data


    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        entry = self.data[idx]
        query = entry['Query']
        entity = entry['Entities']
        
        # Improved input formatting
        input_text = f"extract entities from: {query}"
        
        # Tokenization with more robust handling
        input_encoding = self.tokenizer(
            input_text, 
            return_tensors="pt", 
            padding="max_length", 
            truncation=True, 
            max_length=self.max_length
        )
        
        target_encoding = self.tokenizer(
            entity, 
            return_tensors="pt", 
            padding="max_length", 
            truncation=True, 
            max_length=self.max_length
        )
        
        return {
            'input_ids': input_encoding['input_ids'].squeeze(),
            'attention_mask': input_encoding['attention_mask'].squeeze(),
            'labels': target_encoding['input_ids'].squeeze()
        }

def train_model(dataset_path, model_output_path, batch_size=16, num_epochs=3, learning_rate=3e-4):
    # Set random seed for reproducibility
    torch.manual_seed(42)
    
    # Load and preprocess data
    with open(dataset_path, 'r', encoding='utf-8') as file:
        full_data = json.load(file)
    
    # Print dataset statistics
    print("\nDataset Analysis:")
    print(f"Total instances: {len(full_data)}")

    # Prepare tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    model = T5ForConditionalGeneration.from_pretrained('t5-small').cuda()
    
    # Prepare dataset
    full_dataset = AnnouncementDataset(dataset_path, tokenizer)
    train_size = int(0.85 * len(full_dataset))
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, len(full_dataset) - train_size])
    
    # Create DataLoaders
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Prepare optimizer and learning rate scheduler
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(train_dataloader) * num_epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, 
        num_warmup_steps=int(0.1 * total_steps), 
        num_training_steps=total_steps
    )
    
    # Training loop with more detailed logging
    best_val_loss = float('inf')
    for epoch in range(num_epochs):
        model.train()
        total_train_loss = 0
        
        for batch in train_dataloader:
            # Move batch to GPU
            input_ids = batch['input_ids'].cuda()
            attention_mask = batch['attention_mask'].cuda()
            labels = batch['labels'].cuda()
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(
                input_ids=input_ids, 
                attention_mask=attention_mask, 
                labels=labels
            )
            loss = outputs.loss
            total_train_loss += loss.item()
            
            # Backward pass and optimization
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
        
        # Validation
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for batch in val_dataloader:
                input_ids = batch['input_ids'].cuda()
                attention_mask = batch['attention_mask'].cuda()
                labels = batch['labels'].cuda()
                
                outputs = model(
                    input_ids=input_ids, 
                    attention_mask=attention_mask, 
                    labels=labels
                )
                total_val_loss += outputs.loss.item()
        
        # Calculate average losses
        avg_train_loss = total_train_loss / len(train_dataloader)
        avg_val_loss = total_val_loss / len(val_dataloader)
        
        # Print epoch summary
        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"Train Loss: {avg_train_loss:.4f}")
        print(f"Validation Loss: {avg_val_loss:.4f}")
        
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            # Save the best model
            os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
            model.save_pretrained(model_output_path)
            tokenizer.save_pretrained(model_output_path)
            print(f"Best model saved with validation loss: {best_val_loss:.4f}")
    
    print(f"Final model saved to {model_output_path}")
    return model, tokenizer

def test_model(model_path, test_file_path, output_file_path, batch_size=32):
    model = T5ForConditionalGeneration.from_pretrained(model_path).cuda()
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    
    # Load test data
    with open(test_file_path, 'r', encoding='utf-8') as file:
        test_data = json.load(file)
    
    # Prepare model for generation
    model.eval()
    
    predicted_data = []
    for i in range(0, len(test_data), batch_size):
        batch = test_data[i:i+batch_size]
        
        queries = [f"extract entities from: {entry['Query']}" for entry in batch]
        inputs = tokenizer(queries, return_tensors="pt", padding=True, truncation=True, max_length=128).to('cuda')
        
        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs['input_ids'], 
                attention_mask=inputs['attention_mask'], 
                max_length=128,
                num_return_sequences=1,
                do_sample=False
            )
        
        for j, (entry, output) in enumerate(zip(batch, outputs)):
            entity = tokenizer.decode(output, skip_special_tokens=True).strip()
            
            # Split the output into multiple entities based on commas
            entities = entity.split(',') if entity != 'None' else []
            entities = [e.strip() for e in entities]
            
            entry['Entities'] = entities
            predicted_data.append(entry)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(predicted_data, file, indent=4, ensure_ascii=False)
    
    print(f"Predictions saved to {output_file_path}")
    print(f"Total predictions: {len(predicted_data)}")


# Main execution
if __name__ == "__main__":
    # Paths
    dataset_path = "Data Generation/Generated Data/generated_documents.json"
    model_output_path = "ML Models/NER Models/Documents NER/t5_model"
    test_file_path = "ML Models/NER Models/Documents NER/Documents_Testing.json"
    output_predictions_path = "ML Models/NER Models/Documents NER/Documents_NER_predictions.json"
    
    # Train the model
    model, tokenizer = train_model(dataset_path, model_output_path)
    
    # Test the model
    test_model(model_output_path, test_file_path, output_predictions_path)


# Main execution
if __name__ == "__main__":
    # Paths
    dataset_path = "Data Generation/Generated Data/generated_documents.json"
    model_output_path = "ML Models/NER Models/Documents NER/t5_model"
    test_file_path = "ML Models/NER Models/Documents NER/Documents_Testing.json"
    output_predictions_path = "ML Models/NER Models/Documents NER/Documents_NER_predictions.json"
    
    # Train the model
    model, tokenizer = train_model(dataset_path, model_output_path)
    
    # Test the model
    test_model(model_output_path, test_file_path, output_predictions_path)