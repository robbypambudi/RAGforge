import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DB:
    def __init__(self, type ='postgresql', host = 'localhost', port = '5432'):
        self.type = type
        self.host = host
        self.port = port
        self.engine = None
        self.session = None
        
    def create_engine(self):
        self.engine = create_engine(
            f"{self.type}://{self.host}:{self.port}"
        )
        
    def create_session(self):
        self.session = sessionmaker(bind=self.engine)()
    
    def transaction(self, func):
        try:
            func()
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
    
    def connect(self):
        try:
            self.create_engine()
            self.create_session()
            logger.info("Connected to database")
        except:
            logger.error("Failed to connect to database")
            raise
    
    def __call__(self, *args, **kwds):
        self.connect()
        return self.session
            
            
            
        
        
        
        
        