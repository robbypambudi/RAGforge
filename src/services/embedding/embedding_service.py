
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from src.models import EmbeddingModel
from src.services.storage.files_storage_service import FileStorageService

class EmbeddingService:
  def __init__(self, embedding_model: EmbeddingModel, file_storage_service: FileStorageService):
    self.embedding_model = embedding_model
    self.file_storage_service = file_storage_service
    
    self.text_splitter = self._initialize_text_splitter()
    
    self.initialize_with_preprocessed_documents()
        

  def _initialize_text_splitter(self) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap=200,
    )
    
  def load_and_split_document(self, path: str) -> List[Document]:
    document = PyPDFLoader(path).load()
    return self.text_splitter.split_documents(document)
  
  def split_text(self, splitted_document: Document) -> List[str]:
    return self.text_splitter.split_text(splitted_document)
  
  def embed_documents(self, splitted_document: Document) -> FAISS:
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
     
  def save_embeddings(self, embedded_documents:FAISS, path: str) -> bool:
    try :
      embedded_documents.save_local(path)
      return True
    except Exception as e:
      print(e)
      return False
    
  
  def initialize_with_preprocessed_documents(self):
    # Retrieve database file paths
    db_files = self.file_storage_service.get_all_files()
    db_file_paths = [file[0].metadatas for file in db_files]
    

    # Define documents folder and gather subdirectories containing preprocessed documents
    documents_dir = Path("documents")
    preproc_dirs = [d for d in documents_dir.iterdir() 
                    if d.is_dir() and d.name.startswith("preproc_")]

    print(f"Found {len(preproc_dirs)} preprocessing directories")
    for preproc_dir in preproc_dirs:     
        
        # Look for .txt and .pdf files in the directory
        pdf_files = list(preproc_dir.glob("*.pdf"))
        
        if str(pdf_files) not in [metadata["source"] for metadata in db_file_paths]: 
            print(f"Skipping {preproc_dir.name} as it is already in the database")
            continue
        
        if not pdf_files:
            raise ValueError(f"{preproc_dir.name} is missing a PDF file")
        
        # Process each file
        for file in  pdf_files:
            # Load and split the document
            splitted_document = self.load_and_split_document(str(file))
            
            # Embed the documents
            embedded_documents = self.embed_documents(splitted_document)
          
            # Save the embeddings if the file does not already exist
            embedding_path = str(file.with_suffix('')) 
            if Path(embedding_path).exists():
                print(f"Embeddings for {file.name} already exist, skipping save.")
            else:
                if not self.save_embeddings(embedded_documents, embedding_path):
                    raise ValueError(f"Failed to save {file.name}")
            
            # Save the file information to the database
            if not self.file_storage_service.save_file(
                name=file.name,
                path=embedding_path,
                description="Preprocessed document",
                metadatas={"source": str(file)}
            ):
                raise ValueError(f"Failed to save {file.name} to the database")
            print(f"Processed {file.name} and saved to the database")
    
    
    