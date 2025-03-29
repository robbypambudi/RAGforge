
from sqlalchemy import select
from src.entities.files import Files

from config.databases import DB

class FileRepository:
    
    def __init__ (self, db: DB):
        self.db = db
    
    def get_all_files(self):
        try:
            # Select all files from the database
            stmt = select(Files)
            result = self.db.session.execute(stmt).all()
            return result
        except Exception as e:
            print(e)
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
            print(e)
            return False