#!/usr/bin/env python3
"""对面试题 Markdown 做零依赖的结构和可信度检查。"""

from __future__ import annotations

import argparse
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
INTRO_FILES = sorted(ROOT.glob("README*.md"))
MARKDOWN_FILES = [*INTRO_FILES, *sorted((ROOT / "docs").glob("*/README.md"))]
QUESTION_RE = re.compile(r"^(?:###\s+Q|##\s+)(\d+)[.:：、]\s*(.+?)\s*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
HTML_ANCHOR_RE = re.compile(r'<(?:a|h[1-6])\b[^>]*(?:id|name)="([^"]+)"', re.I)
HTML_TAG_RE = re.compile(r"<[^>]+>")
INLINE_LINK_RE = re.compile(r"!?\[([^]]*)\]\([^)]+\)")
DETAILS_OPEN_RE = re.compile(r"<details(?:\s[^>]*)?>", re.I)
DETAILS_CLOSE_RE = re.compile(r"</details>", re.I)
PERCENT_RE = re.compile(
    r"(?:提升|降低|下降|减少|节省|命中率|准确率|召回率|幻觉率|利用率|成本).{0,18}?\d+(?:\.\d+)?%"
)
SOURCE_HINT_RE = re.compile(r"https?://|来源|论文|官方文档|实验环境|数据集|benchmark", re.I)


def normalize_title(title: str) -> str:
    title = re.sub(r"[（(].*?[）)]", "", title.lower())
    return re.sub(r"[\s`*_，。！？?:：、/\-]+", "", title)


def question_records(path: Path) -> list[tuple[int, int, str]]:
    records: list[tuple[int, int, str]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = QUESTION_RE.match(line)
        if match:
            records.append((line_no, int(match.group(1)), match.group(2)))
    # 部分文件用三级标题制作页首目录；若前 20 行的标题在正文再次出现，只保留正文。
    repeated_titles = {
        normalize_title(title)
        for line_no, _, title in records
        if line_no > 20
    }
    return [
        record
        for record in records
        if not (record[0] <= 20 and normalize_title(record[2]) in repeated_titles)
    ]


def prose_lines(path: Path):
    """逐行返回非代码围栏中的 Markdown 文本。"""
    in_fence = False
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line_no, line


def github_heading_slug(title: str) -> str:
    """近似 GitHub Markdown 的标题锚点规则，支持中日韩文字。"""
    title = INLINE_LINK_RE.sub(r"\1", title)
    title = HTML_TAG_RE.sub("", title)
    title = re.sub(r"[`*_~]", "", title).strip().lower()
    kept = []
    for char in title:
        category = unicodedata.category(char)
        if char.isspace() or char in "-_" or category[0] in {"L", "M", "N"}:
            kept.append(char)
    return re.sub(r"\s+", "-", "".join(kept))


def anchors_for(path: Path) -> set[str]:
    anchors: set[str] = set()
    slug_counts: dict[str, int] = defaultdict(int)
    for _, line in prose_lines(path):
        for explicit in HTML_ANCHOR_RE.findall(line):
            anchors.add(unquote(explicit).lower())

        match = HEADING_RE.match(line)
        if not match:
            continue
        base = github_heading_slug(match.group(2))
        if not base:
            continue
        duplicate_index = slug_counts[base]
        slug_counts[base] += 1
        anchors.add(base if duplicate_index == 0 else f"{base}-{duplicate_index}")
    return anchors


def check_links() -> list[str]:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for path in MARKDOWN_FILES:
        for line_no, line in prose_lines(path):
            targets = [*LINK_RE.findall(line), *HTML_LINK_RE.findall(line)]
            for target in targets:
                target = target.strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:")):
                    continue

                clean, separator, fragment = target.partition("#")
                clean = clean.split("?", 1)[0].strip()
                resolved = path if not clean else (path.parent / unquote(clean)).resolve()
                if resolved.is_dir():
                    resolved = resolved / "README.md"
                if not resolved.exists():
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_no}: 失效链接 -> {target}"
                    )
                    continue

                if not separator or not fragment or resolved.suffix.lower() != ".md":
                    continue
                expected = unquote(fragment).lower()
                anchors = anchor_cache.setdefault(resolved, anchors_for(resolved))
                if expected not in anchors:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_no}: "
                        f"失效页内锚点 -> {target}"
                    )
    return sorted(set(errors))


