# embeddings.py

import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
import voyageai
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

# Load environment variables
load_dotenv()  # This loads the VOYAGE_API_KEY from .env

# Task description for the transformer model
task_name_to_instruct = {
    "default": "Given a question, retrieve passages that answer the question"
}


class EmbeddingFramework:
    def __init__(self, framework, model="voyage-3"):
        self.framework = framework
        self.model = model
        if self.framework == "transformer":
            # Initialize the transformer model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model)
            self.transformer_model = AutoModel.from_pretrained(model, trust_remote_code=True)

    def embed(self, texts, input_type="document"):
        if self.framework == "voyageai":
            # VoyageAI embedding logic
            client = voyageai.Client()  # Initialize client using VOYAGE_API_KEY
            result = client.embed(texts, model=self.model, input_type=input_type)
            return np.vstack(result.embeddings)

        elif self.framework == "transformer":
            # Transformer embedding logic with instruction-based queries
            instruction = "Instruct: " + task_name_to_instruct.get("default", "") + "\nQuery: "
            embeddings = self._get_transformer_embeddings(texts, instruction)
            return embeddings

        else:
            raise ValueError("Unsupported embedding framework.")

    def _get_transformer_embeddings(self, texts, instruction, max_length=32768):
        # Add prefix instruction to each text
        inputs = [instruction + text for text in texts]
        # Get embeddings
        embeddings = self.transformer_model.encode(inputs, max_length=max_length)
        # Normalize embeddings
        normalized_embeddings = F.normalize(embeddings, p=2, dim=1)
        return normalized_embeddings.detach().numpy()


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
