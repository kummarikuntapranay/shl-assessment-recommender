import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("data/faiss.index")
with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def recommend(query, top_k=5):
    query_vec = model.encode([query])
    _, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        item = metadata[idx]
        results.append({
            "assessment_name": item["name"],
            "assessment_url": item["url"]
        })

    return results
