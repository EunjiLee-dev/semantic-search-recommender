import pandas as pd
import re
import ast

# load data
df = pd.read_json("data/raw/yelp_academic_dataset_business.json", lines=True)


# filter 
df = df[df["is_open"] == 1]

df = df[
    [
        "business_id",
        "name",
        "categories",
        "city",
        "state",
        "latitude",
        "longitude",
        "stars",
        "review_count",
        "attributes"
    ]
]

df = df.dropna(subset=["name", "categories"])


# extract price_level
def parse_attributes(attr):
    if pd.isna(attr):
        return {}
    if isinstance(attr, dict):
        return attr
    
    try:
        return ast.literal_eval(attr)
    except:
        return {}

df["attributes_parsed"] = df["attributes"].apply(parse_attributes)

df["price_level"] = df["attributes_parsed"].apply(
    lambda x: x.get("RestaurantsPriceRange2")
)
df["price_level"] = pd.to_numeric(df["price_level"], errors="coerce")


# make text
df["text"] = (
    df["name"].fillna("") + " " +
    df["categories"].fillna("") + " " 
)


# normalization
def normalize_text(text):
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text

df["text"] = df["text"].apply(normalize_text)


# save
df.to_csv("data/processed/poi_clean.csv", index=False)
print("preprocessing done: ", len(df))