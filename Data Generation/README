# **Query Generation for Intent and NER Model Training**

## **Overview**  
This script generates synthetic queries for training the **Intent Recognition** and **Named Entity Recognition (NER)** models. The approach focuses on creating labeled query samples with dynamic entities and intents to simulate diverse and realistic user inputs.

---

## **Data Format**  
The queries are structured in JSON format with three main components:  
- **Intent**: The user’s goal or purpose behind the query (e.g., "Announcements", "Documents").  
- **Query**: The actual user input.  
- **Entities**: Key parts of the query dynamically labeled as entities.

**Example Format**:  
```json
{
    "Intent": "Announcements",
    "Query": "When is the last date to apply for internship?",
    "Entities": [
        "internship application",
        "last date"
    ]
}
```
Another example:  
```json
{
    "Intent": "Documents",
    "Query": "Where can I find the academic calendar?",
    "Entities": [
        "academic calendar"
    ]
}
```

---

## **Process**

1. **Base Query Collection**:  
   - Initial queries are collected and labeled with intents and entities as shown above.

2. **Entity Dictionary Definition**:  
   - A dictionary of entity combinations is created.  
   - Example:
     ```json
     {
         "internship application": ["thesis submission", "project deadline"],
         "last date": ["final day", "submission deadline"]
     }
     ```

3. **Dynamic Query Generation**:  
   - Using the **Faker library**, the script replaces non-entity parts of the query (e.g., phrases like "When is" or "Where can I find") with synthetic data.  
   - Dynamic entities are substituted based on the defined entity dictionary.

4. **Saving Generated Queries**:  
   - The newly generated queries are saved in JSON files categorized by **intent** (e.g., `announcements.json`, `documents.json`).  
   - These files are stored in the same location as the script for easy access.

---

## **Output Example**  
Generated queries in `announcements.json`:  
```json
[
    {
        "Intent": "Announcements",
        "Query": "What is the final day for thesis submission?",
        "Entities": [
            "thesis submission",
            "final day"
        ]
    },
    {
        "Intent": "Announcements",
        "Query": "When is the submission deadline for project deadline?",
        "Entities": [
            "project deadline",
            "submission deadline"
        ]
    }
]
```

---

## **Usage**  
1. Run the script to generate synthetic queries:  
   ```bash
   python generate_queries.py
   ```

2. Check the output files (`announcements.json`, `documents.json`, etc.) in the script's directory.  

---

## **Purpose**  
This approach helps in creating large, diverse, and dynamic training datasets for Intent and NER models, ensuring robust performance in understanding user queries with dynamic entities.  

--- 
