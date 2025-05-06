from fastapi import APIRouter

from app.api.v1.endpoints.collections import router as collections
from app.api.v1.endpoints.files import router as files

routers = APIRouter(prefix='/v1', tags=["v1"])

routers.include_router(collections)
routers.include_router(files)
