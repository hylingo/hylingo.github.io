#!/usr/bin/env python3
"""
为重写的文章生成女声音频（Fish Audio）。
只生成 audio 字段（女声），不生成 audioMale。

用法:
  export FISH_API_KEY=xxx
  python scripts/generate_audio_rewrite8.py --batch 1 --dry-run   # 预览前4篇
  python scripts/generate_audio_rewrite8.py --batch 1              # 生成前4篇
  python scripts/generate_audio_rewrite8.py --batch 2              # 生成后4篇
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JA_PATH = os.path.join(ROOT, "public", "data", "ja_articles.json")
AUDIO_MAP_PATH = os.path.join(ROOT, "public", "data", "audio_map.json")
AUDIO_DIR = os.path.join(ROOT, "audio")

FISH_API_URL = "https://api.fish.audio/v1/tts"
# 元気な女性（女声）
FISH_MODEL_ID = "5161d41404314212af1254556477c17d"

BATCH_1 = [
    "n3-apartment-essay",
    "n3-airport-domestic-essay",
    "n3-interview-essay",
    "n3-accident-essay",
]
BATCH_2 = [
    "n4-first-bus-essay",
    "n4-first-cooking-essay",
    "n4-home-center-essay",
    "n4-unpack-boxes-essay",
]


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "")
    if not key:
        print("错误: 请设置 FISH_API_KEY")
        sys.exit(1)
    return key


def text_to_rel(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"jp/{h}.mp3"


def synthesize(api_key: str, text: str, output_path: str) -> bool:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    payload = {
        "text": text,
        "reference_id": FISH_MODEL_ID,
        "format": "mp3",
        "latency": "normal",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    for attempt in range(3):
        try:
            resp = requests.post(FISH_API_URL, json=payload, headers=headers, timeout=60)
            if resp.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                return True
            elif resp.status_code == 429:
                wait = 5 * (attempt + 1)
                print(f"  限流, 等待{wait}秒...", flush=True)
                time.sleep(wait)
                continue
            else:
                print(f"  API错误 {resp.status_code}: {resp.text[:200]}")
                return False
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
                continue
            print(f"  请求异常: {e}")
            return False
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, required=True, choices=[1, 2], help="1=前4篇 2=后4篇")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    target_ids = BATCH_1 if args.batch == 1 else BATCH_2

    with open(JA_PATH, "r", encoding="utf-8") as f:
        ja = json.load(f)
    with open(AUDIO_MAP_PATH, "r", encoding="utf-8") as f:
        audio_map: dict = json.load(f)

    # 收集待生成
    plan: list[tuple[str, str, dict, str]] = []  # (text, rel, seg_ref, title)
    total_chars = 0
    for item in ja["items"]:
        if item["id"] not in target_ids:
            continue
        title = item.get("titleWord", item["id"])
        for seg in item.get("segments", []):
            text = (seg.get("jp") or seg.get("word") or "").strip()
            if not text:
                continue
            if seg.get("audio"):  # 已有音频，跳过
                continue
            rel = text_to_rel(text)
            plan.append((text, rel, seg, title))
            total_chars += len(text)

    print(f"Batch {args.batch}: {len(plan)} 句, {total_chars} 字")

    if args.dry_run:
        for i, (text, rel, _, title) in enumerate(plan):
            print(f"  [{i+1}/{len(plan)}] [{title}] {rel} <- {text[:40]}")
        print(f"\n[dry-run] 预计字符数: {total_chars}")
        return

    if not plan:
        print("无待生成项。")
        return

    api_key = get_api_key()
    ok = fail = 0

    for i, (text, rel, seg, title) in enumerate(plan):
        out = os.path.join(AUDIO_DIR, rel.replace("/", os.sep))
        print(f"  [{i+1}/{len(plan)}] {title}: {text[:30]}...", end=" ", flush=True)
        if synthesize(api_key, text, out):
            seg["audio"] = rel
            audio_map[text] = rel
            ok += 1
            print("✓")
        else:
            fail += 1
            print("✗")
        time.sleep(0.3)  # 避免限流

    # 写回
    with open(JA_PATH, "w", encoding="utf-8") as f:
        json.dump(ja, f, ensure_ascii=False, indent=2)
    with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(audio_map, f, ensure_ascii=False, indent=2)

    print(f"\n完成: {ok} 成功, {fail} 失败")
    print(f"上传: rclone copy audio/jp/ r2:hylingo-audio/jp/ --transfers 32 --progress")


if __name__ == "__main__":
    main()
