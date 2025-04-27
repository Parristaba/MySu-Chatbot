import random
import json
from tqdm import tqdm

# Define topic categories
topics = [
    "food", "sports", "technology", "movies", "music", "travel", "weather",
    "finance", "cryptocurrency", "fashion", "fitness", "gaming", "politics",
    "celebrities", "relationships", "self-help", "YouTube", "TikTok", "shopping",
    "history", "philosophy", "medicine", "psychology", "cooking", "pets"
]

# Define phrasing templates
phrases = [
    "What's the best {} related to {}?",
    "How can I learn more about {} and {}?",
    "Can you tell me the latest news about {} and {}?",
    "Give me some tips about {} and {}.",
    "What are the most popular {} and {} trends?",
    "How do I start with {} while exploring {}?",
    "Suggest me something combining {} and {}.",
    "Is there any way to improve my {} with the help of {}?",
    "Can you recommend a good {} along with {}?",
    "What is happening in the world of {} and {} right now?",
    "How do celebrities manage {} and {} together?",
    "Explain the impact of {} and {} on modern society.",
    "What are the emerging innovations in {} and {}?",
    "Discuss the importance of {} and {} nowadays.",
    "Where should I travel if I love both {} and {}?",
    "Share some trending news about {} and {}.",
    "How is {} influencing today's {}?",
    "Is {} affecting {} these days?",
    "Give examples of famous {} and {} personalities.",
    "What hobbies involve both {} and {}?",
    "How do {} and {} contribute to health and wellness?",
    "Compare the trends between {} and {}.",
    "Which countries are best known for {} and {}?",
    "How can one balance a career in {} and {}?",
    "Analyze the relationship between {} and {} in current times.",
    "What are some controversies surrounding {} and {}?",
    "How can I become an expert in both {} and {}?",
    "What are some must-visit destinations for {} and {} lovers?",
    "Can you suggest books on {} and {}?",
    "What movies best depict the world of {} and {}?"
]

# Some random topic sub-types
subtopics = [
    "artificial intelligence", "streetwear", "basketball", "sushi", "blockchain",
    "pop music", "mountain hiking", "rainstorms", "Instagram marketing",
    "home workouts", "indie games", "presidential elections", "actor scandals",
    "relationship advice", "cooking pasta", "dog training", "philosophy debates",
    "World War II", "mental health", "medical research", "self-improvement"
]

# Generate 10,000 instances
generated_questions = []

print("Generating 10,000 diverse irrelevant questions...")
for _ in tqdm(range(10000)):
    template = random.choice(phrases)
    topic1 = random.choice(topics)
    topic2 = random.choice(subtopics)
    question = template.format(topic1, topic2)
    generated_questions.append({
        "Query": question,
        "Relevance": "Other"
    })

# Save to JSON
output_path = 'MySu-Chatbot/Message Filter/Non_School_Related_Queries.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(generated_questions, f, indent=4, ensure_ascii=False)

print(f"Done! Labeled dataset saved to {output_path}.")
