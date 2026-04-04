#!/usr/bin/env python3
"""
枚举 Edge TTS 中所有日语（ja-JP）音色，并为每个音色生成一段示例 MP3，便于对比试听。

依赖: pip install -r requirements-edge-tts.txt

用法:
  python scripts/generate_edge_tts_ja_voice_samples.py
  python scripts/generate_edge_tts_ja_voice_samples.py --text "おはようございます。"
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import sys

import edge_tts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "audio", "edge_tts_ja_voice_samples")

DEFAULT_TEXT = (
    "こんにちは。これはエッジの日本語読み上げのサンプルです。"
    "発音の違いを比べてみてください。"
)


def _slug_short_name(short_name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", short_name.strip())
    return s.strip("_") or "voice"


async def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one MP3 per ja-JP Edge TTS voice.")
    parser.add_argument(
        "--text",
        default=DEFAULT_TEXT,
        help="Sample sentence (Japanese).",
    )
    parser.add_argument(
        "--out-dir",
        default=OUT_DIR,
        help="Output directory for MP3 files.",
    )
    args = parser.parse_args()

    voices = await edge_tts.list_voices()
    ja = [v for v in voices if str(v.get("Locale", "")).lower().startswith("ja-jp")]
    if not ja:
        print("No ja-JP voices found.", file=sys.stderr)
        return 1

    os.makedirs(args.out_dir, exist_ok=True)
    print(f"Found {len(ja)} ja-JP voice(s). Writing to {args.out_dir}\n")

    for v in sorted(ja, key=lambda x: x.get("ShortName", "")):
        short = v.get("ShortName", "")
        gender = v.get("Gender", "")
        name = v.get("FriendlyName", short)
        slug = _slug_short_name(short.replace("ja-JP-", ""))
        out_path = os.path.join(args.out_dir, f"{slug}.mp3")
        print(f"  {short}  ({gender})  {name}")
        communicate = edge_tts.Communicate(args.text, short)
        await communicate.save(out_path)

    print(f"\nDone. Open folder: {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
