from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
import json
from dotenv import load_dotenv
import voyageai

load_dotenv() #load VOYAGE_API_KEY environment variable
vo = voyageai.Client() # use VOYAGE_API_KEY for authentication

# Step 1: Load the CSV and deserialize embeddings
def load_data(csv_path):
    df = pd.read_csv(csv_path)

    # Deserialize embeddings
    df['Embeddings'] = df['Embeddings'].apply(lambda x: np.array(json.loads(x)))

    # Create embedding matrix
    embedding_matrix = np.vstack(df['Embeddings'].values)

    return df, embedding_matrix

# Step 2: Initialize and fit NearestNeighbors
def initialize_nn(embedding_matrix, n_neighbors=5, metric='cosine'):
    nn_model = NearestNeighbors(n_neighbors=n_neighbors, metric=metric)
    nn_model.fit(embedding_matrix)
    return nn_model

# Step 3: Embed the query
def embed_query(query):
    result = vo.embed(query, model="voyage-3", input_type="document")
    return result.embeddings


# Step 4: Retrieve nearest neighbors
def retrieve_nearest(query_embedding, nn_model, df, top_k=5):
    # query_embedding = query_embedding.reshape(1, -1)
    distances, indices = nn_model.kneighbors(query_embedding, n_neighbors=top_k)

    # For cosine similarity, similarity = 1 - distance
    similarities = 1 - distances.flatten()

    top_matches = df.iloc[indices.flatten()].copy()
    top_matches['Similarity'] = similarities

    return top_matches


# Step 5: Main function
def main():
    # Paths
    csv_path = 'emerson_products_with_embeddings.csv'  # Replace with your CSV path

    # Load data
    df, embedding_matrix = load_data(csv_path)

    # Initialize NearestNeighbors
    nn_model = initialize_nn(embedding_matrix, n_neighbors=5, metric='cosine')

    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        # Embed the query
        query_embedding = embed_query(query)

        # Retrieve top matches
        top_matches = retrieve_nearest(query_embedding, nn_model, df, top_k=10)

        # Display results
        print("\nTop Matches:")
        for idx, row in top_matches.iterrows():
            print(f"- Name: {row['Product Name']}")
            print(f"- Description: {row['Description']}")
            print(f"  Similarity: {row['Similarity']:.4f}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()