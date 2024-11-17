# embeddings.py

import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
import voyageai
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import time

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
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            # Initialize the transformer model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model)
            self.transformer_model = AutoModel.from_pretrained(model, trust_remote_code=True).to(self.device)


    def embed(self, texts, input_type="document"):
        if self.framework == "voyageai":
            # VoyageAI embedding logic with throttling
            client = voyageai.Client()  # Initialize client using VOYAGE_API_KEY
            embeddings = []
            ii = 0
            for text in texts:
                ii += 1
                print(ii)
                result = client.embed([text], model=self.model, input_type=input_type)
                embeddings.append(result.embeddings[0])
                time.sleep(20)  # Wait for 20 seconds between API calls to stay within rate limits
            return np.vstack(embeddings)


        elif self.framework == "transformer":
            # Transformer embedding logic with instruction-based queries
            instruction = "Instruct: " + task_name_to_instruct.get("default", "") + "\nQuery: "
            embeddings = self._get_transformer_embeddings(texts, instruction)
            return embeddings

        else:
            raise ValueError("Unsupported embedding framework.")

    def _get_transformer_embeddings(self, texts, instruction, max_length=32768, batch_size=16):
        embeddings_list = []
        num_texts = len(texts)
        for i in range(0, num_texts, batch_size):
            batch_texts = texts[i:i + batch_size]
            # Add prefix instruction to each text in the batch
            inputs = [instruction + text for text in batch_texts]
            # Tokenize the batch
            tokenized_inputs = self.tokenizer(inputs, return_tensors="pt", padding=True, truncation=True,
                                              max_length=max_length).to(self.device)
            # Get embeddings
            with torch.no_grad():
                model_output = self.transformer_model(**tokenized_inputs)
                embeddings = model_output.last_hidden_state.mean(dim=1)
            # Normalize embeddings
            normalized_embeddings = F.normalize(embeddings, p=2, dim=1)
            embeddings_list.append(normalized_embeddings.cpu().numpy())
        # Concatenate all embeddings
        return np.vstack(embeddings_list)


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
