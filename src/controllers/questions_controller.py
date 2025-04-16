import os
import logging

from src.lib.response_handler import ResponseHandler
from src.services.rag.chain_service import ChainService
from src.services.rag.vectorstore_service import VectorStoreService
from src.services.rag.memorystore_service import MemorystoreService
from src.types.question_request_type import PostQuestionStreamGeneratorType
from src.services.api.questions_service import QuestionsService
from sse_starlette.sse import EventSourceResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestionsController(ResponseHandler):
  
  def __init__(self, chain_service: ChainService, vectorstore_service: VectorStoreService, memorystore_service: MemorystoreService, questions_service: QuestionsService):
    self.chain_service = chain_service
    self.vectorstore_service = vectorstore_service
    self.memorystore_service = memorystore_service
    self.questions_service = questions_service
  
  async def _chain_stream(self, question: str, id:str, is_output_html: bool = True):
    """
    Initialize the chain service with the specified parameters.
    """
    memorystore = self.memorystore_service.get_memory(id)
    context = self.chain_service.get_context(question, memorystore)
    # Pretty print the context
    logger.info(f"Context: {context}")
    chain_gen = self.chain_service.get_chain(is_stream=True, is_output_html=is_output_html).astream(context)
    
    accumulated_answer = ""
    async for chunk in chain_gen:
      accumulated_answer += chunk
      yield chunk
    
    # After the streaming is done, save the answer to the memory store
    self.memorystore_service.add_ai_message(id, accumulated_answer)
    
  def ask_with_stream(self, payload: PostQuestionStreamGeneratorType):
    """
    Ask a question to the chain service and return the answer.
    """    
    try:
      # Call the chain service with the question
      self.memorystore_service.add_user_message(payload.id, payload.question)
      
      # Call the chain service with the question
      return EventSourceResponse(
        self._chain_stream(
          payload.question,
          payload.id,
        ),
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
      # Tambahkan pesan pengguna ke memory store
      self.memorystore_service.add_user_message(payload.id, payload.question)
      memorystore = self.memorystore_service.get_memory(payload.id)
      
      # Dapatkan context dan dokumen referensi
      context = self.chain_service.get_context(payload.question, memorystore)
      
      # Ambil chain dan dapatkan jawaban dari LL
      answer = self.chain_service.get_chain(is_stream=False, is_output_html=False).invoke(context)
            
      # Simpan jawaban AI ke dalam memory store
      self.memorystore_service.add_ai_message(payload.id, answer)
            
      return self.success(
        data={
          "answer": answer,
        }, 
        status_code=200
      )

    except Exception as e:
      logger.error(f"Error in ask_without_stream: {e}")
      return self.error(message="An error occurred while processing your request.", status_code=500)
    
    
