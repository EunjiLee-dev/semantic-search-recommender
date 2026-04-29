import numpy as np
import re

CHEAP_WORDS = ["cheap", "affordable", "low cost", "inexpensive", "not expensive"]
EXPENSIVE_WORDS = ["expensive", "high end", "luxury", "fine dining", "premium"]


# hard filter
def apply_hard_filters(metadata, intent): 
    filtered_indices = []

    for i, item in enumerate(metadata):
        if intent.get("wifi") and not item.get("WiFi"):
            continue
        if intent.get("reservation") and not item.get("RestaurantsReservations"):
            continue
        if intent.get("parking") and not item.get("BusinessParking"):
            continue
        if intent.get("delivery") and not item.get("RestaurantsDelivery"):
            continue

        filtered_indices.append(i)
    
    return filtered_indices

# intent parser
def parse_query_intent(query):
    query = re.sub(r"[^a-z0-9\s]", " ", query.lower())

    return {
        "cheap": any(word in query for word in CHEAP_WORDS),
        "expensive": any(word in query for word in EXPENSIVE_WORDS),
        "wifi": "wifi" in query,
        "reservation": "reservation" in query or "book" in query,
        "parking": "parking" in query,
        "delivery": "delivery" in query or "takeout" in query
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


# explanation
def build_explanation(semantic, price, distance):
    reasons = []

    if semantic > 0.6:
        reasons.append("Strong semantic match")

    if price > 0.7:
        reasons.append("Matches price preference")

    if distance > 0.6:
        reasons.append("Close to your location")

    if not reasons:
        reasons.append("General match based on similarity")

    return reasons