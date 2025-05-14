from asyncpg import NotNullViolationError
from chromadb.errors import InvalidArgumentError

from app.core.exceptions import ValidationError
from app.repositories import CollectionsRepository
from app.schema.collection_schema import CreateCollectionRequest
from app.services.base_service import BaseService
from rag.chroma.client import ChromaDBHttpClient


class CollectionsService(BaseService):
    """
    Collection service class for handling collection-related operations.
    """

    def __init__(self, collections_repository: CollectionsRepository, chromadb_client: ChromaDBHttpClient,
                 embedding_model) -> None:
        self.collections_repository = collections_repository

        # Initialize the chromadb client service
        self.embedding_model = embedding_model
        self.chromadb_client = chromadb_client
        super().__init__(collections_repository)

    def create(self, payload: CreateCollectionRequest) -> CreateCollectionRequest:
        """
        Create a new collection with the given name. Creates ChromaDB collection and saves to repository.
        If ChromaDB creation fails, repository record is deleted.
        """

        collection = self.collections_repository.create(payload)
        try:
            # Create in repository first
            # Create ChromaDB collection
            # print("Embedding model:", self.embedding_model.get_embedding_model())
            self.chromadb_client.create_collection(
                collection_name=collection.collection_name,
                metadata={
                    "id": collection.id,
                    "description": collection.description,
                    "created_at": collection.created_at,
                },
                embedding_function=self.embedding_model,
            )

            return collection
        except InvalidArgumentError as e:
            # If ChromaDB creation fails, delete from repository
            self.collections_repository.delete_by_id(collection.id)
            raise ValidationError(detail=f"Collection name '{collection.collection_name}' is invalid. {str(e)}")
        except Exception as e:
            # If ChromaDB creation fails, delete from repository
            self.collections_repository.delete_by_id(collection.id)
            raise e

    def get_documents(self, collection_name: str) -> list:
        """
        Get documents from a collection in ChromaDB.
        """
        try:
            # Get documents from ChromaDB
            documents = self.chromadb_client.get_documents(
                collection_name=collection_name,
            )
            return documents

        except Exception as e:
            raise e

    def delete_collection(self, collection_name: str) -> None:
        """
        Delete a collection from ChromaDB and the repository.
        """
        try:
            collection = self.collections_repository.get_by_name(collection_name)

            # Get the collection ID from the repository
            # Delete from repository
            self.collections_repository.delete_by_id(collection.id)

            # Delete from ChromaDB
            self.chromadb_client.delete_collection(collection_name=collection_name)

        except InvalidArgumentError as e:
            raise ValidationError(detail=f"Collection name '{collection_name}' is invalid. {str(e)}")
        except NotNullViolationError as e:
            raise ValidationError(detail=f"Collection name '{collection_name}' is invalid. {str(e)}")
        except Exception as e:
            # If ChromaDB deletion fails, delete from repository
            raise e
