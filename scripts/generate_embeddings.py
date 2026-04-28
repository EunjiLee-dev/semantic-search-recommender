from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# load data
df = pd.read_csv("data/processed/poi_clean.csv")
texts = df["text"].tolist()


# embedding
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=64
)


# save
np.save("data/embeddings/poi_embeddings.npy", embeddings)
np.save("data/embeddings/metadata.npy", df.to_dict("records"))