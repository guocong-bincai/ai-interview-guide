#!/usr/bin/env python3
"""Audit question-to-illustration coverage in Markdown interview guides."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


QUESTION_RE = re.compile(
    r"^(?:###\s+Q(?:\d+)?\s*[:：].+|##\s+\d+\.\s+.+)", re.MULTILINE
)
IMAGE_RE = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*alt="([^"]+)"', re.IGNORECASE)


def iter_sections(text: str):
    matches = list(QUESTION_RE.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        yield match.group(0), text[match.end():end]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--max-kb", type=int, default=250)
    args = parser.parse_args()
    errors: list[str] = []
    checked = 0

    for supplied in args.paths:
        files = sorted(supplied.rglob("*.md")) if supplied.is_dir() else [supplied]
        for markdown in files:
            text = markdown.read_text(encoding="utf-8")
            for heading, section in iter_sections(text):
                checked += 1
                image = IMAGE_RE.search(section)
                if not image:
                    errors.append(f"{markdown}: missing illustration after {heading}")
                    continue
                src, alt = image.groups()
                if len(alt.strip()) < 16:
                    errors.append(f"{markdown}: weak alt text after {heading}")
                asset = (markdown.parent / src).resolve()
                if not asset.exists():
                    errors.append(f"{markdown}: missing asset {src} after {heading}")
                    continue
                if asset.suffix.lower() != ".webp":
                    errors.append(f"{markdown}: non-WebP asset {src} after {heading}")
                size_kb = asset.stat().st_size / 1024
                if size_kb > args.max_kb:
                    errors.append(f"{asset}: {size_kb:.1f} KB exceeds {args.max_kb} KB")

    if errors:
        print(f"Illustration audit failed: {len(errors)} issue(s), {checked} question(s) checked")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Illustration audit passed: {checked} question(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
