
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

from src.lib.response_handler import ResponseHandler
from src.services.rag.vectorstore_service import VectorStoreService
from src.services.embedding.embedding_service import EmbeddingService
from src.services.storage.files_storage_service import FileStorageService

class FilesController(ResponseHandler):

  def __init__(self, file_storage_service: FileStorageService, embedding_service: EmbeddingService, vectorstore_service: VectorStoreService ):
    self.file_storage_service = file_storage_service
    self.embedding_service = embedding_service
    self.vectorstore_service = vectorstore_service
  
  def get_files(self) -> JSONResponse:
    """
    Get all files
    """
    files = self.file_storage_service.get_all_files()
    
    if not files:
      return self.success(data=[], message="No files found", status_code=200)
    
    return self.success(data=files, message="Files retrieved successfully", status_code=200)
  
  def upload_file(self, file: UploadFile = File(...)):
    """
    Upload a file
    """
    # Save the file
    file_path = self.file_storage_service.save_file(file)
    
    # Embed the file
    self.embedding_service.embed_file(file_path)
    
    # Add the file to the vectorstore
    self.vectorstore_service.add_file_to_vectorstore(file_path)
    
    return self.success(data={"file_path": file_path}, message="File uploaded and processed successfully", status_code=201)
    