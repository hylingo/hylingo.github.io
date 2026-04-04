#!/usr/bin/env python3
"""
批量翻译例句（deep-translator + 多线程并发）：
- verbs.json: exampleCn(中文) → exampleEn(英文)
- en_nouns.json: exampleCn(中文) → exampleJp(日文)
"""

import json
import time
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator

DATA_DIR = Path(__file__).resolve().parent.parent / "public" / "data"

WORKERS = 8
SAVE_EVERY = 200

def translate_one(text, src, dest):
    for attempt in range(3):
        try:
            return GoogleTranslator(source=src, target=dest).translate(text)
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

def translate_file(filename, src_field, dst_field, src_lang, dest_lang):
    filepath = DATA_DIR / filename
    print(f"\n{'='*50}")
    print(f"处理: {filename}  ({src_field} → {dst_field}, {src_lang} → {dest_lang})")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "items" in data:
        items = data["items"]
    elif isinstance(data, list):
        items = data
    else:
        print("  未知格式，跳过")
        return

    to_do = [(i, it[src_field]) for i, it in enumerate(items)
             if it.get(src_field) and not it.get(dst_field)]

    total = len(to_do)
    print(f"  总条目: {len(items)}, 需翻译: {total}")
    if total == 0:
        return

    done = 0
    failed = 0

    for batch_start in range(0, total, SAVE_EVERY):
        batch = to_do[batch_start:batch_start + SAVE_EVERY]

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {}
            for idx, text in batch:
                f = pool.submit(translate_one, text, src_lang, dest_lang)
                futures[f] = idx

            for f in as_completed(futures):
                idx = futures[f]
                try:
                    result = f.result()
                    if result:
                        items[idx][dst_field] = result
                        done += 1
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
                    if failed <= 5:
                        print(f"  失败[{idx}]: {e}")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

        print(f"  进度: {done + failed}/{total} (成功: {done}, 失败: {failed})")
        sys.stdout.flush()

    print(f"  完成! 成功: {done}, 失败: {failed}")

if __name__ == "__main__":
    translate_file("verbs.json", "exampleCn", "exampleEn", "zh-CN", "en")
    translate_file("en_nouns.json", "exampleCn", "exampleJp", "zh-CN", "ja")
    print("\n全部完成!")
