import json
import faiss
import pickle
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def build_index():
    with open("data/assessments.json", "r") as f:
        assessments = json.load(f)

    texts = [
        f"{a['name']} {a['description']} {a['test_type']}"
        for a in assessments
    ]

    embeddings = MODEL.encode(texts, show_progress_bar=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, "data/faiss.index")

    with open("data/metadata.pkl", "wb") as f:
        pickle.dump(assessments, f)

    print("Embeddings & index saved")

if __name__ == "__main__":
    build_index()
