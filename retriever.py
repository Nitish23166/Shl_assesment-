import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# Lazy Load Model
# -----------------------------

model = None


def get_model():

    global model

    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')

    return model


# -----------------------------
# Load FAISS Index
# -----------------------------

index = faiss.read_index("shl_index.faiss")


# -----------------------------
# Load Metadata
# -----------------------------

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


# -----------------------------
# Retrieval Function
# -----------------------------

def retrieve_assessments(query, k=10):

    # Load model only when needed
    model = get_model()

    # Create query embedding
    query_vector = model.encode([query])

    query_vector = np.array(query_vector).astype("float32")

    # Search FAISS index
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