import uuid

from app.repositories.files_repository import FilesRepository
from app.schema.file_schema import CreateFileRequest
from app.services.base_service import BaseService


class FilesService(BaseService):
    """
    Files service class for handling file-related operations.
    """

    FILE_PATH = "/files"

    def __init__(self, files_repository: FilesRepository) -> None:
        self.files_repository = files_repository
        super().__init__(files_repository)

    def create(self, file: CreateFileRequest):
        """
        Create a new file.
        """
        # Generate random file name
        file.file_name = uuid.uuid4().hex + "." + file.file.content_type.split("/")[1]
        file.file_path = self.FILE_PATH + "/" + file.file_name
        file.file_type = file.file.content_type
        file.file_size = file.file.size
        return {
            "file_name": file.file_name,
            "file_path": file.file_path,
            "file_type": file.file_type,
            "file_size": file.file_size
        }
