import json

# File paths for the input JSON files
file1_path = 'MySu-Chatbot\Data Generation\Generated Data\generated_announcements.json'
file2_path = 'MySu-Chatbot\Data Generation\Generated Data\generated_documents.json'

# Output file path
output_file_path = 'MySu-Chatbot/Message Filter/School_Related_Queries.json'

# Function to process a JSON file and extract queries with relevance
def process_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        processed_data = []
        for entry in data:
            processed_data.append({
                "Query": entry["Query"],
                "Relevance": "School Related"
            })
        return processed_data

# Process both files
data1 = process_file(file1_path)
data2 = process_file(file2_path)

# Merge the data
merged_data = data1 + data2

# Write the merged data to a new JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)

print(f"Merged data has been saved to {output_file_path}")