from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session as SqlAlchemySession


class DBSession:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)()

    def __enter__(self) -> SqlAlchemySession:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the session when exiting the context manager.
        """
        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()

    def get_session(self) -> SqlAlchemySession:
        """
        Get the current session.
        """
        return self.session
