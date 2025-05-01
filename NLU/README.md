Here's a README for your ML models, incorporating the pipeline and the two NER models.

---

# ML Models for Query Classification and Named Entity Recognition (NER)

This repository contains machine learning models designed for classifying user queries and extracting entities based on the identified intent. The pipeline consists of two primary components:

1. **Intent Classification**: A model that predicts the intent of the query.
2. **Named Entity Recognition (NER)**: A model that extracts relevant entities based on the predicted intent.

The two NER models are designed to handle different types of entity extraction and can be applied depending on the intent classification result.

## Overview

### Pipeline Workflow

1. **Query Input**: A user query is fed into the pipeline.
2. **Intent Classification**: The query is first processed by an intent classification model to predict the intent of the query.
3. **NER Model**: Based on the predicted intent, one of two NER models is applied to extract entities from the query.
4. **Output**: The final output consists of the query's intent and the extracted entities.

### NER Models
- **NER Model 1 (T5-based)**: This model is designed to extract entities from queries related to dynamic information such as class schedules, event announcements, or semester details.
- **NER Model 2**: A secondary NER model used for more general entity extraction tasks, designed to handle queries with less domain-specific structure.

## Requirements

- Python 3.x
- Required Libraries:
  - `transformers` for model loading and inference
  - `torch` for model training and evaluation
  - `scikit-learn` for pipeline management and evaluation
  - `json` for handling data
  - `pandas` for data manipulation (if required)
  - `tensorflow` (if required for any model-specific needs)
  
## Folder Structure

```text
ML Models/
    ├── NER Models/
        ├── Announcements NER/
            ├── announcement_NER_training.py    # Training and evaluation script for NER Model 1
            ├── announcement_NER_model.py       # Pre-trained model for NER Model 1
        ├── General NER/
            ├── general_NER_training.py        # Training and evaluation script for NER Model 2
            ├── general_NER_model.py           # Pre-trained model for NER Model 2
    ├── Intent Classification/
        ├── intent_classifier_model.py        # Model for intent classification
        ├── intent_classifier_training.py     # Training and evaluation script for intent classifier
```

## Components

### 1. Intent Classifier
This model is trained to predict the intent behind the user's query. The model uses a suitable architecture for text classification (e.g., BERT, DistilBERT, or other transformer models) and classifies the input query into predefined categories.

#### How it works:
- Takes the input query and predicts its intent (e.g., "Document Retrieval", "Class Schedule", etc.).
- Based on the predicted intent, the pipeline selects the appropriate NER model to process the query further.

### 2. Named Entity Recognition (NER) Models
There are two NER models in the pipeline. Depending on the intent, the appropriate NER model is selected for entity extraction.

#### NER Model 1: `announcement_NER_model.py`
This model is trained specifically for extracting entities from dynamic information like class schedules, events, and semester-specific details. It uses a T5-based architecture designed for semantic NER tasks.

#### NER Model 2: `general_NER_model.py`
This secondary NER model handles more general entity extraction tasks. It is used when the input query does not match the intent types that require the first model.

### Data Processing and Pipeline

1. **Data Preprocessing**:
   - The input data consists of queries with placeholders (e.g., `\\g<1>`, `\\g<2>`).
   - The intent classifier processes the query to predict the intent.
   - The appropriate NER model is then applied based on the intent prediction.

2. **NER Model Training**:
   - Both NER models (T5-based and General NER) are trained using annotated data, where entity labels are provided for each query.
   - Models use token-based masking for entity extraction.

### Usage

1. **Training Models**:
   - To train the **intent classifier**:
     ```bash
     python ML Models/Intent Classification/intent_classifier_training.py
     ```
   - To train **Announcement NER Model**:
     ```bash
     python ML Models/NER Models/Announcements NER/announcement_NER_training.py
     ```
   - To train **Document NER Model 2**:
     ```bash
     python ML Models/NER Models/General NER/general_NER_training.py
     ```

2. **Predicting with the Pipeline**:
   Once models are trained and the pipeline is ready, you can predict the intent and extract entities from a query as follows:
   
   ```python
   from ML.Models.IntentClassification import predict_intent
   from ML.Models.NER import apply_ner_model
   
   # Sample query
   query = "What is the schedule for class A on Monday?"

   # Step 1: Predict the intent of the query
   intent = predict_intent(query)

   # Step 2: Apply the appropriate NER model based on the predicted intent
   if intent == 'Documents':
       entities = apply_ner_model(query, model_type='announcement')
   else:
       entities = apply_ner_model(query, model_type='general')
   
   print(f"Intent: {intent}")
   print(f"Extracted Entities: {entities}")
   ```

### Outputs

- **Intent**: The predicted intent of the query (e.g., "Documents", "Schedule").
- **Entities**: The extracted entities based on the intent, such as class names, dates, or times.

## Conclusion

This pipeline allows seamless integration of intent classification and NER, providing robust query processing for a variety of use cases, from document retrieval to dynamic information extraction. By leveraging the two NER models, the pipeline ensures high flexibility and accuracy across different types of queries.

---

Let me know if you'd like any further modifications or clarifications!
