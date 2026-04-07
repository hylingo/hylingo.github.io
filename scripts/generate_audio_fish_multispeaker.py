#!/usr/bin/env python3
"""
Fish Audio multi-speaker TTS — 为整篇 dialogue 生成单个 mp3。

特殊用途：用于"整篇直接播放、无单句播放器"的对话文章。
- 把 sections.lines 按 speaker 拼成 <|speaker:0|>... <|speaker:1|>... 格式
- 一次调 multi-speaker API 生成整篇 mp3
- 文件名用 article id：jp/<article-id>.mp3
- 写入 ja_articles.json 的 articleAudio 字段（article 级，不是 segment 级）

用法:
  export FISH_API_KEY=xxx
  python scripts/generate_audio_fish_multispeaker.py --article n3n2-late-night-izakaya-reunion --dry-run
  python scripts/generate_audio_fish_multispeaker.py --article n3n2-late-night-izakaya-reunion
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JA_PATH = os.path.join(ROOT, "public", "data", "ja_articles.json")
AUDIO_DIR = os.path.join(ROOT, "audio")

FISH_API_URL = "https://api.fish.audio/v1/tts"

# voice 模型映射：speaker label → reference_id
SPEAKER_VOICES = {
    "A": "5161d41404314212af1254556477c17d",  # 比留間大地
    "B": "71bf4cb71cd44df6aa603d51db8f92ff",  # ななみん
}


def get_api_key() -> str:
    key = os.environ.get("FISH_API_KEY", "")
    if not key:
        print("错误: 请设置 FISH_API_KEY")
        sys.exit(1)
    return key


def build_multispeaker_text(article: dict) -> tuple[str, list[str]]:
    """把 dialogue 的所有 lines 拼成 <|speaker:N|> 标记的文本。
    返回 (text, ordered_voice_ids)。
    voice id 顺序对应 speaker:0, speaker:1, ...
    """
    if article.get("format") != "dialogue":
        raise ValueError(f"{article['id']} 不是 dialogue 格式")

    # 收集出现过的 speaker（保持出现顺序）
    seen_speakers: list[str] = []
    for sec in article.get("sections", []):
        for ln in sec.get("lines", []):
            sp = ln.get("speaker", "A")
            if sp not in seen_speakers:
                seen_speakers.append(sp)

    if not seen_speakers:
        raise ValueError(f"{article['id']} 没有任何 speaker 标记")

    # speaker 标签 → speaker:N 索引
    speaker_idx = {sp: i for i, sp in enumerate(seen_speakers)}

    # voice ids（按 speaker:0, 1, ... 顺序）
    voice_ids: list[str] = []
    for sp in seen_speakers:
        if sp not in SPEAKER_VOICES:
            raise ValueError(f"speaker {sp} 没有对应的 voice id，请在 SPEAKER_VOICES 中添加")
        voice_ids.append(SPEAKER_VOICES[sp])

    # 拼接 text
    parts: list[str] = []
    for sec in article.get("sections", []):
        for ln in sec.get("lines", []):
            sp = ln.get("speaker", "A")
            text = (ln.get("jp") or ln.get("word") or "").strip()
            if not text:
                continue
            parts.append(f"<|speaker:{speaker_idx[sp]}|>{text}")

    return "".join(parts), voice_ids


def synthesize_multispeaker(api_key: str, text: str, voice_ids: list[str], output_path: str) -> bool:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    payload = {
        "text": text,
        "reference_id": voice_ids,  # 数组形式触发 multi-speaker
        "model": "s2-pro",            # multi-speaker 仅 s2-pro 支持
        "format": "mp3",
        "latency": "normal",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    for attempt in range(3):
        try:
            resp = requests.post(FISH_API_URL, json=payload, headers=headers, timeout=180)
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
                print(f"  API错误 {resp.status_code}: {resp.text[:500]}")
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
    ap.add_argument("--article", required=True, help="文章 id")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(JA_PATH, "r", encoding="utf-8") as f:
        ja = json.load(f)

    article = next((a for a in ja["items"] if a["id"] == args.article), None)
    if not article:
        print(f"错误: 找不到文章 {args.article}")
        sys.exit(1)

    text, voice_ids = build_multispeaker_text(article)
    rel = f"jp/{args.article}.mp3"
    out_path = os.path.join(AUDIO_DIR, "jp", f"{args.article}.mp3")

    print(f"文章: {article.get('titleWord')}")
    print(f"speakers: {len(voice_ids)} 个")
    for i, vid in enumerate(voice_ids):
        print(f"  speaker:{i} -> {vid}")
    print(f"text 长度: {len(text)} 字符 / {len(text.encode('utf-8'))} 字节")
    print(f"输出: {rel}")

    if args.dry_run:
        print()
        print("--- text 预览（前 600 字符） ---")
        print(text[:600])
        print("...")
        print("\n[dry-run] 未实际生成。")
        return

    api_key = get_api_key()
    print("\n开始合成（multi-speaker 单次请求，可能较慢）...")
    if not synthesize_multispeaker(api_key, text, voice_ids, out_path):
        print("❌ 合成失败")
        sys.exit(1)

    size = os.path.getsize(out_path)
    print(f"✅ 完成: {rel} ({size//1024} KB)")

    # 写回 articleAudio 字段
    article["articleAudio"] = rel
    with open(JA_PATH, "w", encoding="utf-8") as f:
        json.dump(ja, f, ensure_ascii=False, indent=2)
    print(f"已写入 {os.path.relpath(JA_PATH, ROOT)} (articleAudio 字段)")
    print(f"上传: rclone copy audio/jp/{args.article}.mp3 r2:hylingo-audio/jp/")


if __name__ == "__main__":
    main()
