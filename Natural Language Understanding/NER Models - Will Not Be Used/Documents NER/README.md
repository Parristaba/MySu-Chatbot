# Named Entity Recognition with T5 for Document Classification

## Overview
This repository contains a pipeline for training and testing a Named Entity Recognition (NER) model using the T5 (Text-to-Text Transfer Transformer) model from Hugging Face's `transformers` library. The model extracts entities from queries related to documents, such as those found in academic or university settings. It uses a dataset in JSON format where each entry contains a query and a list of associated entities.

## Features
- **Custom Dataset Class**: Loads and preprocesses JSON data for entity extraction.
- **T5 Model**: Uses `T5ForConditionalGeneration` to perform text-to-text NER.
- **Training Pipeline**: Supports model training, validation, and optimization with a custom learning rate scheduler.
- **Testing Pipeline**: Evaluates the trained model on unseen data and outputs predictions.
- **Entity Extraction**: Outputs entities extracted from a given query.

## Requirements
- Python 3.x
- PyTorch
- Hugging Face `transformers`
- Scikit-learn
- `json`, `os`, `re` (standard Python libraries)

Install required packages:
```bash
pip install torch transformers sklearn
```

## File Structure
- `announcement_dataset.py`: Contains the dataset class for loading and preprocessing the dataset.
- `train_model.py`: Script for training the model on the provided dataset.
- `test_model.py`: Script for testing the model and generating predictions.
- `generated_documents.json`: Input dataset containing queries and entities.
- `t5_model`: Directory to save the trained model.

## Dataset
The dataset should be in the following format:
```json
[
  {
    "Query": "Where can I check scholarship applications through the career services desk?",
    "Entities": ["check", "scholarship applications", "through the career services desk"]
  },
  {
    "Query": "What resources can I submit in the eLOGO portal?",
    "Entities": ["resources", "submit", "the eLOGO portal"]
  }
]
```

## Training the Model
To train the NER model, run the following script:
```bash
python train_model.py
```
This will:
- Load and preprocess the dataset (`generated_documents.json`).
- Train the T5 model to extract entities.
- Save the best model to `t5_model`.

## Testing the Model
To test the trained model, run the following script:
```bash
python test_model.py
```
This will:
- Load the trained model from `t5_model`.
- Test the model on the provided test dataset (`Documents_Testing.json`).
- Output predictions in the format:
```json
[
  {
    "Query": "Where can I check scholarship applications through the career services desk?",
    "Entities": ["check", "scholarship applications", "through the career services desk"]
  },
  ...
]
```

## Example Output
Sample output after running the model's prediction:
```json
{
    "Query": "Where can I check scholarship applications through the career services desk?",
    "Entities": ["check", "scholarship applications", "through the career services desk"]
},
{
    "Query": "What resources can I submit in the eLOGO portal?",
    "Entities": ["resources", "submit", "the eLOGO portal"]
},
{
    "Query": "Where can I download internship information in person?",
    "Entities": ["download", "internship information", "in person"]
}
```

## Conclusion
This repository provides a complete solution for training and testing a Named Entity Recognition model using T5, which can be easily adapted to other types of text classification tasks involving entity extraction.
