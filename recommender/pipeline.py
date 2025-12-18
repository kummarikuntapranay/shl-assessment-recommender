import json
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load LLM (Embedding Model)
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Load Stored Data
# -----------------------------
INDEX_PATH = "data/faiss.index"
META_PATH = "data/metadata.pkl"

index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)


# -----------------------------
# Stage 1: Text Normalization
# -----------------------------
def normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


# -----------------------------
# Stage 2: Query Embedding (LLM)
# -----------------------------
def embed_query(text: str) -> np.ndarray:
    return model.encode([text])


# -----------------------------
# Stage 3: Vector Retrieval
# -----------------------------
def retrieve_candidates(query_embedding, top_k=30):
    distances, indices = index.search(query_embedding, top_k)
    return indices[0]


# -----------------------------
# Stage 4: Re-ranking & Filtering
# -----------------------------
def rerank_candidates(candidate_indices, query, final_k=10):
    ranked = []

    for idx in candidate_indices:
        item = metadata[idx]

        score = 0
        name = item["name"].lower()
        desc = item["description"].lower()

        # Simple relevance boosts
        if "java" in query and "java" in name:
            score += 3
        if "python" in query and "python" in name:
            score += 3
        if item.get("test_type", "").lower().startswith("p"):
            score += 1  # personality boost
        if item.get("test_type", "").lower().startswith("k"):
            score += 1  # skills boost

        ranked.append((score, item))

    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked[:final_k]


# -----------------------------
# Stage 5: Final Pipeline
# -----------------------------
def recommendation_pipeline(query: str, top_k=10):
    """
    Full end-to-end recommendation pipeline
    """
    # 1. Normalize input
    query_clean = normalize_text(query)

    # 2. Embed query
    query_embedding = embed_query(query_clean)

    # 3. Retrieve candidates
    candidates = retrieve_candidates(query_embedding, top_k=30)

    # 4. Re-rank & filter
    ranked_results = rerank_candidates(candidates, query_clean, final_k=top_k)

    # 5. Format response
    return [
        {
            "assessment_name": item["name"],
            "assessment_url": item["url"]
        }
        for _, item in ranked_results
    ]
