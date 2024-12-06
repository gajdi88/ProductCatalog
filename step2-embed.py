from embeddings import EmbeddingFramework, load_data, save_data, add_embeddings_to_df
from utils import concatenate_columns

# Define paths and initialize embedding framework
input_csv_path = 'emerson_products_97p_nodup.csv'  # Replace with your CSV file path
output_csv_path = 'emerson_products_97p_ANLP_noquery_ST.csv'  # Replace as needed
# embedding_framework = EmbeddingFramework(framework="voyageai", model="voyage-3")
# embedding_framework = EmbeddingFramework(framework="transformer", model="nvidia/NV-Embed-v2")
# embedding_framework = EmbeddingFramework(framework="transformer", model="Alibaba-NLP/gte-large-en-v1.5")
embedding_framework = EmbeddingFramework(framework="sentence-transformer", model="Alibaba-NLP/gte-large-en-v1.5")


# Load data
df = load_data(input_csv_path)
# data_array = df['Description'].astype(str).tolist()
data_array = concatenate_columns(df)

# Get embeddings
embeddings = embedding_framework.embed(data_array,query=False)

# Add embeddings to DataFrame
df = add_embeddings_to_df(df, embeddings)

# Save the DataFrame
save_data(df, output_csv_path)