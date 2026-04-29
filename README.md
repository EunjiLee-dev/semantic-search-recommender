# Semantic Search & Recommendation System

## Goal
Build a natural language search system that supports queries such as:

- "cheap sushi near university"
- "luxury pizza and wine"
- "coffee with wifi and parking"

and returns contextually relevant POI recommendations.

## Tech Stack
- Python
- FastAPI
- Sentence-Transformers (SBERT MiniLM)
- NumPy
- Pandas
- Scikit-learn (TF-IDF baseline)

## Features
- Semantic search using embeddings
- Cosine similarity retrieval
- Ranking system with hybrid scoring (price, distance)
- Hard filtering layer (WiFi, parking, delivery, reservation)
- Explainable Recommendations: Score breakdown, Human-readable explanation of ranking decision

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
Final Ranking
↓
Explainable JSON Response


## Project Structure
- app/ # FastAPI backend
- services/ # search + ranking logic
- baseline/ # TF-IDF implementation
- scripts/ # preprocessing & embedding generation
- evaluation/ # TF-IDF vs SBERT comparison
- data/ # dataset & embeddings

---

## Baseline Comparison
A TF-IDF baseline is implemented for evaluation purposes.

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
- ✔ TF-IDF baseline completed
- ✔ Explainable recommendations added
- ✔ Evaluation framework completed

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
- Test API
```bash
http://127.0.0.1:8000/docs
```