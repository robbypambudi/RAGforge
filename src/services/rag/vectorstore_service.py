from typing import List
from langchain_community.vectorstores import FAISS
import os
import logging

import torch

from models import EmbeddingModel
from src.services.storage.files_storage_service import FileStorageService
from src.constants import BASE_KNOWLEDGE_DOCUMENT_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorstoreService:

    def __init__(self, embedding_model: EmbeddingModel, file_storage_service: FileStorageService, top_k: int=8):
        self._embedding_model = embedding_model,
        self._file_storage_service = file_storage_service,
        self._top_k = top_k
        self.use_gpu = self._check_gpu_availability()

        
        self._vector_store = self._load_vector_store()
        
    def _load_vector_store(self) -> FAISS:
        # Check is BASE_KNOWLEDGE_DOCUMENT_PATH exists
        if not BASE_KNOWLEDGE_DOCUMENT_PATH:
            raise ValueError("BASE_KNOWLEDGE_DOCUMENT_PATH is not set")
        
        embedding_path = f"{BASE_KNOWLEDGE_DOCUMENT_PATH}/embedding"
        
        return FAISS.load_local(folder_path=embedding_path, embeddings=self._embedding_model, allow_dangerous_deserialization=True)
        
    def _check_gpu_availability(self) -> bool:
        """Check if FAISS can run on GPU."""
        has_cuda = torch.cuda.is_available()
        if has_cuda:
            logging.info("GPU detected! Running FAISS on GPU.")
        else:
            logging.warning("No GPU detected. Falling back to CPU FAISS.")
        return has_cuda
    
    def _convert_to_gpu(self, vector_store: FAISS) -> FAISS:
        """Convert FAISS index to GPU if a GPU is available."""
        try:
            index = self._vector_store.index
            res = FAISS.StandardGpuResources()  # Create GPU resource manager
            gpu_index = FAISS.index_cpu_to_gpu(res, 0, index)
            vector_store.index = gpu_index
            logging.info("Successfully converted FAISS index to GPU.")
        except Exception as e:
            logging.error("Failed to convert FAISS to GPU. Falling back to CPU. Error: %s", e)
            self.use_gpu = False  # Fall back to CPU
        return vector_store

    def get_retriever(self):
        if not self._vector_store:
            raise ValueError("Vector store not loaded")
        return self._vector_store.as_retriever(search_kwargs={"top_k": self._top_k})
    
    def get_vector_store(self):
        if not self._vector_store:
            raise ValueError("Vector store not loaded")
        
        return self._vector_store
    
    def load_all_local_embeddings(self):
        files = self._file_storage_service.get_all_files()