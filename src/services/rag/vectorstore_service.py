from typing import List
from langchain_community.vectorstores import FAISS
import os
import logging

import torch

from src.models import EmbeddingModel
from src.services.storage.files_storage_service import FileStorageService
from src.constants import BASE_KNOWLEDGE_DOCUMENT_PATH
from src.entities.files import Files

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorStoreService:

    def __init__(self, embedding_model: EmbeddingModel, file_storage_service: FileStorageService, top_k: int=8):
        self.embedding_model = embedding_model
        self.file_storage_service = file_storage_service
        self.top_k = top_k
        self.use_gpu = self._check_gpu_availability()
        self.vector_store = None
        
        self.load_all_local_embeddings()
        
    def _check_gpu_availability(self) -> bool:
        """Check if FAISS can run on GPU."""
        has_cuda = torch.cuda.is_available()
        if has_cuda:
            logging.info("GPU detected! Running FAISS on GPU.")
        else:
            logging.warning("No GPU detected. Falling back to CPU FAISS.")
        return has_cuda

    def get_retriever(self):
        if not self.vector_store:
            raise ValueError("Vector store not loaded")
        return self.vector_store.as_retriever(search_kwargs={"top_k": self.top_k})
    
    def get_vector_store(self):
        if not self.vector_store:
            raise ValueError("Vector store not loaded")
        
        return self.vector_store
    
    def add_vector_store(self, path: str)-> None:
        """Add a vector store to the existing vector store."""
        
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exist")
        if not os.path.isdir(path):
            raise ValueError(f"Path {path} is not a directory")
        
        # check is vector store is none or not
        if self.vector_store is None:
            self.vector_store = FAISS.load_local(folder_path=path, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
            logging.info(f"Vector store loaded from {path}")
            return
        else:
            vector_store = FAISS.load_local(folder_path=path, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
            self.vector_store.merge_from(vector_store)
            logging.info(f"Vector store merged from {path}")
            return
    
    def load_all_local_embeddings(self):
        logging.info("Loading all local embeddings...")
        files = self.file_storage_service.get_all_files()
        if not files:
            logging.info("No files found.")
            return
        
        for file in files:
            logging.info(f"Loading vector store from {file['path']}")
            self.add_vector_store(file['path'])
    
    def similarity_search(self, query: str, k: int = 8) -> List[Files]:
        """Perform a similarity search on the vector store."""
        if not self.vector_store:
            raise ValueError("Vector store not loaded")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results
    
    def get_chunks_by_filename(self, filename: str):
        vector_dict = self.vector_store.docstore._dict
        chunks_id = []
        
        for id in vector_dict.keys():
            if os.path.basename(vector_dict[id].metadata.get("source")) == filename:
                chunks_id.append(id)
                
        return chunks_id
    
    def delete_document_by_chunks(self, chunks: List[str]):
        self.vector_store.delete(chunks)