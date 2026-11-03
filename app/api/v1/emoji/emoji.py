"""手动 Emoji 记录、历史和统计 REST API。"""

from datetime import datetime

from fastapi import APIRouter, Query

from app.controllers.emoji import emoji_controller
from app.core.ctx import CTX_USER_ID
from app.core.dependency import DependAuth
from app.schemas.base import Success, SuccessExtra
from app.schemas.emoji import EmojiCreate

router = APIRouter()


async def _dict(obj):
    return obj if isinstance(obj, dict) else await obj.to_dict()


@router.post("", response_model=None, dependencies=[DependAuth], summary="提交 Emoji")
async def create_emoji(payload: EmojiCreate):
    item = await emoji_controller.create_record(payload, actor_id=CTX_USER_ID.get())
    return Success(data=await _dict(item))


@router.get("/history", response_model=None, dependencies=[DependAuth], summary="查询 Emoji 历史")
async def emoji_history(user_id: int | None = None, session_id: int | None = None, from_time: datetime | None = None, to_time: datetime | None = None, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    actor_id = CTX_USER_ID.get()
    total, records = await emoji_controller.get_user_history(user_id or actor_id, actor_id, session_id, from_time, to_time, page, page_size)
    return SuccessExtra(data=[await _dict(item) for item in records], total=total, page=page, page_size=page_size)


@router.get("/statistics", response_model=None, dependencies=[DependAuth], summary="查询 Emoji 统计")
async def emoji_statistics(session_id: int | None = None, user_id: int | None = None, from_time: datetime | None = None, to_time: datetime | None = None):
    actor_id = CTX_USER_ID.get()
    if user_id is not None and user_id != actor_id:
        await emoji_controller.get_user_history(user_id, actor_id, session_id, from_time, to_time, 1, 1)
    data = await emoji_controller.statistics(session_id, user_id or (actor_id if session_id is None else None), from_time, to_time)
    return Success(data=data)
