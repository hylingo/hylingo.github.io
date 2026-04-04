#!/usr/bin/env python3
"""
根据英文原文为 public/data/en_articles.json 写入/刷新日语字段：
  titleWord → titleJp
  headingWord → headingJp
  segment/line word → jp

默认只补全「jp 为空」的条目；加 --force 则全部重译。

依赖: pip install deep-translator

示例:
  python scripts/translate_en_articles_jp.py
  python scripts/translate_en_articles_jp.py --batch-save 10 --delay 0.2
  python scripts/translate_en_articles_jp.py --force --batch-save 15
  python scripts/translate_en_articles_jp.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "public" / "data" / "en_articles.json"


def main() -> None:
    ap = argparse.ArgumentParser(description="EN→JA for en_articles.json jp fields")
    ap.add_argument("--path", type=Path, default=DEFAULT_PATH, help="en_articles.json path")
    ap.add_argument("--force", action="store_true", help="Re-translate even when jp already set")
    ap.add_argument("--delay", type=float, default=0.15, help="Seconds between Google requests")
    ap.add_argument(
        "--batch-save",
        type=int,
        default=12,
        help="Write JSON to disk after this many successful translations",
    )
    ap.add_argument("--dry-run", action="store_true", help="Count jobs only, no API / no write")
    args = ap.parse_args()

    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("pip install deep-translator", file=sys.stderr)
        sys.exit(1)

    translator = GoogleTranslator(source="en", target="ja")
    path: Path = args.path
    if not path.exists():
        print(f"Missing {path}", file=sys.stderr)
        sys.exit(1)

    with path.open(encoding="utf-8") as f:
        doc = json.load(f)

    items = doc.get("items") or []

    def need_jp(current: str) -> bool:
        return args.force or not (current or "").strip()

    jobs: list[tuple[str, callable]] = []

    def add_job(en_text: str, setter) -> None:
        en_text = (en_text or "").strip()
        if not en_text:
            return
        jobs.append((en_text, setter))

    for item in items:
        if need_jp(item.get("titleJp", "")):
            add_job(item.get("titleWord", ""), lambda t, v=item: v.__setitem__("titleJp", t))

        if item.get("format") == "essay":
            for seg in item.get("segments") or []:
                if need_jp(seg.get("jp", "")):
                    add_job(seg.get("word", ""), lambda t, s=seg: s.__setitem__("jp", t))
        else:
            for sec in item.get("sections") or []:
                if need_jp(sec.get("headingJp", "")):
                    add_job(sec.get("headingWord", ""), lambda t, s=sec: s.__setitem__("headingJp", t))
                for line in sec.get("lines") or []:
                    if need_jp(line.get("jp", "")):
                        add_job(line.get("word", ""), lambda t, ln=line: ln.__setitem__("jp", t))

    print(f"Jobs: {len(jobs)} (force={args.force}, dry_run={args.dry_run})")
    if args.dry_run:
        return

    if not jobs:
        print("Nothing to do.")
        return

    done = 0
    for i, (text, setter) in enumerate(jobs):
        time.sleep(args.delay)
        try:
            ja = translator.translate(text) or ""
        except Exception as e:
            print(f"[{i + 1}/{len(jobs)}] ERROR: {e!r} :: {text[:70]!r}...", file=sys.stderr)
            continue
        setter(ja)
        done += 1
        print(f"[{i + 1}/{len(jobs)}] ok ({done} done)")
        if done % args.batch_save == 0:
            with path.open("w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
            print(f"  … saved checkpoint ({done} translations)")

    with path.open("w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"Done. Wrote {path} ({done} translations).")


if __name__ == "__main__":
    main()
