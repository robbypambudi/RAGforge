from typing import List

from app.constants import Method

from app.controllers.collection_controller import CollectionController
from src.types.handler_request_type import HandlerRequestType


def collectionRoute(controller: CollectionController) -> List[HandlerRequestType]:
    return [
        HandlerRequestType(
            method=Method.POST.value,
            path='/collection',
            handler=controller.create_collection
        ),
        HandlerRequestType(
            method=Method.GET.value,
            path='/collection',
            handler=controller.get_collections
        ),
        HandlerRequestType(
            method=Method.DELETE.value,
            path='/collection',
            handler=controller.delete_collection
        )
    ]
