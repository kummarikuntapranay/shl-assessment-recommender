import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading catalog...")
with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

print(f"Total catalog items: {len(catalog)}")

for i, item in enumerate(catalog):
    name = str(item.get("name", "")).strip()
    description = str(item.get("description", "")).strip()

    combined_text = (name + " " + description).strip()

    # FORCE keep at least name
    if not combined_text:
        combined_text = name or "unknown assessment"

    texts.append(combined_text)

print(f"Total texts created: {len(texts)}")



print("Loading ML model (ONLY LOCALLY)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")
embeddings = model.encode(texts, batch_size=32)
embeddings = embeddings.astype("float32")

print("Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
faiss.normalize_L2(embeddings)
index.add(embeddings)

print("Saving index...")
faiss.write_index(index, "data/faiss.index")

with open("data/metadata.pkl", "wb") as f:
    pickle.dump(catalog, f)

print("DONE ✅")
