import logging

from starlette.responses import JSONResponse

from src.lib.response_handler import ResponseHandler
from src.services.chroma.chroma_service import ChromaService
from src.services.embedding.embedding_service import EmbeddingService
from src.types.collection_request_type import CreateCollectionPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CollectionController(ResponseHandler):

    def __init__(self, chroma_service: ChromaService, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.chroma_service = chroma_service

    def create_collection(self, payload: CreateCollectionPayload) -> JSONResponse:
        """
        Create a new collection in ChromaDB.
        
        Args:
            payload: CreateCollectionPayload containing collection details
            
        Returns:
            dict: Response containing status and collection details
        """
        try:
            self.chroma_service.create_collection(payload.name)
            logger.info(f"Collection {payload.name} created successfully")
            return self.success(
                message=f"Collection {payload.name} created successfully",
                data={"collection_name": payload.name}
            )
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            return self.error(
                message=f"Failed to create collection: {str(e)}"
            )

    def get_collections(self) -> JSONResponse:
        """
        Get all collections in ChromaDB
        """
        try:
            results = self.chroma_service.get_all_collections()

            return self.success(
                message="Successfully retrieved collections",
                data=results
            )
        except Exception as e:
            logger.error(f"Error retrieving collections: {str(e)}")
            return self.error(
                message=f"Failed to retrieve collections: {str(e)}"
            )
