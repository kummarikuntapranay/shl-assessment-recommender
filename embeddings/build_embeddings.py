import faiss
import numpy as np

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)  # smaller + faster
faiss.normalize_L2(embeddings)

index.add(embeddings)
faiss.write_index(index, "data/faiss.index")
