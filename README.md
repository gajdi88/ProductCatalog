# Product Catalog

This is to scrape a product website, and catalog products for them to be queriable via a chatbot.

## Step 1: Scrape products from emerson.com
Use BeautifulSoup to extract Title, Description, Specs and Features of each product (approx 20k products)
Results in an XLS file with all product details

![image](https://github.com/user-attachments/assets/83e7f044-b9f1-426d-bdce-cc341888fca5)



## Step 2: Use a sentence transformer to embed product names and descriptions
Use HuggingFace's Transformer or SentenceTransformer library to load a model to embed scraped details.
The results get written back into an excel file.


## Step 3: query the vector embeddings - ie find products that match the user's quesitons
Currently, just a simple embedding of the query, and a Knn search for the target embedding.
Retrieval works as expected at this stage - semantic similarities our found.

Disadvantage of the simplicity - for example, if searching for a pressure sensor, the retrieval tends to find devices where pressure is mentioned a lot in the description. The result might be e.g. High-pressure rated flow sensor with a maximum pressure rating of 200 bar (2900 PSI).

------

## Improvement ideas
### RAG-fusion
- You are a helpful assistant that generates multiple search queries based on a single input query. \n Generate multiple search questions related to {question} \n Output (4 queries): “”"
- Whichever doc gets mentioned multiple times, their scores of having been found get added up
Reference paper: [RAG-Fusion: a New Take on Retrieval-Augmented Generation](https://arxiv.org/abs/2402.03367)

### Multi-query
- Re-phrase the question in a few different ways, retrieve multiple times, and then fuse the retrieval in some way
- You are an AI assistant. Your task is to generate five different versions of the given user question to retrieve relevant documents form a vector database. By generating multiple perspectives of the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide alternate questions separated by newlines. Original question: {orig}

### Sub-question
- Decompose problem into sub-problems, then solve sequentially. Plus, Interlieve retrieval with Chain of Thought

### Step-back question - few shot prompting
- You are an expert at world knowledge. Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. Here are a few examples:  Original Question: \<Original Question Example1\> Stepback Question: \<Stepback Question Example1\>

### HyDE - hypothetical answer
- write a hypothetical answer to a question and look up the embedding of the hypothetical answer for a match, rather than a question directly

### Indexing
- Optimise chunk size for embedding - semantic splitters
- Rather than just embedding, embed a summary of each product. Use summary embedding for the query matching - but use the raw document for the last generation step
- Hierarchical indexing (RAPTOR)
  - embed chunks, but then also cluster up chunks, summarise chunks, and embed clusters too
- Colbert - tokenise / chunk up docs as well as the queries. find max per query token.
- alternatives - retrieve, if not too relevant, try more complex retrieval routes
