#!/usr/bin/env python3
import os, sys
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
_env = Path(__file__).parent / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

"""
edu-content-generator — CLI untuk auto-generate konten edukasi Indonesia.

Usage:
  python main.py script   "Ibnu Sina" --duration 10
  python main.py caption  "Ibnu Sina" --platform instagram
  python main.py ideas    --theme "tokoh islam ilmuwan" --count 10
  python main.py package  "Ibnu Sina: Cara Kerja Orang Jenius"
"""

import argparse
import sys
from generator import (
    generate_script,
    generate_caption,
    generate_ideas,
    generate_full_package,
    ContentRequest,
    ContentType,
    Platform,
)
from generator.saver import save_content, save_package


def cmd_script(args):
    req = ContentRequest(
        topic=args.topic,
        content_type=ContentType.SCRIPT,
        duration_minutes=args.duration,
        angle=args.angle,
    )
    print(f"\nGenerating script untuk: {args.topic} ({args.duration} menit)...\n")
    result = generate_script(req)
    path = save_content(result)
    print(result.content)
    print(f"\n✓ Disimpan ke: {path}")
    print(f"  Tokens used: {result.tokens_used}")


def cmd_caption(args):
    platform_map = {
        "youtube": Platform.YOUTUBE,
        "instagram": Platform.INSTAGRAM,
        "tiktok": Platform.TIKTOK,
        "twitter": Platform.TWITTER,
    }
    platform = platform_map.get(args.platform.lower(), Platform.YOUTUBE)
    req = ContentRequest(
        topic=args.topic,
        content_type=ContentType.CAPTION,
        platform=platform,
    )
    print(f"\nGenerating caption {platform.value} untuk: {args.topic}...\n")
    result = generate_caption(req)
    path = save_content(result)
    print(result.content)
    print(f"\n✓ Disimpan ke: {path}")


def cmd_ideas(args):
    req = ContentRequest(
        topic=args.theme,
        content_type=ContentType.IDEAS,
        theme=args.theme,
        idea_count=args.count,
    )
    print(f"\nGenerating {args.count} ide konten dengan tema: {args.theme}...\n")
    result = generate_ideas(req)
    path = save_content(result)
    print(result.content)
    print(f"\n✓ Disimpan ke: {path}")


def cmd_package(args):
    print(f"\nGenerating full package untuk: {args.topic}\n")
    package = generate_full_package(
        topic=args.topic,
        duration_minutes=args.duration,
        angle=args.angle,
    )
    pkg_dir = save_package(package)
    print(f"\n✓ Package lengkap disimpan ke: {pkg_dir}")
    print(f"  Total tokens used: {package.total_tokens}")
    print("\nFile yang dibuat:")
    for f in sorted(pkg_dir.iterdir()):
        print(f"  - {f.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-generate konten edukasi Indonesia dengan Claude AI"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # script
    p_script = sub.add_parser("script", help="Generate script narasi video YouTube")
    p_script.add_argument("topic", help="Topik atau nama tokoh")
    p_script.add_argument("--duration", type=int, default=10, help="Durasi video (menit, default: 10)")
    p_script.add_argument("--angle", default="", help="Sudut pandang konten")
    p_script.set_defaults(func=cmd_script)

    # caption
    p_caption = sub.add_parser("caption", help="Generate caption sosmed")
    p_caption.add_argument("topic", help="Topik atau nama tokoh")
    p_caption.add_argument("--platform", default="youtube",
                           choices=["youtube", "instagram", "tiktok", "twitter"],
                           help="Platform target (default: youtube)")
    p_caption.set_defaults(func=cmd_caption)

    # ideas
    p_ideas = sub.add_parser("ideas", help="Generate ide konten")
    p_ideas.add_argument("--theme", default="tokoh bersejarah dan kebijaksanaan hidup",
                         help="Tema besar untuk ide konten")
    p_ideas.add_argument("--count", type=int, default=5, help="Jumlah ide (default: 5)")
    p_ideas.set_defaults(func=cmd_ideas)

    # package
    p_pkg = sub.add_parser("package", help="Generate paket konten lengkap (script + semua caption + thumbnail)")
    p_pkg.add_argument("topic", help="Topik atau nama tokoh")
    p_pkg.add_argument("--duration", type=int, default=10, help="Durasi video (menit, default: 10)")
    p_pkg.add_argument("--angle", default="", help="Sudut pandang konten")
    p_pkg.set_defaults(func=cmd_package)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
