import random
import json
from faker import Faker

fake = Faker()

def generate_fake_topic():
    course_code = f"{random.choice(['CS', 'MATH', 'HIST', 'ECON', 'BIO'])} {random.randint(100, 599)}.{random.choice(['A', 'B', '0'])}"
    detail = fake.catch_phrase()
    return f"{course_code} {detail}"

announcement_templates = [
    "Has the {topic} been announced?",
    "When is the {topic} going to be published?",
    "Is the {topic} out yet?",
    "Do we have an update about the {topic}?",
    "Did they release the {topic} this week?",
    "What’s the latest news on the {topic}?",
    "Have they posted the {topic}?",
    "Was the {topic} shared recently?",
    "Is there a new announcement about the {topic}?",
    "Have the results for the {topic} been released?",
    "When will the {topic} be available?",
    "Is the timeline for {topic} finalized?",
    "Are there any updates regarding {topic}?",
]

document_templates = [
    "What is the procedure for {topic}?",
    "How does the university handle {topic}?",
    "What rules apply to the {topic}?",
    "Can students apply for {topic}?",
    "What are the criteria for {topic}?",
    "Where can I find information about {topic}?",
    "What’s the policy for {topic}?",
    "What documents are needed for {topic}?",
    "Is there a guideline for the {topic}?",
    "How does the {topic} system work?",
    "Is advisor approval needed for {topic}?",
    "Are there eligibility requirements for {topic}?",
    "How do departments implement {topic} procedures?",
]

def generate_samples(templates, label, count):
    used = set()
    samples = []
    while len(samples) < count:
        template = random.choice(templates)
        topic = generate_fake_topic()
        sentence = template.format(topic=topic)
        if sentence not in used:
            used.add(sentence)
            samples.append({ "text": sentence, "label": label })
    return samples

def generate_dataset(announcement_count=7000, document_count=7000, output_file="intent_dataset.jsonl"):
    ann_data = generate_samples(announcement_templates, "announcement", announcement_count)
    doc_data = generate_samples(document_templates, "document", document_count)
    dataset = ann_data + doc_data
    random.shuffle(dataset)

    with open(output_file, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Dataset created with {len(dataset)} samples → {output_file}")

if __name__ == "__main__":
    generate_dataset()
