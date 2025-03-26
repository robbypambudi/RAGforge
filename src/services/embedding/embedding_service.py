
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from src.models import EmbeddingModel
from src.services.storage.files_storage_service import FileStorageService


class EmbeddingService:
  def __init__(self, embedding_model: EmbeddingModel, file_storage_service: FileStorageService):
    self.embedding_model = embedding_model
    self.file_storage_service = file_storage_service
    self.pdf_loader = PyPDFLoader()
    
    self.text_splitter = self._initialize_text_splitter()
    
    self.initialize_with_preprocessed_documents()
    

  def _initialize_text_splitter(self) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap=200,
    )
    
  def load_and_split_document(self, path: str) -> List[Document]:
    document = self.pdf_loader.load_document(path)
    return self.text_splitter.split_documents(document)
  
  def split_text(self, splitted_document: Document) -> List[str]:
    return self.text_splitter.split_text(splitted_document)
  
  def embed_documents(self, splitted_document: Document) -> List[str]:
     return FAISS.from_documents(
      splitted_document,
      self.embedding_model,
    )
  
  def embed_texts(self, splitted_text: List[str], metadatas: List[dict]) -> List[str]:
     return FAISS.from_texts(
      splitted_text,
      self.embedding_model,
      metadatas,
    )
     
  def save_embeddings(self, embedded_documents, path: str) -> bool:
    try :
      embedded_documents.save_local(path)
      return True
    except Exception as e:
      print(e)
      return False
      
  def initialize_with_preprocessed_documents(self, path: str):
    files = self.file_storage_service.get_all_files()
    print(files)