from src.repositories.memorystore_repository import MemorystoreRepository


class MemorystoreService():

    def __init__(self, memorystore_repository: MemorystoreRepository):
        """
        Service for managing the memory store.

        Args:
            memorystore_repository (MemorystoreRepository): The repository to manage the memory store.
        """
        self.memorystore_repository = memorystore_repository

    def add_user_message(self, chat_id: str, message: str) -> None:
        """
        Add a user message to the memory store.

        Args:
            chat_id (str): The unique identifier for the conversation history.
            message (str): The user message.
        """
        self.memorystore_repository.push_message(chat_id, message, is_user=True)

    def add_ai_message(self, chat_id: str, message: str) -> None:
        """
        Add an AI message to the memory store.

        Args:
            chat_id (str): The unique identifier for the conversation history.
            message (str): The AI message.
        """
        self.memorystore_repository.push_message(chat_id, message, is_user=False)

    def get_memory(self, chat_id: str) -> str:
        """
        Get the memory for a given chat ID.

        Args:
            chat_id (str): The unique identifier for the conversation history.

        Returns:
            str: The conversation history as a string.
        """
        return self.memorystore_repository.get_memory(chat_id)

    def delete_memory(self, chat_id: str) -> None:
        """
        Delete the memory for a given chat ID.

        Args:
            chat_id (str): The unique identifier for the conversation history.
        """
        self.memorystore_repository.delete_memory(chat_id)

    def clear_memory(self) -> None:
        """
        Clear all memories.
        """
        self.memorystore_repository.clear_memory()

    def get_all_histories(self) -> list:
        """
        Get all histories from the memory store.

        Returns:
            list: A list of all conversation histories.
        """
        return self.memorystore_repository.get_all_histories()
