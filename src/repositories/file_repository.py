
from src.entities.files import Files


class FileRepository:
    
    def __init__ (self, db):
        self.db = db
        
    def get_files(self):
        return self.db.query(Files).all()
    
    def get_all_files(self):
        return self.db.query(Files).all()