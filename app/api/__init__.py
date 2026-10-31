from fastapi import APIRouter

from .v1 import v1_router

api_router = APIRouter()
# 版本路由统一挂在 /api/v1，后续可在此处继续接入其他 API 版本。
api_router.include_router(v1_router, prefix="/v1")


__all__ = ["api_router"]
