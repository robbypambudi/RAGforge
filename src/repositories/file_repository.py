
from sqlalchemy import select
from src.entities.files import Files

from config.databases import DB

class FileRepository:
    
    def __init__ (self, db: DB):
        self.db = db
    
    def get_all_files(self):
        return self.db.query(select(Files))