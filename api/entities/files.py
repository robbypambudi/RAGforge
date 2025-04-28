from sqlmodel import SQLModel, Field


class Files(SQLModel):
    name = EmailStr = Field(max_length=512)
    path = Field(max_length=512)
    description = Field(default=None)
    metadatas = Field(default=None)
