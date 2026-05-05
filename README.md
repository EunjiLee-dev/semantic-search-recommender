# Semantic Search & Recommendation System (RAG-based)

## Goal
Build a **production-style semantic search and recommendation system** that supports natural language queries such as:

- "cheap sushi near university"
- "luxury pizza and wine"
- "coffee with wifi and parking"

and returns **context-aware, explainable POI recommendations** using a hybrid Retrieval-Augmented Generation (RAG) pipeline.


## Tech Stack
- Python
- FastAPI
- Sentence-Transformers (SBERT MiniLM)
- NumPy
- Pandas
- Scikit-learn (TF-IDF baseline)


## Features
- Semantic Retrieval: Sentence-BERT (MiniLM) embeddings for semantic search, Cosine similarity-based retrieval
- Ranking system with hybrid scoring (price, distance)
- Hard filtering layer (WiFi, parking, delivery, reservation)
- Human-readable explanations generated via LLM
- Automated evaluation pipeline (TF-IDF baseline vs SBERT comparison)

## System Architecture: End-to-End Pipeline
User Query
↓
FastAPI (/search endpoint)
↓
Sentence-BERT Embedding
↓
Intent Parsing
↓
Hard Filter (WiFi / Parking / Delivery / Reservation)
↓
Cosine Similarity Search
↓
Hybrid Ranking Layer
├── Semantic Score
├── Price Score
├── Distance Score
├── Attribute Score
↓
Top-K Selection
   ↓
Context Builder (relevant_features masking)
   ↓
Qwen2.5:3B (explanation only)
   ↓
Final Explainable Response


## Project Structure
- app/ # FastAPI backend
- services/ # search + ranking logic
- baseline/ # TF-IDF implementation
- scripts/ # preprocessing & embedding generation
- evaluation/ # evaluation framework
- data/ # dataset & embeddings

---

## Baseline Comparison
A TF-IDF baseline is implemented for evaluation purposes.
I evaluated retrieval performance using an internal scoring function
based on relevance, intent match, and attribute consistency.
Each query is scored on a 0–3 scale per retrieved item, averaged over top-K results.

### Overall Performance Comparison

| Query | TF-IDF Score | SBERT Score |
|------|-------------|-------------|
| cheap sushi with parking | **0.0** | **3.0** |
| coffee and bread with wifi | **1.8** | **3.0** |
| hamburger with delivery service | **2.8** | **2.8** |

### Findings:
- TF-IDF struggles with semantic queries and multi-intent inputs
- SBERT significantly improves relevance and context understanding
- Hybrid ranking further improves real-world usability

### Example Query
- input: cheap sushi with parking
- output (SBERT-based system): 
    - Sushi restaurants ranked by semantic + attribute match
    - Parking availability considered in ranking
    - Price level incorporated into scoring

---

## Status
- ✔ Semantic search implemented
- ✔ Hybrid ranking system implemented
- ✔ Intent-aware filtering
- ✔ TF-IDF baseline completed
- ✔ Explainable LLM layer (RAG)
- ✔ Evaluation pipeline with logging

## Future Improvements
- FAISS-based vector indexing for scalability
- Learning-to-rank model
- Web UI (Streamlit / React)
- User personalization layer

---

## How to Run
- Install dependencies
```bash
pip install -r requirements.txt
```
- Preprocess data
```bash
python scripts/preprocess.py
```
- Generate embeddings
```bash
python scripts/generate_embeddings.py
```
- Run API
```bash
uvicorn app.main:app --reload
```
- API docs
```bash
http://127.0.0.1:8000/docs
```
- Run evaluation
```bash
python -m evaluation.run_evaluation
python -m evaluation.compare_models
```
