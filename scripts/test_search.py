import numpy as np

metadata = np.load("data/embeddings/metadata.npy", allow_pickle=True)

print(metadata[0].keys())