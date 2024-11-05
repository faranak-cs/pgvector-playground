import ollama

# dimension = 1024
def get_embeddings(prompt):
    embedding = ollama.embeddings(model='mxbai-embed-large', prompt=(prompt))['embedding']
    return embedding