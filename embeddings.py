# embeddings.py

import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
import voyageai

# Load environment variables
load_dotenv()  # This loads the VOYAGE_API_KEY from .env

class EmbeddingFramework:
    def __init__(self, framework, model="voyage-3"):
        self.framework = framework
        self.model = model

    def embed(self, texts, input_type="document"):
        if self.framework == "voyageai":
            client = voyageai.Client()  # Initialize client using VOYAGE_API_KEY
            result = client.embed(texts, model=self.model, input_type=input_type)
            return np.vstack(result.embeddings)
        elif self.framework == "other_framework":
            # Placeholder for other embedding logic
            pass
        else:
            raise ValueError("Unsupported embedding framework.")

def load_data(input_csv_path):
    df = pd.read_csv(input_csv_path)
    if 'Description' not in df.columns:
        raise ValueError("The CSV does not contain a 'Description' column.")
    return df

def save_data(df, output_csv_path):
    df.to_csv(output_csv_path, index=False)

def add_embeddings_to_df(df, embeddings):
    df['Embeddings'] = [json.dumps(embedding.tolist()) for embedding in embeddings]
    return df