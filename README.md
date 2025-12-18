# shl-assessment-recommender

# SHL Assessment Recommendation System

## Overview

Hiring managers and recruiters often struggle to identify the right assessments for a role due to keyword-based search limitations.  
This project implements an **LLM-based semantic recommendation system** that recommends relevant **SHL Individual Test Solutions** based on a natural language query or job description.

The solution uses **transformer-based embeddings**, **vector similarity search**, and a **re-ranking pipeline** to deliver balanced and relevant recommendations across technical and behavioral skills.

---

## Key Capabilities

- Scrapes SHL’s product catalog directly from the SHL website
- Uses only **Individual Test Solutions** (Pre-packaged Job Solutions excluded)
- Parses and stores structured assessment metadata
- Transformer-based semantic embeddings (LLM)
- Efficient retrieval using FAISS
- Re-ranking logic to balance skill domains
- REST API for programmatic access
- Web application for interactive testing
- Evaluation using **Mean Recall@10**

---

## System Architecture & Pipeline

SHL Website
↓
Scraping & Parsing
↓
Structured Catalog (JSON)
↓
LLM Embeddings (Sentence Transformers)
↓
FAISS Vector Index
↓
Semantic Retrieval
↓
Re-ranking & Filtering
↓
Recommendations (API / Web App)


---

## Implementation

### 1. Data Ingestion & Catalog Construction

- The SHL product catalog is **scraped directly from the SHL website**.
- Only **Individual Test Solutions** are collected.
- **Pre-packaged Job Solutions are explicitly excluded**.
- Each assessment is parsed to extract:
  - Assessment name  
  - URL  
  - Description  
  - Test type (Knowledge & Skills / Personality & Behavior)

The parsed data is cleaned and stored locally to ensure reproducibility.

**Output:**
data/assessments.json


The final dataset contains **more than 377 individual test solutions**, satisfying the requirement.

---

### 2. Embedding & Indexing (LLM Integration)

- A **pretrained transformer-based language model**
  (`sentence-transformers/all-MiniLM-L6-v2`) is used to generate dense semantic embeddings.
- Embeddings are created from assessment name, description, and test type.
- Vectors are normalized and indexed using **FAISS** for efficient similarity search.
- The index and metadata are persisted to disk.

**Outputs:**
data/faiss.index
data/metadata.pkl



This enables **semantic retrieval**, not keyword matching.

---

### 3. Recommendation Pipeline

At inference time, the system executes the following pipeline:

1. **Query Ingestion**
   - Accepts a natural language query or job description.

2. **Text Normalization**
   - Normalizes text for consistent embeddings.

3. **Query Embedding**
   - The query is embedded using the same transformer model.

4. **Vector Retrieval**
   - FAISS retrieves the top-N most semantically similar assessments.

5. **Re-ranking & Filtering**
   - Lightweight heuristic scoring:
     - Boosts skill matches (Java, Python, SQL, etc.)
     - Encourages balance between:
       - Knowledge & Skills (K)
       - Personality & Behavior (P)

6. **Final Recommendation Output**
   - Returns 5–10 relevant assessments with name and URL.

---

### 4. Memory-Safe Backend Design (Important for Deployment)

To operate within **512 MB RAM limits** on free deployment tiers:

- The transformer model and FAISS index are **lazy-loaded** (loaded only on the first request).
- No large models or indexes are loaded at server startup.
- FAISS uses normalized vectors with inner-product similarity.
- The API runs with a **single worker**.

This ensures stable deployment without out-of-memory errors.

---

### 5. API & Web Application

- The pipeline is exposed via a **FastAPI REST API**:
  - `/health` – health check
  - `/recommend` – assessment recommendations
- A lightweight **web application** allows users to:
  - Enter job descriptions or queries
  - View recommendations in a tabular format

Both components are deployable and accessible via public URLs.

---

## Evaluation

### Dataset

- The provided **labeled training dataset** is used for evaluation.
- Each query is associated with one or more **ground-truth SHL assessment URLs**.
- Queries with multiple relevant assessments are grouped correctly.

---

### Metric: Mean Recall@10

The system is evaluated using **Mean Recall@10**, as specified.

For a single query:

Recall@10 =
(Number of relevant assessments in top 10 recommendations) /
(Total relevant assessments for the query)


Mean Recall@10 is computed by averaging Recall@10 across all queries.

---

### Evaluation Process

1. Generate top-10 recommendations for each query in the labeled dataset.
2. Compare predicted URLs with ground-truth URLs.
3. Compute Recall@10 per query.
4. Average results to obtain **Mean Recall@10**.

The evaluation logic is implemented in a dedicated script to ensure transparency and reproducibility.

---

### Iteration & Improvements

- Initial baseline relied purely on vector similarity.
- Improvements included:
  - Enhanced text representations for embeddings
  - Introduction of a re-ranking stage
  - Better balance between technical and behavioral assessments

These changes resulted in measurable improvements in Mean Recall@10.

---

## How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Scrape SHL catalog (run once)
bash
Copy code
python crawler/crawl_shl.py
3. Build embeddings and FAISS index
bash
Copy code
python embeddings/build_embeddings.py
4. Start backend API
bash
Copy code
uvicorn api.main:app --reload
5. Start web application
bash
Copy code
streamlit run frontend/app.py
Deployment
Backend API: Deployed on Render (single worker, lazy-loaded models)

Web Application: Deployed on Streamlit Cloud

Both services are publicly accessible and ready for evaluation.

Submission Artifacts
Public API endpoint URL

Public web application URL

GitHub repository containing:

Complete implementation

Evaluation scripts

This README documentation

CSV file containing predictions on the unlabeled test set

Summary
This project implements a modern retrieval-augmented recommendation system using transformer-based language models, semantic search, and structured evaluation.
The solution is modular, memory-efficient, reproducible, and aligned with real-world hiring and assessment recommendation use cases.



