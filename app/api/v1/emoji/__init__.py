from fastapi import APIRouter

from .emoji import router

emoji_router = APIRouter()
emoji_router.include_router(router, prefix="/emoji", tags=["Emoji模块"])

__all__ = ["emoji_router"]
