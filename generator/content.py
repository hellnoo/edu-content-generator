"""Core content generator menggunakan Claude API."""

import os
from typing import Callable, Optional
import anthropic
from .models import ContentRequest, GeneratedContent, ContentPackage, ContentType, Platform
from .templates import SCRIPT_TEMPLATE, CAPTION_TEMPLATE, IDEA_TEMPLATE, THUMBNAIL_TEMPLATE

MODEL   = "claude-sonnet-4-6"
SYSTEM  = (
    "Kamu adalah content creator dan penulis konten edukasi Indonesia "
    "yang sangat berpengalaman. Selalu jawab dalam Bahasa Indonesia yang "
    "natural, engaging, dan berkualitas tinggi."
)
WORDS_PER_MINUTE = 150


def _words_for_duration(minutes: int) -> int:
    return minutes * WORDS_PER_MINUTE


def _build_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY belum di-set. Copy dari console.anthropic.com lalu isi di file .env"
        )
    return anthropic.Anthropic(api_key=api_key)


def _call_stream(
    client: anthropic.Anthropic,
    prompt: str,
    max_tokens: int = 2048,
    on_chunk: Optional[Callable[[str], None]] = None,
) -> tuple[str, int]:
    """Panggil Claude dengan streaming — on_chunk dipanggil per token."""
    full_text = []
    input_tokens = 0
    output_tokens = 0

    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_text.append(text)
            if on_chunk:
                on_chunk(text)

        usage = stream.get_final_message().usage
        input_tokens  = usage.input_tokens
        output_tokens = usage.output_tokens

    return "".join(full_text), input_tokens + output_tokens


def generate_script(
    req: ContentRequest,
    on_chunk: Optional[Callable[[str], None]] = None,
) -> GeneratedContent:
    client = _build_client()
    prompt = SCRIPT_TEMPLATE.format(
        topic=req.topic,
        duration=req.duration_minutes,
        angle=req.angle,
        words=_words_for_duration(req.duration_minutes),
    )
    max_tok = min(req.duration_minutes * 350 + 500, 4096)
    content, tokens = _call_stream(client, prompt, max_tokens=max_tok, on_chunk=on_chunk)
    return GeneratedContent(
        topic=req.topic, content_type=ContentType.SCRIPT,
        platform=Platform.YOUTUBE, content=content, tokens_used=tokens,
    )


def generate_caption(
    req: ContentRequest,
    on_chunk: Optional[Callable[[str], None]] = None,
) -> GeneratedContent:
    client = _build_client()
    prompt = CAPTION_TEMPLATE.format(topic=req.topic, platform=req.platform.value)
    content, tokens = _call_stream(client, prompt, max_tokens=800, on_chunk=on_chunk)
    return GeneratedContent(
        topic=req.topic, content_type=ContentType.CAPTION,
        platform=req.platform, content=content, tokens_used=tokens,
    )


def generate_ideas(
    req: ContentRequest,
    on_chunk: Optional[Callable[[str], None]] = None,
) -> GeneratedContent:
    client = _build_client()
    theme  = req.theme or req.topic
    prompt = IDEA_TEMPLATE.format(theme=theme, count=req.idea_count)
    max_tok = min(req.idea_count * 300 + 400, 4096)
    content, tokens = _call_stream(client, prompt, max_tokens=max_tok, on_chunk=on_chunk)
    return GeneratedContent(
        topic=theme, content_type=ContentType.IDEAS,
        platform=req.platform, content=content, tokens_used=tokens,
    )


def generate_thumbnail_concept(
    req: ContentRequest,
    title: str = "",
    on_chunk: Optional[Callable[[str], None]] = None,
) -> GeneratedContent:
    client = _build_client()
    prompt = THUMBNAIL_TEMPLATE.format(topic=req.topic, title=title or req.topic)
    content, tokens = _call_stream(client, prompt, max_tokens=600, on_chunk=on_chunk)
    return GeneratedContent(
        topic=req.topic, content_type=ContentType.THUMBNAIL,
        platform=Platform.YOUTUBE, content=content, title=title, tokens_used=tokens,
    )


def generate_full_package(
    topic: str,
    duration_minutes: int = 10,
    angle: str = "",
    on_step: Optional[Callable[[str], None]] = None,
    on_chunk: Optional[Callable[[str], None]] = None,
) -> ContentPackage:
    req = ContentRequest(
        topic=topic, content_type=ContentType.FULL_PACKAGE,
        duration_minutes=duration_minutes,
        angle=angle or "kebijaksanaan hidup dan produktivitas yang relevan untuk anak muda Indonesia",
    )
    package = ContentPackage(topic=topic)

    def step(msg):
        if on_step: on_step(msg)
        if on_chunk: on_chunk(f"\n\n{'─'*40}\n{msg}\n{'─'*40}\n\n")

    step("[1/5] Script video...")
    package.script = generate_script(req, on_chunk=on_chunk)

    title_line = _extract_first_title(package.script.content)

    step("[2/5] Caption YouTube...")
    req.content_type = ContentType.CAPTION
    req.platform = Platform.YOUTUBE
    package.captions["youtube"] = generate_caption(req, on_chunk=on_chunk)

    step("[3/5] Caption Instagram...")
    req.platform = Platform.INSTAGRAM
    package.captions["instagram"] = generate_caption(req, on_chunk=on_chunk)

    step("[4/5] Caption TikTok...")
    req.platform = Platform.TIKTOK
    package.captions["tiktok"] = generate_caption(req, on_chunk=on_chunk)

    step("[5/5] Konsep Thumbnail...")
    package.thumbnail = generate_thumbnail_concept(req, title=title_line, on_chunk=on_chunk)

    return package


def _extract_first_title(script_text: str) -> str:
    for line in script_text.split("\n"):
        line = line.strip().lstrip("#").strip()
        if len(line) > 10:
            return line[:80]
    return ""
