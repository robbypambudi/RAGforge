from config.databases import DB
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_huggingface import HuggingFaceEmbeddings
from src.repositories.file_repository import FileRepository
from src.services.embedding.EmbeddingModel import EmbeddingModel
from src.services.storage.files_storage_service import FileStorageService
from src.constants import EMBED_MODEL_NAME

class App:
    def __init__(self):
        self.app = FastAPI()
        self.db = DB()
        
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
        self.db.connect()
        
        # Initialize the repository
        file_repository = FileRepository(file_path='documents/')
        
        # Intialize the services
        file_storage_service = FileStorageService(file_repository=file_repository)
        
        # Repository
        # file db repository 
        
        embedding_model = EmbeddingModel(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'padding': True, 'max_length': 512}
        )()
        
        
        
        
    def run(self):
        self.configure()
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
        
        