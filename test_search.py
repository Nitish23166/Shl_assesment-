import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("shl_index.faiss")

# Load metadata
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# User query
query = input("Enter hiring requirement: ")

# Convert query to embedding
query_vector = model.encode([query])

query_vector = np.array(query_vector).astype("float32")

# Search top 5 results
k = 5

distances, indices = index.search(query_vector, k)

print("\nTop Matching Assessments:\n")

for i in indices[0]:

    result = metadata[i]

    print("=" * 50)

    print("NAME:", result["name"])

    print("URL:", result["url"])

    print("JOB LEVELS:", result["job_levels"])

    print("KEYS:", result["keys"])

    print("DESCRIPTION:", result["description"][:300])

    print()