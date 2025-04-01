
import os
from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse

from src.lib.response_handler import ResponseHandler
from src.services.rag.vectorstore_service import VectorStoreService
from src.services.embedding.embedding_service import EmbeddingService
from src.services.storage.files_storage_service import FileStorageService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    print("files", files)
    
    if not files:
      return self.success(data=[], message="No files found", status_code=200)
    
    return self.success(data=files, message="Files retrieved successfully", status_code=200)
  
  def upload_file(self, file: UploadFile = File(...), description = Form(...)) -> JSONResponse:
    """ 
    Upload a file
    # Step
    1. Save the file to local storage
    2. Split the document into chunks
    3. Embed the document
    4. Save the embeddings to local storage
    5. Add the vector store to the vector store service
    6. Save the file to the database
    7. Return the file path
    """
    
    filename = file.filename
    dir_path = os.path.join("documents", filename.split(".")[0]) 
    
    try:  
      file_path = self.file_storage_service.save_file_to_local(file, dir_path, filename)
      
      splitted_document = self.embedding_service.load_and_split_document(file_path)
      if not splitted_document:
        raise Exception("No documents found in the file")
      
      metadatas = {"source": file_path}
      
      embedded_documents = self.embedding_service.embed_documents(splitted_document)
      if not embedded_documents:
        raise Exception("Failed to embed documents")
      
      print("dir_path", dir_path)
      
      self.embedding_service.save_embeddings(embedded_documents, dir_path)
      self.vectorstore_service.add_vector_store(dir_path)
      
      self.file_storage_service.save_file(
        name=filename,
        path=dir_path,
        description=description,
        metadatas=metadatas
      )
      
      return self.success(data={
        "file_path": file_path,
        "info":{
          "name": filename,
          "description": description,
          "metadatas": metadatas,
          "chunks": len(splitted_document),
          },
        },
        message="File uploaded successfully", status_code=200
      )
      
    except ValueError as e:
      return self.error(message=str(e), status_code=400)
    except Exception as e:
      # Remove file if it exists
      logger.error(f"Error uploading file: {e}")
      if self.file_storage_service.file_exists(file_path):
        self.file_storage_service.delete_file(file_path)
      return self.error(message="Failed to save file", status_code=500)
