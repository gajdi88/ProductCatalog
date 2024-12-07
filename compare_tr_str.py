from embeddings import EmbeddingFramework, load_data, save_data, add_embeddings_to_df

tref = EmbeddingFramework(framework="transformer", model="Alibaba-NLP/gte-large-en-v1.5")
stref = EmbeddingFramework(framework="sentence-transformer", model="Alibaba-NLP/gte-large-en-v1.5")

sentence =  "This is a test sentence."

tref_embeddings = tref.embed(sentence,query=False)
stref_embeddings = stref.embed(sentence,query=False)

print(tref_embeddings)

# normalise stref_embeddings
from sklearn.preprocessing import normalize
s_em = normalize(stref_embeddings, norm='l2', axis=1, copy=True, return_norm=False)