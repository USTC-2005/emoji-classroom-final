from fastapi import APIRouter

from .courses import router

courses_router = APIRouter()
courses_router.include_router(router, prefix="/courses", tags=["课程模块"])

__all__ = ["courses_router"]
