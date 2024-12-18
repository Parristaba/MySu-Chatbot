Here’s a README for your script:

---

# Data Generation for Announcement and Document Queries

This script generates various query combinations based on entity placeholders (`g1`, `g2`, `g3`) from two input JSON files: `announcement_queries.json` and `document_queries.json`. It generates queries by replacing these placeholders with the corresponding values provided for each entity (`g1`, `g2`, and `g3`) and then exports the generated queries to new JSON files.

## Requirements

- Python 3.x
- The `itertools` module (part of the Python Standard Library)
- The `json` module (part of the Python Standard Library)

## Input Files

1. **announcement_queries.json**:
    - Contains query patterns with placeholders (`g1`, `g2`, `g3`) and corresponding entity values for announcements.
  
2. **document_queries.json**:
    - Contains query patterns with placeholders (`g1`, `g2`, `g3`) and corresponding entity values for documents.

## Output Files

1. **generated_announcements.json**:
    - Stores all generated queries for announcements, where placeholders are replaced with entity values.
  
2. **generated_documents.json**:
    - Stores all generated queries for documents, where placeholders are replaced with entity values.

## Functions

### `generate_announcement_combinations(announcements)`
- Generates all possible query combinations for announcements.
- Takes a dictionary of announcement patterns and their entity values as input.
- Returns a list of generated queries with intent, query text, and corresponding entities.

### `generate_document_combinations(documents)`
- Generates all possible query combinations for documents.
- Takes a dictionary of document patterns and their entity values as input.
- Returns a list of generated queries with intent, query text, and corresponding entities.

### Data Filtering
- The script filters out any queries that still contain unresolved placeholders (e.g., `\\g<1>`, `\\g<2>`, `\\g<3>`).

## Usage

1. Prepare the input files (`announcement_queries.json` and `document_queries.json`) in the specified folder.
2. Run the script.
3. The generated queries will be saved in `generated_announcements.json` and `generated_documents.json`.

## Example

**Input File (`announcement_queries.json`):**
```json
{
  "Announcement query example: \\g<1> will start on \\g<2>": {
    "g1": ["Class A", "Class B"],
    "g2": ["Monday", "Tuesday"],
    "g3": ["Morning", "Afternoon"]
  }
}
```

**Generated Output (`generated_announcements.json`):**
```json
[
  {
    "Intent": "Documents",
    "Query": "Announcement query example: Class A will start on Monday",
    "Entities": ["Class A", "Monday"]
  },
  {
    "Intent": "Documents",
    "Query": "Announcement query example: Class B will start on Tuesday",
    "Entities": ["Class B", "Tuesday"]
  }
]
```

## Conclusion

This script helps automate the process of generating a variety of queries by substituting placeholders with real entity values, allowing for the easy creation of dynamic queries for announcements and documents.
