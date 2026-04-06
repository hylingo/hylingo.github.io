#!/usr/bin/env python3
"""自动修正疑问句：将句末 。 改为 ？"""

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "public" / "data" / "ja_articles.json"

# 疑问句模式（句末 。 前的疑问标志）
Q_PATTERNS = [
    r"ですか。",
    r"ますか。",
    r"でしょうか。",
    r"だろうか。",
    r"のか。",
    r"かな。",
    r"んですか。",
    r"ないか。",
    r"ませんか。",
    r"ことか。",
    r"っていうか。",
    r"ってことか。",
    r"ものか。",
    r"のだろうか。",
]


def fix_questions_in_text(text: str) -> tuple[str, int]:
    """将疑问句的句末 。 替换为 ？，返回 (修正后文本, 修正数)。"""
    count = 0
    for pat in Q_PATTERNS:
        replacement = pat[:-1] + "？"  # 把末尾 。 换成 ？
        while pat in text:
            text = text.replace(pat, replacement, 1)
            count += 1
    return text, count


def process_segment(seg: dict) -> int:
    """修正单个 segment 的 jp 和 word 字段，返回修正数。"""
    total = 0
    for field in ("jp", "word"):
        val = seg.get(field, "")
        if not val:
            continue
        fixed, n = fix_questions_in_text(val)
        if n > 0:
            seg[field] = fixed
            total += n
    return total


def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", data if isinstance(data, list) else [])
    total_fixes = 0
    affected_articles = 0

    for art in items:
        title = art.get("titleWord") or art.get("titleJp") or art.get("id", "?")
        art_fixes = 0

        # essay: segments[]
        for i, seg in enumerate(art.get("segments", [])):
            n = process_segment(seg)
            if n:
                print(f"[{title}] segment[{i}]: {seg.get('jp', '')[:60]}")
                art_fixes += n

        # dialogue: sections[].lines[]
        for sec in art.get("sections", []):
            for i, seg in enumerate(sec.get("lines", [])):
                n = process_segment(seg)
                if n:
                    print(f"[{title}] line[{i}]: {seg.get('jp', '')[:60]}")
                    art_fixes += n

        if art_fixes:
            affected_articles += 1
            total_fixes += art_fixes

    print(f"\n修正了 {affected_articles} 篇文章中的 {total_fixes} 处疑问句标点")

    # 写回
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存到 {DATA}")


if __name__ == "__main__":
    main()
