from chromadb.errors import InvalidArgumentError
from fastapi import Depends

from app.core.exceptions import ValidationError
from app.repositories import CollectionRepository
from app.schema.collection_schema import CreateCollectionRequest
from app.services.base_service import BaseService
from rag.chroma.client import ChromaDBHttpClientService
from rag.llm import EmbeddingModelFactory


class CollectionService(BaseService):
    """
    Collection service class for handling collection-related operations.
    """
    chromadb_client_service: ChromaDBHttpClientService = Depends()
    embedding_model: EmbeddingModelFactory.get_embedding_model("LingAI") = Depends(
        EmbeddingModelFactory.get_embedding_model("LingAI"))

    def __init__(self, collection_repository: CollectionRepository) -> None:
        self.collection_repository = collection_repository

        # Initialize the chromadb client service
        self.chromadb_client_service = ChromaDBHttpClientService()
        # self.embedding_model = EmbeddingModelFactory.get_embedding_model("LingAI")()
        #
        # # Check heartbeat of ChromaDB server
        # if not self.chromadb_client_service.heartbeat():
        #     raise Exception("ChromaDB server is not running or unreachable.")
        super().__init__(collection_repository)

    def create(self, payload: CreateCollectionRequest) -> CreateCollectionRequest:
        """
        Create a new collection with the given name. Creates ChromaDB collection and saves to repository.
        If ChromaDB creation fails, repository record is deleted.
        """

        collection = self.collection_repository.create(payload)
        try:
            # Create in repository first
            # print("Embedding model:", self.embedding_model.get_embedding_model())
            # Create ChromaDB collection
            self.chromadb_client_service.create_collection(
                collection_name=collection.collection_name,
                embedding_function=self.embedding_model.get_embedding_model(),
            )

            return collection
        except InvalidArgumentError as e:
            # If ChromaDB creation fails, delete from repository
            self.collection_repository.delete_by_id(collection.id)
            raise ValidationError(detail=f"Collection name '{collection.collection_name}' is invalid. {str(e)}")
        except Exception as e:
            # If ChromaDB creation fails, delete from repository
            self.collection_repository.delete_by_id(collection.id)
            raise e

    def get_documents(self, collection_name: str) -> list:
        """
        Get documents from a collection in ChromaDB.
        """
        try:
            # Get documents from ChromaDB
            documents = self.chromadb_client_service.get_documents(
                collection_name=collection_name,
            )
            return documents

        except Exception as e:
            raise e
