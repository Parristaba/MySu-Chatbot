import json
import random

# Define categories and sample phrases
categories = {
    "Greetings": [
        "Hello!", "Hi there!", "Good morning!", "Good afternoon!", "Good evening!",
        "Hey!", "Howdy!", "Hi!", "Greetings!", "What's up?", "Hey there!", "Hiya!",
        "How's it going?", "Yo!", "Hi everyone!", "Hello there!", "Hi friend!"
    ],
    "Goodbyes": [
        "Goodbye!", "See you later!", "Bye!", "Take care!", "Catch you later!",
        "Farewell!", "Talk to you soon!", "See ya!", "Have a great day!", "Bye for now!"
    ],
    "Thanks": [
        "Thank you!", "Thanks a lot!", "Much appreciated!", "Thanks so much!",
        "Thanks a ton!", "Thank you very much!", "Thanks!", "I appreciate it!",
        "Many thanks!", "Thanks a million!"
    ]
}

# Generate synthetic queries
def generate_queries(categories, num_queries=10000):
    generated_data = []
    for _ in range(num_queries):
        # Randomly select a phrase from the "Greetings" category
        phrase = random.choice(categories["Greetings"])
        # Append the generated query
        generated_data.append({
            "Query": phrase,
            "Relevance": "Greeting"
        })
    return generated_data

# Generate 5000 queries
generated_queries = generate_queries(categories, num_queries=5000)

# Define output file path
output_file_path = "Message Filter/Training Data/Greeting_Queries.json"

# Save the generated queries to a JSON file
with open(output_file_path, 'w') as f:
    json.dump(generated_queries, f, indent=4)

print(f"✅ Synthetic greetings queries generated and saved to: {output_file_path}")