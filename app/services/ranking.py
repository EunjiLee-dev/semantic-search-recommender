import numpy as np
import re

CHEAP_WORDS = ["cheap", "affordable", "low cost", "inexpensive", "not expensive"]
EXPENSIVE_WORDS = ["expensive", "high end", "luxury", "fine dining", "premium"]


# intent parser
def parse_query_intent(query):
    query = re.sub(r"[^a-z0-9\s]", " ", query.lower())

    return {
        "cheap": any(word in query for word in CHEAP_WORDS),
        "expensive": any(word in query for word in EXPENSIVE_WORDS)
    }

# price
def price_score(query, price_level):
    if price_level is None:
        return 0.5 # default
    
    query = query.lower()

    has_cheap = any(word in query for word in CHEAP_WORDS)
    has_expensive = any(word in query for word in EXPENSIVE_WORDS)
    
    if not has_cheap and not has_expensive:
        return 0.5
    
    if has_cheap:
        return 1.0 if price_level <= 2 else 0.0
    
    if has_expensive:
        return 1.0 if price_level >=3 else 0.0
     
    return 0.5


# distance
def distance_score(user_lat, user_lon, place_lat, place_lon):
    if None in [user_lat, user_lon, place_lat, place_lon]:
        return 0.5
    
    dist = np.sqrt((user_lat - place_lat)**2 + (user_lon - place_lon)**2)

    return 1 / (1 + dist) # closer = higher score 


# final score
def final_score(semantic, price, distance, has_intent):
    if not has_intent:
        return 0.8 * semantic + 0.2 * distance
    
    return (
        0.6 * semantic +
        0.2 * price +
        0.2 * distance
    )
