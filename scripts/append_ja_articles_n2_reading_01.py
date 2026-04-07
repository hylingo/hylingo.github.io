#!/usr/bin/env python3
"""
N2阅读理解长文 #01 → public/data/ja_articles.json
「本を読まなくなった私へ」（致不再读书的我）

约750字，N2読解長文风格，议论随笔。

运行: python3 scripts/append_ja_articles_n2_reading_01.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_ruby as gr  # noqa: E402


def full_reading(sentence: str) -> str:
    parts: list[str] = []
    for w in gr.tagger(sentence):
        k = w.feature.kana
        parts.append(gr.to_hira(k) if k else w.surface)
    return "".join(parts)


def seg(word: str, en: str, zh: str, paragraph_start: bool = False) -> dict:
    w = word.strip()
    d = {
        "word": w, "jp": w, "en": en.strip(), "zh": zh.strip(),
        "reading": full_reading(w), "ruby": gr.make_ruby(w),
    }
    if paragraph_start:
        d["paragraphStart"] = True
    return d


ARTICLE = {
    "id": "n2-reading-books-no-longer-read",
    "level": "N2",
    "format": "essay",
    "titleWord": "本を読まなくなった私へ",
    "titleJp": "本を読まなくなった私へ",
    "titleEn": "To the me who stopped reading books",
    "titleZh": "致不再读书的我",
    "titleRuby": [],
    "segments": [
        seg(
            "気がつけば、もう半年以上、一冊の本も最後まで読み通していない。",
            "Before I knew it, more than half a year had passed without my finishing a single book.",
            "回过神来，已经半年多没有把一本书从头读到尾了。",
            paragraph_start=True,
        ),
        seg(
            "学生時代の私は、通学電車の中でも、寝る前の数十分でも、必ず本を開いていた。むしろ、本を読まない日があるなど考えられなかったと言ってもいい。",
            "When I was a student, I always had a book open—on the train to school, in the few dozen minutes before bed. In fact, you could say a day without reading was unthinkable.",
            "学生时代的我，无论是在上学的电车里，还是睡前的几十分钟，都一定会翻开书本。甚至可以说，没读书的日子根本无法想象。",
        ),
        seg(
            "それがいつの間にか、本棚の本は埃をかぶり、新しく買った本も帯すら外さないまま積み上がっていく一方だ。",
            "Yet at some point, the books on my shelf gathered dust, and even newly bought ones piled up with the obi still on, untouched.",
            "可不知何时起，书架上的书蒙了灰，新买的书连腰封都没拆，就那样越堆越高。",
            paragraph_start=True,
        ),
        seg(
            "代わりに私が手にしているのは、言うまでもなくスマートフォンである。SNS、動画、ニュースアプリ——指先一つで膨大な情報が流れ込んでくる。",
            "What I hold in my hand instead is, needless to say, a smartphone. Social media, videos, news apps—with a flick of my finger, an immense flood of information pours in.",
            "取而代之，我手里拿的不用说就是智能手机。SNS、视频、新闻APP——指尖一动，海量信息便涌进来。",
        ),
        seg(
            "しかし、一日の終わりに「今日は何を知ったのか」と自分に問いかけてみると、答えに詰まってしまうことが多い。",
            "But when I ask myself at the end of the day, \"What did I actually learn today?\", I often find myself at a loss for an answer.",
            "可是到了一天结束时，问自己「今天到底知道了什么」，往往答不上来。",
        ),
        seg(
            "短い文章を次々と消費しているうちに、何かを「知った気になる」ことだけが上手になってしまったのではないか。情報を浴びれば浴びるほど、かえって自分の頭で考える時間は失われていく。",
            "While consuming one short piece after another, perhaps I've only become skilled at \"feeling like I know\" something. The more information I bathe in, the more time I lose for thinking with my own head.",
            "在不断消费碎片文章的过程中，恐怕我变得擅长的只是「自以为知道了」这件事。越是被信息淹没，反而越失去用自己的脑子思考的时间。",
            paragraph_start=True,
        ),
        seg(
            "本を読むという行為は、もともと効率のいいものではない。一冊を読み終えるのに何時間もかかるし、読んだところですぐに役に立つとは限らない。",
            "The act of reading a book is, by nature, not efficient. It takes hours to finish one, and even when you do, it doesn't necessarily help you right away.",
            "读书这件事，本来就不是讲效率的事情。读完一本要花好几个小时，而且读了也未必马上有用。",
        ),
        seg(
            "それでも、ページをめくる静かな時間の中でしか出会えない言葉があり、その言葉に支えられて生きてきた瞬間が、確かに私にはあったはずだ。",
            "Even so, there are words you can only meet in the quiet time of turning pages, and there were surely moments in my life sustained by those words.",
            "即便如此，也有些话只能在翻页的安静时光里遇见，被那些话语支撑着活下去的瞬间，我应该确实有过。",
        ),
        seg(
            "便利さを手に入れる代わりに、私たちは何を手放してきたのだろうか。",
            "In exchange for convenience, what have we let go of?",
            "在换取便利的同时，我们到底放手了什么呢？",
            paragraph_start=True,
        ),
        seg(
            "今日の帰り道、駅前の小さな本屋に寄ってみようと思う。何を買うかは決めていない。ただ、棚の前に立ち、背表紙を一つ一つ眺めるあの時間を、もう一度自分に許してやりたいのだ。",
            "On my way home today, I think I'll drop by the little bookstore in front of the station. I haven't decided what to buy. I just want to give myself, once again, that time of standing before the shelves and gazing at one spine after another.",
            "今天回家路上，我打算去车站前的小书店看看。买什么还没决定。我只是想再一次允许自己拥有那段——站在书架前、一本一本凝视着书脊的时光。",
        ),
    ],
}


def main() -> None:
    fp = ROOT / "public" / "data" / "ja_articles.json"
    data = json.loads(fp.read_text("utf-8"))
    exist = {it["id"] for it in data["items"]}
    if ARTICLE["id"] in exist:
        print(f"⚠️  {ARTICLE['id']} already exists, skipped.")
        return
    data["items"].append(ARTICLE)
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"✅ Added {ARTICLE['id']}, total {len(data['items'])}")


if __name__ == "__main__":
    main()
