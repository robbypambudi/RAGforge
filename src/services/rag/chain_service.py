import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage


from src.services.storage.files_storage_service import FileStorageService
from src.services.rag.vectorstore_service import VectorStoreService


class ChainService:
  
  def __init__(self, file_storage_service: FileStorageService, vectorstore_service: VectorStoreService):
    self.file_storage_service = file_storage_service
    self.vectorstore_service = vectorstore_service
    self.embeddings = None
    self.llm = None
    self.chain = None
    
  def _init_prompt(self, is_output_html: bool = False):
    """
    Prompt template for the chain.
    
    """
    system_msg = (
      "Anda adalah chatbot interaktif bernama Sinta. Anda bertugas untuk menjawab seputar Akademik Departemen Teknik Informatika ITS. Ikuti instruksi ini untuk menjawab pertanyaan/question: jawablah pertanyaan/question dari context yang telah diberikan. Berikan jawaban yang relevan, jika Anda tidak berhasil mendapatkan jawaban yang relevan melalui context, katakan 'saya tidak tahu'.\n"
    )
    
    system_msg = f"{system_msg} Ubah struktur kalimat menjadi HTML tapi hanya gunakan tag <ul> <ol> <li> <p> <br> <h2> <h3> <b> <strong>.\n" if is_output_html else system_msg
    
    prompt = ChatPromptTemplate.from_messages(
      [
        (
          "system",
          system_msg
        ),
        MessagesPlaceholder(variable_name="context"),
        MessagesPlaceholder(variable_name="message"),
      ]
    )
    
    return prompt
  
  def _init_llm(self, is_stream: bool = False):
    """
    Initialize the LLM (Language Model) with the specified parameters.
    """
    return ChatOpenAI(
      model="gpt-3.5-turbo",
      temperature=0.5,
      streaming=is_stream,
      
      api_key="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",
    )
    
  def get_chain(self, is_stream: bool, is_output_html: bool = False):
    """
    Get the chain with the specified parameters.
    """
    chain = (
      self._init_prompt(is_output_html=is_output_html)
      | self._init_llm(is_stream=is_stream)
      | StrOutputParser()
    )    
    return chain
    
  @staticmethod
  def _format_docs(docs):
    """
    Format the documents for the chain.
    """
    return "\n\n".join(
      doc.page_content for doc in docs
    ) if docs else "Tidak ada informasi yang ditemukan."
  
  def format_references(self, docs):
    """
    Format and deduplicate document references, returning a list.
    """
    if not docs:
        return []
    
    seen_sources = set()
    references = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown source")
        if source not in seen_sources:
            seen_sources.add(source)
            references.append(source)
    return references
  
  def get_context(self, question, memorystore):
    try :
      # Ambil context dari vectorstore
      docs = self.vectorstore_service.similarity_search(question)
      
      formatted_docs = self._format_docs(docs)
      return {
        "context": [HumanMessage(content=formatted_docs)],
        "message": memorystore.messages,
      }
    except Exception as e:
      exception_message = str(e)
      raise Exception(f"Error in get_context: {exception_message}")