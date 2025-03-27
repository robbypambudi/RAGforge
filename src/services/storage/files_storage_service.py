import os
import aiofiles
from src.repositories.file_repository import FileRepository
from src.constants import DOCUMENT_PATH

class FileStorageService:
    file_repository: FileRepository
    
    def __init__(self, file_repository: FileRepository) -> None:
        self.file_repository = file_repository
        
    def get_files(self):
        return self.file_repository.get_files()
    
    def get_all_files(self):
        return self.file_repository.get_all_files()
    
        
        