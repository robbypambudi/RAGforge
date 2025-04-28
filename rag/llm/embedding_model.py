import threading
from abc import ABC

import torch


class Base(ABC):
    def __init__(self, key, model_name):
        pass

    def encode(self, texts: list):
        raise NotImplementedError("encode method not implemented in the base class")

    def encode_queries(self, queries: list):
        raise NotImplementedError("encode_queries method not implemented in the base class")

    def total_token_count(self, response) -> int:
        try:
            return response.usage.total_tokens
        except Exception:
            pass
        try:
            return response["usage"]["total_tokens"]
        except Exception:
            pass
        return 0


class DefaultEmbedding(Base):
    _model = None
    _model_name = None
    _model_lock = threading.Lock()

    def __init__(self, key, model_name):
        """
        Initialize the embedding model with the provided key and model name.
        """
        if not DefaultEmbedding._model or model_name != DefaultEmbedding._model_name:
            try:
                # Memuat model dan tokenizer dari HuggingFace
                from sentence_transformers import SentenceTransformer

                # Menggunakan model Linq-Embed-Mistral
                DefaultEmbedding._model_name = model_name
                DefaultEmbedding._model = SentenceTransformer("Linq-AI-Research/Linq-Embed-Mistral",
                                                              device='cuda' if torch.cuda.is_available() else 'cpu')

            except Exception as e:
                print(f"Error loading model: {e}")

        self._model = DefaultEmbedding._model
        self._model_name = DefaultEmbedding._model_name

    def encode(self, texts: list):
        """
        Encode a list of texts using the embedding model
        """
        with DefaultEmbedding._model_lock:
            return DefaultEmbedding._model.encode(texts, show_progress_bar=False, convert_to_tensor=True,
                                                  device='cuda' if torch.cuda.is_available() else 'cpu')

    def encode_queries(self, queries: list):
        """
        Encode a list of queries using the embedding model
        """
        with DefaultEmbedding._model_lock:
            return DefaultEmbedding._model.encode(queries, show_progress_bar=False, convert_to_tensor=True,
                                                  device='cuda' if torch.cuda.is_available() else 'cpu')
