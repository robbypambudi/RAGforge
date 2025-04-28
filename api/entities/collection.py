from sqlmodel import SQLModel, Field


class Collection(SQLModel):
    name: str = Field(max_length=512)
