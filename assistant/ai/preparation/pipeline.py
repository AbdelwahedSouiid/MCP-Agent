import pandas as pd
import numpy as np
from .clean import clean_text

from .embedding import EmbeddingGenerator
from .indexing import FAISSIndexer
import faiss
import os

class RAGPipeline:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embedder = EmbeddingGenerator(model_name)
    
    def run_from_dataframe(self, df: pd.DataFrame, output_dir: str = "ai/data/embeddings"):
        # 2. Génération des embeddings
        df = self.embedder.generate(df)

        # 3. Indexation
        embeddings = np.vstack(df["embedding"].values)
        index = FAISSIndexer.create_index(embeddings)

        # 4. Sauvegarde
        os.makedirs(output_dir, exist_ok=True)
        df.to_pickle(f"{output_dir}/produits_embeddings.pkl")
        faiss.write_index(index, f"{output_dir}/produits_faiss.index")
        return df, index