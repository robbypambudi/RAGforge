from typing import List
from src.constants.http_method import Method
from src.controllers.collection_controller import CollectionController
from src.types.handler_request_type import HandlerRequestType


def collectionRoute(controller: CollectionController) -> List[HandlerRequestType]:
    return [
        HandlerRequestType(
            method=Method.POST.value,
            path='/collection',
            handler=controller.create_collection
        )
    ]
