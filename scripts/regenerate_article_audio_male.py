#!/usr/bin/env python3
"""
为「N2 及以下」精读文章中的句子，用男声（ja-JP-KeitaNeural）另存一份 MP3，
并写入 public/data/article_audio_map_male.json（键为日文句，值为文件名）。

仅处理已在 audio_map.json 中有条目的句子（与现有女声资源一一对应）。
文件名与女声不同：sha256(句 + 固定盐)[:12].mp3，避免覆盖。

依赖: pip install -r requirements-edge-tts.txt

用法:
  python scripts/regenerate_article_audio_male.py
  python scripts/regenerate_article_audio_male.py --dry-run
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import sys

import edge_tts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_PATH = os.path.join(ROOT, "public", "data", "ja_articles.json")
AUDIO_MAP_PATH = os.path.join(ROOT, "public", "data", "audio_map.json")
OUT_MAP_PATH = os.path.join(ROOT, "public", "data", "article_audio_map_male.json")
AUDIO_DIR = os.path.join(ROOT, "public", "audio")
VOICE = "ja-JP-KeitaNeural"
MALE_HASH_SALT = "\nedge-tts:ja-JP-KeitaNeural"
CONCURRENCY = 3


def make_filename_male(text: str) -> str:
    h = hashlib.sha256((text + MALE_HASH_SALT).encode("utf-8")).hexdigest()[:12]
    return f"{h}.mp3"


def article_jp_lines(item: dict) -> list[str]:
    out: list[str] = []
    if item.get("format") == "essay":
        for seg in item.get("segments") or []:
            text = (seg.get("word") or seg.get("jp") or "").strip()
            if text:
                out.append(text)
    else:
        for sec in item.get("sections") or []:
            for line in sec.get("lines") or []:
                text = (line.get("word") or line.get("jp") or "").strip()
                if text:
                    out.append(text)
    return out


def include_article_for_n2_or_below(item: dict) -> bool:
    """N1 篇不包含；其余（含 N2、N5–N3 等）视为 N2 及以下。"""
    return (item.get("level") or "").strip() != "N1"


def collect_targets() -> list[str]:
    with open(ARTICLES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items") or []
    with open(AUDIO_MAP_PATH, "r", encoding="utf-8") as f:
        audio_map: dict[str, str] = json.load(f)

    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if not include_article_for_n2_or_below(item):
            continue
        for jp in article_jp_lines(item):
            if jp in seen:
                continue
            if jp not in audio_map:
                print(f"skip (no audio_map key): {jp[:48]}…", file=sys.stderr)
                continue
            seen.add(jp)
            ordered.append(jp)
    return ordered


async def _one(
    sem: asyncio.Semaphore,
    text: str,
    target_fn: str,
    idx: int,
    total: int,
    dry_run: bool,
) -> tuple[str, bool, str]:
    path = os.path.join(AUDIO_DIR, target_fn)
    if dry_run:
        print(f"[{idx + 1}/{total}] dry-run -> {target_fn}")
        return (text, True, "")
    async with sem:
        try:
            tts = edge_tts.Communicate(text, VOICE)
            await tts.save(path)
            print(f"[{idx + 1}/{total}] ok {target_fn}", flush=True)
            return (text, True, "")
        except Exception as e:
            return (text, False, str(e))


async def main_async(args: argparse.Namespace) -> int:
    os.chdir(ROOT)
    texts = collect_targets()
    if not texts:
        print("No sentences to synthesize.", file=sys.stderr)
        return 1

    planned: list[tuple[str, str]] = []
    seen_fn: dict[str, str] = {}
    for t in texts:
        fn = make_filename_male(t)
        if fn in seen_fn and seen_fn[fn] != t:
            print(f"hash collision: {fn}", file=sys.stderr)
            return 1
        seen_fn[fn] = t
        planned.append((t, fn))

    print(f"Voice: {VOICE} | sentences: {len(planned)}\n")

    if not args.dry_run:
        os.makedirs(AUDIO_DIR, exist_ok=True)

    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [
        _one(sem, text, fn, i, len(planned), args.dry_run)
        for i, (text, fn) in enumerate(planned)
    ]
    results = await asyncio.gather(*tasks)
    failed = [(t, err) for t, ok, err in results if not ok]
    if failed:
        print(f"\n失败 {len(failed)} 条:", file=sys.stderr)
        for t, err in failed[:15]:
            print(f"  {t[:40]}… -> {err}", file=sys.stderr)
        return 1

    out_map = {text: fn for text, fn in planned}
    if not args.dry_run:
        with open(OUT_MAP_PATH, "w", encoding="utf-8") as f:
            json.dump(out_map, f, ensure_ascii=False, separators=(",", ":"))
        print(f"\nWrote {OUT_MAP_PATH} ({len(out_map)} keys).")

    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Edge TTS 男声：N2 及以下文章句")
    p.add_argument("--dry-run", action="store_true", help="只打印计划，不写文件")
    args = p.parse_args()
    raise SystemExit(asyncio.run(main_async(args)))


if __name__ == "__main__":
    main()
