#!/usr/bin/env python3
"""
Generate ruby (furigana) data for Japanese sentences.
Adds a 'ruby' field to each sentence/segment: an array of {t, r?} objects.
Only kanji characters get ruby annotations.
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


def make_ruby(sentence: str) -> list[dict]:
    """Parse a Japanese sentence into ruby tokens."""
    result = []
    for word in tagger(sentence):
        surface = word.surface
        reading = word.feature.kana or ''

        if has_kanji(surface) and reading:
            hira = to_hira(reading)
            # Split kanji prefix from kana suffix
            # e.g. 食べ -> kanji=食, suffix=べ, ruby=た
            kanji_end = -1
            for j in range(len(surface) - 1, -1, -1):
                if '\u4e00' <= surface[j] <= '\u9fff':
                    kanji_end = j
                    break

            # Also check for kana prefix (e.g. お願い -> prefix=お, kanji=願, suffix=い)
            kanji_start = 0
            for j in range(len(surface)):
                if '\u4e00' <= surface[j] <= '\u9fff':
                    kanji_start = j
                    break

            kana_prefix = surface[:kanji_start]
            kanji_part = surface[kanji_start:kanji_end + 1]
            kana_suffix = surface[kanji_end + 1:]

            if kana_prefix:
                result.append({'t': kana_prefix})

            if kanji_part:
                # Trim matching prefix/suffix from reading
                ruby_reading = hira
                if kana_prefix and ruby_reading.startswith(to_hira(kana_prefix) if any('\u30A1' <= c <= '\u30F6' for c in kana_prefix) else kana_prefix):
                    ruby_reading = ruby_reading[len(kana_prefix):]
                elif kana_prefix:
                    ruby_reading = ruby_reading[len(kana_prefix):]
                if kana_suffix and ruby_reading.endswith(kana_suffix):
                    ruby_reading = ruby_reading[:-len(kana_suffix)]

                result.append({'t': kanji_part, 'r': ruby_reading})

            if kana_suffix:
                result.append({'t': kana_suffix})
        else:
            result.append({'t': surface})

    # Merge consecutive non-ruby items
    merged = []
    for item in result:
        if 'r' not in item and merged and 'r' not in merged[-1]:
            merged[-1]['t'] += item['t']
        else:
            merged.append(item)
    return merged


def process_articles(path: str):
    """Add ruby to ja_articles.json segments (Japanese text in `word`)."""
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
