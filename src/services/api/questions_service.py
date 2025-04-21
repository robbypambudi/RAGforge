from src.services.chroma.chroma_service import ChromaService
from src.services.rag.memorystore_service import MemorystoreService
from src.services.rag.vectorstore_service import VectorStoreService
from src.services.rag.chain_service import ChainService


class QuestionsService:

    def __init__(self, memorystore_service: MemorystoreService, chain_service: ChainService,
                 chroma_service: ChromaService):
        self.memorystore_service = memorystore_service
        self.chain_service = chain_service
        self.chroma_service = chroma_service

    async def ask_with_stream(self, question_id: str, question: str):
        """
        Ask a question to the chain service and return the answer.
        """
        try:
            # Call the chain service with the question
            memorystore = self.memorystore_service.get_memory(question_id)

            context = self.chain_service.get_context(question, memorystore)

            # Call the chain service with the question
            chain_gen = self.chain_service.get_chain(is_stream=True, is_output_html=False).astream(context)

            accumulated_answer = ""
            for answer in chain_gen:
                if answer:
                    accumulated_answer += answer
                    yield answer
                else:
                    yield "No answer found."

            self.memorystore_service.add_ai_message(question_id, accumulated_answer)

        except Exception as e:
            yield "An error occurred while processing your request."
            # Handle the error appropriately
