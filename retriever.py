import json

# Load metadata
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


def retrieve_assessments(query, k=5):

    query = query.lower()

    scored_results = []

    for item in metadata:

        combined_text = (
            item["name"] + " " +
            item["description"] + " " +
            " ".join(item["keys"]) + " " +
            " ".join(item["job_levels"])
        ).lower()

        score = 0

        for word in query.split():

            if word in combined_text:
                score += 1

        scored_results.append((score, item))

    scored_results.sort(reverse=True, key=lambda x: x[0])

    top_results = [item for score, item in scored_results[:k]]

    results = []

    for item in top_results:

        results.append({
            "name": item["name"],
            "url": item["url"],
            "description": item["description"],
            "job_levels": item["job_levels"],
            "keys": item["keys"]
        })

    return results