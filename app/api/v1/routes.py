from fastapi import APIRouter

from app.api.v1.endpoints.collections import router as collections

routers = APIRouter(prefix='/v1', tags=["v1"])

routers.include_router(collections)
