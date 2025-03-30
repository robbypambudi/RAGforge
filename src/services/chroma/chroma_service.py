import chromadb
import logging

class ChromaService:
    def __init__(self, host: str, port: int = 8000, collection_name: str = 'its_collection'):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logging.info(f"ChromaDB client initialized with host {host} and port {port}.")
    
    def add_documents(self, doc_id: str, embedding: list, metadata: dict):
        """Add documents to the ChromaDB collection."""
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            metadatas=[metadata or {}]
        )
        logging.info(f"Document {doc_id} added to ChromaDB collection.")
    
    def query_embeddings(self, query_embedding: list, n_results: int = 5):
        """Query the ChromaDB collection with an embedding."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        logging.info(f"Query executed with {n_results} results.")
        return results
    
    def get_collection(self):
        """Get the ChromaDB collection."""
        return self.collection
    
    def get_all_documents(self):
        """Get all documents in the ChromaDB collection."""
        documents = self.collection.get()
        logging.info(f"Retrieved {len(documents)} documents from ChromaDB collection.")
        return documents
    
    def delete_document(self, doc_id: str):
        """Delete a document from the ChromaDB collection."""
        self.collection.delete(ids=[doc_id])
        logging.info(f"Document {doc_id} deleted from ChromaDB collection.")
    
    def clear_collection(self):
        """Clear the ChromaDB collection."""
        self.collection.clear()
        logging.info("ChromaDB collection cleared.")
        
    def close(self):
        """Close the ChromaDB client."""
        self.client.close()
        logging.info("ChromaDB client closed.")
        