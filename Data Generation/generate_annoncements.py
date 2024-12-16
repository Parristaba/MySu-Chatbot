import json
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Synonym dictionary
synonyms = {
    "internship opportunities": ["internship openings", "internship programs", "internship availabilities", "internship positions"],
    "finals exam calendar": ["final exam schedule", "final exam timetable", "finals schedule", "exam period calendar"],
    "add/drop period": ["course change deadline", "course adjustment period", "course modification window", "registration change period"],
    "sports events": ["athletic events", "sports competitions", "sports matches", "recreational sports events"],
    "general events": ["campus activities", "student events", "university events", "community events"],
    "school service": ["campus facilities", "university services", "school amenities", "campus resources"],
    "course substitution": ["course replacement", "class substitution", "course swap", "subject replacement"],
    "class changes": ["class schedule updates", "class timing adjustments", "class rescheduling", "course schedule changes"],
    "holidays": ["public holidays", "semester breaks", "university holidays", "academic holidays"]
}

# Load JSON file with queries
with open("Templates For Data Generation/announcements_queries.json", "r") as file:
    queries = json.load(file)

# Function to generate new queries with multiple Faker-based variations
def generate_variations(data, synonyms, subs_per_entity=10, variations_per_sub=10):
    new_queries = []

    for entry in data:
        intent = entry["Intent"]
        query = entry["Query"]
        entities = entry["Entities"]

        # Process each entity in the query
        for entity in entities:
            if entity in synonyms:
                # Get synonyms for the entity
                sampled_synonyms = random.sample(synonyms[entity], min(subs_per_entity, len(synonyms[entity])))
                
                for synonym in sampled_synonyms:
                    # Generate multiple variations with Faker
                    for _ in range(variations_per_sub):
                        # Replace the entity with the synonym
                        updated_query = query.replace(entity, synonym)

                        # Update other parts of the query with Faker
                        updated_query = replace_non_entities(updated_query, synonym)

                        # Add the new entity to the list of entities
                        updated_entities = list(set(entities + [synonym]))

                        # Add the new entry
                        new_entry = {
                            "Intent": intent,
                            "Query": updated_query,
                            "Entities": updated_entities
                        }
                        new_queries.append(new_entry)
    return new_queries


# Function to replace non-entity parts of the query with Faker
def replace_non_entities(query, entity):
    words = query.split()
    new_words = []

    for word in words:
        if word.lower() not in entity.lower():
            # Replace words outside entity
            if word.istitle():
                new_words.append(fake.word().title())
            else:
                new_words.append(fake.word())
        else:
            new_words.append(word)

    return " ".join(new_words)

# Generate new queries
new_data = generate_variations(queries, synonyms)

# Save to a new JSON file
with open("Generated Data/generated_annoncement.json", "w") as file:
    json.dump(new_data, file, indent=4)

print("New queries generated and saved to output.json")
