from pydantic import BaseModel, Field


class CreateCollectionPayload(BaseModel):
    name: str = Field(..., description="Name for collection")
    description: str = Field(..., description='Description for collection')
