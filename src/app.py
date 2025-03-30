from config.databases import DB
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEmbeddings
from src.services.rag.chain_service import ChainService
from src.services.chroma.chroma_service import ChromaService
from src.services.rag.vectorstore_service import VectorStoreService
from src.repositories.file_repository import FileRepository
from src.models.EmbeddingModel import EmbeddingModel
from src.services.storage.files_storage_service import FileStorageService
from src.services.rag.memorystore_service import MemorystoreService

from src.services.embedding.embedding_service import EmbeddingService
class App:
    def __init__(self):
        self.app = FastAPI()
        self.db = DB(
            type=os.getenv("DB_TYPE"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        
        
    def __middleware__(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def configure(self):
        self.__middleware__()
        
        embedding_model = EmbeddingModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'padding': True, 'max_length': 512}
        )()
        
        # Initialize the repository
        file_repository = FileRepository(db=self.db)
        
        # Intialize the services
        # chroma_service = ChromaService(host="localhost", port=8000, collection_name="my_collection")
        file_storage_service = FileStorageService(file_repository=file_repository)
        embedding_service = EmbeddingService(embedding_model=embedding_model, file_storage_service=file_storage_service)

        vectorstore_service = VectorStoreService(embedding_model=embedding_model, file_storage_service=file_storage_service, top_k=8)
        chain_service = ChainService(file_storage_service=file_storage_service, vectorstore_service=vectorstore_service)
        memorystore_service = MemorystoreService()
        
        # Routes 
        
    def run(self):
        self.configure()
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
        
        