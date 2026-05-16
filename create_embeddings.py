import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load cleaned catalog
with open("cleaned_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract searchable text
texts = [item["combined_text"] for item in catalog]

# Create embeddings
embeddings = model.encode(texts)

# Convert to numpy array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "shl_index.faiss")

# Save metadata separately
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print("Embeddings created successfully!")
print(f"Total assessments indexed: {len(catalog)}")