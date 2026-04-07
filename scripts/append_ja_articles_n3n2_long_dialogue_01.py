#!/usr/bin/env python3
"""
N3-N2 长 dialogue #01 → public/data/ja_articles.json
「深夜の居酒屋で」（同期との再会）

两个老同事在深夜居酒屋偶然重逢，从闲聊到人生感慨。
约 25 行，4 个场景。两个男声适用。

运行: python3 scripts/append_ja_articles_n3n2_long_dialogue_01.py
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


def line(speaker: str, word: str, en: str, zh: str) -> dict:
    w = word.strip()
    return {
        "word": w, "jp": w, "en": en.strip(), "zh": zh.strip(),
        "reading": full_reading(w), "ruby": gr.make_ruby(w),
        "speaker": speaker,
    }


def section(heading, heading_en, heading_zh, badge, lines_list):
    return {
        "badge": badge,
        "headingWord": heading, "headingJp": heading,
        "headingEn": heading_en, "headingZh": heading_zh,
        "lines": lines_list,
    }


ARTICLE = {
    "id": "n3n2-late-night-izakaya-reunion",
    "level": "N3–N2",
    "format": "dialogue",
    "titleWord": "深夜の居酒屋で（同期との再会）",
    "titleJp": "深夜の居酒屋で（同期との再会）",
    "titleEn": "At a late-night izakaya (reunion with an old colleague)",
    "titleZh": "深夜居酒屋（与老同事的重逢）",
    "titleRuby": [],
    "sections": [
        section("再会", "Reunion", "重逢", "🍶", [
            line("A", "あれ？……ちょっと待って、もしかして田中じゃない？",
                 "Hold on a sec... could that be you, Tanaka?",
                 "诶？……等等，你不会是田中吧？"),
            line("B", "え？……うわ、山本？嘘だろ、こんなところで。",
                 "Huh? ...Wow, Yamamoto? You're kidding, here of all places.",
                 "啊？……哇，山本？不会吧，居然在这儿碰上。"),
            line("A", "いや、こっちこそびっくりだよ。何年ぶりだ、これ。",
                 "No, I'm the one who's shocked. How many years has it been?",
                 "我才吓一跳呢。这都几年没见了？"),
            line("B", "うーん、お前が会社辞めたのが、確か俺が結婚した年だったから……",
                 "Hmm, you quit the company the same year I got married, so...",
                 "嗯，你辞职那年好像就是我结婚那年，所以……"),
            line("A", "ああ、じゃあもう七年くらい経つのか。早いな、本当に。",
                 "Ah, so it's been about seven years already. Time really flies.",
                 "啊，那已经七年左右了啊。真快。"),
            line("B", "とりあえず座れよ。ちょうど一人で飲んでたところだから。",
                 "Anyway, sit down. I was just drinking alone anyway.",
                 "总之先坐下。我正一个人喝着呢。"),
            line("A", "じゃあ、お言葉に甘えて。すみません、生ビール一つお願いします。",
                 "Well then, don't mind if I do. Excuse me, one draft beer please.",
                 "那我就不客气了。不好意思，来一杯生啤。"),
            line("B", "しかし、本当に久しぶりだな。全然変わってないように見えるけど。",
                 "But really, it's been so long. You look like you haven't changed at all.",
                 "话说真的好久了。看起来你一点都没变。"),
            line("A", "嘘つけ。鏡見るたびに、あ、歳取ったなって思うよ。",
                 "Yeah right. Every time I look in the mirror, I think, oh, I've gotten old.",
                 "胡说。每次照镜子都觉得，哎，老了。"),
        ]),
        section("昔の話", "Old times", "过去的事", "📷", [
            line("B", "なあ、覚えてる？入社してすぐの頃、あの部長によく怒られてたよな。",
                 "Hey, remember? Right after we joined the company, we used to get yelled at by that department head all the time.",
                 "诶你还记得吗？刚入职那会儿，老被那个部长骂。"),
            line("A", "ああ、田村部長な。あの人、声がでかくてさ、廊下まで響いてた。",
                 "Ah, Tamura. That guy had such a loud voice, it echoed all the way down the hallway.",
                 "啊，田村部长。那人嗓门大，骂人连走廊都听得见。"),
            line("B", "お前、報告書のミスで一時間以上説教されたことあったよな。",
                 "You got lectured for over an hour once because of a mistake in your report, didn't you?",
                 "你不是有一次因为报告里的错被训了一个多小时？"),
            line("A", "あれ、本当に泣きそうだったよ。あの時、田中がトイレでこっそり缶コーヒー渡してくれたの、今でも覚えてる。",
                 "I was honestly about to cry then. I still remember how you secretly handed me a can of coffee in the bathroom.",
                 "那次真的快哭了。当时你在厕所偷偷递给我一罐咖啡的事，到现在还记得。"),
            line("B", "そんなことあったっけ？俺、全然覚えてないわ。",
                 "Did that happen? I don't remember at all.",
                 "有这回事吗？我完全不记得了。"),
            line("A", "覚えてないのかよ。こっちは一生忘れないっつーの。",
                 "You don't remember?! I'm telling you, I'll never forget that.",
                 "你居然忘了？！我可是一辈子都忘不了。"),
        ]),
        section("近況", "How we're doing", "近况", "💼", [
            line("B", "それで、今は何してるの？どっかに勤めてる？",
                 "So, what are you doing now? Working somewhere?",
                 "话说，你现在在干嘛？在哪儿上班？"),
            line("A", "実は、去年から自分で小さい会社やってるんだ。",
                 "Actually, I started running my own little company last year.",
                 "其实，去年开始自己开了个小公司。"),
            line("B", "へえ、すごいじゃん。やっぱり昔から独立したがってたもんな、お前。",
                 "Wow, impressive. You always wanted to go independent, didn't you.",
                 "哇厉害啊。你以前就一直想独立创业嘛。"),
            line("A", "まあね。でも、やってみたら思った以上に大変でさ。",
                 "Yeah, well. But once I actually tried, it was harder than I'd thought.",
                 "嗯。不过真做起来，比想象的还辛苦。"),
            line("A", "毎月の支払いのことを考えると、夜眠れないこともあるよ。",
                 "When I think about the monthly bills, there are nights I can't sleep.",
                 "一想到每月要付的钱，有时候晚上都睡不着。"),
            line("B", "そうだろうな。会社にいると気づかないけど、毎月給料がもらえるって、本当はすごくありがたいことなんだよな。",
                 "I bet. You don't notice it when you're at a company, but getting a paycheck every month is really something to be grateful for.",
                 "可不是嘛。在公司感觉不到，但每个月能领到工资这件事，其实是非常值得感激的。"),
            line("A", "ほんとそう思う。あの頃の俺、文句ばっかり言ってたけどさ。",
                 "I really think so. Back then, all I did was complain.",
                 "真的这么觉得。那会儿的我啊，光会发牢骚。"),
            line("B", "お前だけじゃないよ。みんなそんなもんだ。",
                 "Not just you. Everyone's like that.",
                 "也不光你。大家都那样。"),
        ]),
        section("家族の話", "Family", "家庭", "👨‍👩‍👧", [
            line("A", "そういえば、田中、子供できたんだろ？",
                 "Oh right, you've got kids now, don't you, Tanaka?",
                 "对了，田中你不是有孩子了吗？"),
            line("B", "うん、上が五歳で、下が二歳。毎日もうバタバタだよ。",
                 "Yeah, the older one's five and the younger one's two. Every day is just chaos.",
                 "嗯，老大五岁，老二两岁。每天都忙得团团转。"),
            line("A", "それは大変だな。でも、家に帰って子供の顔見たら、疲れも飛ぶんじゃない？",
                 "That sounds rough. But when you get home and see your kids' faces, doesn't the tiredness just disappear?",
                 "那挺辛苦的。不过回家看到孩子的脸，疲劳也会一下子飞了吧？"),
            line("B", "まあ、たまにはな。でも正直、自分の時間が全然ないのはつらい。",
                 "Well, sometimes. But honestly, having no time for myself is rough.",
                 "嗯，偶尔吧。不过说实话，完全没自己的时间挺难受的。"),
            line("B", "山本は？結婚は？",
                 "What about you, Yamamoto? Married?",
                 "山本你呢？结婚了吗？"),
            line("A", "してないよ、まだ。仕事にかまけてたら、いつの間にかこの歳。",
                 "Nope, not yet. I got caught up in work, and before I knew it, here I am at this age.",
                 "没呢。一忙工作，不知不觉就到这岁数了。"),
            line("B", "後悔してる？",
                 "Do you regret it?",
                 "后悔吗？"),
            line("A", "後悔……というか、ときどき、ふと寂しくなる瞬間があるんだよな。",
                 "Regret... well, more like, sometimes I just suddenly feel lonely.",
                 "后悔……倒不如说，有时候会突然感到寂寞。"),
            line("A", "今日みたいに、誰かと飲んでて、家に帰ったあと、あの静けさがちょっとな。",
                 "Like today, after drinking with someone and going home—that silence gets to me a bit.",
                 "像今天这样，跟人喝完酒回到家，那种安静有点……"),
            line("B", "……うん。それは、わかる気がするよ。",
                 "...Yeah. I think I get that.",
                 "……嗯。那种感觉，我好像懂。"),
        ]),
        section("別れ際", "Saying goodbye", "告别", "🚃", [
            line("A", "あ、もうこんな時間か。終電、ぎりぎりだな。",
                 "Oh, it's already this late. The last train—I'm cutting it close.",
                 "啊，已经这个点了啊。末班车，够呛了。"),
            line("B", "本当だ。話してると、時間ってあっという間に過ぎるな。",
                 "Yeah really. When you're talking, time just flies by.",
                 "真的。聊起天来，时间过得飞快。"),
            line("A", "今日は本当にありがとな。久しぶりに、心から笑った気がする。",
                 "Thanks for today, really. I feel like I laughed from the heart for the first time in a long while.",
                 "今天真的谢谢你。感觉好久没有从心底笑过了。"),
            line("B", "こっちこそ。たまには昔の同期と話すのも、悪くないもんだな。",
                 "Same here. Talking with an old colleague every now and then isn't bad at all.",
                 "我才该谢你呢。偶尔跟老同事聊聊，挺不错的。"),
            line("A", "また連絡するよ。今度はもっと早い時間に飲もう。",
                 "I'll be in touch. Next time, let's drink at a more reasonable hour.",
                 "我再联系你。下次早点喝。"),
            line("B", "ああ、楽しみにしてる。お互い、無理しすぎるなよ。",
                 "Yeah, looking forward to it. Let's both not push ourselves too hard.",
                 "嗯，等着你。咱俩都别太逞强。"),
            line("A", "うん。じゃあ、またな。",
                 "Yeah. Well, see you.",
                 "嗯。那，再见。"),
            line("B", "またな。気をつけて帰れよ。",
                 "See you. Get home safe.",
                 "再见。路上小心。"),
        ]),
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
    chars = sum(len(l["jp"]) for sec in ARTICLE["sections"] for l in sec["lines"])
    lines = sum(len(sec["lines"]) for sec in ARTICLE["sections"])
    print(f"✅ Added {ARTICLE['id']}, {lines} lines, {chars} chars, total {len(data['items'])}")


if __name__ == "__main__":
    main()
