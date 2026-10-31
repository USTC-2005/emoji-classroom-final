"""AI 推理服务入库 REST API。"""

from fastapi import APIRouter

router = APIRouter()

# AI 服务使用独立令牌，不复用学生 JWT；接入结果后再交给 ai_ingest 服务处理。
# TODO: POST /ai/emoji-results，使用独立 AI_SERVICE_TOKEN
