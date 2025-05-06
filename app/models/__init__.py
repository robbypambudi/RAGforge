import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(sa_type=DateTime, default=func.now())
    updated_at: datetime = Field(sa_type=DateTime, default=func.now())
