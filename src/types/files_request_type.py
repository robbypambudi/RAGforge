from pydantic import BaseModel

class DeleteFileRequestType(BaseModel):
    file_id: int
    file_name: str
