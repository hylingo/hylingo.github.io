#!/usr/bin/env python3
"""
Migrate article JSON to unified schema:
  segments/lines: word (source line), jp, en, zh, reading, ruby?, audioKey?
  titles: titleWord, titleJp, titleEn, titleZh, titleRuby?
  dialogue headings: headingWord, headingJp, headingEn, headingZh

Legacy: read public/data/articles.json (old jp-only schema) → ja_articles.json.
Current: to re-run migration, place an old-format export as articles.json or edit script.
Reads public/data/en_articles.json → overwrites with migrated version (expects old jp=English).

Requires: pip install deep-translator
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public" / "data"

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Install: pip install deep-translator", file=sys.stderr)
    sys.exit(1)

JA_EN = GoogleTranslator(source="ja", target="en")
EN_JA = GoogleTranslator(source="en", target="ja")
DELAY = 0.12


def tr(translator: GoogleTranslator, text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    time.sleep(DELAY)
    try:
        return translator.translate(text) or ""
    except Exception as e:
        print(f"translate error: {e!r} :: {text[:60]!r}", file=sys.stderr)
        return ""


def migrate_line_ja(seg: dict) -> dict:
    d = {k: v for k, v in seg.items() if k not in ("jp", "zh", "reading")}
    jp_text = seg["jp"]
    return {
        "word": jp_text,
        "jp": jp_text,
        "en": tr(JA_EN, jp_text),
        "zh": seg.get("zh", ""),
        "reading": seg.get("reading", ""),
        **d,
    }


def migrate_line_en(seg: dict) -> dict:
    d = {k: v for k, v in seg.items() if k not in ("jp", "zh", "reading")}
    en_text = seg["jp"]
    return {
        "word": en_text,
        "jp": tr(EN_JA, en_text),
        "en": en_text,
        "zh": seg.get("zh", ""),
        "reading": seg.get("reading", ""),
        **d,
    }


def migrate_section_ja(sec: dict) -> dict:
    hj = sec["headingJa"]
    hz = sec["headingZh"]
    out = {
        "headingWord": hj,
        "headingJp": hj,
        "headingEn": tr(JA_EN, hj),
        "headingZh": hz,
        "lines": [migrate_line_ja(line) for line in sec["lines"]],
    }
    if "badge" in sec:
        out["badge"] = sec["badge"]
    return out


def migrate_section_en(sec: dict) -> dict:
    hw = sec["headingJa"]
    hz = sec["headingZh"]
    out = {
        "headingWord": hw,
        "headingJp": tr(EN_JA, hw),
        "headingEn": hw,
        "headingZh": hz,
        "lines": [migrate_line_en(line) for line in sec["lines"]],
    }
    if "badge" in sec:
        out["badge"] = sec["badge"]
    return out


def migrate_item_ja(item: dict) -> dict:
    base = {k: v for k, v in item.items() if k not in ("titleJa", "titleZh", "segments", "sections")}
    tw = item["titleJa"]
    tzh = item["titleZh"]
    out = {
        **base,
        "titleWord": tw,
        "titleJp": tw,
        "titleEn": tr(JA_EN, tw),
        "titleZh": tzh,
    }
    if item.get("format") == "essay":
        out["segments"] = [migrate_line_ja(s) for s in item["segments"]]
    else:
        out["sections"] = [migrate_section_ja(s) for s in item["sections"]]
    return out


def migrate_item_en(item: dict) -> dict:
    base = {k: v for k, v in item.items() if k not in ("titleJa", "titleZh", "segments", "sections")}
    tw = item["titleJa"]
    tzh = item["titleZh"]
    out = {
        **base,
        "titleWord": tw,
        "titleJp": tr(EN_JA, tw),
        "titleEn": tw,
        "titleZh": tzh,
    }
    if item.get("format") == "essay":
        out["segments"] = [migrate_line_en(s) for s in item["segments"]]
    else:
        out["sections"] = [migrate_section_en(s) for s in item["sections"]]
    return out


def main() -> None:
    ja_path = PUBLIC / "articles.json"
    if not ja_path.exists():
        print(f"Skip JA: missing {ja_path} (already on ja_articles.json?)", file=sys.stderr)
        ja_doc = None
    else:
        with ja_path.open(encoding="utf-8") as f:
            ja_doc = json.load(f)
    if ja_doc is not None:
        ja_items = [migrate_item_ja(it) for it in ja_doc["items"]]
        out_ja = PUBLIC / "ja_articles.json"
        with out_ja.open("w", encoding="utf-8") as f:
            json.dump({"items": ja_items}, f, ensure_ascii=False, indent=2)
        print(f"Wrote {out_ja} ({len(ja_items)} items)")

    en_path = PUBLIC / "en_articles.json"
    with en_path.open(encoding="utf-8") as f:
        en_doc = json.load(f)
    items = en_doc.get("items") or []
    if items and "titleJa" in items[0]:
        en_items = [migrate_item_en(it) for it in items]
        with en_path.open("w", encoding="utf-8") as f:
            json.dump({"items": en_items}, f, ensure_ascii=False, indent=2)
        print(f"Updated {en_path} ({len(en_items)} items)")
    else:
        print(f"Skip EN: {en_path} already uses titleWord schema", file=sys.stderr)


if __name__ == "__main__":
    main()
