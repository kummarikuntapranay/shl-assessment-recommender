from fastapi import FastAPI
from pydantic import BaseModel
from recommender.recommend import recommend

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend_assessments(req: QueryRequest):
    results = recommend(req.query, top_k=5)
    return {
        "recommendations": [
            {
                "assessment_name": r["assessment_name"],
                "assessment_url": r["assessment_url"]
            }
            for r in results
        ]
    }
