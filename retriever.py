import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("shl_index.faiss")

# Load metadata
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


def retrieve_assessments(query, k=10):

    query_vector = model.encode([query])

    query_vector = np.array(query_vector).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = []

    for i in indices[0]:

        item = metadata[i]

        results.append({
            "name": item["name"],
            "url": item["url"],
            "description": item["description"],
            "job_levels": item["job_levels"],
            "keys": item["keys"]
        })

    return results