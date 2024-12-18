import json
import itertools

# Load the input files
announcement_file_path = 'Data Generation/Templates For Data Generation/announcement_queries.json'
document_file_path = 'Data Generation/Templates For Data Generation/document_queries.json'

with open(announcement_file_path, 'r') as f:
    announcements = json.load(f)

with open(document_file_path, 'r') as f:
    documents = json.load(f)

# Define the output file paths
generated_announcements_file_path = 'Data Generation/Generated Data/generated_announcements.json'
generated_documents_file_path = 'Data Generation/Generated Data/generated_documents.json'

def generate_announcement_combinations(announcements):
    """
    Generate all possible query combinations for announcements based on entity placeholders (g1, g2, g3).
    
    Args:
        announcements (dict): A dictionary where keys are query patterns containing placeholders
                              and values are dictionaries with possible values for 'g1', 'g2', and 'g3'.

    Returns:
        list: A list of dictionaries, where each dictionary represents a generated query
              with intent, query text, and corresponding entities.
    """
    generated_data = []
    
    for pattern, entities in announcements.items():
        g1_values = entities.get('g1', [])
        g2_values = entities.get('g2', [])
        g3_values = entities.get('g3', [])
        
        # Generate combinations for g1 + g2
        for g1, g2 in itertools.product(g1_values, g2_values):
            query = pattern.replace("\\g<1>", g1).replace("\\g<2>", g2)
            generated_data.append({
                "Intent": "Documents",
                "Query": query,
                "Entities": [g1, g2]
            })
        
        # If g3 exists, generate combinations for g1 + g2 + g3
        if g3_values:
            for g1, g2, g3 in itertools.product(g1_values, g2_values, g3_values):
                query = pattern.replace("\\g<1>", g1).replace("\\g<2>", g2).replace("\\g<3>", g3)
                generated_data.append({
                    "Intent": "Documents",
                    "Query": query,
                    "Entities": [g1, g2, g3]
                })
        else:
            # Ensure g3 placeholders are not included in queries if g3 values are empty
            for g1, g2 in itertools.product(g1_values, g2_values):
                query = pattern.replace("\\g<1>", g1).replace("\\g<2>", g2)
                # Remove any lingering \\g<3> if g3 values are not present
                query = query.replace("\\g<3>", "")
                generated_data.append({
                    "Intent": "Documents",
                    "Query": query,
                    "Entities": [g1, g2]
                })
    
    return generated_data


def generate_document_combinations(documents):
    """
    Generate all possible query combinations for documents based on entity placeholders (g1, g2, g3).
    
    Args:
        documents (dict): A dictionary where keys are query patterns containing placeholders
                          and values are dictionaries with possible values for 'g1', 'g2', and 'g3'.

    Returns:
        list: A list of dictionaries, where each dictionary represents a generated query
              with intent, query text, and corresponding entities.
    """
    generated_data = []
    
    for pattern, entities in documents.items():
        g1_values = entities.get('g1', [])
        g2_values = entities.get('g2', [])
        g3_values = entities.get('g3', [])
        
        # Generate combinations for g1 + g2
        for g1, g2 in itertools.product(g1_values, g2_values):
            query = pattern.replace("\\g<1>", g1).replace("\\g<2>", g2)
            generated_data.append({
                "Intent": "Documents",
                "Query": query,
                "Entities": [g1, g2]
            })
        
        # If g3 exists, generate combinations for g1 + g2 + g3
        if g3_values:
            for g1, g2, g3 in itertools.product(g1_values, g2_values, g3_values):
                query = pattern.replace("\\g<1>", g1).replace("\\g<2>", g2).replace("\\g<3>", g3)
                generated_data.append({
                    "Intent": "Documents",
                    "Query": query,
                    "Entities": [g1, g2, g3]
                })
        else:
            # Ensure g3 placeholders are not included in queries if g3 values are empty
            for g1, g2 in itertools.product(g1_values, g2_values):
                query = pattern.replace("\\g<1>", g1).replace("\\g<2>", g2)
                # Remove any lingering \\g<3> if g3 values are not present
                query = query.replace("\\g<3>", "")
                generated_data.append({
                    "Intent": "Documents",
                    "Query": query,
                    "Entities": [g1, g2]
                })
    
    return generated_data


# Generate announcements and documents
generated_announcements = generate_announcement_combinations(announcements)
generated_documents = generate_document_combinations(documents)

# Filter out any queries with unresolved placeholders
generated_announcements = [entry for entry in generated_announcements if "\\g<1>" not in entry["Query"] and "\\g<2>" not in entry["Query"] and "\\g<3>" not in entry["Query"]]
generated_documents = [entry for entry in generated_documents if "\\g<1>" not in entry["Query"] and "\\g<2>" not in entry["Query"] and "\\g<3>" not in entry["Query"]]

# Write the generated data to JSON files
with open(generated_announcements_file_path, 'w') as f:
    json.dump(generated_announcements, f, indent=4)

with open(generated_documents_file_path, 'w') as f:
    json.dump(generated_documents, f, indent=4)

print("Data generation complete.")
