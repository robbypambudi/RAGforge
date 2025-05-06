from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.middleware import inject
from app.schema.file_schema import FindFiles, CreateFileRequest
from app.services.files_service import FilesService

router = APIRouter(prefix="/files", tags=["files"])


@router.get("", tags=["get"])
@inject
def index(
        query: FindFiles = Depends(),
        service: FilesService = Depends(Provide[Container.files_service])
):
    """
    Get all files
    """
    return service.get_list(query)


# Create a new file
@router.post("", tags=["post"])
@inject
def create(
        payload: CreateFileRequest = Depends(),
        service: FilesService = Depends(Provide[Container.files_service])
):
    """
    Create a new file
    """
    return service.create(payload)
