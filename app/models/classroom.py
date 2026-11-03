"""课堂情绪业务模型。

这些模型只保存业务数据，不保存原始视频或人脸图像。用户和教师通过
``User`` 外键关联，所有资源归属校验统一放在 controllers 层完成。
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin
from .enums import EmojiSource, EmojiType


class Course(BaseModel, TimestampMixin):
    """一门由教师负责的课程。"""

    name = fields.CharField(max_length=100, description="课程名称", index=True)
    description = fields.CharField(max_length=500, null=True, description="课程描述")
    teacher = fields.ForeignKeyField(
        "models.User", related_name="courses", on_delete=fields.CASCADE, description="教师ID", index=True
    )

    class Meta:
        table = "course"
        unique_together = (("name", "teacher"),)


class ClassSession(BaseModel, TimestampMixin):
    """课程的一次课堂会话。"""

    course = fields.ForeignKeyField(
        "models.Course", related_name="sessions", on_delete=fields.CASCADE, description="课程ID", index=True
    )
    start_time = fields.DatetimeField(description="开始时间", index=True)
    end_time = fields.DatetimeField(description="结束时间", index=True)
    classroom = fields.CharField(max_length=100, null=True, description="教室")
    class_name = fields.CharField(max_length=100, null=True, description="班级")

    class Meta:
        table = "class_session"
        indexes = (("course_id", "start_time"),)


class ScheduleUser(BaseModel, TimestampMixin):
    """课堂会话中的用户排课关系。"""

    session = fields.ForeignKeyField(
        "models.ClassSession",
        related_name="scheduled_users",
        on_delete=fields.CASCADE,
        description="课堂会话ID",
        index=True,
    )
    user = fields.ForeignKeyField(
        "models.User", related_name="scheduled_sessions", on_delete=fields.CASCADE, description="用户ID", index=True
    )
    scheduled_at = fields.DatetimeField(auto_now_add=True, description="安排时间", index=True)

    class Meta:
        table = "schedule_user"
        unique_together = (("session", "user"),)


class EmojiRecord(BaseModel):
    """学生手动或 AI 生成的一条情绪记录。"""

    user = fields.ForeignKeyField(
        "models.User",
        related_name="emoji_records",
        on_delete=fields.SET_NULL,
        null=True,
        description="用户ID",
        index=True,
    )
    session = fields.ForeignKeyField(
        "models.ClassSession",
        related_name="emoji_records",
        on_delete=fields.CASCADE,
        description="课堂会话ID",
        index=True,
    )
    emoji_type = fields.CharEnumField(EmojiType, max_length=32, description="Emoji类型", index=True)
    timestamp = fields.DatetimeField(auto_now_add=True, description="记录时间", index=True)
    source = fields.CharEnumField(
        EmojiSource, max_length=10, default=EmojiSource.MANUAL, description="记录来源", index=True
    )
    confidence = fields.FloatField(null=True, description="AI置信度")
    device_source = fields.CharField(max_length=100, null=True, description="设备来源")

    class Meta:
        table = "emoji_record"
        indexes = (("session_id", "timestamp"), ("user_id", "timestamp"), ("source", "timestamp"))
