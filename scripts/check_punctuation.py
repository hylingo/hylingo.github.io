#!/usr/bin/env python3
"""检查 ja_articles.json 中所有 segment 的标点问题，输出需要修改的条目。"""

import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "public" / "data" / "ja_articles.json"

# ---------------------------------------------------------------------------
# 辅助
# ---------------------------------------------------------------------------

def sentences_in(text: str) -> list[str]:
    """按句号拆分（保留句号），忽略空串。"""
    parts = re.split(r"(?<=。)", text)
    return [p for p in parts if p.strip()]


def is_question(sent: str) -> bool:
    """判断句子是否是疑问句。"""
    # 结尾已有 ？ 的不算
    if sent.rstrip().endswith("？"):
        return False
    # 常见疑问模式
    patterns = [
        r"ですか。$",
        r"ますか。$",
        r"でしょうか。$",
        r"だろうか。$",
        r"のか。$",
        r"かな。$",
        r"んですか。$",
        r"ないか。$",
        r"ませんか。$",
        r"でしょう。$",
        r"か。$",           # 最宽泛，放最后
    ]
    for p in patterns:
        if re.search(p, sent.rstrip()):
            return True
    return False


def check_long_no_comma(sent: str) -> bool:
    """句子超过 15 字且无逗号。"""
    clean = sent.replace("。", "").replace("？", "").replace("！", "").strip()
    return len(clean) > 15 and "、" not in clean


def find_enumeration(sent: str) -> bool:
    """检测 AとBとC 并列结构（3 项以上用 と 连接）。"""
    # 匹配含 2 个以上 と 的模式
    return len(re.findall(r"と", sent)) >= 2 and "、" not in sent and len(sent) > 10


# ---------------------------------------------------------------------------
# 主检查
# ---------------------------------------------------------------------------

def check_segment(title: str, idx: int, text: str) -> list[dict]:
    issues = []
    sents = sentences_in(text)

    for sent in sents:
        # 1. 疑问句缺问号
        if is_question(sent):
            suggested = re.sub(r"。$", "？", sent.rstrip())
            issues.append({
                "type": "疑问句缺问号",
                "sentence": sent.strip(),
                "suggestion": suggested,
            })

        # 2. 长句无逗号
        if check_long_no_comma(sent):
            issues.append({
                "type": "长句无逗号(>15字)",
                "sentence": sent.strip(),
                "suggestion": "",
            })

        # 3. 列举无逗号
        if find_enumeration(sent):
            issues.append({
                "type": "并列结构可加逗号",
                "sentence": sent.strip(),
                "suggestion": "",
            })

    return issues


def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", data if isinstance(data, list) else [])

    total_issues = 0
    results = {}  # {issue_type: count}

    for art in items:
        title = art.get("titleWord") or art.get("titleJp") or art.get("id", "?")

        # essay format: segments[]
        segments = art.get("segments", [])
        # dialogue format: sections[].lines[]
        if not segments:
            for sec in art.get("sections", []):
                segments.extend(sec.get("lines", []))

        for i, seg in enumerate(segments):
            text = seg.get("jp") or seg.get("word") or ""
            if not text:
                continue

            issues = check_segment(title, i, text)
            if issues:
                print(f"\n[{title}] segment[{i}]:")
                print(f"  原文: {text}")
                for iss in issues:
                    tag = iss["type"]
                    results[tag] = results.get(tag, 0) + 1
                    total_issues += 1
                    print(f"  问题: {tag}")
                    if iss["sentence"] != text.strip():
                        print(f"    句子: {iss['sentence']}")
                    if iss["suggestion"]:
                        print(f"    建议: {iss['suggestion']}")

    # 汇总
    print("\n" + "=" * 60)
    print(f"总计发现 {total_issues} 个问题:")
    for k, v in sorted(results.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
