from rag.llm.embedding_model import DefaultEmbedding


class EmbeddingModelFactory:
    """
    A factory class for creating embedding models.
    """
    _models = {
        "LingAI": DefaultEmbedding
    }

    @classmethod
    def get_embedding_model(cls, model_name: str):
        """
        Get the embedding model class based on the model name.
        """
        if model_name not in cls._models:
            raise ValueError(f"Model '{model_name}' is not supported.")

        return cls._models[model_name]
