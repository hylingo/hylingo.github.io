#!/usr/bin/env python3
"""
为学英语语料写入 meaningJp：根据英文 word 做 EN→JA 翻译。

目标文件:
  public/data/en_sentences.json
  public/data/en_nouns.json

默认只补全「meaningJp 为空」的条目；--force 则全部重译。

依赖: pip install deep-translator

示例:
  python scripts/fill_meaning_jp_en_vocab.py --both
  python scripts/fill_meaning_jp_en_vocab.py --sentences --batch-save 15 --delay 0.15
  python scripts/fill_meaning_jp_en_vocab.py --nouns --max-items 100 --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SENTENCES_PATH = ROOT / "public" / "data" / "en_sentences.json"
NOUNS_PATH = ROOT / "public" / "data" / "en_nouns.json"


def process_file(
    path: Path,
    translator,
    *,
    force: bool,
    delay: float,
    batch_save: int,
    dry_run: bool,
    max_items: int | None,
) -> tuple[int, int]:
    if not path.exists():
        print(f"Missing {path}", file=sys.stderr)
        return 0, 0

    with path.open(encoding="utf-8") as f:
        rows: list[dict] = json.load(f)

    def need_jp(current: str) -> bool:
        return force or not (current or "").strip()

    jobs: list[tuple[str, object]] = []
    for obj in rows:
        if not need_jp(obj.get("meaningJp", "")):
            continue
        text = (obj.get("word") or "").strip()
        if not text:
            continue
        jobs.append((text, obj))

    if max_items is not None:
        jobs = jobs[: max(0, max_items)]

    print(f"{path.name}: jobs={len(jobs)} (force={force}, dry_run={dry_run})", flush=True)
    if dry_run:
        return len(jobs), 0

    if not jobs:
        print(f"  Nothing to do for {path.name}.", flush=True)
        return 0, 0

    done = 0
    for i, (text, obj) in enumerate(jobs):
        time.sleep(delay)
        try:
            ja = translator.translate(text) or ""
        except Exception as e:
            print(f"  [{i + 1}/{len(jobs)}] ERROR: {e!r} :: {text[:80]!r}...", file=sys.stderr)
            continue
        obj["meaningJp"] = ja
        done += 1
        print(f"  [{i + 1}/{len(jobs)}] ok ({done} done)", flush=True)
        if done % batch_save == 0:
            with path.open("w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
            print(f"  … checkpoint saved ({done} translations)", flush=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path} ({done} translations).", flush=True)
    return len(jobs), done


def main() -> None:
    ap = argparse.ArgumentParser(description="Fill meaningJp for en_sentences / en_nouns")
    ap.add_argument("--sentences", action="store_true", help="Process en_sentences.json")
    ap.add_argument("--nouns", action="store_true", help="Process en_nouns.json")
    ap.add_argument("--both", action="store_true", help="Process both files")
    ap.add_argument("--force", action="store_true", help="Re-translate even when meaningJp is set")
    ap.add_argument("--delay", type=float, default=0.15, help="Seconds between Google requests")
    ap.add_argument(
        "--batch-save",
        type=int,
        default=12,
        help="Write JSON after this many successful translations",
    )
    ap.add_argument("--dry-run", action="store_true", help="Count jobs only, no API / no write")
    ap.add_argument("--max-items", type=int, default=None, help="Cap translations per file (debug)")
    args = ap.parse_args()

    do_sentences = args.both or args.sentences
    do_nouns = args.both or args.nouns
    if not do_sentences and not do_nouns:
        ap.print_help()
        print("\nSpecify --sentences, --nouns, or --both.", file=sys.stderr)
        sys.exit(1)

    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("pip install deep-translator", file=sys.stderr)
        sys.exit(1)

    translator = GoogleTranslator(source="en", target="ja")
    total_jobs = 0
    total_done = 0
    if do_sentences:
        j, d = process_file(
            SENTENCES_PATH,
            translator,
            force=args.force,
            delay=args.delay,
            batch_save=args.batch_save,
            dry_run=args.dry_run,
            max_items=args.max_items,
        )
        total_jobs += j
        total_done += d
    if do_nouns:
        j, d = process_file(
            NOUNS_PATH,
            translator,
            force=args.force,
            delay=args.delay,
            batch_save=args.batch_save,
            dry_run=args.dry_run,
            max_items=args.max_items,
        )
        total_jobs += j
        total_done += d

    if args.dry_run:
        print(f"Dry run: {total_jobs} jobs total.", flush=True)
    else:
        print(f"Done. {total_done} translations written (of {total_jobs} jobs).", flush=True)


if __name__ == "__main__":
    main()
