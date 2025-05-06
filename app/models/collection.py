from sqlmodel import String, Text, Field

from app.models import BaseModel


class Collection(BaseModel, table=True):
    __tablename__ = 'collections'
    collection_name: str = Field(sa_type=String, nullable=True, unique=True)
    description: str = Field(sa_type=Text, nullable=True)

    def normalize(self):
        self.collection_name = self.collection_name.lower()
