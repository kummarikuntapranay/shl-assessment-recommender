from fastapi import FastAPI
from pydantic import BaseModel
from recommender.pipeline import recommendation_pipeline
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# App initialization
# -----------------------------
app = FastAPI(title="SHL Assessment Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request schema
# -----------------------------
class QueryRequest(BaseModel):
    query: str

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Recommendation endpoint
# -----------------------------
@app.post("/recommend")
def recommend(request: QueryRequest):
    results = recommendation_pipeline(request.query)
    return {
        "recommendations": results
    }
