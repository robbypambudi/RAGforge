import chromadb
import logging
from chromadb import Collection, QueryResult, GetResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaService:
    def __init__(self, host: str, port: int = 8000):
        self.client = chromadb.HttpClient(host=host, port=port)
        logger.info(f"ChromaDB client initialized with host {host} and port {port}.")

    @staticmethod
    def add_document(self, doc_id: str, embedding: list, metadata: dict, collection: Collection):
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    @staticmethod
    def query_embeddings(self, query_embedding: list, n_results: int = 5, collection: Collection = None) -> QueryResult:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

    @staticmethod
    def get_all_documents(self, collection: Collection) -> GetResult:
        documents = collection.get()
        logger.info(f"Retrieved all documents from collection {collection.name}")
        return documents

    @staticmethod
    def delete_document(self, doc_id: str, collection: Collection):
        collection.delete(ids=[doc_id])
        logger.info(f"Document {doc_id} deleted from collection {collection.name}.")

    def get_collection(self, collection_name: str) -> Collection:
        if collection_name not in self.client.list_collections():
            raise ValueError("Collection not found")

        return self.client.get_collection(collection_name)
