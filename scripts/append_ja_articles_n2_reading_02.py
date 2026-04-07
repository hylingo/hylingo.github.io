#!/usr/bin/env python3
"""
N2阅读理解长文 #02 → public/data/ja_articles.json
「時間に正確すぎる国で」（在过于守时的国家里）

约1000字，N2読解長文风格。

运行: python3 scripts/append_ja_articles_n2_reading_02.py
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
    "id": "n2-reading-too-punctual-country",
    "level": "N2",
    "format": "essay",
    "titleWord": "時間に正確すぎる国で",
    "titleJp": "時間に正確すぎる国で",
    "titleEn": "In a country too punctual for its own good",
    "titleZh": "在过于守时的国家里",
    "titleRuby": [],
    "segments": [
        seg(
            "ある外国人の友人が、日本に来て一番驚いたことは何かと聞かれて、こう答えたことがある。「電車が時刻表どおりに来ること。それも、秒単位で。」",
            "A foreign friend of mine, when asked what surprised him most after coming to Japan, once answered like this: \"That the trains come exactly on schedule. And by the second, no less.\"",
            "有一位外国朋友被问到来日本后最惊讶的事是什么时，曾这样回答：「电车真的会按时刻表来。而且，是按秒计算。」",
            paragraph_start=True,
        ),
        seg(
            "私たち日本人にとっては、電車が定刻に来るのは当たり前のことであって、特に意識したこともなかった。むしろ、一分でも遅れれば駅員がアナウンスで謝罪する光景にすら、何の違和感も覚えない。",
            "For us Japanese, trains arriving on time is simply taken for granted—not something we ever consciously notice. We don't even feel anything strange about the sight of station staff apologizing over the loudspeaker for a delay of even a single minute.",
            "对我们日本人来说，电车准点到站是理所当然的事，甚至从来没有特意意识过。哪怕只晚了一分钟，车站工作人员就会通过广播道歉——对这样的画面，我们也丝毫不觉得有什么奇怪。",
        ),
        seg(
            "しかし、彼の言葉を聞いてから、私は少しずつそのことを違う角度から眺めるようになった。",
            "But after hearing his words, I gradually came to look at it from a different angle.",
            "可是听了他那句话之后，我开始一点一点从不同的角度来看这件事。",
        ),
        seg(
            "考えてみれば、日本社会において「時間を守る」ということは、単なる礼儀の問題ではない。それは、相手の時間を奪わないという倫理であり、同時に、自分自身を律するための厳しい規範でもある。",
            "Come to think of it, in Japanese society, \"keeping time\" is not merely a matter of manners. It is an ethic of not stealing another's time, and at the same time, a strict discipline imposed on oneself.",
            "仔细想想，在日本社会，「守时」并不只是礼貌问题。它既是一种「不夺走对方时间」的伦理，同时也是一种约束自己的严格规范。",
            paragraph_start=True,
        ),
        seg(
            "約束の五分前に着くことが当然とされ、五分遅れただけで信用を失いかねない。会議の開始時刻には全員がすでに着席しており、終了時刻もきっちり守られる。",
            "Arriving five minutes early to an appointment is taken as a given, and being just five minutes late can cost you trust. By the meeting's start time, everyone is already seated, and the end time is observed just as strictly.",
            "约定的时间提前五分钟到是理所当然，仅仅迟到五分钟就可能失去信用。会议开始时大家早已就座，结束时间也分秒不差。",
        ),
        seg(
            "こうした正確さが日本の経済や社会の効率を支えてきたことは、否定しようがない。新幹線が世界に誇られるのも、宅配便が翌日には届くのも、すべてはこの「時間への忠実さ」の上に成り立っている。",
            "There's no denying that this precision has long supported the efficiency of Japan's economy and society. The pride Japan takes in its bullet trains, the way parcels arrive the very next day—all of it stands on this \"faithfulness to time.\"",
            "这种精确性长期支撑着日本的经济和社会效率，这一点无法否认。新干线之所以能引以为豪，快递之所以能次日送达，全都建立在这种「对时间的忠实」之上。",
        ),
        seg(
            "けれども、その一方で、私たちは何か大切なものを少しずつすり減らしてきたのではないだろうか。",
            "And yet, on the other hand, haven't we, little by little, been wearing away something important?",
            "可是另一方面，我们是不是也在一点一点地磨损着某些重要的东西？",
            paragraph_start=True,
        ),
        seg(
            "予定どおりに進まないことへの不安。一分の遅れも許されない緊張感。電車が止まれば舌打ちが聞こえ、列が少し乱れれば溜息がもれる。便利さと引き換えに、私たちはずいぶんと余裕を失ってしまったように思えてならない。",
            "The anxiety when things don't go as planned. The tension of not being allowed even a minute's delay. When a train stops, you hear clicks of the tongue; when a line breaks down a little, sighs escape. In exchange for convenience, it seems to me we have lost a great deal of our composure.",
            "对计划无法按时进行的不安。连一分钟延误都不被允许的紧张感。电车一停，就能听到咂嘴声；队伍稍微乱一点，就有人叹气。在换取便利的同时，我总觉得我们已经失去了相当多的从容。",
        ),
        seg(
            "外国を旅していると、時間に対するもっとゆるやかな感覚に出会うことがある。バスは来ないかもしれないし、店は気まぐれに閉まっているかもしれない。最初は戸惑うものの、しばらくいるうちに、不思議と心がほどけていくのを感じる。",
            "Traveling abroad, you sometimes encounter a more relaxed sense of time. The bus may not come; the shop may be closed on a whim. At first you're flustered, but after staying a while, strangely, you feel your heart loosening.",
            "在外国旅行时，有时会遇到一种更加宽松的时间观。公交车可能不来，店铺可能心血来潮就关了门。一开始虽然不知所措，但待上一段时间后，竟会奇妙地感到心松了下来。",
        ),
        seg(
            "もちろん、ルーズな社会に憧れているわけではない。時間を守ることそのものは、間違いなく美徳である。問題は、それが行き過ぎたとき、私たちの心からゆとりや寛容さまで奪ってしまうという点にある。",
            "Of course, I'm not longing for a lax society. Punctuality itself is, without question, a virtue. The problem lies in the fact that when it goes too far, it strips even composure and tolerance from our hearts.",
            "当然，我并不是在向往一个散漫的社会。守时本身毫无疑问是美德。问题在于，当它走得太远时，连同从容和宽容也会从我们心里被夺走。",
            paragraph_start=True,
        ),
        seg(
            "電車が遅れたとき、苛立つ代わりに「まあ、こういう日もある」と肩の力を抜くことが、私たちにはもう少し必要なのかもしれない。一分の遅れに目くじらを立てる社会と、一分の遅れを笑って許せる社会と、本当に豊かなのはどちらだろうか。",
            "When the train is late, instead of getting irritated, perhaps what we need a little more of is the ability to shrug and say, \"Well, days like this happen too.\" Between a society that makes a fuss over a one-minute delay, and a society that can smile and forgive that minute, which is truly the richer one?",
            "电车晚点的时候，或许我们更需要的是放松一下肩膀、想一句「嘛，也会有这样的日子」，而不是焦躁。一个对一分钟延误大动肝火的社会，和一个能笑着原谅那一分钟的社会——真正富足的，到底是哪一边呢？",
        ),
        seg(
            "あの友人は、こうも言っていた。「時間が正確すぎる国は、たぶん、人にも正確さを求めすぎる国なんだろうね。」その言葉は、今でも私の中で静かに響き続けている。",
            "That friend also said this: \"A country where time is too precise is probably also a country that demands too much precision from its people.\" Those words still echo quietly inside me.",
            "那位朋友还说过这样一句话：「时间过于精确的国家，大概也是对人过于严苛的国家吧。」那句话至今仍在我心中静静地回响。",
            paragraph_start=True,
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
    # 统计字数
    total = sum(len(s["jp"]) for s in ARTICLE["segments"])
    print(f"✅ Added {ARTICLE['id']}, {total} chars, total {len(data['items'])}")


if __name__ == "__main__":
    main()
