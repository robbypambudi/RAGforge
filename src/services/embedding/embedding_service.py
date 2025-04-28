import logging
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter

from src.models.EmbeddingModel import EmbeddingModel
from src.services.chroma.chroma_service import ChromaService
from src.services.storage.files_storage_service import FileStorageService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _initialize_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200,
    )


def _initialize_token_splitter() -> SentenceTransformersTokenTextSplitter:
    return SentenceTransformersTokenTextSplitter(
        model_name="sentence-transformers/all-mpnet-base-v2",
        chunk_overlap=0,
        chunk_size=256
    )


class EmbeddingService:
    def __init__(self, embedding_model: EmbeddingModel, file_storage_service: FileStorageService,
                 chroma_service: ChromaService):
        self.chroma_service = chroma_service
        self.embedding_model = embedding_model
        self.file_storage_service = file_storage_service
        self.text_splitter = _initialize_text_splitter()
        # self.token_splitter = _initialize_token_splitter()

        self.initialize_with_preprocessed_documents()

    def load_and_split_document(self, path: str) -> List[Document]:
        try:
            documents = PyPDFLoader(path).load()
            split_docs = self.text_splitter.split_documents(documents)
            # Filter out empty documents
            filtered_docs = [doc for doc in split_docs if doc.page_content.strip()]
            return filtered_docs
        except Exception as e:
            logger.error(f"Error loading document {path}: {str(e)}")
            return []

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query using the embedding model
        """
        return self.embedding_model.embed_query(query)

    # def token_splitter(self, texts):
    #     token_split_texts = []
    #     for text in texts:
    #         split_texts = self.token_splitter.split_text(text)
    #         token_split_texts.extend(split_texts)
    #     return token_split_texts

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents using the embedding model
        """
        return self.embedding_model.embed_documents(texts)

    def get_embedding_fn(self):
        """
        Get the embedding function from the embedding model
        """
        return self.embedding_model.get_model().embed_documents

    def initialize_with_preprocessed_documents(self):
        # Retrieve database file paths
        db_files = self.file_storage_service.get_all_files()

        if not db_files:
            logger.warning("No files found in the database")
            return

        # Define documents folder and gather subdirectories containing preprocessed documents
        documents_dir = Path("documents")
        preproc_dirs = [d for d in documents_dir.iterdir()
                        if d.is_dir() and d.name.startswith("preproc_")]

        logger.info(f"Found {len(preproc_dirs)} preprocessed directories")

        if not preproc_dirs:
            logger.warning("No preprocessed directories found")
            return

        for preproc_dir in preproc_dirs:
            pdf_files = list(preproc_dir.glob("*.pdf"))

            if str(pdf_files) not in [file["metadatas"]["source"] for file in db_files]:
                logger.warning(f"{preproc_dir.name} is not in the database")
                continue

            if not pdf_files:
                raise ValueError(f"{preproc_dir.name} is missing a PDF file")

            # Process each file
            for file in pdf_files:
                # Load and split the document
                split_document = self.load_and_split_document(str(file))

                # Embed the documents
                texts = [doc.page_content for doc in split_document]
                metadatas = [doc.metadata | {"source": str(file)} for doc in split_document]

                embeddings = self.embedding_model.get_model().embed_documents(texts)

                # Save to chroma
                for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
                    print("Embedding:", embedding)

                # Save the embeddings if the file does not already exist
                # embedding_path = str(file.with_suffix(''))

                # Save the file information to the database
                # if not self.file_storage_service.save_file(
                #         name=file.name,
                #         path=embedding_path,
                #         description="Preprocessed document",
                #
                # ):
                #     raise ValueError(f"Failed to save {file.name} to the database")
                # logger.info(f"File {file.name} saved successfully")
