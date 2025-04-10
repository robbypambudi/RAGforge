import os
from src.entities.files import Files
from src.repositories.file_repository import FileRepository

class FileStorageService:
    file_repository: FileRepository
    
    def __init__(self, file_repository: FileRepository) -> None:
        self.file_repository = file_repository
        
    def get_all_files(self):
        try:
            files = self.file_repository.get_all_files()
            return [
                {
                    "id": file[0].id,
                    "name": file[0].name,
                    "path": file[0].path,
                    "description": file[0].description,
                    "metadatas": file[0].metadatas
                }
                for file in files
            ]
        except Exception as e:
            print(e)
    
    def save_file(self, name: str, path: str, description: str, metadatas: str) -> bool:
        try:
            return self.file_repository.save(name=name, path=path, description=description, metadatas=metadatas)
        except Exception as e:
            print(e)
            return False
    
    def save_file_to_local(self, file, dir_name: str, filename: str) -> str:
        """
        Save a file to the local storage
        """
        # 
        os.makedirs(dir_name, exist_ok=True)

        # Save the file
        full_path = os.path.join(dir_name, filename)
        # Check if the file already exists
        if os.path.exists(full_path):
            raise ValueError(f"File {filename} already exists")

        return self.file_repository.save_file_to_local(file, full_path)
        
    def get_file_by_file_name(self, file_name: str):
        """
        Get a file by its name
        """
        try:
            file = self.file_repository.get_file_by_file_name(file_name)
            if not file:
                raise ValueError(f"File with name {file_name} does not exist")
            return file
        except Exception as e:
            print(e)
            return None
              
    def verify_file_by_id_name(self, file_id: str, file_name: str):
        """
        Verify a file by its ID and name
        """
        try:
            file = self.file_repository.get_file_by_id(file_id)
            if not file:
                raise ValueError(f"File with ID {file_id} does not exist")
            
            if file.name != file_name:
                raise ValueError(f"File with ID {file_id} does not match name {file_name}")
            
            return file
        except Exception as e:
            print(e)
            return None

    def delete_file(self, file: Files) -> bool:
        """
        Delete a file
        1. Delete from the database
        2. Delete from the local storage
        """
        try:
            # Delete from the database
            if not file:
                raise ValueError(f"File with ID {file.id} does not exist")
            
            if self.file_repository.delete_file(file):
                # Delete from the local storage
                self.file_repository.delete_local_file(file.path)
                return True
            else:
                raise ValueError(f"Failed to delete file with ID {file.id}")
                        
        except Exception as e:
            print(e)
            raise e 