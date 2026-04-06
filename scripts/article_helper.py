#!/usr/bin/env python3
"""
Article generation helper — two modes:

1. suggest  — Analyze uncovered vocab, recommend scenes that naturally cover them
2. validate — After writing an article, check coverage, colloquialism, format

Usage:
  python3 scripts/article_helper.py suggest --topic 生活用品 --level N4-N3
  python3 scripts/article_helper.py suggest --topic 食物料理 --level N3
  python3 scripts/article_helper.py validate --file scripts/draft_article.json
  python3 scripts/article_helper.py validate --file scripts/draft_article.json --format dialogue
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import fugashi

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"
tagger = fugashi.Tagger()


# ─── helpers ───────────────────────────────────────────────────────
def get_lemmas_and_surfaces(text: str) -> tuple[set[str], set[str]]:
    lemmas, surfaces = set(), set()
    for w in tagger(text):
        if w.feature.lemma:
            lemmas.add(w.feature.lemma)
        surfaces.add(str(w))
    return lemmas, surfaces


def load_existing_coverage() -> tuple[set[str], set[str]]:
    """Load all lemmas/surfaces already covered by existing articles."""
    articles = json.loads((DATA / "ja_articles.json").read_text())["items"]
    all_lemmas, all_surfaces = set(), set()
    for art in articles:
        segs = art.get("segments") or []
        for sec in art.get("sections", []):
            segs += sec.get("lines", [])
        for s in segs:
            text = s.get("jp") or s.get("word", "")
            l, su = get_lemmas_and_surfaces(text)
            all_lemmas |= l
            all_surfaces |= su
    return all_lemmas, all_surfaces


def load_vocab() -> list[dict]:
    nouns = json.loads((DATA / "nouns.json").read_text())
    verbs = json.loads((DATA / "verbs.json").read_text())
    for n in nouns:
        n["_src"] = "noun"
    for v in verbs:
        v["_src"] = "verb"
        v.setdefault("level", "?")
    return nouns + verbs


def is_covered(word: str, lemmas: set, surfaces: set) -> bool:
    return word in lemmas or word in surfaces


# ─── suggest mode ──────────────────────────────────────────────────
# Scene templates: each scene has a name, description, and which topics it naturally covers
SCENE_LIBRARY = [
    # 生活用品
    {"name": "引っ越し先で段ボールを開ける",
     "name_zh": "在新家拆快递箱",
     "topics": ["生活用品", "住房租房"],
     "natural_words": "家具 家電 冷蔵庫 洗濯機 掃除機 電子レンジ 照明 カーテン 布団 毛布 枕 ソファー 本棚 鏡 ハンガー".split(),
     "level_range": ["N5", "N4", "N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "友達の部屋に遊びに行く",
     "name_zh": "去朋友家玩",
     "topics": ["生活用品", "住房租房"],
     "natural_words": "スリッパ 座布団 クッション テレビ エアコン 扇風機 時計 写真 カレンダー 棚".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["dialogue"]},

    {"name": "衣替えでクローゼットを整理する",
     "name_zh": "换季整理衣柜",
     "topics": ["生活用品"],
     "natural_words": "洋服 シャツ セーター コート ズボン スカート 靴下 下着 帽子 靴 鞄 スーツ ワンピース ネックレス 指輪 アクセサリー ハンガー".split(),
     "level_range": ["N5", "N4", "N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "ホームセンターで日用品を買う",
     "name_zh": "在家居店买日用品",
     "topics": ["生活用品", "购物消费"],
     "natural_words": "石鹸 歯ブラシ ティッシュ ゴミ袋 電球 電池 テープ 針 糸 道具 ペンキ スイッチ コンセント".split(),
     "level_range": ["N5", "N4", "N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "子どもの頃の部屋を思い出す",
     "name_zh": "回忆小时候的房间",
     "topics": ["生活用品", "家庭"],
     "natural_words": "おもちゃ 人形 ぬいぐるみ ピアノ ギター アルバム 本棚 押入れ 飾り".split(),
     "level_range": ["N4", "N3"],
     "formats": ["essay"]},

    # 食物料理
    {"name": "初めて自炊する留学生",
     "name_zh": "第一次自己做饭的留学生",
     "topics": ["食物料理"],
     "natural_words": "朝ご飯 昼ご飯 晩ご飯 米 卵 醤油 砂糖 塩 油 フライパン 包丁 皿 茶碗 お湯 炊飯器".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay", "dialogue"]},

    {"name": "友達とスーパーで食材を選ぶ",
     "name_zh": "和朋友在超市挑食材",
     "topics": ["食物料理", "购物消费"],
     "natural_words": "牛肉 豚肉 鶏肉 果物 卵 豆腐 牛乳 バター チーズ ぶどう 小麦粉 調味料".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["dialogue"]},

    {"name": "お弁当を作る朝",
     "name_zh": "做便当的早晨",
     "topics": ["食物料理"],
     "natural_words": "お弁当 弁当箱 おかず 卵 醤油 焼く 炒める 煮る 冷ます 材料 食料品".split(),
     "level_range": ["N4", "N3"],
     "formats": ["essay"]},

    {"name": "居酒屋で忘年会",
     "name_zh": "在居酒屋开忘年会",
     "topics": ["食物料理"],
     "natural_words": "お酒 日本酒 ワイン ビール 焼肉 寿司 餃子 デザート ケーキ アイスクリーム ジュース 乾杯 おかわり".split(),
     "level_range": ["N4", "N3", "N2"],
     "formats": ["dialogue"]},

    {"name": "料理教室に通い始める",
     "name_zh": "开始上烹饪课",
     "topics": ["食物料理"],
     "natural_words": "材料 小麦粉 片栗粉 だし 酢 胡椒 食器 皿 スプーン フォーク ナイフ 茹でる 炒める 煮る 焼く 味わう".split(),
     "level_range": ["N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "お菓子を作ってプレゼントする",
     "name_zh": "做点心送人",
     "topics": ["食物料理", "人际关系"],
     "natural_words": "お菓子 チョコレート ケーキ 砂糖 バター 小麦粉 卵 クリーム 材料 オーブン".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay"]},

    # 家庭/人际
    {"name": "実家に帰省してリビングで家族と過ごす",
     "name_zh": "回老家和家人在客厅相聚",
     "topics": ["家庭", "生活用品"],
     "natural_words": "お父さん お母さん 兄 姉 弟 妹 両親 家族 居間 台所 兄弟 皆さん".split(),
     "level_range": ["N5", "N4"],
     "formats": ["essay", "dialogue"]},

    {"name": "家族の紹介 ― うちの家族はこんな人たち",
     "name_zh": "介绍家人——我家人是这样的",
     "topics": ["家庭"],
     "natural_words": "お父さん お母さん 兄 姉 弟 妹 両親 祖父 祖母 息子 孫 父親 母親 兄弟 姉妹 大勢".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay"]},

    {"name": "お正月に親戚が集まる",
     "name_zh": "新年亲戚聚会",
     "topics": ["家庭"],
     "natural_words": "親戚 おじさん 伯父 叔母 従兄弟 従姉妹 孫 祖父 祖母 お年玉 男の子 女の子 赤ん坊 末っ子 双子".split(),
     "level_range": ["N5", "N4", "N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "子どもの成長を夫婦で話す",
     "name_zh": "夫妻聊孩子的成长",
     "topics": ["家庭"],
     "natural_words": "夫 妻 息子 赤ん坊 お子さん 保護者 産む 男の子 女の子 迷子 夫妻 家内 主人".split(),
     "level_range": ["N4", "N3", "N2"],
     "formats": ["dialogue"]},

    {"name": "おじいちゃんの家での夏休み",
     "name_zh": "在爷爷家过暑假",
     "topics": ["家庭"],
     "natural_words": "祖父 祖母 孫 お兄さん お姉さん 弟 妹 田舎 老人 年寄 先祖 子孫 おもちゃ 人形".split(),
     "level_range": ["N5", "N4", "N3", "N2"],
     "formats": ["essay"]},

    {"name": "彼女・彼氏を親に紹介する",
     "name_zh": "把男/女朋友介绍给父母",
     "topics": ["家庭", "人际关系"],
     "natural_words": "彼 彼女 恋人 両親 お父さん お母さん 奥さん 紹介 緊張 夫人 婦人 花嫁".split(),
     "level_range": ["N4", "N3", "N2"],
     "formats": ["dialogue"]},

    {"name": "結婚式に出席する",
     "name_zh": "参加婚礼",
     "topics": ["家庭", "人际关系"],
     "natural_words": "花嫁 夫妻 親戚 冠婚葬祭 司会 義理 知人 知り合い 仲間 皆さん".split(),
     "level_range": ["N3", "N2"],
     "formats": ["essay"]},

    {"name": "週末に友達とピクニック",
     "name_zh": "周末和朋友野餐",
     "topics": ["人际关系", "食物料理"],
     "natural_words": "親友 仲間 友達 お弁当 サンドイッチ 果物 お菓子 紅茶 お茶 飲み物".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay", "dialogue"]},

    {"name": "友達と喧嘩して仲直りする",
     "name_zh": "和朋友吵架后和好",
     "topics": ["人际关系"],
     "natural_words": "親友 仲間 仲直り 友情 友好 悪口 失恋 恋 他人".split(),
     "level_range": ["N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "先輩に仕事の相談をする",
     "name_zh": "向前辈请教工作上的事",
     "topics": ["人际关系", "工作职场"],
     "natural_words": "先輩 後輩 部下 同士 弟子 人物 人材 人格".split(),
     "level_range": ["N3", "N2"],
     "formats": ["dialogue"]},

    {"name": "隣の人に挨拶する ― 新生活のご近所付き合い",
     "name_zh": "和邻居打招呼——新生活的邻里交往",
     "topics": ["人际关系"],
     "natural_words": "隣人 知り合い 知人 大勢 皆さん お見舞い 義理 人通り".split(),
     "level_range": ["N3", "N2"],
     "formats": ["essay", "dialogue"]},

    {"name": "留学先でホストファミリーと暮らす",
     "name_zh": "在寄宿家庭生活",
     "topics": ["家庭", "人际关系"],
     "natural_words": "お父さん お母さん お兄さん お姉さん 外国人 僕 あなた 皆さん 親しい".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay", "dialogue"]},

    {"name": "友達の引っ越しを手伝う",
     "name_zh": "帮朋友搬家",
     "topics": ["人际关系", "生活用品"],
     "natural_words": "親友 仲間 彼ら 手伝い 家具 段ボール 鞄 靴 帽子".split(),
     "level_range": ["N4", "N3"],
     "formats": ["dialogue"]},

    {"name": "病気の友人をお見舞いに行く",
     "name_zh": "去探望生病的朋友",
     "topics": ["人际关系", "健康医疗"],
     "natural_words": "お見舞い 看病 親友 知り合い 果物 お菓子 花 有難い".split(),
     "level_range": ["N3", "N2"],
     "formats": ["essay", "dialogue"]},

    # 健康医疗
    {"name": "体調が悪くて会社を休む",
     "name_zh": "身体不舒服请假",
     "topics": ["健康医疗"],
     "natural_words": "医者 看護師 熱 頭 お腹 背中 鼻 指 腹 体温".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay", "dialogue"]},

    # 交通
    {"name": "初めての土地でバスに乗る",
     "name_zh": "在陌生的地方坐公交",
     "topics": ["交通出行"],
     "natural_words": "運転手 駐車場 信号 交差点 横断歩道 入口 バス停 切符 乗り換え".split(),
     "level_range": ["N5", "N4", "N3"],
     "formats": ["essay", "dialogue"]},

    # 工作
    {"name": "新入社員の一日",
     "name_zh": "新员工的一天",
     "topics": ["工作职场"],
     "natural_words": "社長 部長 課長 先輩 後輩 部下 担当者 会議室 名刺".split(),
     "level_range": ["N3", "N2"],
     "formats": ["essay", "dialogue"]},
]


def cmd_suggest(args):
    vocab = load_vocab()
    lemmas, surfaces = load_existing_coverage()

    # Filter uncovered words by topic
    uncovered = [
        v for v in vocab
        if not is_covered(v["word"], lemmas, surfaces)
        and (not args.topic or v.get("topic", "") == args.topic)
    ]

    if args.topic:
        print(f"\n{'='*60}")
        print(f"话题「{args.topic}」未覆盖词: {len(uncovered)}")
        print(f"{'='*60}")

    # Score each scene
    scored_scenes = []
    for scene in SCENE_LIBRARY:
        if args.topic and args.topic not in scene["topics"]:
            continue
        if args.level:
            # Check level overlap
            target_levels = set(args.level.replace("–", "-").split("-"))
            if not target_levels & set(scene["level_range"]):
                continue

        # How many uncovered words does this scene naturally cover?
        uncov_words = {v["word"] for v in uncovered}
        natural_hit = [w for w in scene["natural_words"] if w in uncov_words]
        # Also check broader coverage: words in this topic that match scene topics
        broader_hit = [
            v for v in uncovered
            if v.get("topic", "") in scene["topics"]
            and v.get("level", "?") in scene["level_range"]
        ]

        score = len(natural_hit) * 3 + len(broader_hit)
        scored_scenes.append((scene, natural_hit, broader_hit, score))

    scored_scenes.sort(key=lambda x: -x[3])

    print(f"\n{'='*60}")
    print(f"推荐场景 (按覆盖潜力排序)")
    print(f"{'='*60}")

    for scene, natural_hit, broader_hit, score in scored_scenes[:8]:
        print(f"\n📍 {scene['name']}（{scene['name_zh']}）")
        print(f"   级别: {'/'.join(scene['level_range'])}  格式: {'/'.join(scene['formats'])}")
        print(f"   直接覆盖: {len(natural_hit)}词 — {' '.join(natural_hit[:15])}")
        print(f"   潜在覆盖: {len(broader_hit)}词（同话题同级别）")

        # Show uncovered words grouped by level for this scene's topics
        by_level = defaultdict(list)
        for v in broader_hit:
            by_level[v.get("level", "?")].append(v["word"])
        for lv in ["N5", "N4", "N3", "N2", "N1"]:
            ws = by_level.get(lv, [])
            if ws:
                print(f"   [{lv}] {' '.join(ws[:20])}")

    # Also show uncovered words not matched by any scene
    all_scene_words = set()
    for scene in SCENE_LIBRARY:
        all_scene_words.update(scene["natural_words"])
    orphan = [v for v in uncovered if v["word"] not in all_scene_words]
    if orphan:
        print(f"\n{'='*60}")
        print(f"未被任何场景覆盖的词（可能需要新场景）: {len(orphan)}")
        print(f"{'='*60}")
        by_level = defaultdict(list)
        for v in orphan[:50]:
            by_level[v.get("level", "?")].append(v["word"])
        for lv in ["N5", "N4", "N3", "N2", "N1"]:
            ws = by_level.get(lv, [])
            if ws:
                print(f"  [{lv}] {' '.join(ws[:25])}")


# ─── validate mode ────────────────────────────────────────────────
COLLOQUIAL_MARKERS = [
    (r"〜?てる[。？、]", "縮約形 ～ている→～てる"),
    (r"〜?ちゃ[うっ]", "縮約形 ～てしまう→～ちゃう"),
    (r"〜?じゃん", "口語 じゃん"),
    (r"んだ[けど。よね]", "説明の「んだ」"),
    (r"[かな。？]$", "終助詞 かな"),
    (r"[よね。？]$", "終助詞 よね"),
    (r"[っけ。？]$", "終助詞 っけ"),
    (r"えーと|ええと|まあ|なんか|ほら|あのさ", "フィラー（填充词）"),
    (r"けど[、。]", "逆接の口語形 けど"),
    (r"っていう|って[、。]", "引用の口語形 って"),
]


def check_colloquialism(lines: list[str]) -> dict:
    """Check how colloquial dialogue lines are."""
    markers_found = Counter()
    for line in lines:
        for pattern, name in COLLOQUIAL_MARKERS:
            if re.search(pattern, line):
                markers_found[name] += 1

    total = len(lines)
    unique_markers = len(markers_found)
    score = min(100, unique_markers * 15 + sum(markers_found.values()) * 3)

    return {
        "score": score,
        "unique_markers": unique_markers,
        "total_lines": total,
        "markers": dict(markers_found),
    }


def cmd_validate(args):
    vocab = load_vocab()
    lemmas, surfaces = load_existing_coverage()

    # Load the draft article
    draft_path = Path(args.file)
    if not draft_path.exists():
        print(f"❌ File not found: {draft_path}")
        sys.exit(1)

    draft = json.loads(draft_path.read_text())
    if isinstance(draft, list):
        items = draft
    elif isinstance(draft, dict) and "items" in draft:
        items = draft["items"]
    else:
        items = [draft]

    for item in items:
        print(f"\n{'='*60}")
        print(f"验证: {item.get('titleZh', item.get('titleWord', '?'))}")
        print(f"级别: {item.get('level', '?')}  格式: {item.get('format', '?')}")
        print(f"{'='*60}")

        # Collect all text
        segs = item.get("segments") or []
        for sec in item.get("sections", []):
            segs += sec.get("lines", [])

        all_text = ""
        all_lines = []
        for s in segs:
            text = s.get("jp") or s.get("word") or s[0] if isinstance(s, tuple) else ""
            if isinstance(s, tuple):
                text = s[0]
            all_text += text
            all_lines.append(text)

        # MeCab analysis
        art_lemmas, art_surfaces = get_lemmas_and_surfaces(all_text)

        # New coverage from this article
        newly_covered = []
        for v in vocab:
            word = v["word"]
            if not is_covered(word, lemmas, surfaces) and is_covered(word, art_lemmas, art_surfaces):
                newly_covered.append(v)

        print(f"\n📊 覆盖统计:")
        print(f"   新覆盖词数: {len(newly_covered)}")

        if newly_covered:
            by_level = defaultdict(list)
            for v in newly_covered:
                by_level[v.get("level", "?")].append(v["word"])
            for lv in ["N5", "N4", "N3", "N2", "N1", "?"]:
                ws = by_level.get(lv, [])
                if ws:
                    print(f"   [{lv}] {' '.join(ws)}")

        # Colloquialism check (for dialogues)
        fmt = item.get("format", args.format or "essay")
        if fmt == "dialogue":
            coll = check_colloquialism(all_lines)
            print(f"\n🗣️ 口语化评分: {coll['score']}/100")
            print(f"   口语特征种类: {coll['unique_markers']}/10")
            if coll["markers"]:
                for marker, count in sorted(coll["markers"].items(), key=lambda x: -x[1]):
                    print(f"     ✓ {marker}: {count}处")
            if coll["score"] < 40:
                print(f"\n   ⚠️ 口语化不足。建议添加:")
                missing = [name for _, name in COLLOQUIAL_MARKERS if name not in coll["markers"]]
                for m in missing[:5]:
                    print(f"     · {m}")

        # Sentence count and length
        print(f"\n📝 结构:")
        print(f"   句子数: {len(all_lines)}")
        lengths = [len(l) for l in all_lines if l]
        if lengths:
            print(f"   平均句长: {sum(lengths)/len(lengths):.0f}字")
            print(f"   最短/最长: {min(lengths)}/{max(lengths)}")

        # Format check
        issues = []
        for s in segs:
            if isinstance(s, dict):
                text = s.get("jp") or s.get("word", "")
                if "？。" in text:
                    issues.append(f"标点重复「？。」: {text[:30]}")
                if not s.get("zh"):
                    issues.append(f"缺中文翻译: {text[:30]}")
                if not s.get("en"):
                    issues.append(f"缺英文翻译: {text[:30]}")

        if issues:
            print(f"\n⚠️ 格式问题:")
            for iss in issues[:10]:
                print(f"   · {iss}")
        else:
            print(f"\n✅ 格式检查通过")


# ─── main ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Article generation helper")
    sub = parser.add_subparsers(dest="cmd")

    p_suggest = sub.add_parser("suggest", help="Recommend scenes for uncovered vocab")
    p_suggest.add_argument("--topic", help="Filter by topic (e.g. 生活用品, 食物料理)")
    p_suggest.add_argument("--level", help="Target level (e.g. N4-N3, N2)")

    p_validate = sub.add_parser("validate", help="Validate a draft article")
    p_validate.add_argument("--file", required=True, help="Path to draft JSON")
    p_validate.add_argument("--format", help="Force format (essay/dialogue)")

    args = parser.parse_args()
    if args.cmd == "suggest":
        cmd_suggest(args)
    elif args.cmd == "validate":
        cmd_validate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
