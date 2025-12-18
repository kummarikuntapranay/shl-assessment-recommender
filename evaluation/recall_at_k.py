import pandas as pd
from collections import defaultdict
import csv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from recommender.recommend import recommend


def recall_at_k(predicted, relevant, k=10):
    predicted_k = predicted[:k]
    hits = len(set(predicted_k) & set(relevant))
    return hits / len(relevant) if relevant else 0.0


if __name__ == "__main__":

    # 🔹 Load real labeled train data
    df = pd.read_csv("data/train.csv")

    # 🔹 Group by query (VERY IMPORTANT)
    query_to_relevant = defaultdict(list)

    for _, row in df.iterrows():
        query_to_relevant[row["Query"]].append(row["Assessment_url"])

    recalls = []

    for query, relevant_urls in query_to_relevant.items():
        results = recommend(query, top_k=10)
        predicted_urls = [r["assessment_url"] for r in results]

        r_at_10 = recall_at_k(predicted_urls, relevant_urls, k=10)
        recalls.append(r_at_10)

        print("\nQuery:")
        print(query[:120], "...")
        print(f"Relevant URLs count: {len(relevant_urls)}")
        print(f"Recall@10: {r_at_10:.2f}")

    mean_recall = sum(recalls) / len(recalls)

    print("\n==============================")
    print(f"MEAN RECALL@10: {mean_recall:.3f}")
    print("==============================")
