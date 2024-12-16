import faiss
import numpy as np
import os
import pickle
from config import Config

class VectorStore:
    def __init__(self, db_path=Config.VECTOR_DB_PATH):
        self.db_path = db_path
        self.index = None
        self.embeddings = None
        self.metadata = None

    def save_index(self, index, embeddings, metadata):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Save the FAISS index, embeddings, and metadata
        faiss.write_index(index, self.db_path)
        with open(self.db_path + '.pkl', 'wb') as f:
            pickle.dump({'embeddings': embeddings, 'metadata': metadata}, f)

    def load_index(self):
        if os.path.exists(self.db_path):
            # Load the FAISS index and embeddings
            self.index = faiss.read_index(self.db_path)
            with open(self.db_path + '.pkl', 'rb') as f:
                data = pickle.load(f)
                self.embeddings = data['embeddings']
                self.metadata = data['metadata']
        else:
            print(f"Index file at {self.db_path} does not exist. Creating a new one.")
            self.index = None  # Or create a new index here if required
            self.embeddings = np.array([])  # Initialize as empty
            self.metadata = []  # Initialize as empty

        return self.index, self.embeddings, self.metadata

    def insert_documents(self, embeddings, metadata):
        if self.index is None:
            # Initialize index if it doesn't exist
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.embeddings = embeddings
            self.metadata = metadata
        else:
            # Ensure the index is of the same dimensionality
            if embeddings.shape[1] != self.embeddings.shape[1]:
                raise ValueError("Dimensionality of the new embeddings does not match the existing index.")

            # Add new embeddings to the index
            self.index.add(embeddings)
            self.embeddings = np.vstack((self.embeddings, embeddings))
            self.metadata.extend(metadata)

        return self.index, self.embeddings, self.metadata
