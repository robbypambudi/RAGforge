import os
from fastapi import File
from sqlalchemy import select
from src.entities.files import Files

from config.databases import DB

class FileRepository:
    
    def __init__ (self, db: DB):
        self.db = db
    
    def get_all_files(self) -> list:
        try:
            # Select all files from the database
            stmt = select(Files)
            result = self.db.session.execute(stmt).all()
            return result
        except Exception as e:
            return []
        
    
    def save(self, name: str, path: str, description: str, metadatas: str) -> bool:
        try:
            new_file = Files(
                name=name,
                path=path,
                description=description,
                metadatas=metadatas
            )
            self.db.transaction(
                lambda: self.db.session.add(new_file)
            )
            return True
        except Exception as e:
            return False
    
    def save_file_to_local(self, file, full_path) -> str:
    
        if os.path.exists(full_path):
            raise ValueError(f"Path {full_path} already exists")
        
        # Save the file
        with open(full_path, "wb") as f:
            f.write(file.file.read())
            
        # Close the file
        return full_path

    def get_file_by_id(self, file_id: str) -> Files:
        """
        Get a file by its ID
        """
        try:
            stmt = select(Files).where(Files.id == file_id)
            result = self.db.session.execute(stmt).scalar_one_or_none()
            return result
        except Exception as e:
            return None
        
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
            return False
    
    def get_file_by_file_name(self, file_name: str) -> Files:
        """
        Get a file by its name
        """
        try:
            stmt = select(Files).where(Files.name == file_name)
            result = self.db.session.execute(stmt).scalar_one_or_none()
            return result
        except Exception as e:
            return None
        
            
        