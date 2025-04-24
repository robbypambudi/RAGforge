import logging

from chromadb import QueryResult
from chromadb.types import Collection
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.services.chroma.chroma_service import ChromaService
from src.services.embedding.embedding_service import EmbeddingService
from src.services.storage.files_storage_service import FileStorageService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChainService:

    def __init__(self, file_storage_service: FileStorageService, chroma_service: ChromaService,
                 embedding_service: EmbeddingService):
        self.file_storage_service = file_storage_service
        self.chroma_service = chroma_service
        self.embedding_service = embedding_service
        self.llm = None
        self.chain = None

    @staticmethod
    def _init_prompt(is_output_html: bool = False):
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

    @staticmethod
    def _init_llm(is_stream: bool = False):
        """
        Initialize the LLM (Language Model) with the specified parameters.
        """
        return ChatOpenAI(
            model="gpt-4o",
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
    def _format_docs(docs: QueryResult):
        """
        Format the documents for the chain.
        """
        if not docs or not docs.get('metadatas') or not docs.get('documents'):
            return "Tidak ada informasi yang ditemukan."

        formatted_docs = []
        for doc, metadata in zip(docs['documents'][0], docs['metadatas'][0]):
            formatted_doc = f"Content: {doc}\n"
            if metadata.get('source'):
                formatted_doc += f"Source: {metadata['source']}\n"
                formatted_docs.append(formatted_doc)

            return "\n\n".join(formatted_docs)
        return None

    @staticmethod
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

    def get_context(self, question, memorystore, collection: Collection = None):
        # Check if the vectorstore is initialized
        if not self.chroma_service:
            return {
                "context": [HumanMessage(content="Vectorstore belum diinisialisasi.")],
                "message": memorystore.messages,
            }
        #  No collection is currently selected.
        query_embedding = self.embedding_service.embed_query(question)
        # docs
        docs = self.chroma_service.query_embeddings(
            query_embedding=query_embedding,
            collection=collection,
            n_results=5
        )
        # Print the retrieved documents
        logger.info(f"Retrieved documents: {docs}")
        formatted_docs = self._format_docs(docs)
        return {
            "context": [HumanMessage(content=formatted_docs)],
            "message": memorystore.messages,
        }
