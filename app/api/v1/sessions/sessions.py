"""课堂会话和排课 REST API。"""

from fastapi import APIRouter

router = APIRouter()

# 会话路由负责课堂实例和排课关系，不应把课程定义与课堂实例混为一张表。
# TODO: GET /sessions、POST /sessions、POST /sessions/{id}/schedule
