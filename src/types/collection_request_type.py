from pydantic import BaseModel, Field


class CreateCollectionPayload(BaseModel):
    name: str = Field(..., description="Name for collection")
    description: str = Field(..., description='Description for collection')


class DeleteCollectionPayload(BaseModel):
    """
    Payload for deleting a collection in ChromaDB.
    """
    name: str = Field(..., description="Name for collection")
