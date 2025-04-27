# similarity_search_test.py

import json
from similarity_search import search_announcements  # Import your search module

# === CONFIGURATION ===
TEST_SET_FILE = "MySu-Chatbot/Vector Database/sim_search_test_2_set.json"
OUTPUT_FILE = "MySu-Chatbot/Vector Database/sim_search_test_2_results.json"
TOP_K = 5  # Number of top results to retrieve

# === STEP 1: Load Test Set ===
print("[1/4] Loading test set...")
with open(TEST_SET_FILE, "r", encoding="utf-8") as f:
    test_samples = json.load(f)

print(f"Loaded {len(test_samples)} test samples.")

# === STEP 2: Perform Similarity Search for Each Query ===
print("[2/4] Running similarity search...")
results = []

for item in test_samples:
    query_handled = item["Query_handled"]
    query_original = item["Query"]
    announcement_gt = item["Announcement"]

    # Call the search function
    retrieved_results = search_announcements(query_handled, top_k=TOP_K)

    # Build the new result object
    result_entry = {
        "Query": query_original,
        "Query_handled": query_handled,
        "Announcement": announcement_gt,
        "Retrieved_Results": retrieved_results
    }

    results.append(result_entry)

print("[3/4] Search completed for all queries.")

# === STEP 3: Save Test Results with Retrieved Data ===
print(f"[4/4] Saving results to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n✅ Test completed successfully! Results saved.")
