from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse

class ResponseHandler:
    @staticmethod
    def success(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
        """Returns a standardized success response."""
        return JSONResponse(
            content={
                "status": "success",
                "message": message,
                "data": data,
            },
            status_code=status_code,
        )

    @staticmethod
    def error(message: str, status_code: int = 400, errors: Optional[Any] = None) -> JSONResponse:
        """Returns a standardized error response."""
        return JSONResponse(
            content={
                "status": "error",
                "message": message,
                "errors": errors,
            },
            status_code=status_code,
        )