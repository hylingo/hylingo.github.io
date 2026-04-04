#!/usr/bin/env python3
"""
为 ja_articles.json 中缺少 audio / audioMale 的句子生成 Edge TTS MP3，
更新 audio_map.json、article_audio_map_male.json（合并）、ja_articles.json。

输出: 仓库根目录 audio/jp/*.mp3（与 docs/r2-audio-upload.md 中 rclone 路径一致）

依赖: pip install -r requirements-edge-tts.txt

用法:
  python scripts/generate_ja_article_audio_missing.py
  python scripts/generate_ja_article_audio_missing.py --dry-run
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
JA_PATH = os.path.join(ROOT, "public", "data", "ja_articles.json")
AUDIO_MAP_PATH = os.path.join(ROOT, "public", "data", "audio_map.json")
MALE_MAP_PATH = os.path.join(ROOT, "public", "data", "article_audio_map_male.json")

VOICE_F = "ja-JP-NanamiNeural"
VOICE_M = "ja-JP-KeitaNeural"
MALE_SALT = "\nedge-tts:ja-JP-KeitaNeural"
CONCURRENCY = 5


def female_rel(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"jp/{h}.mp3"


def male_rel(text: str) -> str:
    h = hashlib.sha256((text + MALE_SALT).encode("utf-8")).hexdigest()[:12]
    return f"jp/{h}.mp3"


def disk_path(rel: str) -> str:
    return os.path.join(ROOT, "audio", rel.replace("/", os.sep))


def file_ok(path: str) -> bool:
    return os.path.isfile(path) and os.path.getsize(path) > 0


async def synth_one(
    sem: asyncio.Semaphore,
    text: str,
    rel: str,
    voice: str,
    idx: int,
    total: int,
    dry_run: bool,
) -> tuple[bool, str]:
    path = disk_path(rel)
    if dry_run:
        print(f"[{idx + 1}/{total}] dry-run {voice} -> {rel}")
        return True, ""
    async with sem:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if file_ok(path):
                print(f"[{idx + 1}/{total}] skip exists {rel}", flush=True)
                return True, ""
            tts = edge_tts.Communicate(text, voice)
            await tts.save(path)
            print(f"[{idx + 1}/{total}] ok {rel}", flush=True)
            return True, ""
        except Exception as e:
            return False, str(e)


def iter_segments(data: dict):
    for item in data.get("items") or []:
        lvl = (item.get("level") or "").strip()
        is_n1 = lvl == "N1"
        if item.get("format") == "essay":
            for seg in item.get("segments") or []:
                yield seg, is_n1
        else:
            for sec in item.get("sections") or []:
                for line in sec.get("lines") or []:
                    yield line, is_n1


async def main_async(args: argparse.Namespace) -> int:
    os.chdir(ROOT)
    with open(JA_PATH, "r", encoding="utf-8") as f:
        ja = json.load(f)
    with open(AUDIO_MAP_PATH, "r", encoding="utf-8") as f:
        audio_map: dict[str, str] = json.load(f)
    with open(MALE_MAP_PATH, "r", encoding="utf-8") as f:
        male_map: dict[str, str] = json.load(f)

    missing_f_texts: set[str] = set()
    missing_m_texts: set[str] = set()
    for seg, is_n1 in iter_segments(ja):
        text = (seg.get("word") or seg.get("jp") or "").strip()
        if not text:
            continue
        if not seg.get("audio"):
            missing_f_texts.add(text)
        if not is_n1 and not seg.get("audioMale"):
            missing_m_texts.add(text)

    # 1) 补全字段（仅影响缺 audio 的精读句）
    for seg, is_n1 in iter_segments(ja):
        text = (seg.get("word") or seg.get("jp") or "").strip()
        if not text:
            continue
        if not seg.get("audio"):
            if text not in audio_map:
                audio_map[text] = female_rel(text)
            seg["audio"] = audio_map[text]
        if not is_n1 and not seg.get("audioMale"):
            if text not in male_map:
                male_map[text] = male_rel(text)
            seg["audioMale"] = male_map[text]

    # 2) 待合成：仅「原先缺 audio / audioMale」的句，且本地无文件
    plan_f: list[tuple[str, str]] = []
    seen_f: set[str] = set()
    for text in sorted(missing_f_texts):
        rf = audio_map.get(text)
        if not rf or text in seen_f:
            continue
        seen_f.add(text)
        if not file_ok(disk_path(rf)):
            plan_f.append((text, rf))

    plan_m: list[tuple[str, str]] = []
    seen_m: set[str] = set()
    for text in sorted(missing_m_texts):
        rm = male_map.get(text)
        if not rm or text in seen_m:
            continue
        seen_m.add(text)
        if not file_ok(disk_path(rm)):
            plan_m.append((text, rm))

    n = len(plan_f) + len(plan_m)
    print(f"待合成: 女声 {len(plan_f)} + 男声 {len(plan_m)} = {n}", flush=True)

    if args.dry_run:
        return 0

    if n == 0:
        print("本地文件已齐，仅写回 JSON。", flush=True)
    else:
        sem = asyncio.Semaphore(CONCURRENCY)
        tasks = [
            synth_one(sem, text, rel, VOICE_F, i, n, False)
            for i, (text, rel) in enumerate(plan_f)
        ]
        off = len(plan_f)
        tasks.extend(
            synth_one(sem, text, rel, VOICE_M, off + i, n, False)
            for i, (text, rel) in enumerate(plan_m)
        )
        results = await asyncio.gather(*tasks)
        bad = [r for r in results if not r[0]]
        if bad:
            print(f"合成失败 {len(bad)} 条", file=sys.stderr)
            return 1

    with open(JA_PATH, "w", encoding="utf-8") as f:
        json.dump(ja, f, ensure_ascii=False, separators=(",", ":"))
    with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(audio_map, f, ensure_ascii=False, separators=(",", ":"))
    with open(MALE_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(male_map, f, ensure_ascii=False, separators=(",", ":"))

    print("已写入 ja_articles.json, audio_map.json, article_audio_map_male.json", flush=True)
    print("上传: rclone copy audio/jp/ r2:hylingo-audio/jp/ --transfers 32 --progress", flush=True)
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    raise SystemExit(asyncio.run(main_async(args)))


if __name__ == "__main__":
    main()
