from typing import List, Dict, Generator

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from loguru import logger

prompt = """
Kamu adalah seorang asisten yang ahli dan membantu pengguna dalam menjawab pertanyaan.
Kamu harus memberikan jawaban yang akurat dan relevan berdasarkan pengetahuan yang kamu miliki.
Pengguna akan memberikan pertanyaan, berdasarkan informasi yang diambil dari buku petunjuk teknis.
Jawablah pertanyaan pengguna hanya berdasarkan informasi yang diberikan.
Berikut adalah informasi yang diberikan:
"""


class OpenAIChat:
    """
    Class untuk mengelola interaksi chat dengan OpenAI API.
    """

    def __init__(self, key: str, model_name: str = "gpt-3.5-turbo") -> None:
        """
        Inisialisasi OpenAIChat.

        Args:
            key (str): OpenAI API key
            model_name (str): Nama model OpenAI yang akan digunakan
        """
        self.chat_model = ChatOpenAI(
            api_key=key,
            model=model_name,
            temperature=0.7
        )
        self.output_parser = StrOutputParser()
        logger.info(f"OpenAIChat initialized with model: {model_name}")

    def _prepare_messages(self, question: str, context_pairs: list[list]) -> List:
        """
        Menyiapkan pesan untuk chat.

        Args:
            question (str): Pertanyaan dari pengguna
            context_pairs (List[Dict]): Daftar pasangan konteks (pertanyaan dan jawaban)

        Returns:
            List: Daftar pesan yang telah disiapkan
        """
        messages = [
            SystemMessage(content=prompt.strip()),
        ]

        # Menambahkan konteks dari pairs
        context = ""
        for pair in context_pairs:
            context += f"Q: {pair[0]}\nA: {pair[1]}\n\n"
        context = context.strip()

        return messages + [
            HumanMessage(content=f"{context}\n\nQ: {question}\nA:")
        ]

    def chat(self, question: str, context_pairs: list[list]) -> str:
        """
        Melakukan chat dengan mode normal (non-streaming).

        Args:
            question (str): Pertanyaan dari pengguna
            context_pairs (str): Full answer dari model

        Returns:
            str: Jawaban dari model
        """
        try:
            messages = self._prepare_messages(question, context_pairs)
            response = self.chat_model.invoke(messages)
            answer = self.output_parser.parse(response.content)
            logger.info(f"Generated response for question: {question}")
            return answer
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            raise

    async def chat_with_stream(self, question: str, context_pairs: List[list]):
        """
        Melakukan chat dengan mode streaming.

        Args:
            question (str): Pertanyaan dari pengguna
            context_pairs (List[list]): Daftar pasangan konteks

        Returns:
            Generator: Generator untuk streaming response
        """
        try:
            messages = self._prepare_messages(question, context_pairs)
            async for chunk in self.chat_model.astream(messages):
                if chunk.content:
                    processed_chunk = self.output_parser.parse(chunk.content)
                    logger.debug(f"Streaming chunk: {processed_chunk}")
                    yield processed_chunk
        except Exception as e:
            error_msg = f"Error in chat streaming: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
