from typing import List
from src.controllers.files_controller import FilesController
from src.constants.http_method import Method
from src.types.handler_request_type import HandlerRequestType


def filesRoute(controller: FilesController) -> List[HandlerRequestType]:
    return [
        HandlerRequestType(
            method=Method.GET.value,
            path="/files",
            handler=controller.get_files,
        ),
        HandlerRequestType(
            method=Method.POST.value,
            path="/files",
            handler=controller.upload_file,
        ),
        HandlerRequestType(
            method=Method.DELETE.value,
            path="/files/knowledge",
            handler=controller.delete_file_with_knowledge,
        ),
        HandlerRequestType(
            method=Method.GET.value,
            path="/files/knowledge",
            handler=controller.get_file_by_file_name,
        )
    ]
