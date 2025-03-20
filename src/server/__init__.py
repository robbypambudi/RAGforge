import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class Server:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)