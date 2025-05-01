import os
from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.controllers.collection_controller import CollectionController
from app.controllers.files_controller import FilesController
from app.controllers.histories_controller import HistoriesController
from app.controllers.questions_controller import QuestionsController
from config.databases import DB
from src.models.EmbeddingModel import EmbeddingModel
from src.repositories.file_repository import FileRepository
from src.repositories.memorystore_repository import MemorystoreRepository
from src.routes import RoutesRegister
from src.routes.collection_route import collectionRoute
from src.routes.files_route import filesRoute
from src.routes.histories_route import historiesRoute
from src.routes.questions_route import questionsRoute
from src.services.api.questions_service import QuestionsService
from src.services.chroma.chroma_service import ChromaService
from src.services.embedding.embedding_service import EmbeddingService
from src.services.rag.chain_service import ChainService
from src.services.rag.memorystore_service import MemorystoreService
from src.services.storage.files_storage_service import FileStorageService


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
        )

        # Initialize the repository
        file_repository = FileRepository(db=self.db)
        memorystore_repository = MemorystoreRepository()

        # Initialize the services
        chroma_service = ChromaService(host="localhost", port=8000)
        file_storage_service = FileStorageService(file_repository=file_repository)
        embedding_service = EmbeddingService(embedding_model=embedding_model,
                                             file_storage_service=file_storage_service,
                                             chroma_service=chroma_service)
        memorystore_service = MemorystoreService(memorystore_repository=memorystore_repository)
        chain_service = ChainService(file_storage_service=file_storage_service,
                                     chroma_service=chroma_service,
                                     embedding_service=embedding_service)
        questions_service = QuestionsService(memorystore_service=memorystore_service,
                                             chain_service=chain_service,
                                             chroma_service=chroma_service)

        # Controller
        files_controller = FilesController(
            file_storage_service=file_storage_service,
            embedding_service=embedding_service,
            memorystore_service=memorystore_service,
            chroma_service=chroma_service,
        )
        questions_controller = QuestionsController(
            chroma_service=chroma_service,
            chain_service=chain_service,
            memorystore_service=memorystore_service,
            questions_service=questions_service
        )
        histories_controller = HistoriesController(
            memorystore_service=memorystore_service,
        )
        collection_controller = CollectionController(
            chroma_service=chroma_service
        )

        # Routes
        routes = RoutesRegister(app=self.app)
        routes.register_routes(filesRoute(controller=files_controller))
        routes.register_routes(questionsRoute(controller=questions_controller))
        routes.register_routes(historiesRoute(controller=histories_controller))
        routes.register_routes(collectionRoute(controller=collection_controller))

        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(_request: Request, exc: RequestValidationError):
            errors = [
                {
                    "field": ".".join(map(str, err["loc"][1:])),  # skip 'body'
                    "message": err["msg"]
                }
                for err in exc.errors()
            ]
            return JSONResponse(
                status_code=422,
                content={"errors": errors}
            )

    def run(self):
        self.configure()
        uvicorn.run(self.app, host="0.0.0.0", port=8080)
