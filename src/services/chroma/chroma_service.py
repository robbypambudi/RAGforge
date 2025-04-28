import logging

import chromadb
from chromadb import Collection, QueryResult, GetResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaService:
    def __init__(self, host: str, port: int = 8000):
        self.client = chromadb.HttpClient(host=host, port=port)
        logger.info(f"ChromaDB client initialized with host {host} and port {port}.")

    @staticmethod
    def add_document(doc_id: str, embedding: list, metadata: dict, collection: Collection, document: str):
        collection.add(
            ids=[doc_id],
            documents=document,
            metadatas=[metadata]
        )

    @staticmethod
    def query_embeddings(query_embedding: list = None, n_results: int = 5,
                         collection: Collection = None) -> QueryResult:
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
        collections = [collection.name for collection in self.client.list_collections()]
        if collection_name not in collections:
            raise ValueError("Collection not found")

        return self.client.get_collection(collection_name)

    def create_collection(self, collection_name: str) -> Collection:
        collections = [collection.name for collection in self.client.list_collections()]
        if collection_name in collections:
            raise ValueError("Collection already exists")
        return self.client.create_collection(collection_name)

    def get_all_collections(self) -> list:
        collections = self.client.list_collections()

        return [collection.name for collection in collections]

    def delete_collection(self, collection_name: str):
        collections = [collection.name for collection in self.client.list_collections()]
        if collection_name not in collections:
            raise ValueError("Collection not found")
        self.client.delete_collection(collection_name)
        logger.info(f"Collection {collection_name} deleted successfully.")
