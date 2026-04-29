CHEAP_WORDS = ["cheap", "affordable", "low cost"]
EXPENSIVE_WORDS = ["expensive", "high-end", "luxury"]
NEGATIONS = ["not", "no"]

def contains_negation(query, word):
    return f"not {word}" in query or f"no {word}" in query


def price_score(query, price_level):
    if price_level is None:
        return 0.5 # default
    
    query = query.lower()
    
    for word in EXPENSIVE_WORDS:
        if contains_negation(query, word):
            return 1.0 if price_level <= 2 else 0.0
        
    for word in CHEAP_WORDS:
        if contains_negation(query, word):
            return 1.0 if price_level >= 3 else 0.0
        
    for word in CHEAP_WORDS:
        if word in query:
            return 1.0 if price_level <= 2 else 0.0
        
    for word in EXPENSIVE_WORDS:
        if word in query:
            return 1.0 if price_level >= 3 else 0.0
        
    return 0.5