"""Simpan hasil generate ke file."""

import json
import os
import re
from pathlib import Path
from .models import GeneratedContent, ContentPackage, ContentType


OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"


def _slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text[:50]


def save_content(content: GeneratedContent) -> Path:
    """Simpan satu piece of content ke file .md."""
    type_dir = {
        ContentType.SCRIPT: OUTPUTS_DIR / "scripts",
        ContentType.CAPTION: OUTPUTS_DIR / "captions",
        ContentType.IDEAS: OUTPUTS_DIR / "ideas",
        ContentType.THUMBNAIL: OUTPUTS_DIR / "ideas",
    }.get(content.content_type, OUTPUTS_DIR)

    type_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{content.created_at}_{_slug(content.topic)}.md"
    filepath = type_dir / filename

    header = f"# {content.topic}\n\n"
    header += f"**Tipe:** {content.content_type.value}  \n"
    header += f"**Platform:** {content.platform.value}  \n"
    header += f"**Dibuat:** {content.created_at}  \n"
    header += f"**Tokens:** {content.tokens_used}\n\n---\n\n"

    filepath.write_text(header + content.content, encoding="utf-8")
    return filepath


def save_package(package: ContentPackage) -> Path:
    """Simpan full package ke satu folder."""
    pkg_dir = OUTPUTS_DIR / "packages" / f"{package.created_at}_{_slug(package.topic)}"
    pkg_dir.mkdir(parents=True, exist_ok=True)

    if package.script:
        (pkg_dir / "script.md").write_text(package.script.content, encoding="utf-8")

    for platform, caption in package.captions.items():
        (pkg_dir / f"caption_{platform}.md").write_text(caption.content, encoding="utf-8")

    if package.thumbnail:
        (pkg_dir / "thumbnail_concept.md").write_text(package.thumbnail.content, encoding="utf-8")

    meta = {
        "topic": package.topic,
        "created_at": package.created_at,
        "total_tokens": package.total_tokens,
        "files": [f.name for f in pkg_dir.iterdir()],
    }
    (pkg_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return pkg_dir
