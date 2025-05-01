import re

# Custom stopwords that often appear in university-related questions
CUSTOM_STOPWORDS = {
    "what", "when", "where", "who", "which", "how",
    "is", "are", "was", "were", "do", "does", "did",
    "can", "could", "should", "would", "will", "shall",
    "i", "you", "we", "they", "the", "a", "an",
    "of", "on", "for", "in", "at", "to", "from", "about",
    "please", "tell", "me", "us", "know", "give", "show",
    "be", "have", "has", "had", "it", "this", "that"
}

def prune_query(query: str) -> str:
    """
    Prunes a user query by removing common stopwords and keeping semantically meaningful tokens.
    
    Args:
        query (str): The original user query.
    
    Returns:
        str: A pruned version of the query suitable for RAG embedding.
    """
    # Normalize and tokenize
    query = query.lower()
    tokens = re.findall(r"\b\w+\b", query)

    # Filter tokens
    pruned_tokens = [token for token in tokens if token not in CUSTOM_STOPWORDS]

    return " ".join(pruned_tokens)