

from typing import List
from src.controllers.questions_controller import QuestionsController
from src.constants.http_method import Method
from src.types.handler_request_type import HandlerRequestType

def questionsRoute(controller: QuestionsController) -> List[HandlerRequestType]:
  return [
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions",
      handler=controller.ask_with_stream,
    ),
    HandlerRequestType(
      method=Method.POST.value,
      path="/questions/no-stream",
      handler=controller.ask_without_stream,
    )
  ]