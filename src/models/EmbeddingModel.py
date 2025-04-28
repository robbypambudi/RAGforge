from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:

    def __init__(self, model_name, model_kwargs, encode_kwargs) -> None:
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.encode_kwargs = encode_kwargs
        self._model = None

        self._init_model()

    def get_model(self) -> HuggingFaceEmbeddings:
        if self._model is None:
            self._model = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=self.model_kwargs,
                encode_kwargs=self.encode_kwargs
            )
        return self._model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Embed documents using the embedding model
        """
        return self.get_model().embed_documents(texts)

    def embed_query(self, query):
        """
        Embed query using the embedding model
        """
        return self.get_model().embed_query(query)

    def _init_model(self):
        """
        Initialize the embedding model
        """
        self._model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs
        )
