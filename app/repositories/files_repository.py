from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.files import Files
from app.repositories.base_repository import BaseRepository
from app.services.base_service import RepositoryProtocol


class FilesRepository(BaseRepository, RepositoryProtocol):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Files)
