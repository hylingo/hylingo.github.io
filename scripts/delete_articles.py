#!/usr/bin/env python3
"""
Delete articles from ja_articles.json and clean up audio references.

Usage:
  python3 scripts/delete_articles.py --ids n4-clinic-essay n4-clinic-dialogue ...
  python3 scripts/delete_articles.py --bases n4-clinic n4-ward-office ...  # deletes both -essay and -dialogue
  python3 scripts/delete_articles.py --bases-file scripts/round1_bases.txt

This script:
1. Removes articles from ja_articles.json
2. Removes corresponding entries from article_audio_map_male.json
3. Exports CDN audio paths to docs/audio-to-delete.txt for manual R2 cleanup

It does NOT delete from R2 directly — run rclone separately using the exported list.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"


def get_segs(article: dict) -> list[dict]:
    segs = article.get("segments") or []
    for sec in article.get("sections", []):
        segs += sec.get("lines", [])
    return segs


def main():
    parser = argparse.ArgumentParser(description="Delete articles and clean up audio")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ids", nargs="+", help="Exact article IDs to delete")
    group.add_argument("--bases", nargs="+", help="Base IDs (will delete both -essay and -dialogue)")
    group.add_argument("--bases-file", help="File with base IDs, one per line")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without doing it")
    args = parser.parse_args()

    # Resolve IDs to delete
    if args.ids:
        ids_to_delete = set(args.ids)
    elif args.bases:
        bases = args.bases
    elif args.bases_file:
        bases = [line.strip() for line in Path(args.bases_file).read_text().splitlines() if line.strip() and not line.startswith("#")]

    if not args.ids:
        # Expand bases to actual IDs
        ids_to_delete = set()
        for b in bases:
            ids_to_delete.add(f"{b}-essay")
            ids_to_delete.add(f"{b}-dialogue")

    # Load data
    articles_path = DATA / "ja_articles.json"
    male_map_path = DATA / "article_audio_map_male.json"

    articles_data = json.loads(articles_path.read_text())
    male_map = json.loads(male_map_path.read_text())

    # Find articles to delete
    to_delete = [a for a in articles_data["items"] if a["id"] in ids_to_delete]
    found_ids = {a["id"] for a in to_delete}
    missing = ids_to_delete - found_ids

    if missing:
        # Some IDs don't exist (e.g. base has only essay, no dialogue) - that's OK
        real_missing = set()
        for m in missing:
            # Check if it's just a missing pair half
            base = m.replace("-essay", "").replace("-dialogue", "")
            if f"{base}-essay" not in found_ids and f"{base}-dialogue" not in found_ids:
                real_missing.add(m)
        if real_missing:
            print(f"⚠ IDs not found: {real_missing}")

    # Collect audio paths and male_map keys
    audio_paths = set()
    male_keys_to_delete = set()

    for a in to_delete:
        for s in get_segs(a):
            if s.get("audio"):
                audio_paths.add(s["audio"])
            if s.get("audioMale"):
                audio_paths.add(s["audioMale"])
            jp = s.get("jp") or s.get("word", "")
            if jp in male_map:
                male_keys_to_delete.add(jp)

    print(f"\n{'='*50}")
    print(f"删除计划:")
    print(f"  文章: {len(to_delete)} 篇")
    print(f"  CDN音频: {len(audio_paths)} 个")
    print(f"  male_map条目: {len(male_keys_to_delete)} 个")
    print(f"{'='*50}")

    for a in to_delete:
        n = len(get_segs(a))
        print(f"  {a['id']:40s} [{a['level']:8s}] {n:2d}句")

    if args.dry_run:
        print(f"\n(dry run — 未执行删除)")
        return

    # 1. Remove articles from JSON
    articles_data["items"] = [a for a in articles_data["items"] if a["id"] not in found_ids]
    articles_path.write_text(json.dumps(articles_data, ensure_ascii=False, indent=2) + "\n")
    print(f"\n✓ ja_articles.json: 删除 {len(to_delete)} 篇, 剩余 {len(articles_data['items'])} 篇")

    # 2. Remove male_map entries
    removed_male = 0
    for key in male_keys_to_delete:
        if key in male_map:
            del male_map[key]
            removed_male += 1
    male_map_path.write_text(json.dumps(male_map, ensure_ascii=False))
    print(f"✓ article_audio_map_male.json: 删除 {removed_male} 条, 剩余 {len(male_map)} 条")

    # 3. Export audio paths for R2 deletion
    audio_delete_path = ROOT / "docs" / "audio-to-delete.txt"
    # Append to existing file if present
    existing = set()
    if audio_delete_path.exists():
        existing = set(audio_delete_path.read_text().splitlines())
    all_paths = sorted(existing | audio_paths)
    audio_delete_path.write_text("\n".join(all_paths) + "\n")
    print(f"✓ docs/audio-to-delete.txt: 新增 {len(audio_paths)} 个路径, 总计 {len(all_paths)} 个")

    print(f"\n⚠ 还需手动执行 R2 删除:")
    print(f"  rclone delete r2:hylingo-audio --include-from docs/audio-to-delete.txt")
    print(f"  或逐个: while read f; do rclone deletefile r2:hylingo-audio/$f; done < docs/audio-to-delete.txt")


if __name__ == "__main__":
    main()
