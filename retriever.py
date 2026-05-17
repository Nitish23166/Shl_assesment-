import json

# -----------------------------
# LOAD METADATA
# -----------------------------

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


# -----------------------------
# RETRIEVAL FUNCTION
# -----------------------------

def retrieve_assessments(query, k=5):

    query = query.lower().strip()

    scored_results = []

    # -----------------------------
    # Technical Keywords
    # -----------------------------

    technical_keywords = [
        "java",
        "python",
        "sql",
        "backend",
        "frontend",
        "react",
        "developer",
        "engineer",
        "software",
        "programming",
        "cloud",
        "api",
        ".net",
        "javascript",
        "core java",
        "spring",
        "django",
        "node"
    ]

    # -----------------------------
    # Business Keywords
    # -----------------------------

    business_keywords = [
        "manager",
        "leadership",
        "sales",
        "marketing",
        "analyst",
        "communication",
        "personality",
        "behavior",
        "competency",
        "management"
    ]

    # -----------------------------
    # LOOP THROUGH ALL ASSESSMENTS
    # -----------------------------

    for item in metadata:

        combined_text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("keys", [])) + " " +
            " ".join(item.get("job_levels", []))
        ).lower()

        score = 0

        # -----------------------------
        # Basic Keyword Matching
        # -----------------------------

        for word in query.split():

            if word in combined_text:
                score += 3

        # -----------------------------
        # Technical Role Boosting
        # -----------------------------

        for tech_word in technical_keywords:

            if tech_word in query and tech_word in combined_text:
                score += 5

        # -----------------------------
        # Business Role Boosting
        # -----------------------------

        for biz_word in business_keywords:

            if biz_word in query and biz_word in combined_text:
                score += 4

        # -----------------------------
        # Exact Assessment Name Boost
        # -----------------------------

        if query in item.get("name", "").lower():
            score += 15

        # -----------------------------
        # Penalize Mismatched Technologies
        # -----------------------------

        if "java" in query:

            if ".net" in combined_text or "asp.net" in combined_text:
                score -= 8

        if ".net" in query:

            if "java" in combined_text:
                score -= 8

        if "frontend" in query:

            if "backend" in combined_text:
                score -= 2

        if "backend" in query:

            if "frontend" in combined_text:
                score -= 2

        # -----------------------------
        # Keep Only Relevant Results
        # -----------------------------

        if score > 0:
            scored_results.append((score, item))

    # -----------------------------
    # SORT RESULTS
    # -----------------------------

    scored_results.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    # -----------------------------
    # TOP K RESULTS
    # -----------------------------

    top_results = [
        item for score, item in scored_results[:k]
    ]

    # -----------------------------
    # FORMAT OUTPUT
    # -----------------------------

    results = []

    for item in top_results:

        results.append({
            "name": item.get("name", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
            "job_levels": item.get("job_levels", []),
            "keys": item.get("keys", [])
        })

    return results