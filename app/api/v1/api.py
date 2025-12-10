from fastapi import APIRouter
from app.api.v1.endpoints import items, auth, chat

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
