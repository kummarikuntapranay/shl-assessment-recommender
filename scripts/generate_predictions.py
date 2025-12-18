import csv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from recommender.recommend import recommend


test_queries = [
    "Hiring Java developer with collaboration skills",
    "Looking for Python and SQL analyst"
]

with open("submission/predictions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "Assessment_url"])

    for query in test_queries:
        results = recommend(query, top_k=10)
        for r in results:
            writer.writerow([query, r["assessment_url"]])
