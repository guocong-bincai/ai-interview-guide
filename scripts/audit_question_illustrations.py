#!/usr/bin/env python3
"""Audit one-to-one question illustration coverage and WebP constraints."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from PIL import Image


QUESTION_RE = re.compile(r"^###\s+Q(\d+)\s*[:：]\s*(.+)$", re.MULTILINE)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc="([^"]+)"', re.IGNORECASE)
ALT_RE = re.compile(r'\balt="([^"]*)"', re.IGNORECASE)
WIDTH_RE = re.compile(r'\bwidth="([^"]+)"', re.IGNORECASE)
HREF_RE = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>', re.IGNORECASE)
MEMORY_RE = re.compile(r"🧠\s*图解记忆：([^<\n]+)")


def iter_sections(text: str):
    matches = list(QUESTION_RE.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        yield int(match.group(1)), match.group(2).strip(), text[match.end():end]


def local_target(markdown: Path, target: str) -> Path:
    return (markdown.parent / unquote(target.split("#", 1)[0])).resolve()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--max-kb", type=int, default=250)
    args = parser.parse_args()

    errors: list[str] = []
    checked = 0
    referenced: list[Path] = []
    expected_asset_dirs: set[Path] = set()

    for supplied in args.paths:
        files = sorted(supplied.rglob("*.md")) if supplied.is_dir() else [supplied]
        for markdown in files:
            if not markdown.exists():
                errors.append(f"missing Markdown path: {markdown}")
                continue
            text = markdown.read_text(encoding="utf-8")
            module = markdown.parent.name
            root = markdown.resolve().parents[2]
            expected_asset_dir = root / "assets" / "illustrations" / module
            expected_asset_dirs.add(expected_asset_dir)
            numbers: list[int] = []

            for number, title, section in iter_sections(text):
                checked += 1
                numbers.append(number)
                images = IMG_RE.findall(section)
                if len(images) != 1:
                    errors.append(
                        f"{markdown}: Q{number} expected exactly one image, found {len(images)}"
                    )
                    continue

                tag = images[0]
                src_match = SRC_RE.search(tag)
                alt_match = ALT_RE.search(tag)
                width_match = WIDTH_RE.search(tag)
                if not src_match:
                    errors.append(f"{markdown}: Q{number} image has no src")
                    continue
                src = src_match.group(1)
                asset = local_target(markdown, src)
                referenced.append(asset)

                hrefs = HREF_RE.findall(section)
                if len(hrefs) != 1 or hrefs[0] != src:
                    errors.append(f"{markdown}: Q{number} clickable href must equal image src")
                if not alt_match or len(alt_match.group(1).strip()) < 16:
                    errors.append(f"{markdown}: Q{number} alt text is missing or too short")
                if not width_match or width_match.group(1) != "760":
                    errors.append(f"{markdown}: Q{number} image width must be 760")
                memory = MEMORY_RE.search(section)
                if not memory or len(memory.group(1).strip()) < 8:
                    errors.append(f"{markdown}: Q{number} missing meaningful 图解记忆 caption")
                if asset.parent != expected_asset_dir:
                    errors.append(f"{markdown}: Q{number} image is outside its module asset directory")
                if not asset.name.startswith(f"q{number:02d}-"):
                    errors.append(f"{markdown}: Q{number} image filename does not start q{number:02d}-")
                if asset.suffix.lower() != ".webp":
                    errors.append(f"{markdown}: Q{number} image is not WebP: {src}")
                if not asset.exists():
                    errors.append(f"{markdown}: Q{number} missing asset: {src}")
                    continue
                if asset.stat().st_size > args.max_kb * 1024:
                    size_kb = asset.stat().st_size / 1024
                    errors.append(f"{asset}: {size_kb:.1f} KB exceeds {args.max_kb} KB")
                try:
                    with Image.open(asset) as image:
                        width, height = image.size
                        if width * 9 != height * 16:
                            errors.append(f"{asset}: {width}x{height} is not 16:9")
                except Exception as exc:  # pragma: no cover - surfaced as audit error
                    errors.append(f"{asset}: cannot read image ({exc})")

            if numbers and numbers != list(range(1, len(numbers) + 1)):
                errors.append(f"{markdown}: question numbering is not continuous: {numbers}")

    duplicates = [path for path, count in Counter(referenced).items() if count > 1]
    for path in duplicates:
        errors.append(f"illustration reused by multiple questions: {path}")

    referenced_set = set(referenced)
    for asset_dir in sorted(expected_asset_dirs):
        if not asset_dir.exists():
            errors.append(f"missing module asset directory: {asset_dir}")
            continue
        for asset in sorted(asset_dir.glob("q??-*.webp")):
            if asset.resolve() not in referenced_set:
                errors.append(f"orphan illustration not referenced by a question: {asset}")

    if errors:
        print(f"Illustration audit failed: {len(errors)} issue(s), {checked} question(s) checked")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(
        f"Illustration audit passed: {checked} question(s), "
        f"{len(referenced_set)} unique 16:9 WebP files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
