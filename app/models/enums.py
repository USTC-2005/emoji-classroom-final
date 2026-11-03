from enum import Enum, StrEnum


class EnumBase(Enum):
    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class EmojiSource(StrEnum):
    """情绪记录的产生方式。"""

    MANUAL = "MANUAL"
    AI = "AI"


class EmojiType(StrEnum):
    """系统支持的基础情绪类型。"""

    HAPPY = "HAPPY"
    SAD = "SAD"
    ANGRY = "ANGRY"
    SURPRISED = "SURPRISED"
    NEUTRAL = "NEUTRAL"
