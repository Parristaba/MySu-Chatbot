Here's a README template for the provided file:

---

# Intent Classification with DistilBERT

This repository contains a PyTorch implementation of an intent classification model based on the DistilBERT architecture. The model classifies text queries into two intents: "Announcements" and "Documents." The dataset consists of two JSON files, one for announcements and another for documents. The main functionality includes model training, evaluation, and saving the trained model with its tokenizer.

## File Overview

### `intent_classification.py`

This script defines and trains a DistilBERT-based model for intent classification. Key components of the script include:

- **Custom Dataset Class**: `IntentDataset` handles the tokenization and preparation of data for training.
- **Model Architecture**: `IntentClassificationModel` is based on the pre-trained DistilBERT model for feature extraction, followed by a fully connected layer for classification.
- **Data Loading**: `load_data` combines two JSON files (announcements and documents) into a single dataset.
- **Training and Evaluation**: Functions for training (`train_model`) and evaluating (`evaluate_model`) the model.
- **Model Saving**: `save_model` saves the trained model, tokenizer, and configuration for later use.

## Requirements

- PyTorch
- Transformers
- CUDA (optional for GPU usage)

## Dataset

The dataset consists of two files:
1. `generated_announcements.json`: Contains query-intent pairs for announcements.
2. `generated_documents.json`: Contains query-intent pairs for documents.

The `Query` field in both files holds the text query, and the `Intent` field indicates whether the query pertains to announcements (labeled as 0) or documents (labeled as 1).

## How to Run

1. Clone this repository.
2. Install dependencies:

```bash
pip install torch transformers
```

3. Prepare your dataset in the following structure:

```text
Data Generation/
    Generated Data/
        generated_announcements.json
        generated_documents.json
```

4. Run the script:

```bash
python intent_classification.py
```

The script will:
- Load and preprocess the data.
- Split the dataset into training and test sets.
- Train the model.
- Evaluate the model on the test set.
- Save the trained model and tokenizer.

## Hyperparameters

- **Batch size**: 32
- **Learning rate**: 2e-5
- **Epochs**: 1
- **Max length**: 128

## Outputs

The model, tokenizer, and configuration are saved to the following directory:

```text
ML Models/
    Intent Model/
        DistilBert Trained/
            pytorch_model.bin
            tokenizer/
            config.json
```

**Note**: The model achived perfect accuracy score on the dataset. However, since the dataset has synthetic data only, this accuracy will probably drop when predicting human written queries.
