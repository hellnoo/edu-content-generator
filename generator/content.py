"""Core content generator menggunakan Claude API."""

import os
import anthropic
from .models import ContentRequest, GeneratedContent, ContentPackage, ContentType, Platform
from .templates import SCRIPT_TEMPLATE, CAPTION_TEMPLATE, IDEA_TEMPLATE, THUMBNAIL_TEMPLATE


WORDS_PER_MINUTE = 150  # rata-rata kecepatan narasi


def _words_for_duration(minutes: int) -> int:
    return minutes * WORDS_PER_MINUTE


def _build_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY belum di-set. "
            "Jalankan: export ANTHROPIC_API_KEY=sk-ant-..."
        )
    return anthropic.Anthropic(api_key=api_key)


def _call_claude(client: anthropic.Anthropic, prompt: str, max_tokens: int = 4096) -> tuple[str, int]:
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=max_tokens,
        system=(
            "Kamu adalah content creator dan penulis konten edukasi Indonesia "
            "yang sangat berpengalaman. Selalu jawab dalam Bahasa Indonesia yang "
            "natural, engaging, dan berkualitas tinggi."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text
    tokens = message.usage.input_tokens + message.usage.output_tokens
    return text, tokens


def generate_script(req: ContentRequest) -> GeneratedContent:
    """Generate script narasi video YouTube."""
    client = _build_client()
    prompt = SCRIPT_TEMPLATE.format(
        topic=req.topic,
        duration=req.duration_minutes,
        angle=req.angle,
        words=_words_for_duration(req.duration_minutes),
    )
    content, tokens = _call_claude(client, prompt, max_tokens=8192)
    return GeneratedContent(
        topic=req.topic,
        content_type=ContentType.SCRIPT,
        platform=Platform.YOUTUBE,
        content=content,
        tokens_used=tokens,
    )


def generate_caption(req: ContentRequest) -> GeneratedContent:
    """Generate caption untuk platform tertentu."""
    client = _build_client()
    prompt = CAPTION_TEMPLATE.format(
        topic=req.topic,
        platform=req.platform.value,
    )
    content, tokens = _call_claude(client, prompt, max_tokens=1024)
    return GeneratedContent(
        topic=req.topic,
        content_type=ContentType.CAPTION,
        platform=req.platform,
        content=content,
        tokens_used=tokens,
    )


def generate_ideas(req: ContentRequest) -> GeneratedContent:
    """Generate ide konten dalam jumlah tertentu."""
    client = _build_client()
    theme = req.theme or req.topic
    prompt = IDEA_TEMPLATE.format(theme=theme, count=req.idea_count)
    content, tokens = _call_claude(client, prompt, max_tokens=4096)
    return GeneratedContent(
        topic=theme,
        content_type=ContentType.IDEAS,
        platform=req.platform,
        content=content,
        tokens_used=tokens,
    )


def generate_thumbnail_concept(req: ContentRequest, title: str = "") -> GeneratedContent:
    """Generate konsep visual thumbnail."""
    client = _build_client()
    prompt = THUMBNAIL_TEMPLATE.format(
        topic=req.topic,
        title=title or req.topic,
    )
    content, tokens = _call_claude(client, prompt, max_tokens=1024)
    return GeneratedContent(
        topic=req.topic,
        content_type=ContentType.THUMBNAIL,
        platform=Platform.YOUTUBE,
        content=content,
        title=title,
        tokens_used=tokens,
    )


def generate_full_package(topic: str, duration_minutes: int = 10, angle: str = "") -> ContentPackage:
    """Generate paket lengkap: script + caption semua platform + thumbnail concept."""
    req = ContentRequest(
        topic=topic,
        content_type=ContentType.FULL_PACKAGE,
        duration_minutes=duration_minutes,
        angle=angle or "kebijaksanaan hidup dan produktivitas yang relevan untuk anak muda Indonesia",
    )

    package = ContentPackage(topic=topic)

    print(f"[1/5] Generating script ({duration_minutes} menit)...")
    package.script = generate_script(req)

    title_line = _extract_first_title(package.script.content)

    print("[2/5] Generating caption YouTube...")
    req.content_type = ContentType.CAPTION
    req.platform = Platform.YOUTUBE
    package.captions["youtube"] = generate_caption(req)

    print("[3/5] Generating caption Instagram...")
    req.platform = Platform.INSTAGRAM
    package.captions["instagram"] = generate_caption(req)

    print("[4/5] Generating caption TikTok...")
    req.platform = Platform.TIKTOK
    package.captions["tiktok"] = generate_caption(req)

    print("[5/5] Generating thumbnail concept...")
    package.thumbnail = generate_thumbnail_concept(req, title=title_line)

    return package


def _extract_first_title(script_text: str) -> str:
    """Coba ekstrak judul dari baris pertama script."""
    for line in script_text.split("\n"):
        line = line.strip().lstrip("#").strip()
        if len(line) > 10:
            return line[:80]
    return ""
