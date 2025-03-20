from src.server import Server

class App:
    def __init__(self):
        self.name = "Chatbot API"
        self.version = "1.0.0"
        self.author = "robby.pambudi10@gmail.com"
        self.server = None
        
    def run(self):
        print(f"{self.name} {self.version} by {self.author}")
        self.server = Server()
        self.server.run()
        