# logging_config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="error.log",
    filemode="a",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("myapp")
