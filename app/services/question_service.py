from rag.chroma.client import ChromaDBHttpClient


class QuestionService:
    """
    Question service class for handling question-related operations.
    """

    def __init__(self, chromadb_client: ChromaDBHttpClient) -> None:
        self.chromadb_client = chromadb_client
