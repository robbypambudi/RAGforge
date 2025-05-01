from sqlalchemy import Column, String, Text

from app.models import BaseModel


class Collection(BaseModel, table=True):
    __tablename__ = 'collections'
    collection_name: str = Column(String(255), nullable=False, unique=True)
    description: str = Column(Text, nullable=True)

    def normalize(self):
        self.collection_name = self.collection_name.lower()
