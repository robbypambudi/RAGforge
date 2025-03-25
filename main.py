from src.app import App
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    app = App()
    app.run()