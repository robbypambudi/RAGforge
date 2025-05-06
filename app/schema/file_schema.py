from typing import Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel

from app.schema.base_schema import FindBase


class BaseFile(BaseModel):
    file_name: str = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    collection_id: Optional[int] = None

    class Config:
        from_attributes = True


class FindFiles(FindBase, BaseFile): ...


class CreateFileRequest:
    def __init__(
            self,
            file_name: str = Form(...),
            file: UploadFile = File(...)
    ):
        self.file_name = file_name
        self.file = file
