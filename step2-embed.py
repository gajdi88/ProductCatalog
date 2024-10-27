import voyageai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import json

load_dotenv() #load VOYAGE_API_KEY environment variable

vo = voyageai.Client() # use VOYAGE_API_KEY for authentication

input_csv_path = 'emerson_products.csv'  # Replace with your CSV file path
output_csv_path = 'original_dataset_with_embeddings.csv'  # Replace as needed

# Read the CSV file
df = pd.read_csv(input_csv_path)

# Check if 'Description' column exists
if 'Description' not in df.columns:
    raise ValueError("The CSV does not contain a 'Description' column.")


description_array = df['Description'].astype(str).tolist()

result = vo.embed(description_array, model="voyage-3", input_type="document")
print(result.embeddings)

embeddings = np.vstack(result.embeddings)

df['Embeddings'] = [json.dumps(embedding.tolist()) for embedding in embeddings]
df.to_csv(output_csv_path, index=False)