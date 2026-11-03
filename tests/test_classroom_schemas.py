"""A 模块 Schema 单元测试：校验课程、课堂会话和 Emoji 记录的字段约束。"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models.enums import EmojiSource, EmojiType
from app.schemas.classroom import ClassSessionCreate, CourseCreate
from app.schemas.emoji import EmojiCreate


class TestCourseCreate:
    def test_valid_course(self):
        obj = CourseCreate(name="数据结构", teacher_id=1, description="计算机基础课")
        assert obj.name == "数据结构"
        assert obj.teacher_id == 1

    def test_blank_name_rejected(self):
        with pytest.raises(ValidationError):
            CourseCreate(name="", teacher_id=1)

    def test_teacher_id_must_be_positive(self):
        with pytest.raises(ValidationError):
            CourseCreate(name="数据结构", teacher_id=0)


class TestClassSessionCreate:
    def test_valid_time_range(self):
        obj = ClassSessionCreate(
            course_id=1,
            start_time=datetime(2026, 11, 3, 10, 0, 0),
            end_time=datetime(2026, 11, 3, 11, 0, 0),
        )
        assert obj.end_time > obj.start_time

    def test_end_must_be_after_start(self):
        with pytest.raises(ValidationError):
            ClassSessionCreate(
                course_id=1,
                start_time=datetime(2026, 11, 3, 10, 0, 0),
                end_time=datetime(2026, 11, 3, 9, 0, 0),
            )


class TestEmojiCreate:
    def test_manual_emoji_rejects_confidence(self):
        with pytest.raises(ValidationError):
            EmojiCreate(
                session_id=1,
                user_id=2,
                emoji_type=EmojiType.HAPPY,
                source=EmojiSource.MANUAL,
                confidence=0.9,
            )

    def test_ai_emoji_requires_confidence(self):
        with pytest.raises(ValidationError):
            EmojiCreate(session_id=1, emoji_type=EmojiType.HAPPY, source=EmojiSource.AI)

    def test_ai_confidence_must_be_between_0_and_1(self):
        with pytest.raises(ValidationError):
            EmojiCreate(
                session_id=1,
                emoji_type=EmojiType.HAPPY,
                source=EmojiSource.AI,
                confidence=1.5,
            )

    def test_ai_emoji_valid(self):
        obj = EmojiCreate(
            session_id=1,
            emoji_type=EmojiType.HAPPY,
            source=EmojiSource.AI,
            confidence=0.88,
            device_source="camera-01",
        )
        assert obj.source is EmojiSource.AI
        assert obj.confidence == 0.88
