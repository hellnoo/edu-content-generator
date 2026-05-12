"""Data models untuk konten yang di-generate."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class Platform(str, Enum):
    YOUTUBE = "YouTube"
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    TWITTER = "Twitter"


class ContentType(str, Enum):
    SCRIPT = "script"
    CAPTION = "caption"
    IDEAS = "ideas"
    THUMBNAIL = "thumbnail"
    FULL_PACKAGE = "full_package"


@dataclass
class ContentRequest:
    topic: str
    content_type: ContentType
    platform: Platform = Platform.YOUTUBE
    duration_minutes: int = 10
    angle: str = "kebijaksanaan hidup dan produktivitas"
    idea_count: int = 5
    theme: str = ""


@dataclass
class GeneratedContent:
    topic: str
    content_type: ContentType
    platform: Platform
    content: str
    title: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    tokens_used: int = 0

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "content_type": self.content_type.value,
            "platform": self.platform.value,
            "title": self.title,
            "created_at": self.created_at,
            "tokens_used": self.tokens_used,
            "content": self.content,
        }


@dataclass
class ContentPackage:
    topic: str
    script: Optional[GeneratedContent] = None
    captions: dict[str, GeneratedContent] = field(default_factory=dict)
    thumbnail: Optional[GeneratedContent] = None
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))

    @property
    def total_tokens(self) -> int:
        total = 0
        if self.script:
            total += self.script.tokens_used
        for cap in self.captions.values():
            total += cap.tokens_used
        if self.thumbnail:
            total += self.thumbnail.tokens_used
        return total
