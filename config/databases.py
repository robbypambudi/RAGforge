import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DB:
    def __init__(self, type ='postgresql', host = 'localhost', port = '5432', user = 'aws-0-ap-southeast-1.pooler.supabase.com', password = None, database: str = None):
        self.type = type
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.engine = None
        self.session = None
        
        self.connect()
        
        
    def create_engine(self):
        url = f"{self.type}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(url)
        
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
            
    def query(self, query):
        return self.session.execute(query)

    def connect(self):
        try:
            self.create_engine()
            self.create_session()
            
            if self.session:
                logger.info("Database connected")
            else:
                logger.error("Failed to connect to database")
                raise
        except:
            logger.error("Failed to connect to database")
            raise
            
            
            
        
        
        
        
        