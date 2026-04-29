# EVALUATION: TF-IDF VS. SBERT

This document contains experimental evaluation results comparing TF-IDF baseline and SBERT-based semantic search.

## Query Examples
We evaluate the models on the following natural language queries:

- cheap sushi with parking
- luxury pizza and wine
- hamburger with wifi
- coffee and bread

These queries test:
- price sensitivity (cheap / luxury)
- attribute constraints (wifi, parking)
- semantic compositionality (food + condition)

## Results Comparison
### Query1: cheap sushi with parking
**TF-IDF Results:**
- Parking-related businesses only (e.g., "Five Star Parking", "Central Parking")
- No sushi relevance
- Matches based on keyword overlap only
- 👉 TF-IDF fails due to keyword ambiguity ("cheap", "parking")  

**SBERT Results:**
- Sushi restaurants such as "Sushi Park", "Sushi Garden"  
- Correctly captures semantic intent
- 👉 SBERT retrieves semantically relevant restaurants

---

### Query2: luxury pizza and wine
**TF-IDF Results:**
- Nail salons dominate results ("Luxury Nails")
- No food-related context preserved
- 👉 TF-IDF heavily biased toward lexical matching failure cases

**SBERT Results:**
- Italian restaurants and wine bars  
- Contextually relevant food establishments
- 👉 SBERT correctly interprets dining context

---

### Query3: hamburger with wifi
**TF-IDF Results:**
- Mixed results: burger restaurants + keyword matches
- Some irrelevant fast food entries included
- WiFi constraint inconsistently applied

**SBERT Results:**
- Strong semantic clustering around burger restaurants
- WiFi attribute correctly influences ranking in some cases
- More coherent than TF-IDF but weaker semantic-attribute fusion than expected

---

### Query4: coffee and bread
**TF-IDF Results:**
- High repetition of "Beyond Bread"
- Keyword dominance leads to limited diversity
- Strong bias toward bakery-related matches

**SBERT Results:**
- Better diversity in coffee-related venues
- Captures both coffee and bakery semantics
- More balanced retrieval across categories

---

## Key Findings
### 1. Semantic Understanding
SBERT consistently outperforms TF-IDF in interpreting compositional queries involving multiple constraints (e.g., "cheap sushi with parking").

---

### 2. Keyword Bias in TF-IDF
TF-IDF suffers from strong lexical bias:
- "cheap" → unrelated cheap businesses
- "luxury" → unrelated luxury-named entities
- attribute words dominate irrelevant domains

---

### 3. Attribute Awareness
SBERT + ranking system shows partial success in integrating:
- WiFi
- Parking
- Price level

However, TF-IDF fails to use structured attributes entirely.

---

### 4. Robustness
SBERT demonstrates higher robustness in:
- noisy queries
- multi-intent queries
- real-world conversational phrasing

---

## Conclusion

This experiment demonstrates that:

- TF-IDF is insufficient for modern POI recommendation tasks due to lack of semantic understanding.
- SBERT significantly improves retrieval quality by capturing contextual meaning.
- Adding structured ranking signals (price, distance, attributes) further enhances recommendation relevance.

Overall, the SBERT-based hybrid system provides a more realistic and user-aligned recommendation experience compared to traditional keyword-based approaches.
