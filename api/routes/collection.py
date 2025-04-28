from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import col, delete, func, select

from api.entities.collection import Collection

router = APIRouter(prefix="/collection", tags=["collection"])

@router.get("/")
