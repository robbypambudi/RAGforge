import uuid

from pydantic import BaseModel

from app.schema.base_schema import FindBase
from app.utils.schema import AllOptional, as_form


class BaseCollection(BaseModel):
    collection_name: str
    description: str

    class Config:
        from_attributes = True


class FindCollection(FindBase, BaseCollection, metaclass=AllOptional): ...


class ListCollection(BaseCollection):
    id: uuid.UUID


@as_form
class CreateCollectionRequest(BaseCollection): ...
