#!/usr/bin/env python3
"""
根据当前 public/data 下仍被引用的音频，修剪 audio_map.json，并生成 R2 待删清单。

已移除的 sentences.json / en_sentences.json 中的音频若仍只在旧 map 里出现，会被剔除并列入删除清单。

用法（仓库根目录）:
  python scripts/prune_orphan_audio.py              # 修剪 map + 写清单
  python scripts/prune_orphan_audio.py --dry-run   # 只打印统计，不改文件

删除 CDN（Cloudflare R2）上文件时，在配置好 rclone 后执行:
  rclone deletefile r2:hylingo-audio/jp/xxx.mp3   # 或对清单批量处理
详见 docs/r2-audio-upload.md「删除孤儿音频」一节。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"
AUDIO_MAP_PATH = DATA / "audio_map.json"
OUT_LIST = ROOT / "docs" / "orphan-audio-r2-delete.txt"

DATA_FILES = [
    "nouns.json",
    "verbs.json",
    "ja_articles.json",
    "en_articles.json",
    "en_nouns.json",
]
MALE_MAP = "article_audio_map_male.json"


def _norm_audio(s: str) -> str:
    return s.strip().lstrip("/")


def collect_audio_from_obj(obj, out: set[str]) -> None:
    if obj is None:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("audio", "audioExample", "audioMale") and isinstance(v, str) and v.strip():
                out.add(_norm_audio(v))
            collect_audio_from_obj(v, out)
    elif isinstance(obj, list):
        for x in obj:
            collect_audio_from_obj(x, out)


def load_needed_paths() -> set[str]:
    needed: set[str] = set()
    for name in DATA_FILES:
        p = DATA / name
        if not p.is_file():
            continue
        with open(p, encoding="utf-8") as f:
            collect_audio_from_obj(json.load(f), needed)
    mp = DATA / MALE_MAP
    if mp.is_file():
        with open(mp, encoding="utf-8") as f:
            m = json.load(f)
        if isinstance(m, dict):
            for v in m.values():
                if isinstance(v, str) and v.strip():
                    needed.add(_norm_audio(v))
    return needed


def _git_show_audio(path_in_repo: str) -> set[str]:
    paths: set[str] = set()
    try:
        raw = subprocess.check_output(
            ["git", "show", f"HEAD:{path_in_repo}"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return paths
    try:
        collect_audio_from_obj(json.loads(raw.decode("utf-8")), paths)
    except json.JSONDecodeError:
        pass
    return paths


def try_git_show_removed_sentence_audio() -> set[str]:
    """从 git HEAD 中已删除的句子库 JSON 收集音频（补全「仅句子用过」的孤儿文件）。"""
    jp = _git_show_audio("public/data/sentences.json")
    en = _git_show_audio("public/data/en_sentences.json")
    return jp | en


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    needed = load_needed_paths()
    with open(AUDIO_MAP_PATH, encoding="utf-8") as f:
        audio_map: dict[str, str] = json.load(f)

    new_map: dict[str, str] = {}
    orphan_from_map: set[str] = set()
    for k, v in audio_map.items():
        if not isinstance(v, str) or not v.strip():
            continue
        fn = _norm_audio(v)
        if fn in needed:
            new_map[k] = v
        else:
            orphan_from_map.add(fn)

    # 句子库直链、但已从 map 摘掉的文件
    sentence_audio = try_git_show_removed_sentence_audio()
    orphan_from_sentences_only = sentence_audio - needed

    to_delete = sorted(orphan_from_map | orphan_from_sentences_only)

    print(f"needed unique audio paths (from data JSON): {len(needed)}")
    print(f"audio_map entries before: {len(audio_map)}")
    print(f"audio_map entries after:  {len(new_map)}")
    print(f"orphan files (map + optional git sentences, deduped): {len(to_delete)}")

    if args.dry_run:
        return 0

    with open(AUDIO_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(new_map, f, ensure_ascii=False, separators=(",", ":"))

    OUT_LIST.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_LIST, "w", encoding="utf-8") as f:
        f.write("# One path per line, relative to R2 bucket root (hylingo-audio)\n")
        f.write("# Delete with rclone — see docs/r2-audio-upload.md\n\n")
        for line in to_delete:
            f.write(line + "\n")

    print(f"Wrote {AUDIO_MAP_PATH.relative_to(ROOT)}")
    print(f"Wrote {OUT_LIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
