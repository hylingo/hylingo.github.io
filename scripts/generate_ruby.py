#!/usr/bin/env python3
"""
Generate ruby (furigana) data for Japanese sentences.
Adds a 'ruby' field to each sentence/segment: an array of {t, r?} objects.

Segmentation strategy:
- Uses MeCab (fugashi) for word-level tokenization
- Kanji words get hiragana readings
- Particles and auxiliary verbs stay as individual tokens
- Adjacent katakana tokens merge (e.g. マイ+ナンバー+カード → マイナンバーカード)
- Adjacent plain hiragana tokens merge (e.g. すみ+ませ+ん → すみません)
- Punctuation stays separate
"""

import json
import sys
import fugashi

tagger = fugashi.Tagger()


def to_hira(kata: str) -> str:
    """Convert katakana to hiragana."""
    return ''.join(
        chr(ord(c) - 96) if '\u30A1' <= c <= '\u30F6' else c
        for c in kata
    )


def has_kanji(s: str) -> bool:
    return any('\u4e00' <= c <= '\u9fff' for c in s)


def _is_katakana(c: str) -> bool:
    return '\u30A0' <= c <= '\u30FF' or c == 'ー'


def make_ruby(sentence: str) -> list[dict]:
    """Parse a Japanese sentence into ruby tokens with word-level granularity."""
    words = tagger(sentence)
    raw: list[dict] = []

    for w in words:
        surface = w.surface
        if not surface:
            continue

        pos1 = w.feature.pos1 if hasattr(w.feature, 'pos1') else ''
        reading = to_hira(w.feature.kana) if w.feature.kana else None

        has_k = has_kanji(surface)
        is_all_kata = all(_is_katakana(c) for c in surface) and len(surface) > 0
        is_particle = pos1 == '助詞'
        is_aux = pos1 == '助動詞'

        token: dict = {'t': surface}
        if has_k and reading and reading != surface:
            token['r'] = reading

        # Classify token type for merge decisions
        if has_k:
            tp = 'kanji'
        elif is_all_kata:
            tp = 'kata'
        elif is_particle:
            tp = 'particle'
        elif is_aux:
            tp = 'aux'
        else:
            tp = 'hira'

        token['_type'] = tp
        raw.append(token)

    # Merge adjacent tokens of the same "mergeable" type
    merged: list[dict] = []
    for token in raw:
        tp = token['_type']
        clean: dict = {'t': token['t']}
        if 'r' in token:
            clean['r'] = token['r']

        # Merge adjacent katakana tokens
        if tp == 'kata' and merged and merged[-1].get('_type') == 'kata':
            merged[-1]['t'] += clean['t']
            continue

        # Merge adjacent plain hiragana tokens (not particles/aux)
        if tp == 'hira' and merged and merged[-1].get('_type') == 'hira':
            merged[-1]['t'] += clean['t']
            continue

        clean['_type'] = tp
        merged.append(clean)

    # Strip internal type markers
    for m in merged:
        m.pop('_type', None)

    return merged


def full_reading(sentence: str) -> str:
    """Generate full hiragana reading for a sentence."""
    parts: list[str] = []
    for w in tagger(sentence):
        k = w.feature.kana
        parts.append(to_hira(k) if k else w.surface)
    return ''.join(parts)


def process_articles(path: str):
    """Add ruby to ja_articles.json segments."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for item in data['items']:
        for seg in item.get('segments', []):
            text = (seg.get('word') or seg.get('jp') or '').strip()
            seg['ruby'] = make_ruby(text) if text else []
            count += 1
        for sec in item.get('sections', []):
            for line in sec.get('lines', []):
                text = (line.get('word') or line.get('jp') or '').strip()
                line['ruby'] = make_ruby(text) if text else []
                count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Articles: processed {count} segments')


def process_sentences(path: str):
    """Add ruby to sentences.json."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for item in data:
        item['ruby'] = make_ruby(item['word'])
        count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Sentences: processed {count} items')


def process_nouns(path: str):
    """Add ruby to nouns.json."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    for item in data:
        item['ruby'] = make_ruby(item['word'])
        count += 1

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Nouns: processed {count} items')


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    base = 'public/data'

    if target in ('articles', 'all'):
        process_articles(f'{base}/ja_articles.json')
    if target in ('sentences', 'all'):
        process_sentences(f'{base}/sentences.json')
    if target in ('nouns', 'all'):
        process_nouns(f'{base}/nouns.json')
