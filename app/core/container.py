from dependency_injector import containers, providers

from app.core.config import settings
from app.core.database import Database
from app.repositories import CollectionRepository
from app.services.collection_service import CollectionService
from rag.chroma.client import ChromaDBHttpClient
from rag.embedding.embedding_factory import EmbeddingFactory


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.collections",
            "app.core.dependencies",
        ]
    )
    embedding_factory = providers.Singleton(
        EmbeddingFactory,
    )
    embedding_model = providers.ThreadSafeSingleton(
        lambda factory: factory.get("Default"),
        embedding_factory,
    )
    chromadb_client = providers.Singleton(ChromaDBHttpClient, host='localhost', port=8000)
    db = providers.Singleton(Database, db_url=str(settings.SQLALCHEMY_DATABASE_URI))

    collection_repository = providers.Factory(CollectionRepository, session_factory=db.provided.session)

    # Service layer
    collection_service = providers.Factory(CollectionService, collection_repository=collection_repository,
                                           chromadb_client=chromadb_client, embedding_model=embedding_model)
