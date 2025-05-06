from typing import List

import numpy as np
from chromadb import Documents, EmbeddingFunction
from loguru import logger
from sentence_transformers import SentenceTransformer


class DefaultEmbedding(EmbeddingFunction):
    def __init__(self, device: str = 'cpu'):
        # Initialize the SentenceTransformer model
        logger.info('Initializing default embedding model')
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)

    def __call__(self, input: Documents) -> np.ndarray:
        # Encode a single text into a vector
        vector = self.encode(input)
        return vector

    def encode(self, text: str) -> np.ndarray:
        # Encode a single text into a vector
        vector = self.model.encode(text, convert_to_numpy=True)
        return vector

    def encode_queries(self, texts: List[str]) -> np.ndarray:
        # Encode multiple texts into a 2D array of vectors
        vectors = self.model.encode(texts, convert_to_numpy=True)
        return vectors
