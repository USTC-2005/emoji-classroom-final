from fastapi import APIRouter

from .sessions import router

sessions_router = APIRouter()
sessions_router.include_router(router, prefix="/sessions", tags=["课堂模块"])

__all__ = ["sessions_router"]
