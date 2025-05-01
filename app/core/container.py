from dependency_injector import containers, providers

from app.core.config import settings
from app.core.database import Database
from app.repositories import CollectionRepository
from app.services.collection_service import CollectionService
from rag.chroma.client import ChromaDBHttpClientService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.collections",
            "app.core.dependencies",
        ]
    )
    chromadb_client_service = providers.Singleton(ChromaDBHttpClientService)

    db = providers.Singleton(Database, db_url=str(settings.SQLALCHEMY_DATABASE_URI))

    collection_repository = providers.Factory(CollectionRepository, session_factory=db.provided.session)

    # Service layer
    collection_service = providers.Factory(CollectionService, collection_repository=collection_repository)
