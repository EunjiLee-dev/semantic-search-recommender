import pandas as pd

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
).str.lower()

# save
df.to_csv("data/processed/poi_clean.csv", index=False)
print("preprocessing done: ", len(df))