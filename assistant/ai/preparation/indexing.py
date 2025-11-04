import numpy as np
import faiss

class FAISSIndexer:
    @staticmethod
    def create_index(embeddings: np.ndarray) -> faiss.Index:
        """Crée un index FAISS L2."""
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype("float32"))
        return index