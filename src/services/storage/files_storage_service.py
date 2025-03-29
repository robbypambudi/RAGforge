import os
import aiofiles
from src.repositories.file_repository import FileRepository
from src.constants import DOCUMENT_PATH

class FileStorageService:
    file_repository: FileRepository
    
    def __init__(self, file_repository: FileRepository) -> None:
        self.file_repository = file_repository
        
    
    def get_all_files(self):
        return self.file_repository.get_all_files()
    
    def save_file(self, name: str, path: str, description: str, metadatas: str) -> bool:
        try:
            return self.file_repository.save(name=name, path=path, description=description, metadatas=metadatas)
        except Exception as e:
            print(e)
            return False
        
        
        