import random
import json
from tqdm import tqdm
import os

# Broader and richer topics
topics = [
    "Champions League", "NBA", "AI tools", "K-pop", "TikTok trends",
    "Elon Musk", "Taylor Swift", "Netflix", "Ukraine conflict", "iPhone 15",
    "Bitcoin", "Reddit", "Fortnite", "One Piece", "Stranger Things",
    "YouTube influencers", "Oscars", "Olympics", "F1", "Amazon deals",
    "World Cup", "celebrity gossip", "Spotify Wrapped", "Memes", "ChatGPT"
]

subtopics = [
    "semi-finals", "transfer news", "release date", "latest controversy",
    "ranking", "AI impact", "earnings report", "Twitter reaction",
    "episode review", "political backlash", "public opinion", "fan theories",
    "match schedule", "drama", "leaks", "user backlash", "travel advisory",
    "new features", "fashion collabs", "gaming strategies"
]

# Natural question templates
phrases = [
    "What happened during the {} {}?",
    "Can you update me on the {} {}?",
    "Why is the {} {} trending right now?",
    "What's the hype around the {} {}?",
    "Who performed best in the {} {}?",
    "Explain the drama involving {} and {}.",
    "What's the public reaction to {} {}?",
    "Did {} really say something controversial in the {}?",
    "What's the fan theory about {} {}?",
    "Can you summarize the outcome of {} {}?",
    "Why are people boycotting {} {}?",
    "Any predictions for the {} {}?",
    "What are the consequences of {} {} for society?",
    "Why is {} considered overrated in {}?",
    "Who won the {} {} and why was it controversial?",
    "What makes {} {} such a big deal this year?",
    "Give me a short analysis on {} {}.",
    "What are social media users saying about {} {}?",
    "Did something unexpected happen during {} {}?",
    "Is it true that {} got banned from {}?"
]

generated_questions = []

print("Generating 10,000 realistic irrelevant questions...")
for _ in tqdm(range(10000)):
    template = random.choice(phrases)
    topic1 = random.choice(topics)
    topic2 = random.choice(subtopics)
    question = template.format(topic1, topic2)
    generated_questions.append({
        "Query": question,
        "Relevance": "Other"
    })

# Save

output_path = 'Message Filter\Training Data/Non_School_Related_Queries.json'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(generated_questions, f, indent=4, ensure_ascii=False)

print(f"Done! Labeled dataset saved to {output_path}.")
