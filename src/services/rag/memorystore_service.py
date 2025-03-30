from langchain.memory import ChatMessageHistory

class MemorystoreService:
    """
    A class to manage the memorystore for RAG (Retrieval-Augmented Generation) applications.
    """
    def __init__(self) -> None:
        self.memorystore: dict[str, ChatMessageHistory] = {}
    
    def add_user_message(self, chat_id: str, message:str) -> None:
      """
        Menambahkan pesan dari pengguna ke histori percakapan.
        
        Args:
            id (str): Identifier unik untuk histori percakapan.
            message (str): Pesan dari pengguna.
      """ 
      if chat_id not in self.memorystore:
        self.create_new_memory(chat_id)
      
      self.memorystore[chat_id].add_user_message(message)
      
    def add_ai_message(self, chat_id: str, message:str) -> None:
      """
        Menambahkan pesan dari AI ke histori percakapan.
        
        Args:
            id (str): Identifier unik untuk histori percakapan.
            message (str): Pesan dari AI.
      """ 
      if chat_id not in self.memorystore:
        self.create_new_memory(chat_id)
      
      self.memorystore[chat_id].add_ai_message(message)
      
    def delete_memory_by_chat_id(self, chat_id: str) -> None:
        """
        Delete memory by chat ID.
        """
        if chat_id in self.memorystore:
            del self.memorystore[chat_id]
            
    def get_memory_by_chat_id(self, chat_id: str) -> ChatMessageHistory:
        """
        Get memory by chat ID.
        """
        if chat_id not in self.memorystore:
            raise ValueError(f"Memory for chat ID {chat_id} not found.")
        return self.memorystore[chat_id]
      
        
    def create_new_memory(self, chat_id: str) -> None:
        """
        Create a new memory for a given chat ID.
        """
        self.memorystore[chat_id] = ChatMessageHistory()
        
    