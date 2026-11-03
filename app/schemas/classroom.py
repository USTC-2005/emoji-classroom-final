"""课程、课堂会话和排课的请求/响应契约。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="课程名称")
    teacher_id: int = Field(gt=0, description="教师ID")
    description: str | None = Field(default=None, max_length=500)


class CourseUpdate(BaseModel):
    id: int | None = Field(default=None, gt=0, description="课程ID；由路径参数提供")
    name: str | None = Field(default=None, min_length=1, max_length=100)
    teacher_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, max_length=500)


class CourseOut(ORMModel):
    id: int
    name: str
    teacher_id: int
    description: str | None = None
    created_at: datetime
    updated_at: datetime


class ClassSessionCreate(BaseModel):
    course_id: int = Field(gt=0, description="课程ID")
    start_time: datetime
    end_time: datetime
    classroom: str | None = Field(default=None, max_length=100)
    class_name: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


class ClassSessionUpdate(BaseModel):
    id: int | None = Field(default=None, gt=0, description="课堂会话ID；由路径参数提供")
    course_id: int | None = Field(default=None, gt=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    classroom: str | None = Field(default=None, max_length=100)
    class_name: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time is not None and self.end_time is not None and self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


class ClassSessionOut(ORMModel):
    id: int
    course_id: int
    start_time: datetime
    end_time: datetime
    classroom: str | None = None
    class_name: str | None = None
    created_at: datetime
    updated_at: datetime


class ScheduleUserCreate(BaseModel):
    session_id: int | None = Field(default=None, gt=0, description="课堂会话ID；由路径参数提供")
    user_id: int = Field(gt=0, description="用户ID")
    scheduled_at: datetime | None = None


class ScheduleUserOut(ORMModel):
    id: int
    session_id: int
    user_id: int
    scheduled_at: datetime
    created_at: datetime
    updated_at: datetime


# 便于路由层按“Session”命名引用，同时保留模型的完整名称。
SessionCreate = ClassSessionCreate
SessionUpdate = ClassSessionUpdate
SessionOut = ClassSessionOut
