import random
import json
from faker import Faker

fake = Faker()

# --- Topic Generators --- #
def gen_exam_topic():
    course_code = f"{random.choice(['CS', 'MATH', 'HIST', 'ECON', 'BIO'])} {random.randint(100, 599)}.{random.choice(['A', 'B', '0'])}"
    return f"{course_code} exam"

def gen_leave_or_exit_topic():
    return random.choice([
        "semester leave", "cancellation of enrollment", "dismissal from the university", "withdrawal from a course"
    ])

def gen_major_minor_topic():
    return random.choice([
        "double major application", "minor program eligibility", "major declaration", "diploma program change",
        "degree requirements", "course substitution", "repeating a course"
    ])

def gen_financial_topic():
    return random.choice([
        "tuition fees", "payment deadlines", "scholarship applications", "scholarship evaluations"
    ])

def gen_graduation_topic():
    return random.choice([
        "graduation application", "graduation requirements", "diploma supplement", "degree evaluation"
    ])

def gen_course_reg_topic():
    return random.choice([
        "course registration", "add-drop dates", "registration overrides", "course scheduling"
    ])

def gen_pure_topic():
    return random.choice([
        "PURE program projects", "PURE program requirements", "PURE program participation"
    ])

def gen_prep_topic():
    return random.choice([
        "Foundation Development Year rules", "prep year dismissal", "prep year semester leave"
    ])

def gen_internship_exchange_topic():
    return random.choice([
        "Erasmus application", "exchange program quotas", "mandatory internship process"
    ])

def gen_academic_eval_topic():
    return random.choice([
        "grading system", "student feedback surveys", "academic assessment forms"
    ])

def gen_other_topic():
    return random.choice([
        "student ID card", "WiFi maintenance", "mentor program application", "discipline policies", "library hours"
    ])

topic_generators = [
    gen_exam_topic, gen_leave_or_exit_topic, gen_major_minor_topic,
    gen_financial_topic, gen_graduation_topic, gen_course_reg_topic,
    gen_pure_topic, gen_prep_topic, gen_internship_exchange_topic,
    gen_academic_eval_topic, gen_other_topic
]

# --- Templates --- #
announcement_templates = [
    "When is {topic}?",
    "Has {topic} come out yet?",
    "Any idea when they’ll post {topic}?",
    "Is {topic} available now?",
    "Did they share anything about {topic}?",
    "Do you know if {topic} is published?",
    "When are they announcing {topic}?",
    "Was there an update about {topic}?",
    "What’s the date for {topic}?",
    "Where can I see the {topic} announcement?",
    "Did the university release {topic} already?",
    "Is {topic} posted anywhere?",
    "Do we know when {topic} is expected?",
    "What’s the latest on {topic}?",
    "When can we expect {topic} to be released?",
    "Is it too late to check {topic}?",
    "Was {topic} updated this week?",
    "Have the dates for {topic} been announced?",
    "Has anyone seen the new {topic}?",
    "Is today the release date for {topic}?",
]

document_templates = [
    "How do I apply for {topic}?",
    "Where can I find the rules for {topic}?",
    "What do I need for {topic}?",
    "Is there a guide for {topic}?",
    "Any prerequisites for {topic}?",
    "Who’s eligible for {topic}?",
    "Can I get help with {topic} stuff?",
    "How does the process work for {topic}?",
    "What are the steps for {topic}?",
    "Do I need to talk to my advisor about {topic}?",
    "Can I apply for {topic} as a second year?",
    "Where’s the info page for {topic}?",
    "What’s the general policy about {topic}?",
    "How do students usually handle {topic}?",
    "What documents should I prepare for {topic}?",
    "Is {topic} open to international students?",
    "What’s the eligibility for {topic}?",
    "How is {topic} different by department?",
    "Where do I even start with {topic}?",
    "Can I find a PDF guide for {topic}?",
]

# --- Generation Logic --- #
def generate_pairs(num_pairs=10000):
    pairs = []
    for _ in range(num_pairs // 2):
        topic_func = random.choice(topic_generators)
        topic = topic_func()

        # --- Positive pair ---
        if random.random() < 0.5:
            templates = random.sample(announcement_templates, 2)
            label = 1
        else:
            templates = random.sample(document_templates, 2)
            label = 1

        q1 = templates[0].format(topic=topic)
        q2 = templates[1].format(topic=topic)
        pairs.append({ "query1": q1, "query2": q2, "label": label })

        # --- Negative pair ---
        ann_template = random.choice(announcement_templates)
        doc_template = random.choice(document_templates)
        q1 = ann_template.format(topic=topic)
        q2 = doc_template.format(topic=topic)
        pairs.append({ "query1": q1, "query2": q2, "label": 0 })

    return pairs

def write_pairs_to_file(pairs, output_file="contrastive_pairs_dataset.jsonl"):
    with open(output_file, "w", encoding="utf-8") as f:
        for pair in pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    print(f"✅ Contrastive dataset written → {output_file} with {len(pairs)} samples.")

if __name__ == "__main__":
    pairs = generate_pairs(num_pairs=12000)  # 6000 pos + 6000 neg
    write_pairs_to_file(pairs)
