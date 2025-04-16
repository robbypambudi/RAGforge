import uuid


class CustomException(Exception):
    """
    Custom exception class for the application.
    """

    def __init__(self, message: str, status_code: int = 400, error_code: str = "UNKNOWN_ERROR", error_id: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.error_id = error_id or str(uuid.uuid4())
        super().__init__(f"[{self.error_id}] {self.message}")
