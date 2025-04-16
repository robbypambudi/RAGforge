import os
import logging
from typing import List

from fastapi import File, Form, UploadFile
from fastapi.responses import JSONResponse

from src.lib.response_handler import ResponseHandler
from src.services.rag.vectorstore_service import VectorStoreService
from src.services.embedding.embedding_service import EmbeddingService
from src.services.storage.files_storage_service import FileStorageService
from src.services.rag.memorystore_service import MemorystoreService
from src.services.chroma.chroma_service import ChromaService

from src.types.files_request_type import DeleteFileRequestType, UploadFileForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FilesController(ResponseHandler):

    def __init__(
            self,
            file_storage_service: FileStorageService,
            embedding_service: EmbeddingService,
            vectorstore_service: VectorStoreService,
            memorystore_service: MemorystoreService,
            chroma_service: ChromaService
    ):
        self.file_storage_service = file_storage_service
        self.embedding_service = embedding_service
        self.vectorstore_service = vectorstore_service
        self.memorystore_service = memorystore_service
        self.chroma_service = chroma_service

    def get_files(self) -> JSONResponse:
        """
        Get all files
        """
        files = self.file_storage_service.get_all_files()

        if not files:
            return self.success(data=[], message="No files found", status_code=200)

        return self.success(data=files, message="Files retrieved successfully", status_code=200)

    def upload_file(self,
                    description: str = Form(...),
                    collection_name: str = Form(...),
                    file: UploadFile = File(...)
                    ) -> JSONResponse:
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

            embedded_documents = self.embedding_service.embed_documents(splitted_document)
            if not embedded_documents:
                raise Exception("Failed to embed documents")

            self.chroma_service.use_collection(collection_name)

            for i, (chunk, embedding) in enumerate(zip(splitted_document, embedded_documents)):
                self.chroma_service.add_document(
                    doc_id=f"{filename}_chunk_{i}",
                    embedding=embedding,
                    metadata={
                        "source": file_path,
                        "chunk": chunk,
                        "filename": filename,
                        "description": description,
                    }
                )

            self.file_storage_service.save_file(
                name=filename,
                path=dir_path,
                description=description,
                metadatas={"source": file_path}
            )

            return self.success(data={
                "file_path": file_path,
                "info": {
                    "name": filename,
                    "description": description,
                    "metadatas": {
                        "source": file_path,
                    },
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

            return self.error(message="Failed to save file", status_code=500)

    async def delete_file_with_knowledge(self, payload: DeleteFileRequestType) -> JSONResponse:
        """
        Delete a file by its ID and name
        """

        try:
            file = self.file_storage_service.verify_file_by_id_name(payload.file_id, payload.file_name)

            if not file:
                return self.error(message="File not found", status_code=404)
            # Delete the file from chunks
            chunks: List[str] = self.vectorstore_service.get_chunks_by_filename(file.name)

            if not chunks:
                return self.error(message="No chunks found for the file", status_code=404)

            self.file_storage_service.delete_file(file)
            self.vectorstore_service.delete_document_by_chunks(chunks)
            self.memorystore_service.clear_memory()

            return self.success(data={
                "id": file.id,
                "file": file.name,
                "chunks": chunks
            }, message="File deleted successfully", status_code=200)

        except ValueError as e:
            logger.error(f"Error deleting file: {e}")
            return self.error(message="File not found", status_code=404)
        except FileNotFoundError as e:
            logger.error(f"Error deleting file: {e}")
            return self.error(message="File not found", status_code=404)
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return self.error(message="Failed to delete file", status_code=500)

    async def get_file_by_file_name(self, file_name: str) -> JSONResponse:
        """
        Get a file by its name
        """
        try:
            file = self.file_storage_service.get_file_by_file_name(file_name)
            if not file:
                return self.error(message="File not found", status_code=404)

            chunks = self.vectorstore_service.get_chunks_by_filename(file.name)
            if not chunks:
                return self.error(message="No chunks found for the file", status_code=404)

            return self.success(data={
                "id": file.id,
                "file": file.name,
                "chunks": chunks
            }, message="File retrieved successfully", status_code=200)

        except ValueError as e:
            logger.error(f"Error retrieving file: {e}")
            return self.error(message="File not found", status_code=404)

        except Exception as e:
            logger.error(f"Error retrieving file: {e}")
            return self.error(message="Failed to retrieve file", status_code=500)
