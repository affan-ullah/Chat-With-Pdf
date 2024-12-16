from src.vector_store import VectorStore
from src.embedding_service import EmbeddingService
from config import Config

class QueryEngine:
    def __init__(self, embedding_service, vector_store):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def semantic_search(self, query):
        """
        Perform similarity search in the vector database and return the most relevant chunks.
        """
        query_embedding = self.embedding_service.create_embeddings([query])  # Convert query to embedding

        # Perform similarity search in the vector database
        index, embeddings, metadata = self.vector_store.load_index()
        D, I = index.search(query_embedding, k=5)  # Get the top 5 similar chunks

        # Retrieve and return the metadata of the top results
        results = [metadata[i] for i in I[0]]
        return results
