#!/usr/bin/env python3
"""
用 Fish Audio TTS 为 ja_articles.json 全部 segment 重新生成音频。
替换原有 Edge TTS 音频。

用法:
  # 先测试几条
  python scripts/generate_audio_fish.py --test 3

  # 全量生成（跳过已存在的文件）
  python scripts/generate_audio_fish.py

  # 强制重新生成全部
  python scripts/generate_audio_fish.py --force

环境变量:
  FISH_API_KEY  — Fish Audio API Key
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

# Fish Audio 配置
FISH_API_URL = "https://api.fish.audio/v1/tts"
FISH_MODEL_ID = "5161d41404314212af1254556477c17d"  # 比留間大地

# 请求间隔（秒），避免触发限流
REQUEST_DELAY = 0.3


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "")
    if not key:
        print("错误: 请设置环境变量 FISH_API_KEY")
        print("  export FISH_API_KEY=your_key_here")
        sys.exit(1)
    return key


def text_to_rel(text: str) -> str:
    """文本 -> 相对路径 jp/xxxx.mp3（SHA256 前 12 位）。"""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"jp/{h}.mp3"


def disk_path(rel: str) -> str:
    return os.path.join(AUDIO_DIR, rel.replace("/", os.sep))


def file_ok(path: str) -> bool:
    return os.path.isfile(path) and os.path.getsize(path) > 1000  # >1KB 才算有效


def synthesize(api_key: str, text: str, output_path: str) -> bool:
    """调用 Fish Audio TTS API 生成音频。"""
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
                print(f"  限流, 等待{wait}秒...", end=" ", flush=True)
                time.sleep(wait)
                continue
            else:
                print(f"  API 错误 {resp.status_code}: {resp.text[:200]}")
                return False
        except Exception as e:
            if attempt < 2:
                print(f"  重试({attempt+1})...", end=" ", flush=True)
                time.sleep(3)
                continue
            print(f"  请求异常: {e}")
            return False
    return False


def iter_segments(data: dict):
    """遍历所有 segment，yield (seg, article_title)。"""
    for item in data.get("items") or []:
        title = item.get("titleWord") or item.get("titleJp") or item.get("id", "?")
        if item.get("format") == "essay":
            for seg in item.get("segments") or []:
                yield seg, title
        else:
            for sec in item.get("sections") or []:
                for line in sec.get("lines") or []:
                    yield line, title


def main():
    parser = argparse.ArgumentParser(description="Fish Audio TTS 批量生成")
    parser.add_argument("--test", type=int, default=0, help="只生成前 N 条用于试听")
    parser.add_argument("--force", action="store_true", help="强制重新生成（覆盖已有文件）")
    parser.add_argument("--dry-run", action="store_true", help="只显示计划，不实际生成")
    args = parser.parse_args()

    api_key = get_api_key()

    with open(JA_PATH, "r", encoding="utf-8") as f:
        ja = json.load(f)
    with open(AUDIO_MAP_PATH, "r", encoding="utf-8") as f:
        audio_map: dict = json.load(f)

    # 收集所有待生成的 (text, rel_path)
    plan: list[tuple[str, str, str]] = []  # (text, rel, title)
    seen_texts: set[str] = set()

    for seg, title in iter_segments(ja):
        text = (seg.get("jp") or seg.get("word") or "").strip()
        if not text or text in seen_texts:
            continue
        seen_texts.add(text)

        rel = text_to_rel(text)
        path = disk_path(rel)

        if not args.force and file_ok(path):
            continue

        plan.append((text, rel, title))

        # 确保 audio_map 和 segment 有正确的路径
        audio_map[text] = rel
        seg["audio"] = rel

    # 也更新未在 plan 中但缺少 audio 字段的 segment
    for seg, title in iter_segments(ja):
        text = (seg.get("jp") or seg.get("word") or "").strip()
        if text and not seg.get("audio"):
            rel = text_to_rel(text)
            audio_map[text] = rel
            seg["audio"] = rel

    if args.test:
        plan = plan[:args.test]

    total = len(plan)
    print(f"待生成: {total} 条音频")
    if total == 0:
        print("全部音频已存在，无需生成。")
        return

    if args.dry_run:
        for i, (text, rel, title) in enumerate(plan):
            print(f"[{i+1}/{total}] [{title}] {rel} <- {text[:40]}")
        return

    # 开始生成（并发）
    WORKERS = 5
    ok_count = 0
    fail_count = 0
    def do_one(idx_item):
        i, (text, rel, title) = idx_item
        path = disk_path(rel)
        if synthesize(api_key, text, path):
            size = os.path.getsize(path)
            print(f"[{i+1}/{total}] OK ({size//1024}KB) [{title}] {text[:40]}", flush=True)
            return True
        else:
            print(f"[{i+1}/{total}] FAIL [{title}] {text[:40]}", flush=True)
            return False

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(do_one, (i, item)): i for i, item in enumerate(plan)}
        for fut in as_completed(futures):
            if fut.result():
                ok_count += 1
            else:
                fail_count += 1

    print(f"\n完成: {ok_count} 成功, {fail_count} 失败, 共 {total} 条")

    # 保存更新后的 JSON
    with open(JA_PATH, "w", encoding="utf-8") as f:
        json.dump(ja, f, ensure_ascii=False, indent=2)
    with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(audio_map, f, ensure_ascii=False, indent=2)
    print(f"已更新 {JA_PATH} 和 {AUDIO_MAP_PATH}")


if __name__ == "__main__":
    main()
