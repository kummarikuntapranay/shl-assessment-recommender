import json
import os

# ensure data folder exists
os.makedirs("data", exist_ok=True)

assessments = [
    {
        "name": "Java Programming Test",
        "url": "https://www.shl.com/solutions/products/java-programming-test/",
        "description": "Assess Java programming skills",
        "test_type": "K"
    },
    {
        "name": "Teamwork Assessment",
        "url": "https://www.shl.com/solutions/products/teamwork-assessment/",
        "description": "Assess collaboration and teamwork skills",
        "test_type": "P"
    },
    {
        "name": "Python Coding Test",
        "url": "https://www.shl.com/solutions/products/python-coding-test/",
        "description": "Assess Python programming skills",
        "test_type": "K"
    }
]



with open("data/assessments.json", "w", encoding="utf-8") as f:
    json.dump(assessments, f, indent=2)

    print("✅ assessments.json created successfully")