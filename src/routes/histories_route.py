from typing import List
from src.controllers.histories_controller import HistoriesController
from src.constants.http_method import Method
from src.types.handler_request_type import HandlerRequestType

def historiesRoute(controller: HistoriesController):
  """
  Register route of histories
  """
  return [
    HandlerRequestType(
      method=Method.GET.value,
      path="/histories",
      handler=controller.get_all,
    ),
    HandlerRequestType(
      method=Method.GET.value,
      path="/histories/{chat_id}",
      handler=controller.get_memory_by_id,
    ),
  ]