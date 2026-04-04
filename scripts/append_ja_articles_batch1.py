#!/usr/bin/env python3
"""
向 public/data/ja_articles.json 追加精读文章（日语），并保持单行 JSON 格式。

依赖（与 generate_ruby.py 相同）: pip install 'fugashi[unidic-lite]'
建议在项目 .venv 中: .venv/bin/python scripts/append_ja_articles_batch1.py

本批次学习目标:
- N4–N3 医疗: 症状说明、受付、診察の定型、薬局
- N3 职场沟通: メールの限界、口頭で日程を確定、ビジネス表現
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


def enrich_segment(word: str, en: str, zh: str) -> dict:
    w = word.strip()
    return {
        "word": w,
        "jp": w,
        "en": en.strip(),
        "zh": zh.strip(),
        "reading": full_reading(w),
        "ruby": gr.make_ruby(w),
    }


def enrich_line(speaker: str, word: str, en: str, zh: str) -> dict:
    d = enrich_segment(word, en, zh)
    d["speaker"] = speaker
    return d


def enrich_title_ruby(title_word: str) -> list:
    return gr.make_ruby(title_word.strip())


def section(
    heading: str,
    heading_en: str,
    heading_zh: str,
    badge: str,
    lines: list[tuple[str, str, str, str]],
) -> dict:
    """lines: (speaker 'A'|'B', word, en, zh)"""
    return {
        "badge": badge,
        "headingWord": heading,
        "headingJp": heading,
        "headingEn": heading_en,
        "headingZh": heading_zh,
        "lines": [enrich_line(sp, w, e, z) for sp, w, e, z in lines],
    }


NEW_ITEMS: list[dict] = [
    # --- N4–N3 医疗 ---
    {
        "id": "n4-clinic-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "かかりつけのクリニックで",
        "titleJp": "かかりつけのクリニックで",
        "titleEn": "At my regular clinic",
        "titleZh": "在常去的诊所",
        "titleRuby": [],  # filled below
        "segments": [
            (
                "風邪のような気がしたので、近所のクリニックへ行った。",
                "I felt like I was coming down with a cold, so I went to a nearby clinic.",
                "我觉得像要感冒，就去了附近的诊所。",
            ),
            (
                "受付で「今日はどうされましたか」と聞かれ、のどの痛みと熱があると説明した。",
                'At reception they asked, "What brings you in today?" and I explained my sore throat and fever.',
                "在接待处被问「今天哪里不舒服」，我说明了喉咙痛和发烧。",
            ),
            (
                "保険証を出し、問診票に名前と症状を書いた。",
                "I showed my health insurance card and wrote my name and symptoms on the intake form.",
                "出示保险证，在问诊表上写了姓名和症状。",
            ),
            (
                "待合室では、呼ばれるまで雑誌をめくりながら待った。",
                "In the waiting room I flipped through a magazine until my name was called.",
                "在候诊室翻杂志等到叫号。",
            ),
            (
                "看護師さんに体温を測ってもらうと、三十八度だった。",
                "The nurse took my temperature; it was 38 degrees.",
                "护士量体温，是三十八度。",
            ),
            (
                "診察室に入ると、先生に「いつからですか」と聞かれた。",
                'In the exam room the doctor asked, "Since when?"',
                "进诊室后，医生问「从什么时候开始的」。",
            ),
            (
                "昨日の夜からだと答えると、のどをよく見てくれた。",
                "When I said since last night, they looked carefully at my throat.",
                "我回答从昨晚开始，医生仔细看了喉咙。",
            ),
            (
                "大事には至らないが、今日は無理せず休むようにと言われた。",
                "They said it was nothing serious, but told me not to push myself and to rest today.",
                "医生说没有大碍，但叫我今天别勉强、好好休息。",
            ),
            (
                "薬は三日分で、飲み方は紙に書いてもらった。",
                "I got three days' worth of medicine, with instructions written on paper.",
                "药开了三天份，用法写在纸上。",
            ),
            (
                "会計を済ませてから、すぐ近くの薬局へ処方せんを持っていった。",
                "After paying, I took the prescription to a pharmacy right nearby.",
                "付完账，马上把处方拿到附近的药房。",
            ),
            (
                "薬剤師に「食後に飲んでください」と丁寧に言われた。",
                'The pharmacist politely told me, "Please take this after meals."',
                "药剂师客气地说「请饭后服用」。",
            ),
            (
                "家に帰って薬を飲み、ゆっくり眠った。",
                "I went home, took the medicine, and slept well.",
                "回家吃药，好好睡了一觉。",
            ),
            (
                "次の日にはのどの痛みがだいぶ楽になり、ほっとした。",
                "The next day my throat felt much better, and I was relieved.",
                "第二天喉咙轻松多了，松了一口气。",
            ),
        ],
    },
    {
        "id": "n4-clinic-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "クリニックで（受付・診察）",
        "titleJp": "クリニックで（受付・診察）",
        "titleEn": "At the clinic (reception and exam)",
        "titleZh": "在诊所（接待与看诊）",
        "titleRuby": [],
        "sections": [
            section(
                "受付",
                "Reception",
                "接待处",
                "🏥",
                [
                    (
                        "A",
                        "おはようございます。本日はどのような症状でしょうか。",
                        "Good morning. What symptoms are you having today?",
                        "早上好。今天主要是哪里不舒服？",
                    ),
                    (
                        "B",
                        "のどが痛くて、熱っぽいです。昨日の夜からです。",
                        "My throat hurts and I feel feverish. It started last night.",
                        "喉咙痛，有点发烧。从昨晚开始的。",
                    ),
                    (
                        "A",
                        "かしこまりました。保険証と、こちらの問診票にお名前をお願いします。",
                        "Understood. Please show your insurance card and write your name on this intake form.",
                        "好的。请出示保险证，并在这张问诊表上填写姓名。",
                    ),
                    (
                        "B",
                        "はい……書きました。これでよろしいでしょうか。",
                        "Yes... I've finished. Is this all right?",
                        "好的……写好了。这样可以吗？",
                    ),
                    (
                        "A",
                        "ありがとうございます。では、こちらでお待ちください。お呼びしたら診察室へどうぞ。",
                        "Thank you. Please wait here. When we call you, please go to the exam room.",
                        "谢谢。请在此等候。叫到您时请进诊室。",
                    ),
                ],
            ),
            section(
                "待合室",
                "Waiting area",
                "候诊室",
                "🪑",
                [
                    (
                        "B",
                        "（小さな声で）緊張するなあ……番号、合ってるかな。",
                        "(Quietly) I'm nervous... I hope I heard the number right.",
                        "（小声）好紧张……号码没听错吧。",
                    ),
                    (
                        "A",
                        "リンさん、診察室へどうぞ。",
                        "Ms. Rin, please come to the exam room.",
                        "琳小姐，请进诊室。",
                    ),
                    (
                        "B",
                        "はい、失礼します。",
                        "Yes, excuse me.",
                        "好的，打扰了。",
                    ),
                ],
            ),
            section(
                "診察",
                "Examination",
                "看诊",
                "🩺",
                [
                    (
                        "A",
                        "では、のどを見せてください。あー、と言ってみてください。",
                        "Please show me your throat. Say \"ah\" for me.",
                        "请让我看一下喉咙。请发「啊——」的声音。",
                    ),
                    (
                        "B",
                        "あー……。",
                        "Ahh...",
                        "啊——……",
                    ),
                    (
                        "A",
                        "少し赤いですね。咳は出ますか。",
                        "It's a little red. Are you coughing?",
                        "有点红。会咳嗽吗？",
                    ),
                    (
                        "B",
                        "ときどき、少し出ます。",
                        "Sometimes, a little.",
                        "偶尔，有一点点。",
                    ),
                    (
                        "A",
                        "わかりました。今日は休んで、薬を飲んで様子を見ましょう。無理はしないでくださいね。",
                        "I see. Rest today, take the medicine, and see how it goes. Please don't overdo it.",
                        "明白了。今天先休息，吃药观察。请不要勉强。",
                    ),
                    (
                        "B",
                        "はい、ありがとうございます。",
                        "Yes, thank you very much.",
                        "好的，非常感谢。",
                    ),
                ],
            ),
            section(
                "帰り",
                "Leaving",
                "离开",
                "💊",
                [
                    (
                        "B",
                        "すみません、会計はこちらでよかったでしょうか。",
                        "Excuse me, is this the right place to pay?",
                        "请问，结账是在这里吗？",
                    ),
                    (
                        "A",
                        "はい、こちらです。二千三百円になります。お大事にどうぞ。",
                        "Yes, here. That will be 2,300 yen. Please take care.",
                        "是的，这边。共二千三百日元。请多保重。",
                    ),
                    (
                        "B",
                        "ありがとうございました。",
                        "Thank you very much.",
                        "谢谢您。",
                    ),
                ],
            ),
        ],
    },
    # --- N3 职场：日程調整 ---
    {
        "id": "n3-schedule-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "日程は、短い会話から決まることもある",
        "titleJp": "日程は、短い会話から決まることもある",
        "titleEn": "Sometimes a schedule is settled in a short conversation",
        "titleZh": "有时，日程是在简短对话里定下来的",
        "titleRuby": [],
        "segments": [
            (
                "新しいプロジェクトが始まり、チームで初めての打ち合わせの日時を決めなければならなかった。",
                "A new project started, and our team had to set a date and time for the first meeting.",
                "新项目启动，团队必须定下第一次开会的时间。",
            ),
            (
                "私はメールで三つの候補日を送り、「ご都合のよい日を教えてください」と書いた。",
                'I emailed three candidate dates and wrote, "Please let me know which day works for you."',
                "我发了邮件列出三个候选日期，并写「请告知方便的一天」。",
            ),
            (
                "ところが返信は一人分だけで、「その週は少し厳しいです」とだけ返ってきた。",
                'But only one person replied, saying just, "That week is a bit tight for me."',
                "结果只有一个人回信，而且只写「那周有点难」。",
            ),
            (
                "別の候補が書かれていないので、会議は宙に浮いたままになってしまった。",
                "With no alternative suggested, the meeting was left up in the air.",
                "没有写别的备选，会议就一直悬着。",
            ),
            (
                "廊下で別のメンバーに会ったので、カレンダーを携帯で見せながら、五分ほど声で調整してみた。",
                "I ran into another member in the hallway and tried to coordinate in person for about five minutes, showing our calendars on our phones.",
                "在走廊遇到另一位成员，用手机日历对着面，试着用五分钟口头协调。",
            ),
            (
                "すると「火曜の午後なら空いています」とすぐ言ってくれ、他の二人にも口頭で聞いて回ると、同じ日にまとまった。",
                'Then they quickly said, "Tuesday afternoon is open," and when I asked the other two in person, we settled on the same day.',
                "对方马上说「周二下午可以」，我又口头问了另外两人，最后定在同一天。",
            ),
            (
                "メールは記録には向いているが、曖昧な一言で止まってしまうこともあると痛感した。",
                "I felt sharply that email is good for records, but it can also stop at a vague one-liner.",
                "我深切感到：邮件适合留记录，但也可能停在一句含糊的话上。",
            ),
            (
                "特に「検討します」「できれば」などは、本当に調整する気があるのか読みにくい。",
                'Especially phrases like "I\'ll consider it" or "If possible" are hard to read for real intent.',
                "尤其是「研究一下」「可以的话」之类，很难读出对方是否真的想协调。",
            ),
            (
                "対面や短い通話なら、間の取り方や表情から、続きの一言を引き出しやすい。",
                "In person or on a short call, pacing and facial cues make it easier to draw out the next sentence.",
                "面对面或简短电话，从停顿和表情更容易引出下一句话。",
            ),
            (
                "もちろん、決まった内容はあとでメールに書き、誤解がないように共有する必要がある。",
                "Of course, what we decide should be written up in email afterward and shared to avoid misunderstanding.",
                "当然，定下来的内容事后要用邮件写清楚、共享，以免误会。",
            ),
            (
                "それでも最初の一本目の矢は、短い会話の方が早いことが多いと思う。",
                "Still, the first step is often faster with a short conversation.",
                "即便如此，第一步往往还是短对话更快。",
            ),
            (
                "忙しい職場ほど、「今、三十秒だけいいですか」と切り出す勇気が、あとで時間を返してくれる。",
                'The busier the workplace, the more courage to say, "Do you have thirty seconds now?" pays back time later.',
                "越忙的职场，越需要勇气开口「现在能占用三十秒吗」，这会在以后把时间省回来。",
            ),
        ],
    },
    {
        "id": "n3-schedule-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "打ち合わせの日程を決める（廊下で）",
        "titleJp": "打ち合わせの日程を決める（廊下で）",
        "titleEn": "Setting a meeting time (in the hallway)",
        "titleZh": "商定会议时间（在走廊）",
        "titleRuby": [],
        "sections": [
            section(
                "声をかける",
                "Starting the conversation",
                "开口",
                "☕",
                [
                    (
                        "A",
                        "高橋さん、ちょっといいですか。新プロジェクトのキックオフ、日程だけ決めたくて。",
                        "Takahashi, do you have a moment? I just want to fix a date for the new project kickoff.",
                        "高桥，打扰一下。新项目启动会，我想先把日程定下来。",
                    ),
                    (
                        "B",
                        "あ、はい。メール、ちゃんと返せなくてすみません。",
                        "Oh, yes. Sorry I didn't reply properly to the email.",
                        "啊，好的。邮件我没好好回，不好意思。",
                    ),
                    (
                        "A",
                        "いえいえ。口頭の方が早いときもあって。今週と来週、どちらが動きやすいですか。",
                        "No worries. Sometimes it's faster in person. Which is easier for you, this week or next?",
                        "没事。有时候口头更快。这周和下周，哪边比较好安排？",
                    ),
                ],
            ),
            section(
                "候補を絞る",
                "Narrowing options",
                "缩小范围",
                "📅",
                [
                    (
                        "B",
                        "来週の方がいいです。火曜か水曜なら、午後は比較的空いています。",
                        "Next week is better. Tuesday or Wednesday, the afternoon is relatively free.",
                        "下周比较好。周二或周三的话，下午相对空。",
                    ),
                    (
                        "A",
                        "ありがとうございます。では火曜の三時から一時間、会議室Aでどうでしょう。",
                        "Thanks. How about Tuesday from 3:00 for an hour, in meeting room A?",
                        "谢谢。那周二三点开始一小时，会议室 A 可以吗？",
                    ),
                    (
                        "B",
                        "大丈夫だと思います。他の二人は、もう聞きましたか。",
                        "I think that's fine. Have you already asked the other two?",
                        "应该可以。另外两位你问过了吗？",
                    ),
                ],
            ),
            section(
                "合意とフォロー",
                "Agreement and follow-up",
                "共识与跟进",
                "✅",
                [
                    (
                        "A",
                        "今さっき佐藤さんにも聞いて、同じ時間でOKでした。木村さんだけ、留守番電話でした。",
                        "I just asked Sato, too, and they're OK with the same time. Only Kimura was on voicemail.",
                        "刚才也问了佐藤，同一时间可以。只有木村是语音信箱。",
                    ),
                    (
                        "B",
                        "木村さんなら、たぶん水曜の方が都合いいって前に言ってました。",
                        "If it's Kimura, they mentioned before that Wednesday might work better.",
                        "木村的话，之前好像说过周三更方便。",
                    ),
                    (
                        "A",
                        "なるほど。じゃあ水曜三時に変えて、二人に確認メール出します。高橋さんもCC入れますね。",
                        "I see. I'll switch to Wednesday at 3:00 and send a confirmation email to both of you. I'll CC you, Takahashi.",
                        "原来如此。那我改成周三三点，给两人发确认邮件。高桥也抄送你。",
                    ),
                    (
                        "B",
                        "助かります。曖昧なままだと、ずっと先送りになりますからね。",
                        "That helps. If it stays vague, it just keeps getting pushed back.",
                        "帮大忙了。一直含糊的话就会一直往后拖。",
                    ),
                ],
            ),
            section(
                "締め",
                "Closing",
                "收尾",
                "🙌",
                [
                    (
                        "A",
                        "ですよね。口で一度決めてからメール、これで進めます。",
                        "Right. Decide once by mouth, then email — I'll move ahead that way.",
                        "是啊。先口头定一下再发邮件，我就这么推进。",
                    ),
                    (
                        "B",
                        "了解です。よろしくお願いします。",
                        "Got it. Thanks for handling it.",
                        "了解。拜托了。",
                    ),
                ],
            ),
        ],
    },
]


def build_items() -> list[dict]:
    out: list[dict] = []
    for raw in NEW_ITEMS:
        item = {k: v for k, v in raw.items() if k not in ("segments", "sections")}
        item["titleRuby"] = enrich_title_ruby(item["titleWord"])
        if raw["format"] == "essay":
            item["segments"] = [enrich_segment(w, e, z) for w, e, z in raw["segments"]]
        else:
            item["sections"] = raw["sections"]
        out.append(item)
    return out


def main() -> None:
    path = ROOT / "public" / "data" / "ja_articles.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    items: list = doc["items"]
    existing_ids = {it["id"] for it in items}
    built = build_items()
    for it in built:
        if it["id"] in existing_ids:
            print(f"Skip: id already exists: {it['id']}", file=sys.stderr)
            sys.exit(1)
    items.extend(built)
    path.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Appended {len(built)} articles → {path}")
    for it in built:
        n = len(it.get("segments") or [])
        for sec in it.get("sections") or []:
            n += len(sec.get("lines") or [])
        print(f"  - {it['id']}: {n} sentences/lines")


if __name__ == "__main__":
    main()
