# Named Entity Recognition (NER) for Announcements Dataset

## Overview
This project uses a T5 model to extract entities dynamically from a dataset of queries. The entities are subject to change based on the structure of each query, and the model is trained to detect them based on the semantics of the text. The goal is to predict entities like "research conference" or "first-year students' orientation" in a variety of queries.

## Features
- **Dynamic Entity Extraction**: Entities are extracted based on query semantics, not fixed patterns. This allows for flexibility as the structure of queries may change over time.
- **Data Preprocessing**: The dataset is cleaned and preprocessed to handle entity extraction and improve tokenization.
- **Custom Dataset Class**: The `AnnouncementDataset` class is used to load and preprocess the data, tokenize it, and format it for the T5 model.
- **Training & Evaluation**: The model is trained on a dataset split into training and validation sets, with detailed loss tracking for optimization.
- **Predictions**: The trained model generates predictions for new queries, which are saved in a specified output file.

## File Structure
- `Data Generation/Generated Data/generated_announcements.json`: Input training data (queries with entities).
- `ML Models/NER Models/Announcements NER/t5_model`: Path where the trained model and tokenizer are saved.
- `ML Models/NER Models/Announcements NER/Announcements_Testing.json`: Input test data (queries for prediction).
- `ML Models/NER Models/Announcements NER/Announcements_NER_predictions.json`: Output file where predictions are saved.

## How It Works
1. **Data Preparation**: 
   - The dataset (`generated_announcements.json`) consists of queries with associated entities.
   - The `AnnouncementDataset` class processes the dataset, cleaning the queries and preparing the entities for training.

2. **Training**:
   - The model is trained on the dataset using the `train_model()` function. The T5 model is fine-tuned for conditional generation, where the task is to generate entities based on the input query.
   - The dataset is split into training and validation sets for evaluation during training.

3. **Testing**:
   - After training, the model is used to predict entities in unseen queries from a test dataset (`Announcements_Testing.json`).
   - The predicted entities are saved in `Announcements_NER_predictions.json`.

4. **Dynamic Entity Extraction**:
   - Entities in the queries are dynamically extracted, allowing the model to adapt to new types of entities or query structures over time.
   
5. **Example Predictions**:
   The predicted output for sample queries may look like the following:

   ```json
   {
       "Query": "When is the research conference scheduled for this year?",
       "Entities": [
           "research conference"
       ]
   },
   {
       "Query": "When is the first-year students' orientation taking place?",
       "Entities": [
           "first-year students' orientation"
       ]
   },
   {
       "Query": "When will the environmental sustainability forum be held this year?",
       "Entities": [
           "environmental sustainability forum"
       ]
   },
   {
       "Query": "When is the last day to withdraw from a class this semester?",
       "Entities": [
           "last day to withdraw from a class"
       ]
   }
   ```

## Requirements
- **Python 3.x**
- **PyTorch** (`torch`)
- **Transformers** (`transformers`)
- **Scikit-learn** (`sklearn`)

Install the necessary dependencies using:

```bash
pip install torch transformers scikit-learn
```

## Usage

### Training the Model
To train the model, run the following command:
```bash
python train_model.py
```
Make sure to specify the correct paths for your dataset, model output, and test data.

### Testing the Model
To test the model and generate predictions, run:
```bash
python test_model.py
```

## Notes
- The model extracts entities dynamically based on the query's semantic structure, so it adapts to varying query formats.
- The test data mimics human-written queries to evaluate how well the model generalizes to real-world use cases.
