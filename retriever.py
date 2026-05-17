import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# Global Variables
# -----------------------------

model = None
index = None
metadata = None


# -----------------------------
# Lazy Load Model
# -----------------------------

def get_model():

    global model

    if model is None:
        model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

    return model


# -----------------------------
# Lazy Load FAISS Index
# -----------------------------

def get_index():

    global index

    if index is None:
        index = faiss.read_index("shl_index.faiss")

    return index


# -----------------------------
# Lazy Load Metadata
# -----------------------------

def get_metadata():

    global metadata

    if metadata is None:
        with open("metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)

    return metadata


# -----------------------------
# Retrieval Function
# -----------------------------

def retrieve_assessments(query, k=10):

    model = get_model()

    index = get_index()

    metadata = get_metadata()

    # Create embedding
    query_vector = model.encode([query])

    query_vector = np.array(query_vector).astype("float32")

    # Search FAISS
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