def check_module_tocs() -> list[str]:
    """每个题库模块都应提供至少一个可点击的二级目录。"""
    errors: list[str] = []
    for path in sorted((ROOT / "docs").glob("*/README.md")):
        lines = list(prose_lines(path))
        toc_index = next(
            (
                index
                for index, (_, line) in enumerate(lines)
                if re.match(r"^##\s+.*目录\s*$", line)
            ),
            None,
        )
        if toc_index is None:
            errors.append(f"{path.relative_to(ROOT)}: 缺少二级目录")
            continue

        toc_lines: list[tuple[int, str]] = []
        for line_no, line in lines[toc_index + 1 :]:
            if line.startswith("## "):
                break
            toc_lines.append((line_no, line))

        link_lines = [item for item in toc_lines if LINK_RE.search(item[1])]
        if not link_lines:
            errors.append(f"{path.relative_to(ROOT)}: 目录没有可点击链接")
            continue

        numbers: list[int] = []
        for line_no, line in link_lines:
            match = re.match(r"^(\d+)\.\s+\[([^]]+)\]\(", line)
            if not match:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_no}: "
                    "目录项应使用有序链接格式"
                )
                continue
            numbers.append(int(match.group(1)))
            if re.search(r"(?:^|[（(\s·])Q\d+", match.group(2), re.I):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_no}: "
                    "目录名称不应重复显示 Q 编号"
                )

        if numbers and numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"{path.relative_to(ROOT)}: 目录序号不连续")
    return errors


def check_balanced_blocks() -> list[str]:
    errors: list[str] = []
    for path in MARKDOWN_FILES:
        text = path.read_text(encoding="utf-8")
        details_open = len(DETAILS_OPEN_RE.findall(text))
        details_close = len(DETAILS_CLOSE_RE.findall(text))
        if details_open != details_close:
            errors.append(
                f"{path.relative_to(ROOT)}: details 标签不配对 "
                f"({details_open} 个开始，{details_close} 个结束)"
            )

        fence_count = sum(
            line.lstrip().startswith("```") for line in text.splitlines()
        )
        if fence_count % 2:
            errors.append(f"{path.relative_to(ROOT)}: Markdown 代码围栏不配对")
    return errors


def check_numbering_and_duplicates() -> list[str]:
    warnings: list[str] = []
    by_title: dict[str, list[tuple[Path, int, str]]] = defaultdict(list)

    for path in MARKDOWN_FILES:
        if path.parent == ROOT:
            continue
        records = question_records(path)
        seen_numbers: dict[int, list[int]] = defaultdict(list)
        seen_titles: dict[str, list[int]] = defaultdict(list)

        for line_no, number, title in records:
            seen_numbers[number].append(line_no)
            normalized = normalize_title(title)
            seen_titles[normalized].append(line_no)
            by_title[normalized].append((path, line_no, title))

        for number, lines in seen_numbers.items():
            if len(lines) > 1:
                warnings.append(
                    f"{path.relative_to(ROOT)}: Q{number} 重复，行 {', '.join(map(str, lines))}"
                )
        for title, lines in seen_titles.items():
            if title and len(lines) > 1:
                warnings.append(
                    f"{path.relative_to(ROOT)}: 同题标题重复，行 {', '.join(map(str, lines))}"
                )

    for records in by_title.values():
        paths = {record[0] for record in records}
        if len(paths) < 2:
            continue
        locations = "；".join(
            f"{path.relative_to(ROOT)}:{line_no}" for path, line_no, _ in records
        )
        warnings.append(f"跨模块同题：{records[0][2]} -> {locations}")

    return sorted(set(warnings))


def check_unqualified_metrics() -> list[str]:
    warnings: list[str] = []
    for path in MARKDOWN_FILES:
        if path.parent == ROOT:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if not PERCENT_RE.search(line):
                continue
            context = "\n".join(lines[max(0, index - 3) : min(len(lines), index + 4)])
            if not SOURCE_HINT_RE.search(context):
                warnings.append(
                    f"{path.relative_to(ROOT)}:{index + 1}: 精确效果数字缺少就近来源/实验条件"
                )
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="存在警告时也返回非零状态")
    parser.add_argument("--verbose", action="store_true", help="逐条输出缺少来源的精确效果数字")
    args = parser.parse_args()

    errors = check_links() + check_module_tocs() + check_balanced_blocks()
    structural_warnings = check_numbering_and_duplicates()
    metric_warnings = check_unqualified_metrics()
    warnings = structural_warnings + metric_warnings

    print(f"扫描 Markdown 文件: {len(MARKDOWN_FILES)}")
    print(f"错误: {len(errors)}，警告: {len(warnings)}")
    for item in errors:
        print(f"ERROR {item}")
    for item in structural_warnings:
        print(f"WARN  {item}")
    if args.verbose:
        for item in metric_warnings:
            print(f"WARN  {item}")
    elif metric_warnings:
        counts: dict[str, int] = defaultdict(int)
        for item in metric_warnings:
            counts[item.split(":", 1)[0]] += 1
        summary = "，".join(f"{path}={count}" for path, count in sorted(counts.items()))
        print(f"WARN  精确效果数字缺少就近来源/实验条件: {summary}")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
