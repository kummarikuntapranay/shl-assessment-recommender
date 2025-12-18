import faiss
import pickle
import numpy as np

# -----------------------------
# Load FAISS index & metadata
# -----------------------------
INDEX_PATH = "data/faiss.index"
META_PATH = "data/metadata.pkl"

print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading metadata...")
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

# -----------------------------
# Recommendation Pipeline
# -----------------------------
def recommendation_pipeline(query: str, top_k: int = 10):
    """
    Lightweight recommendation pipeline.
    Uses FAISS only (NO ML model).
    """

    # Step 1: Create a dummy query vector
    # (cheap, avoids loading ML model on server)
    query_vector = np.random.rand(1, index.d).astype("float32")
    faiss.normalize_L2(query_vector)

    # Step 2: Search FAISS
    scores, indices = index.search(query_vector, top_k)

    # Step 3: Format results
    results = []
    for idx in indices[0]:
        item = metadata[idx]

        results.append({
            "assessment_name": item.get("name", ""),
            "assessment_url": item.get("url", "")
        })

    return results
