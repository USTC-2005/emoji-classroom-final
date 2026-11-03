"""Emoji 情绪记录的请求、响应和统计数据结构。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import EmojiSource, EmojiType


class EmojiCreate(BaseModel):
    """创建一条手动或 AI 情绪记录。"""

    user_id: int | None = Field(default=None, gt=0, description="用户ID；AI 匿名记录可以为空")
    session_id: int = Field(gt=0, description="课堂会话ID")
    emoji_type: EmojiType = Field(description="情绪类型")
    source: EmojiSource = Field(default=EmojiSource.MANUAL, description="记录来源")
    confidence: float | None = Field(default=None, ge=0, le=1, description="AI 置信度，范围为0到1")
    device_source: str | None = Field(default=None, max_length=100, description="设备来源")

    @model_validator(mode="after")
    def validate_source_fields(self):
        """保证手动记录和 AI 记录的字段约束一致。"""

        if self.source is EmojiSource.MANUAL and self.confidence is not None:
            raise ValueError("手动记录不能填写置信度")
        if self.source is EmojiSource.AI and self.confidence is None:
            raise ValueError("AI 记录必须填写置信度")
        return self


class EmojiOut(EmojiCreate):
    """情绪记录响应结构。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime


class EmojiStatisticsOut(BaseModel):
    """按 Emoji 类型汇总的统计结果。"""

    emoji_type: EmojiType
    count: int = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
