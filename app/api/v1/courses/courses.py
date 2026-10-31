"""课程 REST API。"""

from fastapi import APIRouter

router = APIRouter()

# 课程路由最终应调用 CourseController，并在写入时校验教师归属。
# TODO: GET/POST/PUT/DELETE /courses
