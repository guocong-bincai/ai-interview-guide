#!/usr/bin/env python3
"""将题库中过长的编程代码块包装为 GitHub 可折叠区域。"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = sorted((ROOT / "docs").glob("*/README.md"))
CODE_LANGUAGES = {
    "bash",
    "csharp",
    "go",
    "http",
    "java",
    "javascript",
    "json",
    "markdown",
    "php",
    "python",
    "rust",
    "sh",
    "shell",
    "sql",
    "typescript",
    "yaml",
}


def previous_nonblank(lines: list[str]) -> str:
    for line in reversed(lines):
        if line.strip():
            return line.strip()
    return ""


def transform(text: str, min_lines: int) -> tuple[str, int]:
    lines = text.splitlines()
    output: list[str] = []
    changed = 0
    index = 0

    while index < len(lines):
        opening = lines[index]
        stripped = opening.lstrip()
        if not stripped.startswith("```"):
            output.append(opening)
            index += 1
            continue

        info = stripped[3:].strip()
        language = info.split(maxsplit=1)[0].lower() if info else ""
        end = index + 1
        while end < len(lines) and not lines[end].lstrip().startswith("```"):
            end += 1

        if end == len(lines):
            output.extend(lines[index:])
            break

        block = lines[index : end + 1]
        code_lines = end - index - 1
        already_wrapped = previous_nonblank(output).startswith("<summary>")
        should_wrap = (
            language in CODE_LANGUAGES
            and code_lines >= min_lines
            and not already_wrapped
        )

        if should_wrap:
            label = language.upper() if language in {"sql", "http"} else language.title()
            output.extend(
                [
                    "<details>",
                    f"<summary>展开 {label} 代码示例（{code_lines} 行）</summary>",
                    "",
                    *block,
                    "",
                    "</details>",
                ]
            )
            changed += 1
        else:
            output.extend(block)

        index = end + 1

    trailing_newline = "\n" if text.endswith("\n") else ""
    return "\n".join(output) + trailing_newline, changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-lines", type=int, default=30, help="折叠代码块的最小行数")
    parser.add_argument("--check", action="store_true", help="只检查，不修改文件")
    args = parser.parse_args()

    total = 0
    changed_files = 0
    for path in DOCS:
        original = path.read_text(encoding="utf-8")
        updated, count = transform(original, args.min_lines)
        if not count:
            continue
        total += count
        changed_files += 1
        print(f"{path.relative_to(ROOT)}: {count} 个长代码块")
        if not args.check:
            path.write_text(updated, encoding="utf-8")

    action = "待折叠" if args.check else "已折叠"
    print(f"{action}: {total} 个代码块，涉及 {changed_files} 个文件")
    return 1 if args.check and total else 0


if __name__ == "__main__":
    raise SystemExit(main())
