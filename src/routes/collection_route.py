from typing import List

from api.constants import Method
from api.controllers.collection_controller import CollectionController
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
