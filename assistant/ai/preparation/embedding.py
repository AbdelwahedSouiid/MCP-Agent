import pandas as pd
from ai.utils.model_loader import ModelLoader

class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = ModelLoader.get_model(model_name)
    
    def generate(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        df["embedding"] = df[text_column].apply(self.model.encode)
        return df
