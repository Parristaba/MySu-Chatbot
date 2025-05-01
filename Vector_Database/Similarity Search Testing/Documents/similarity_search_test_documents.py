import sys
import json

sys.path.append(r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Vector Database")
from similarity_search import search_similar_content


# === QUERIES TO RUN ===
queries = [
    "What are PURE projects which has area of Computer Science and Engineering",
    "For Undergraduate students, when is the Course Withdrawal period start",
    "When is the tuition payment for spring semester starts",
    "How to register for freshman university courses",
    "When are the course registration days",
    "What are the degree requirements for Computer Science and Engineering",
    "How can I apply for graduation",
    "What is the minimum passing grade of a course"
]

# === OUTPUT FILE ===
OUTPUT_PATH = r"C:\Users\kagan_ntaijui\Desktop\MySu-Chatbot\Vector Database\Similarity Search Testing\Documents\sim_search_test_1_results.json"

# === BUILD RESULTS ===
print("🔍 Running document search for test queries...")
results_to_save = []

for query in queries:
    top_results = search_similar_content(query, is_document=True, k=3)
    results_to_save.append({
        "query": query,
        "top_results": top_results
    })

# === SAVE TO JSON ===
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results_to_save, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved similarity search results to: {OUTPUT_PATH}")
