import os
import aiofiles
from src.repositories.file_repository import FileRepository
from src.constants import DOCUMENT_PATH

class FileStorageService:
    _file_repository: FileRepository
    
    def __init__(self, file_repository: FileRepository) -> None:
        self._file_repository = file_repository
        
    async def get_files(self):
        return await self._file_repository.get_files()
        
        