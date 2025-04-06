from config.databases import DB
import uvicorn
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

from langchain_huggingface import HuggingFaceEmbeddings
from src.models.EmbeddingModel import EmbeddingModel

from src.controllers.files_controller import FilesController
from src.controllers.questions_controller import QuestionsController
from src.controllers.histories_controller import HistoriesController

from src.repositories.file_repository import FileRepository
from src.repositories.memorystore_repository import MemorystoreRepository

from src.services.rag.memorystore_service import MemorystoreService
from src.services.rag.chain_service import ChainService
from src.services.chroma.chroma_service import ChromaService
from src.services.rag.vectorstore_service import VectorStoreService
from src.services.storage.files_storage_service import FileStorageService
from src.services.api.questions_service import QuestionsService

from src.services.embedding.embedding_service import EmbeddingService
from src.routes import RoutesRegister

from src.routes.files_route import filesRoute
from src.routes.questions_route import questionsRoute
from src.routes.histories_route import historiesRoute

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
        memorystore_repository = MemorystoreRepository()
        
        # Intialize the services
        # chroma_service = ChromaService(host="localhost", port=8000, collection_name="my_collection")
        file_storage_service = FileStorageService(file_repository=file_repository)
        embedding_service = EmbeddingService(embedding_model=embedding_model, file_storage_service=file_storage_service)
        memorystore_service = MemorystoreService(memorystore_repository=memorystore_repository)

        vectorstore_service = VectorStoreService(embedding_model=embedding_model, file_storage_service=file_storage_service, top_k=8)
        chain_service = ChainService(file_storage_service=file_storage_service, vectorstore_service=vectorstore_service)
        questions_service = QuestionsService(memorystore_service=memorystore_service, vectorstore_service=vectorstore_service, chain_service=chain_service)
        
        # Controller
        files_controller = FilesController(
            file_storage_service=file_storage_service,
            embedding_service=embedding_service,
            vectorstore_service=vectorstore_service,
        )
        questions_controller = QuestionsController(
            chain_service=chain_service,
            vectorstore_service=vectorstore_service,
            memorystore_service=memorystore_service,
            questions_service=questions_service
        )
        histories_controller = HistoriesController(
            memorystore_service=memorystore_service,
        )
        
        # Routes
        routes = RoutesRegister(app=self.app)
        routes.register_routes(filesRoute(controller=files_controller))
        routes.register_routes(questionsRoute(controller=questions_controller))
        routes.register_routes(historiesRoute(controller=histories_controller))

        # Custom 404 handler
        @self.app.exception_handler(StarletteHTTPException)
        async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
            if exc.status_code == 404:
                return JSONResponse(
                    status_code=404,
                    content={"detail": "This route does not exist.",
                             "status": "error"},
                )
            return await http_exception_handler(request, exc)
        
    def run(self):
        self.configure()
        uvicorn.run(self.app, host="0.0.0.0", port=8000)