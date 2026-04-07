#!/usr/bin/env python3
"""
Fish Audio TTS — 仅为本轮新增的 N2 文章生成音频。

按文章 id 过滤，不依赖本地文件存在性判断。
生成后写回 ja_articles.json 的 audio 字段、更新 audio_map.json。

用法:
  export FISH_API_KEY=xxx
  python scripts/generate_audio_fish_n2_batch.py --dry-run
  python scripts/generate_audio_fish_n2_batch.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JA_PATH = os.path.join(ROOT, "public", "data", "ja_articles.json")
AUDIO_MAP_PATH = os.path.join(ROOT, "public", "data", "audio_map.json")
AUDIO_DIR = os.path.join(ROOT, "audio")

FISH_API_URL = "https://api.fish.audio/v1/tts"
FISH_MODEL_ID = "5161d41404314212af1254556477c17d"  # 比留間大地

# 本轮要生成的文章 id
TARGET_IDS = {
    "n2-grammar-travel-essay",
    "n2-grammar-travel-dialogue",
    "n2-grammar-work-essay",
    "n2-grammar-work-dialogue",
    "n2-grammar-study-essay",
    "n2-grammar-study-dialogue",
    "n2-grammar-society-essay",
    "n2-grammar-society-dialogue",
    "n2-grammar-tech-essay",
    "n2-grammar-tech-dialogue",
    "n2-grammar-health-essay",
    "n2-grammar-health-dialogue",
    "n2-grammar-environment-essay",
    "n2-grammar-environment-dialogue",
    "n2-grammar-culture-essay",
    "n2-grammar-culture-dialogue",
    "n2-grammar-relationship-essay",
    "n2-grammar-relationship-dialogue",
    "n2-reading-books-no-longer-read",
    "n2-reading-too-punctual-country",
}


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "")
    if not key:
        print("错误: 请设置 FISH_API_KEY")
        sys.exit(1)
    return key


def text_to_rel(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"jp/{h}.mp3"


def disk_path(rel: str) -> str:
    return os.path.join(AUDIO_DIR, rel.replace("/", os.sep))


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


def iter_target_segments(data: dict):
    """只 yield 在 TARGET_IDS 里的文章的 segments/lines。"""
    for item in data.get("items") or []:
        if item.get("id") not in TARGET_IDS:
            continue
        title = item.get("titleWord") or item.get("id")
        if item.get("format") == "essay":
            for seg in item.get("segments") or []:
                yield seg, title
        else:
            for sec in item.get("sections") or []:
                for line in sec.get("lines") or []:
                    yield line, title


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()

    with open(JA_PATH, "r", encoding="utf-8") as f:
        ja = json.load(f)
    with open(AUDIO_MAP_PATH, "r", encoding="utf-8") as f:
        audio_map: dict = json.load(f)

    # 校验目标文章都存在
    found_ids = {it.get("id") for it in ja.get("items", [])} & TARGET_IDS
    missing = TARGET_IDS - found_ids
    if missing:
        print(f"错误: 以下 id 未在 ja_articles.json 中找到: {missing}")
        sys.exit(1)
    print(f"目标文章: {len(found_ids)} 篇")

    # 收集待生成 (text, rel, title) — 不查本地，按文章id过滤
    plan: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for seg, title in iter_target_segments(ja):
        text = (seg.get("jp") or seg.get("word") or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        rel = text_to_rel(text)
        plan.append((text, rel, title))
        # 同步写回字段
        audio_map[text] = rel
        seg["audio"] = rel

    total = len(plan)
    total_chars = sum(len(t) for t, _, _ in plan)
    print(f"待生成: {total} 条唯一句子, 共 {total_chars} 字")

    if args.dry_run:
        for i, (text, rel, title) in enumerate(plan):
            print(f"[{i+1}/{total}] [{title}] {rel} <- {text[:50]}")
        print("\n[dry-run] 未实际生成。")
        return

    if total == 0:
        print("无待生成项。")
        return

    api_key = get_api_key()

    ok = fail = 0
    def do_one(idx_item):
        i, (text, rel, title) = idx_item
        path = disk_path(rel)
        if synthesize(api_key, text, path):
            size = os.path.getsize(path)
            print(f"[{i+1}/{total}] OK ({size//1024}KB) [{title}] {text[:40]}", flush=True)
            return True
        print(f"[{i+1}/{total}] FAIL [{title}] {text[:40]}", flush=True)
        return False

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(do_one, (i, item)): i for i, item in enumerate(plan)}
        for fut in as_completed(futures):
            if fut.result():
                ok += 1
            else:
                fail += 1

    print(f"\n完成: {ok} 成功, {fail} 失败 / {total}")

    with open(JA_PATH, "w", encoding="utf-8") as f:
        json.dump(ja, f, ensure_ascii=False, indent=2)
    with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(audio_map, f, ensure_ascii=False, indent=2)
    print(f"已更新 {os.path.relpath(JA_PATH, ROOT)} 和 {os.path.relpath(AUDIO_MAP_PATH, ROOT)}")
    print("上传: rclone copy audio/jp/ r2:hylingo-audio/jp/ --transfers 32 --progress")


if __name__ == "__main__":
    main()
