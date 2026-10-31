"""手动 Emoji 记录和历史 REST API。"""

from fastapi import APIRouter

router = APIRouter()

# 手动记录和 AI 记录最终都进入同一套 EmojiRecord 查询链路，但来源字段必须保留。
# TODO: POST /emoji、GET /emoji/history、GET /emoji/statistics
