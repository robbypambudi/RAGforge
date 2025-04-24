from langchain_community.chat_message_histories import ChatMessageHistory


class MemorystoreRepository:
    """
    A class to manage the memorystore for RAG (Retrieval-Augmented Generation) applications.
    """

    def __init__(self) -> None:
        self.memorystore: dict[str, ChatMessageHistory] = {}

    def create_new_memory(self, chat_id: str) -> None:
        """
        Create a new memory for a given chat ID.
        """
        self.memorystore[chat_id] = ChatMessageHistory()

    def push_message(self, chat_id: str, message: str, is_user: bool = True) -> None:
        """
        Push a message to the memory for a given chat ID.
        """
        if chat_id not in self.memorystore:
            self.create_new_memory(chat_id)

        if is_user:
            self.memorystore[chat_id].add_user_message(message)
        else:
            self.memorystore[chat_id].add_ai_message(message)

    def get_memory(self, chat_id: str) -> ChatMessageHistory:
        """
        Get the memory for a given chat ID.
        """
        if chat_id not in self.memorystore:
            raise ValueError(f"Memory for chat ID {chat_id} not found.")

        return self.memorystore[chat_id]

    def delete_memory(self, chat_id: str) -> None:
        """
        Delete the memory for a given chat ID.
        """
        if chat_id in self.memorystore:
            del self.memorystore[chat_id]
        else:
            raise ValueError(f"Memory for chat ID {chat_id} not found.")

    def clear_memory(self) -> None:
        """
        Clear all memories.
        """
        self.memorystore.clear()

    def get_all_histories(self) -> list:
        """
        Get all histories from the memory store.

        Returns:
            list: A list of all conversation histories with their IDs.
        """
        return [
            {
                "chat_id": chat_id,
                "history": history.messages
            }
            for chat_id, history in self.memorystore.items()
        ]

    def get_all_histories_as_dict(self) -> dict:
        """
        Get all histories from the memory store as a dictionary.
        """
        return {chat_id: history.messages for chat_id, history in self.memorystore.items()}
