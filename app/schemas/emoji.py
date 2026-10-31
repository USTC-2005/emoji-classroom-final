"""Emoji 记录的请求/响应模型和枚举。"""

from enum import StrEnum


class EmojiSource(StrEnum):
    MANUAL = "MANUAL"
    AI = "AI"


# TODO: 添加 EmojiType、EmojiCreate、EmojiOut、EmojiStatisticsOut。
