import chromadb
import logging
from chromadb import Collection, QueryResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaService:
    def __init__(self, host: str, port: int = 8000):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collections = [] # Cache for collections
        self.current_collection_name = None
        logger.info(f"ChromaDB client initialized with host {host} and port {port}.")
        
    def use_collection(self, collection_name: str) -> None:
        """Use a specific collection in ChromaDB."""
        if collection_name not in self.client.list_collections():
            self.collections[collection_name] = self.client.create_collection(name=collection_name)
            logger.info(f"Created new collection {collection_name}.")
        else:
            logger.info(f"Using existing collection {collection_name}.")
        self.current_collection_name = collection_name
    
    def get_current_collection(self) -> Collection:
        """Get the current collection."""
        if self.current_collection_name is None:
            raise ValueError("No collection is currently selected.")
        return self.collections[self.current_collection_name]
    
    def add_document(self, doc_id: str, embedding: list, metadata: dict):
        collection = self.get_current_collection()
        
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[metadata]
        )
        logger.info(f"Document {doc_id} added to collection {self.current_collection_name}.")

    def query_embeddings(self, query_embedding: list, n_results: int = 5) -> QueryResult:
        collection = self.get_current_collection()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        logger.info(f"Query executed on collection {self.current_collection_name} with {n_results} results.")
        return results
    
    def get_all_documents(self) -> list:
        collection = self.get_current_collection()
        
        documents = collection.get()
        logger.info(f"Retrieved all documents from collection {self.current_collection_name}.")
        return documents
    
    def delete_document(self, doc_id: str):
        collection = self.get_current_collection()
        
        collection.delete(ids=[doc_id])
        logger.info(f"Document {doc_id} deleted from collection {self.current_collection_name}.")
    