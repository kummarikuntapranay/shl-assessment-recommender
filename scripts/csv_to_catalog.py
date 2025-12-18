import csv
import json

INPUT_CSV = "data/train.csv"  # CHANGE name if needed
OUTPUT_JSON = "data/catalog.json"

catalog = []

with open(INPUT_CSV, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        catalog.append({
            "name": row.get("Assessment_name") or row.get("name"),
            "url": row.get("Assessment_url") or row.get("url"),
            "description": row.get("Description", "")
        })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print("catalog.json created successfully ✅")
