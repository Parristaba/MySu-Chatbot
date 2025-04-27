import os
import pandas as pd
import re
import json
from sentence_transformers import SentenceTransformer

# Initialize Sentence-BERT model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text: str) -> str:
    """Cleans text by removing extra whitespace."""
    if pd.isna(text):
        return ""
    return re.sub(r'\s+', ' ', str(text)).strip()


def construct_text(row: pd.Series, file_type: str) -> str:
    """Constructs a meaningful sentence from row based on known structure."""
    if file_type == "shuttle_schedule":
        return f"{row['Direction']} shuttle from {row['Departure']} to {row['Arrival']} at {row['Time']}"

    elif file_type == "mysu_events":
        title = clean_text(row.get("title", ""))
        author = clean_text(row.get("author", ""))
        location = clean_text(row.get("location", ""))
        start = clean_text(row.get("start_date", ""))
        end = clean_text(row.get("end_date", ""))
        event_type = clean_text(row.get("type", ""))
        return (
            f"Event: {title} by {author} at {location} "
            f"from {start} to {end}. Type: {event_type}."
        )

    elif file_type == "academic_calendar":
        base = clean_text(row.get("All Terms", ""))
        relevant_fields = [col for col in row.index if col != "All Terms"]
        groups = [col for col in relevant_fields if not pd.isna(row[col]) and str(row[col]).strip() != ""]
        return f"Deadline: {base} | Applies to: {', '.join(groups)}"

    elif file_type == "announcements":
        title = clean_text(row.get("Title", ""))
        author = clean_text(row.get("Author", ""))
        unit = clean_text(row.get("Unit", ""))
        start = clean_text(row.get("Start Date", ""))
        end = clean_text(row.get("End Date", ""))
        category = clean_text(row.get("Category", ""))
        return (
            f"Announcement: {title} by {author} from {unit}, running from {start} to {end}. "
            f"Category: {category}."
        )

    elif file_type == "april_meals_2025":
        date = clean_text(row.get("Date", ""))
        name = clean_text(row.get("Name", ""))
        category = clean_text(row.get("Category", ""))
        calories = clean_text(str(row.get("Calories", "")))
        cal_type = clean_text(row.get("Calorie Type", ""))
        lunch = row.get("Lunch", False)
        dinner = row.get("Dinner", False)

        meals = []
        if lunch:
            meals.append("lunch")
        if dinner:
            meals.append("dinner")
        meal_text = " and ".join(meals) if meals else "not served"

        return (
            f"On {date}, dish '{name}' ({category}, {calories} kcal, {cal_type} calorie) "
            f"is served at {meal_text}."
        )

    else:
        # Fallback: concatenate all columns
        return " | ".join([clean_text(str(cell)) for cell in row])


def process_csv(file_path: str, section_name: str) -> str:
    """Processes CSV file: clean, encode, save text and embeddings."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")

    df = pd.read_csv(file_path)

    if df.empty or df.shape[1] == 0:
        raise ValueError(f"{file_path} is empty or has no usable content.")

    # Build cleaned text entries
    texts = [clean_text(construct_text(row, section_name)) for _, row in df.iterrows()]

    # Encode with Sentence-BERT
    embeddings = model.encode(texts)

    # Save fallback .txt
    os.makedirs("data", exist_ok=True)
    with open(f"data/{section_name}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(texts))

    # Save embeddings to JSON
    os.makedirs("embeddings", exist_ok=True)
    with open(f"embeddings/{section_name}.json", "w", encoding="utf-8") as f:
        json.dump([
            {"id": f"{section_name}_{i}", "text": text, "embedding": embedding.tolist()}
            for i, (text, embedding) in enumerate(zip(texts, embeddings))
        ], f, indent=2)

    return f"{len(texts)} entries processed and stored from '{section_name}'."


# --- Main Test Block ---
if __name__ == "__main__":
    print(process_csv(
        "Web Application/Web Scraping/Data/shuttle_schedule_tryy.csv",
        "shuttle_schedule"
    ))

    print(process_csv(
        "Web Application/Web Scraping/Data/mysu_events.csv",
        "mysu_events"
    ))

    print(process_csv(
        "Web Application/Web Scraping/Data/academic_calendar.csv",
        "academic_calendar"
    ))

    print(process_csv(
        "Web Application/Web Scraping/Data/announcements.csv",
        "mysu_announcements"
    ))

    print(process_csv(
        "Web Application/Web Scraping/Data/april_meals_2025.csv",
        "april_meals_2025"
    ))
