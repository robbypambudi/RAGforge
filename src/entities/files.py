
import datetime
from sqlalchemy import Column, DateTime, Integer, String
from . import Base

class Files(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    path = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    metadatas = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return f"<Files(name={self.name}, path={self.path}, description={self.description})>"