#!/usr/bin/env python3
"""
Tag articles with grammar points from grammar.json.
Adds a "grammar" field to each article: list of grammar IDs found in its sentences.
"""

import json
import re
import os

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), '..', 'public', 'data', 'grammar.json')
ARTICLES_PATH = os.path.join(os.path.dirname(__file__), '..', 'public', 'data', 'ja_articles.json')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {path}")

def get_article_sentences(article):
    """Extract all Japanese sentences from an article."""
    sentences = []
    if article.get('format') == 'dialogue':
        for section in article.get('sections', []):
            for seg in section.get('lines', section.get('segments', [])):
                if seg.get('jp'):
                    sentences.append(seg['jp'])
    else:
        for seg in article.get('segments', []):
            if seg.get('jp'):
                sentences.append(seg['jp'])
    return sentences


# Skip overly generic particles / single kana that match almost everything
SKIP_IDS = {
    # Single-char particles (match everything)
    'ga-1', 'ga-2', 'ka-1', 'ka-2', 'to-1-n5', 'to-2-n5',
    'na', 'ni-he', 'ni', 'no-1', 'no-2', 'ha', 'mo', 'ya',
    'de-1', 'de-2', 'to-1-n4', 'to-2-n4',
    'shi', 'sa',  # single kana
    'ki',  # 気 too generic
    'jou',  # 上 too generic
}

# Patterns that need phrase-level regex (not just substring)
# key=grammar_id, value=regex pattern to search in sentences
CUSTOM_MATCHERS = {
    'te-iru': r'ていま|ている',
    'te-kara': r'てから',
    'te-kudasai': r'てください',
    'te-wa-ikenai': r'てはいけ|ではいけ',
    'te-mo-ii': r'てもいい|でもいい',
    'naide-kudasai': r'ないでください',
    'hou-ga-ii-1': r'ほうがいい|方がいい',
    'hou-ga-ii-2': r'ないほうがいい|ない方がいい',
    'ta-koto-ga-aru': r'たことがあ',
    'no-ga-heta': r'のが下手|のがへた',
    'no-ga-jouzu': r'のが上手|のがじょうず',
    'no-ga-suki': r'のが好き|のがすき',
    'yori-no-hou-ga': r'より.*方が|より.*ほうが',
    'te-ageru': r'てあげ',
    'te-aru': r'てある|であ[りる]',
    'te-iku': r'ていく|ていき',
    'te-itadakemasenka': r'ていただけ',
    'te-iru-tokoro': r'ているところ',
    'te-oku': r'ておく|ておき|とく|とい',
    'te-kuru': r'てくる|てき[たまて]',
    'te-kureru': r'てくれ',
    'te-shimau': r'てしまう|てしまい|てしまっ|ちゃう|ちゃっ',
    'te-sumimasen': r'てすみません',
    'te-hoshii': r'てほしい|てほし[かく]',
    'te-miru': r'てみ[るたまて]',
    'te-morau': r'てもらう|てもらい|てもらっ|てもらえ',
    'te-yokatta': r'てよかった',
    'koto-ga-dekiru': r'ことができ',
    'koto-ni-suru': r'ことにす[るれ]|ことにし[たてま]',
    'koto-ni-naru': r'ことにな[るっり]',
    'ka-dou-ka': r'かどうか',
    'kamo-shirenai': r'かもしれ[なま]|かもしれません',
    'sou-da-1': r'そうで[すだ]',
    'sou-da-2': r'そうで[すだ]',
    'sugiru': r'すぎ[るてた]',
    'ta-bakari': r'たばかり',
    'te-mo': r'ても[、。]|ても[^ら]',
    'you-ni-suru': r'ようにし[てた]',
    'you-ni-naru': r'ようにな[っりる]',
    'zu-ni': r'ずに[、はい]',
    'ni-chigai-nai': r'に違いない|にちがいない',
    'to-wa-kagiranai': r'とは限らない|とはかぎらない',
    'wake-ga-nai': r'わけがない|わけがあり',
    'wake-da': r'わけだ|わけで[すは]',
    'wake-dewa-nai': r'わけではな|わけじゃな',
    'wake-ni-wa-ikanai': r'わけにはいか|わけにいか',
    'naze-nara': r'なぜなら|なぜかというと',
    'ni-tsuite': r'について',
    'ni-totte': r'にとって',
    'ni-yotte': r'によって|により|による',
    'ni-yoruto': r'によると|によれば',
    'ni-taishite': r'に対して|に対する',
    'ni-kurabete': r'に比べ[てる]|にくらべ',
    'ni-kansuru': r'に関す[るし]|に関して',
    'ni-oite': r'において|における',
}


def build_matchers(grammar_items):
    """Build a list of (grammar_id, level, compiled_regex) tuples."""
    matchers = []

    for item in grammar_items:
        gid = item['id']
        pattern = item['pattern']
        level = item['level']

        if gid in SKIP_IDS:
            continue

        # Use custom matcher if available
        if gid in CUSTOM_MATCHERS:
            rx = re.compile(CUSTOM_MATCHERS[gid])
            matchers.append((gid, level, rx))
            continue

        # Extract keywords from pattern
        p = pattern.replace('〜', '').replace('○○', '')
        variants = [v.strip() for v in p.split('/') if v.strip()]

        if not variants:
            continue

        # Skip if all variants are <= 1 char (too generic)
        if all(len(k) <= 1 for k in variants):
            continue

        regexes = []
        for kw in variants:
            escaped = re.escape(kw)
            regexes.append(escaped)

        combined = '|'.join(regexes)
        try:
            rx = re.compile(combined)
            matchers.append((gid, level, rx))
        except re.error:
            pass

    return matchers


def tag_articles():
    grammar_data = load_json(GRAMMAR_PATH)
    articles_data = load_json(ARTICLES_PATH)

    matchers = build_matchers(grammar_data['items'])
    grammar_lookup = {item['id']: item for item in grammar_data['items']}
    print(f"Built {len(matchers)} matchers from {len(grammar_data['items'])} grammar points")

    stats = {'total_articles': 0, 'total_tags': 0}

    for article in articles_data['items']:
        sentences = get_article_sentences(article)
        if not sentences:
            continue

        text = '\n'.join(sentences)
        matched_ids = []

        for gid, level, rx in matchers:
            if rx.search(text):
                matched_ids.append(gid)

        # Sort by level then id
        level_order = {'N5': 0, 'N4': 1, 'N3': 2, 'N2': 3, 'N1': 4}
        matched_ids.sort(key=lambda x: (level_order.get(grammar_lookup[x]['level'], 5), x))

        article['grammar'] = matched_ids
        stats['total_articles'] += 1
        stats['total_tags'] += len(matched_ids)

        print(f"  {article['id']}: {len(matched_ids)} grammar points")

    save_json(ARTICLES_PATH, articles_data)

    avg = stats['total_tags'] / max(stats['total_articles'], 1)
    print(f"\nDone! {stats['total_articles']} articles, avg {avg:.1f} grammar points per article")

if __name__ == '__main__':
    tag_articles()
