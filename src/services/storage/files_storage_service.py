import os
from src.repositories.file_repository import FileRepository
from src.constants import DOCUMENT_PATH

class FileStorageService:
    file_repository: FileRepository
    
    def __init__(self, file_repository: FileRepository) -> None:
        self.file_repository = file_repository
        
    
    def get_all_files(self):
        raw_files = []
        try:
            files = self.file_repository.get_all_files()
            for file in files:
                raw_files.append({
                    "name": file[0].name,
                    "path": file[0].path,
                    "description": file[0].description,
                    "metadatas": file[0].metadatas
                })
            return raw_files
        except Exception as e:
            print(e)
    
    def save_file(self, name: str, path: str, description: str, metadatas: str) -> bool:
        try:
            return self.file_repository.save(name=name, path=path, description=description, metadatas=metadatas)
        except Exception as e:
            print(e)
            return False
    
    def save_file_to_local(self, file, dir_name: str, filename: str) -> str:
                
        os.makedirs(dir_name, exist_ok=True)

        # Save the file
        full_path = os.path.join(dir_name, filename)
        # Check if the file already exists
        if os.path.exists(full_path):
            raise ValueError(f"File {filename} already exists")

        return self.file_repository.save_file_to_local(file, full_path)
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists
        """
        return os.path.exists(file_path)
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                raise ValueError(f"File {file_path} does not exist")
        except Exception as e:
            print(e)
            return False
        