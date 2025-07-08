from datetime import datetime

import chromadb.utils.embedding_functions as embedding_functions
from loguru import logger
from pypdf import PdfReader

from app.core.config import settings
from app.models.files import Files
from app.repositories.files_repository import FilesRepository
from rag.chroma.client import ChromaDBHttpClient
from rag.nlp.doc_chunking import DocumentChunker
from rag.nlp.doc_cleaner import DocumentCleaner


def read_pdf(file_path: str):
    """
    Read a PDF file and return its content.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        logger.error("Error reading PDF file: {}", e)
        raise


class PipelineService:
    doc_cleaner = DocumentCleaner()
    doc_chunker = DocumentChunker()
    huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
        api_key=settings.HUGGINGFACE_API_KEY,
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    def __init__(self, files_repository: FilesRepository, chromadb_client: ChromaDBHttpClient):
        self.file_repository = files_repository
        self.chromadb_client = chromadb_client

    def run_pipeline(self, files: Files):
        """
        Run the pipeline with the given ID.
        """
        # Update the file status to processing
        logger.info("Starting pipeline for file: {}", files.id)
        try:
            self.file_repository.update(
                id=files.id,
                schema=Files(
                    status="processing",
                    processing_started_at=datetime.now()
                )
            )
            logger.info("Updated file status to processing for file: {}", files.id)

            # Simulate pipeline processing
            # clean_text = self.doc_cleaner.clean_document(read_pdf(files.file_path))
            clean_text = read_pdf(files.file_path)
            logger.info("Cleaned text for file: {}", files.id)
            chunks = self.doc_chunker.chunk_text(clean_text)
            logger.info("Chunked text for file: {}", files.id)

            # Query the collection name from the database
            collection_name = self.file_repository.get_collection_name(files.collection_id)

            logger.info("Collection name for file {}: {}", files.id, collection_name)
            if not collection_name:
                raise ValueError(f"Collection with ID {files.collection_id} not found.")
            # Add chunks to ChromaDB
            ids = [str(files.id) + "_" + str(i) for i in range(len(chunks))]
            metadata = [
                {
                    "text": text,
                    "file_name": files.file_name,
                } for text in chunks
            ]
            logger.info("Preparing to add chunks to ChromaDB for file: {}", files.id)
            self.chromadb_client.add_documents(
                ids=ids,
                documents=chunks,
                metadatas=metadata,
                collection_name=collection_name,
                # embedding_function=self.huggingface_ef
            )

            logger.info("Added chunks to ChromaDB for file: {}", files.id)
            # Update the file status to completed
            self.file_repository.update(
                id=files.id,
                schema=Files(
                    status="completed",
                    metadatas={
                        "collection_name": collection_name,
                        "chunk_count": len(chunks),
                        "chunk_size": self.doc_chunker.chunk_size,
                        "chunk_overlap": self.doc_chunker.chunk_overlap,
                    },
                    processing_ended_at=datetime.now()
                )
            )

        except Exception as e:
            logger.error("Error processing file: {}", e)
            # Update the file status to error
            self.file_repository.update(
                id=files.id,
                schema=Files(
                    status="failed",
                    processing_ended_at=datetime.now()
                )
            )
