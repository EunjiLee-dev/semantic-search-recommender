import pandas as pd
import re

# load data
df = pd.read_json("data/raw/yelp_academic_dataset_business.json", lines=True)


# filter 
df = df[df.get("is_open", 1) == 1]

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


# make text
df["text"] = (
    df["name"].fillna("") + " " +
    df["categories"].fillna("") + " " +
    df["city"].fillna("") + " " +
    df["state"].fillna("")
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