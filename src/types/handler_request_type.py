from typing import Callable, Optional
from pydantic import BaseModel


class HandlerRequestType(BaseModel):
    method: str
    path: str
    handler: Callable
    status_code: Optional[int] = 200
