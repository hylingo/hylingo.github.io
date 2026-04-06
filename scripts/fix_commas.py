#!/usr/bin/env python3
"""
为日语长句自动添加逗号，提升 TTS 朗读自然度。
规则：
1. 句首接续词后加逗号（でも → でも、）
2. 从句关键词后加逗号（ですが/けど/ので/たら/ば 等）
3. 引号内不动，短句不动，已有逗号不动
"""

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "public" / "data" / "ja_articles.json"

CONJUNCTIONS = [
    "しかし", "しかも", "また", "そして", "それから", "それで", "それに",
    "だから", "ですから", "ただ", "ただし", "つまり", "でも", "けれど",
    "けれども", "ところが", "ところで", "なぜなら", "もちろん",
    "たとえば", "例えば", "一方で", "逆に", "むしろ",
    "さらに", "なお", "ちなみに", "要するに",
    "とにかく", "いずれにしても", "そもそも", "実は", "確かに",
    "結局", "やはり", "やっぱり",
]

CLAUSE_KEYWORDS = [
    "ですが", "ますが",
    "んだけど", "だけど", "ですけど", "けれど", "けども",
    "ですので", "ますので", "なので",
    "したら", "きたら", "いたら", "んだら", "なったら",
    "すれば", "くれば", "なれば", "であれば",
]


def is_inside_quotes(text, pos):
    depth = 0
    for i in range(pos):
        if text[i] == "\u300c":
            depth += 1
        elif text[i] == "\u300d":
            depth = max(0, depth - 1)
    return depth > 0


def add_conjunction_comma(sent):
    for conj in sorted(CONJUNCTIONS, key=len, reverse=True):
        if sent.startswith(conj) and len(sent) > len(conj):
            after = sent[len(conj)]
            if after != "\u3001" and after != "\u300d":
                sent = conj + "\u3001" + sent[len(conj):]
                break
    return sent


def add_clause_commas(sent):
    for kw in sorted(CLAUSE_KEYWORDS, key=len, reverse=True):
        idx = sent.find(kw)
        while idx != -1:
            end = idx + len(kw)
            if (not is_inside_quotes(sent, idx)
                    and end < len(sent)
                    and sent[end] not in "\u3001\u3002\uff1f\uff01\u300d\u2026\uff0e"
                    and sent[end] not in "\u306d\u3088\u306a\u3055\u305e\u308f"
                    and not sent[end:].startswith("\u3057\u3044")):
                sent = sent[:end] + "\u3001" + sent[end:]
                end += 1  # account for inserted char
            idx = sent.find(kw, end + 1)
    return sent


def fix_sentence(sent):
    if not sent or len(sent) <= 20:
        return sent
    if "\u3001" in sent:
        return sent
    sent = add_conjunction_comma(sent)
    if "\u3001" not in sent:
        sent = add_clause_commas(sent)
    return sent


def fix_text(text):
    parts = re.split(r"(\u3002|\uff1f|\uff01)", text)
    result = []
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i] + parts[i + 1]
        result.append(fix_sentence(sentence))
    if len(parts) % 2 == 1 and parts[-1]:
        result.append(fix_sentence(parts[-1]))
    return "".join(result)


def process_segment(seg):
    old = seg.get("jp", "")
    changed = False
    for field in ("jp", "word"):
        val = seg.get(field, "")
        if not val:
            continue
        fixed = fix_text(val)
        if fixed != val:
            seg[field] = fixed
            changed = True
    return changed, old, seg.get("jp", "")


def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", data if isinstance(data, list) else [])
    total = 0
    changes = []

    for art in items:
        title = art.get("titleWord") or art.get("titleJp") or "?"
        segments = art.get("segments", [])
        if not segments:
            for sec in art.get("sections", []):
                segments.extend(sec.get("lines", []))

        for i, seg in enumerate(segments):
            changed, old, new = process_segment(seg)
            if changed:
                total += 1
                changes.append((title, i, old, new))

    for title, idx, old, new in changes:
        print(f"[{title}] seg[{idx}]:")
        print(f"  \u65e7: {old}")
        print(f"  \u65b0: {new}")
        print()

    print(f"\u603b\u8ba1\u4fee\u6539 {total} \u4e2a segment")

    if total > 0:
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\u5df2\u4fdd\u5b58\u5230 {DATA}")


if __name__ == "__main__":
    main()
