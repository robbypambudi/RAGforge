import os
import logging

from src.lib.response_handler import ResponseHandler
from src.services.rag.chain_service import ChainService
from src.services.rag.vectorstore_service import VectorStoreService
from src.repositories.memorystore_repository import MemorystoreRepository
from src.types.question_request_type import PostQuestionStreamGeneratorType
from src.services.api.questions_service import QuestionsService
from sse_starlette.sse import EventSourceResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionsController(ResponseHandler):
  
  def __init__(self, chain_service: ChainService, vectorstore_service: VectorStoreService, memorystore_service: MemorystoreRepository, questions_service: QuestionsService):
    self.chain_service = chain_service
    self.vectorstore_service = vectorstore_service
    self.memorystore_service = memorystore_service
    self.questions_service = questions_service
    
  def ask_with_stream(self, question: str):
    """
    Ask a question to the chain service and return the answer.
    """
    self.memorystore_service.add_user_message(question.id, question.question)
    
    try:
      # Call the chain service with the question
      self.memorystore_service.add_user_message(question.id, question.question)
      
      # Call the chain service with the question
      return EventSourceResponse(
        self.chain_service.ask_with_stream(question.question),
        media_type="text/event-stream",
      )
    except Exception as e:
      logger.error(f"Error in ask_with_stream: {e}")
      return self.error(message="An error occurred while processing your request.", status_code=500)
    
  def ask_without_stream(self, payload: PostQuestionStreamGeneratorType):
    """
    Ask a question to the chain service and return the answer.
    """    
    
    try:
      self.memorystore_service.add_user_message(payload.id, payload.question)
      memorystore = self.memorystore_service.get_memory_by_chat_id(payload.id)
      context = self.chain_service.get_context(payload.question, memorystore)
      print(f"Context: {context}")
      answer = self.chain_service.get_chain(is_stream=False, is_output_html=False).invoke(context)
      print(f"Answer: {answer}")
      self.memorystore_service.add_ai_message(payload.id, answer)
      
      return self.success(data=answer, status_code=200)
    except Exception as e:
      logger.error(f"Error in ask_without_stream: {e}")
      return self.error(message="An error occurred while processing your request.", status_code=500)
    
    
