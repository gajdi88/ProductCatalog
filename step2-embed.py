from embeddings import EmbeddingFramework, load_data, save_data, add_embeddings_to_df


# Define paths and initialize embedding framework
input_csv_path = 'emerson_products.csv'  # Replace with your CSV file path
output_csv_path = 'original_dataset_with_embeddings.csv'  # Replace as needed
#embedding_framework = EmbeddingFramework(framework="voyageai", model="voyage-3")
embedding_framework = EmbeddingFramework(framework="transformer", model="nvidia/NV-Embed-v2")


# Load data
df = load_data(input_csv_path)
description_array = df['Description'].astype(str).tolist()

# Get embeddings
embeddings = embedding_framework.embed(description_array)

# Add embeddings to DataFrame
df = add_embeddings_to_df(df, embeddings)

# Save the DataFrame
save_data(df, output_csv_path)