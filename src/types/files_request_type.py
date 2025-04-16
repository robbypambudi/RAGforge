from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional, List


class DeleteFileRequestType(BaseModel):
    file_id: int
    file_name: str

class GetFileRequestType(BaseModel):
    file_name: str
    
class UploadFileForm(BaseModel):
    description: str
    collection_name: str
    file: UploadFile