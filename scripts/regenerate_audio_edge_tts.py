#!/usr/bin/env python3
"""
用本地 Microsoft Edge TTS（edge-tts）按 audio_map.json 重录 MP3。

默认：使用新文件名（SHA256 前 12 位十六进制 + .mp3，与旧版 MD5 命名区分），
写入 public/audio（实际为仓库根目录 audio/），更新 audio_map.json，并删除本条旧文件。

依赖:
  pip install -r requirements-edge-tts.txt

用法:
  python scripts/regenerate_audio_edge_tts.py --limit 20    # 试跑
  python scripts/regenerate_audio_edge_tts.py                 # 全量
  python scripts/regenerate_audio_edge_tts.py --keep-names    # 不改名，仅覆盖原路径
  python scripts/regenerate_audio_edge_tts.py --keys-file scripts/audio_keys_new.txt \\
      --remove-keys-file scripts/audio_keys_old.txt   # 只录新键、并删掉旧键与 mp3

环境变量:
  EDGE_TTS_VOICE  默认 ja-JP-NanamiNeural
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
AUDIO_DIR = os.path.join(ROOT, "public", "audio")
AUDIO_MAP_PATH = os.path.join(ROOT, "public", "data", "audio_map.json")
VOICE = os.environ.get("EDGE_TTS_VOICE", "ja-JP-NanamiNeural")
CONCURRENCY = 3


def make_filename_v2(text: str) -> str:
    """与旧版 MD5[:12] 区分的新命名（全库重录后统一用此规则）。"""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"{h}.mp3"


async def _one(
    sem: asyncio.Semaphore,
    text: str,
    target_rel: str,
    idx: int,
    total: int,
) -> tuple[str, bool, str]:
    path = os.path.join(AUDIO_DIR, target_rel)
    async with sem:
        try:
            tts = edge_tts.Communicate(text, VOICE)
            await tts.save(path)
            print(f"[{idx + 1}/{total}] ok {target_rel}", flush=True)
            return (text, True, "")
        except Exception as e:
            return (text, False, str(e))


def _read_keys_file(path: str) -> list[str]:
    out: list[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.append(s)
    return out


async def main_async(args: argparse.Namespace) -> int:
    os.chdir(ROOT)
    if not os.path.isdir(AUDIO_DIR):
        print("missing", AUDIO_DIR, file=sys.stderr)
        return 1
    with open(AUDIO_MAP_PATH, "r", encoding="utf-8") as f:
        audio_map: dict[str, str] = json.load(f)

    if args.remove_keys_file and not args.keys_file:
        drop = _read_keys_file(args.remove_keys_file)
        if not drop:
            print("remove-keys-file 为空", file=sys.stderr)
            return 1
        pruned = 0
        for k in drop:
            if k not in audio_map:
                print(f"remove-keys: 无此键（跳过）: {k[:40]}…", file=sys.stderr)
                continue
            fn = audio_map.pop(k)
            p = os.path.join(AUDIO_DIR, fn)
            if os.path.isfile(p):
                try:
                    os.remove(p)
                except OSError as e:
                    print(f"未删除 {fn}: {e}", file=sys.stderr)
            pruned += 1
        with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
            json.dump(audio_map, f, ensure_ascii=False, separators=(",", ":"))
        print(f"已移除 {pruned} 条键及 mp3。")
        return 0

    if args.keys_file:
        key_lines = _read_keys_file(args.keys_file)
        if not key_lines:
            print("keys-file 为空", file=sys.stderr)
            return 1
        slice_items = [(k, audio_map.get(k)) for k in key_lines]
    else:
        items = list(audio_map.items())
        start = max(0, args.start)
        end = len(items) if args.limit is None else min(len(items), start + args.limit)
        slice_items = items[start:end]

    total = len(slice_items)
    if total == 0:
        print("nothing to do")
        return 0

    # 预计算目标文件名并检测冲突
    planned: list[tuple[str, str | None, str]] = []  # text, old_fn or None, target_fn
    seen_new: dict[str, str] = {}
    for text, old_fn in slice_items:
        if args.keep_names:
            if not old_fn:
                print(f"--keep-names 要求键已在 map 中，缺失: {text!r}", file=sys.stderr)
                return 1
            target_fn = old_fn
        else:
            target_fn = make_filename_v2(text)
        if target_fn in seen_new and seen_new[target_fn] != text:
            print(
                f"文件名冲突: {target_fn} <- {seen_new[target_fn]!r} 与 {text!r}",
                file=sys.stderr,
            )
            return 1
        seen_new[target_fn] = text
        planned.append((text, old_fn, target_fn))

    print(f"Voice: {VOICE}")
    mode = "覆盖原文件名" if args.keep_names else "新文件名 (sha256[:12]) + 更新 map + 删旧文件"
    if args.keys_file:
        print(f"{mode} | keys-file {total} 条\n")
    else:
        items_n = len(audio_map)
        start = max(0, args.start)
        end = items_n if args.limit is None else min(items_n, start + (args.limit or 0))
        print(f"{mode} | {total} 条 (索引 {start}..{end - 1} / 共 {items_n})\n")

    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [
        _one(sem, text, target_fn, i, total)
        for i, (text, _old, target_fn) in enumerate(planned)
    ]
    results = await asyncio.gather(*tasks)

    failed = [(t, err) for t, ok, err in results if not ok]
    if failed:
        print(f"\n失败 {len(failed)} 条:", file=sys.stderr)
        for t, err in failed[:20]:
            print(f"  {t[:40]}… -> {err}", file=sys.stderr)
        if len(failed) > 20:
            print(f"  … 另有 {len(failed) - 20} 条", file=sys.stderr)
        return 1

    # 写回完整 audio_map（只改本批次的值）
    for (text, old_fn, target_fn), (_t, ok, _e) in zip(planned, results):
        if ok:
            audio_map[text] = target_fn

    with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(audio_map, f, ensure_ascii=False, separators=(",", ":"))

    if not args.keep_names and not args.no_delete_old:
        removed = 0
        for text, old_fn, target_fn in planned:
            if not old_fn or old_fn == target_fn:
                continue
            old_path = os.path.join(AUDIO_DIR, old_fn)
            if os.path.isfile(old_path):
                try:
                    os.remove(old_path)
                    removed += 1
                except OSError as e:
                    print(f"未删除旧文件 {old_fn}: {e}", file=sys.stderr)
        if removed:
            print(f"\n已删除 {removed} 个被替换的旧 mp3。")

    if args.remove_keys_file:
        drop = _read_keys_file(args.remove_keys_file)
        pruned = 0
        for k in drop:
            if k not in audio_map:
                print(f"remove-keys: 无此键（跳过）: {k[:40]}…", file=sys.stderr)
                continue
            fn = audio_map.pop(k)
            p = os.path.join(AUDIO_DIR, fn)
            if os.path.isfile(p):
                try:
                    os.remove(p)
                except OSError as e:
                    print(f"未删除 {fn}: {e}", file=sys.stderr)
            pruned += 1
        if pruned:
            with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
                json.dump(audio_map, f, ensure_ascii=False, separators=(",", ":"))
            print(f"\n已移除 {pruned} 条旧键及对应 mp3。")

    print("\nDone. audio_map.json 已更新。")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Edge TTS 重录并可选更换 mp3 文件名")
    p.add_argument("--start", type=int, default=0, help="跳过 map 迭代中前 N 条")
    p.add_argument("--limit", type=int, default=None, help="最多处理条数（默认全部）")
    p.add_argument(
        "--keep-names",
        action="store_true",
        help="不改名，仅在原路径上覆盖（旧行为）",
    )
    p.add_argument(
        "--no-delete-old",
        action="store_true",
        help="改名模式下不删除被替换的旧 mp3（便于对比）",
    )
    p.add_argument(
        "--keys-file",
        metavar="PATH",
        help="仅处理列出的日文键（每行一条，# 开头为注释）；新键会写入 map",
    )
    p.add_argument(
        "--remove-keys-file",
        metavar="PATH",
        help="处理完成后从 map 删除这些键并删除对应 mp3（用于替换词条后的旧短句）",
    )
    args = p.parse_args()
    raise SystemExit(asyncio.run(main_async(args)))


if __name__ == "__main__":
    main()
