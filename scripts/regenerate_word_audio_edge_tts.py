#!/usr/bin/env python3
"""
用 Edge TTS 重录单词 mp3（女声 ja-JP-NanamiNeural），落到 audio/jp/<hash>.mp3。

复用 nouns.json 中既有的 audio 字段（jp/xxx.mp3）做文件名，前端 / audio_map.json 不需要改。
合成文本优先用 reading（假名），缺失时回退 word。

用法:
  pip install -r requirements-edge-tts.txt
  python scripts/regenerate_word_audio_edge_tts.py --dry-run
  python scripts/regenerate_word_audio_edge_tts.py --concurrency 8
  python scripts/regenerate_word_audio_edge_tts.py --start 0 --limit 500   # 分批
  python scripts/regenerate_word_audio_edge_tts.py --upload                # 跑完后自动 rclone 上传

断点续传：默认 --skip-existing，本地已存在的 mp3 不重录。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
NOUNS_PATH = ROOT / "public" / "data" / "nouns.json"
VERBS_PATH = ROOT / "public" / "data" / "verbs.json"
AUDIO_DIR = ROOT / "audio"

VOICE = "ja-JP-NanamiNeural"
RATE = "-5%"        # 稍慢，单词更清楚
PITCH = "+0Hz"
RCLONE_REMOTE = "r2:hylingo-audio"


def load_words() -> list[dict]:
    items: list[dict] = []
    for path in (NOUNS_PATH, VERBS_PATH):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(data, list):
            continue
        for entry in data:
            audio = entry.get("audio")
            word = entry.get("word")
            if not audio or not word:
                continue
            text = entry.get("reading") or word
            items.append({"word": word, "text": text, "audio": audio})
    # 去重（按 audio 路径）
    seen = set()
    unique: list[dict] = []
    for it in items:
        if it["audio"] in seen:
            continue
        seen.add(it["audio"])
        unique.append(it)
    return unique


async def synth_one(item: dict, sem: asyncio.Semaphore, skip_existing: bool, retries: int = 3) -> tuple[str, str]:
    """返回 (status, word)。status: ok/skip/fail"""
    rel = item["audio"]                       # 例 jp/abc123.mp3
    out_path = AUDIO_DIR / rel
    if skip_existing and out_path.exists() and out_path.stat().st_size > 0:
        return ("skip", item["word"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    async with sem:
        for attempt in range(1, retries + 1):
            try:
                comm = edge_tts.Communicate(
                    text=item["text"],
                    voice=VOICE,
                    rate=RATE,
                    pitch=PITCH,
                )
                tmp = out_path.with_suffix(".mp3.part")
                await comm.save(str(tmp))
                if tmp.stat().st_size == 0:
                    raise RuntimeError("empty mp3")
                tmp.replace(out_path)
                return ("ok", item["word"])
            except Exception as e:
                if attempt == retries:
                    print(f"  ✗ {item['word']} ({item['text']}): {e}", file=sys.stderr)
                    return ("fail", item["word"])
                await asyncio.sleep(1.5 * attempt)
    return ("fail", item["word"])


async def run(items: list[dict], concurrency: int, skip_existing: bool) -> tuple[int, int, int]:
    sem = asyncio.Semaphore(concurrency)
    tasks = [synth_one(it, sem, skip_existing) for it in items]
    ok = skip = fail = 0
    done = 0
    total = len(tasks)
    for fut in asyncio.as_completed(tasks):
        status, word = await fut
        done += 1
        if status == "ok":
            ok += 1
        elif status == "skip":
            skip += 1
        else:
            fail += 1
        if done % 25 == 0 or done == total:
            print(f"  [{done}/{total}] ok={ok} skip={skip} fail={fail}")
    return ok, skip, fail


def upload_to_r2() -> None:
    src = AUDIO_DIR / "jp"
    if not src.exists():
        print("没有 audio/jp 目录，跳过上传")
        return
    cmd = [
        "rclone", "copy", str(src) + "/",
        f"{RCLONE_REMOTE}/jp/",
        "--transfers", "16",
        "--checkers", "16",
        "--progress",
    ]
    print("上传:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--start", type=int, default=0, help="从第 N 条开始（分批用）")
    ap.add_argument("--limit", type=int, default=0, help="最多处理 N 条，0=全部")
    ap.add_argument("--no-skip-existing", action="store_true", help="不跳过已存在的本地 mp3")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--upload", action="store_true", help="跑完后 rclone 上传到 R2")
    args = ap.parse_args()

    items = load_words()
    print(f"词总数: {len(items)}")

    sliced = items[args.start:]
    if args.limit > 0:
        sliced = sliced[: args.limit]
    print(f"本批: start={args.start} count={len(sliced)} 并发={args.concurrency} 音色={VOICE}")

    if args.dry_run:
        for it in sliced[:10]:
            print(f"  - {it['word']}  →  {it['text']}  →  audio/{it['audio']}")
        print("(dry-run，未生成)")
        return

    AUDIO_DIR.mkdir(exist_ok=True)
    ok, skip, fail = asyncio.run(
        run(sliced, args.concurrency, skip_existing=not args.no_skip_existing)
    )
    print(f"完成: ok={ok} skip={skip} fail={fail}")

    if args.upload and fail == 0:
        upload_to_r2()
    elif args.upload:
        print("有失败，跳过上传；修复后可单独跑：")
        print(f"  rclone copy audio/jp/ {RCLONE_REMOTE}/jp/ --transfers 16 --progress")


if __name__ == "__main__":
    main()
