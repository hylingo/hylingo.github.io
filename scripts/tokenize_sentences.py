#!/usr/bin/env python3
"""为 sentences.json 每条句子做分词，并标记语法点对应的 token 范围。

用法：python scripts/tokenize_sentences.py
依赖：fugashi, unidic-lite
"""

import json
import re
from pathlib import Path
from fugashi import Tagger

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "data" / "sentences.json"

tagger = Tagger()

# 助词等粘附前面的词，不单独成 token（显示时无间隙）
ATTACH_POS = {"助詞", "助動詞", "補助記号", "接尾辞"}


def tokenize(sentence: str) -> list[dict]:
    """分词并合并助词到前一个词，返回 [{text, base}]"""
    raw = tagger(sentence)
    tokens: list[dict] = []
    for node in raw:
        surface = node.surface
        pos1 = node.feature.pos1 if node.feature else ""
        base = str(node.feature.lemma) if node.feature and node.feature.lemma else surface

        # 助词/助动词/标点/接尾辞 粘到前一个 token
        if pos1 in ATTACH_POS and tokens:
            tokens[-1]["text"] += surface
            # base 不合并，保留主词的 base
        else:
            tokens.append({"text": surface, "base": base})

    return tokens


def match_grammar_spans(tokens: list[dict], grammar: list[dict], sentence: str) -> list[dict]:
    """为每个 grammar point 找到它在 tokens 里高亮的 index 范围。

    策略：用 grammar 的 regex pattern 在原句中找到匹配位置，
    然后映射回 token index。
    """
    if not grammar:
        return grammar

    # 每个 token 在原句中的 start/end 位置
    positions: list[tuple[int, int]] = []
    offset = 0
    for tk in tokens:
        txt = tk["text"]
        idx = sentence.find(txt, offset)
        if idx == -1:
            idx = offset
        positions.append((idx, idx + len(txt)))
        offset = idx + len(txt)

    # 从 add_grammar.py 加载 pattern -> regex 的映射
    from add_grammar import GRAMMAR as GRAMMAR_RULES

    pattern_to_regex: dict[str, str] = {}
    for regex_str, disp, *_ in GRAMMAR_RULES:
        if disp not in pattern_to_regex:
            pattern_to_regex[disp] = regex_str

    result = []
    for g in grammar:
        g_copy = {**g}
        regex_str = pattern_to_regex.get(g["pattern"])
        if regex_str:
            m = re.search(regex_str, sentence)
            if m:
                ms, me = m.start(), m.end()
                # 找到覆盖的 token indices
                indices = []
                for i, (ts, te) in enumerate(positions):
                    if te > ms and ts < me:
                        indices.append(i)
                if indices:
                    g_copy["highlight"] = indices
        result.append(g_copy)
    return result


def main():
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))

    data = json.loads(SRC.read_text("utf-8"))
    total = len(data)
    tokenized = 0

    for item in data:
        sentence = item["word"]
        tokens = tokenize(sentence)

        # 只存 text 列表（base 暂时不需要在前端用）
        item["tokens"] = [t["text"] for t in tokens]

        # 如果有 grammar，计算高亮 indices
        if item.get("grammar"):
            item["grammar"] = match_grammar_spans(tokens, item["grammar"], sentence)

        tokenized += 1

    SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"Done: {tokenized}/{total} sentences tokenized.")

    # 统计
    highlighted = sum(1 for it in data if any(g.get("highlight") for g in it.get("grammar", [])))
    print(f"Grammar with highlight indices: {highlighted}")

    # 示例
    for item in data:
        if item.get("grammar") and any(g.get("highlight") for g in item["grammar"]):
            print(f"\n例: {item['word']}")
            print(f"  tokens: {item['tokens']}")
            for g in item["grammar"]:
                print(f"  {g['pattern']} -> highlight={g.get('highlight', [])}")
            break


if __name__ == "__main__":
    main()
