from typing import List

from api.constants import Method
from api.controllers.questions_controller import QuestionsController
from src.types.handler_request_type import HandlerRequestType


def questionsRoute(controller: QuestionsController) -> List[HandlerRequestType]:
    return [
        HandlerRequestType(
            method=Method.POST.value,
            path="/questions/no-stream",
            handler=controller.ask_without_stream,
        ),
        HandlerRequestType(
            method=Method.POST.value,
            path="/questions/stream",
            handler=controller.ask_with_stream,
        )
    ]
