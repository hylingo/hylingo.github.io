#!/usr/bin/env python3
"""
batch20 → public/data/ja_articles.json

详细学车文章 (实用场景):
- n3-driving-school essay (教習所で免許を取る, 25句)
- n3-driving-school dialogue (教習所での会話, 3幕)

运行: python3 scripts/append_ja_articles_batch20.py
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


def line(speaker: str, word: str, en: str, zh: str) -> dict:
    d = seg(word, en, zh)
    d["speaker"] = speaker
    return d


def section(heading, heading_en, heading_zh, badge, lines_list):
    return {
        "badge": badge,
        "headingWord": heading, "headingJp": heading,
        "headingEn": heading_en, "headingZh": heading_zh,
        "lines": lines_list,
    }


NEW_ITEMS: list[dict] = [

    # ═══════════════════════════════════════════
    # 1. n3-driving-school essay (详细版)
    # ═══════════════════════════════════════════
    {
        "id": "n3-driving-school-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "自動車教習所で免許を取るまで",
        "titleJp": "自動車教習所で免許を取るまで",
        "titleEn": "Getting a driver's license at driving school",
        "titleZh": "在驾校考驾照的全过程",
        "titleRuby": [],
        "segments": [
            # ── 报名 ──
            seg("日本で車を運転するには、自動車教習所に通って免許を取るのが一般的だ。",
                "In Japan, the typical way to drive a car is to attend a driving school and get a license.",
                "在日本开车的话，一般是去驾校学然后考驾照。", True),
            seg("教習所に入るには、まず入校手続きが必要だ。住民票、身分証明書、印鑑を持って受付に行く。",
                "To enroll in a driving school, you first need to complete the admission procedures. Bring your residence certificate, ID, and personal seal to the reception.",
                "进驾校首先要办入校手续。带上住民票、身份证明和印章去前台。"),
            seg("視力検査もある。眼鏡やコンタクトをしている人は、つけた状態で検査する。",
                "There's also a vision test. People who wear glasses or contacts take the test while wearing them.",
                "还有视力检查。戴眼镜或隐形的人戴着检查。"),
            seg("料金は教習所によって違うが、普通免許のATで二十五万円から三十万円くらいだ。",
                "The fee varies by school, but for a regular automatic license it's about 250,000 to 300,000 yen.",
                "费用因驾校不同，普通驾照自动挡大概二十五万到三十万日元。"),

            # ── 第一段階 ──
            seg("教習は第一段階と第二段階に分かれている。第一段階では教習所の中のコースで練習する。",
                "The training is divided into Stage 1 and Stage 2. In Stage 1, you practice on the course inside the driving school.",
                "课程分为第一阶段和第二阶段。第一阶段在驾校内的场地练习。", True),
            seg("学科教習では交通ルールや標識の意味を学ぶ。教科書とビデオを使った授業だ。",
                "In classroom lessons, you learn traffic rules and the meaning of road signs. Classes use textbooks and videos.",
                "学科课上学交通规则和标识的含义。用教材和视频上课。"),
            seg("技能教習では、実際に車に乗って運転を練習する。最初は教官が横に座って、一つ一つ教えてくれる。",
                "In practical lessons, you actually get in a car and practice driving. At first, the instructor sits beside you and teaches you step by step.",
                "技能课上实际坐进车里练习驾驶。一开始教练坐在旁边一步步教。"),
            seg("初めてハンドルを握ったときは手が震えた。アクセルとブレーキの加減が難しい。",
                "My hands trembled the first time I held the steering wheel. Controlling the gas and brake was hard.",
                "第一次握方向盘的时候手在抖。油门和刹车的力度很难掌握。"),
            seg("S字カーブとクランクが特に難しかった。何度もポールにぶつかりそうになった。",
                "The S-curve and crank course were especially difficult. I almost hit the poles many times.",
                "S弯和曲道特别难。好几次差点撞到杆子。"),
            seg("坂道発進も最初はエンストしてしまった。クラッチとアクセルのタイミングが合わない。",
                "I also stalled on hill starts at first. The timing of the clutch and gas didn't match.",
                "坡道起步一开始也熄火了。离合和油门的时机对不上。"),

            # ── 仮免 ──
            seg("第一段階が終わると、仮免許の試験がある。学科試験と技能試験の両方に合格しなければならない。",
                "After Stage 1, there's the provisional license test. You must pass both a written test and a practical test.",
                "第一阶段结束后有临时驾照考试。笔试和技能考试都要通过。", True),
            seg("学科試験は五十問の○×問題で、九十点以上が合格だ。ひっかけ問題が多いので注意が必要だ。",
                "The written test has 50 true/false questions, and you need 90 points or above to pass. There are many trick questions, so be careful.",
                "笔试是五十道判断题，九十分以上合格。陷阱题很多要注意。"),
            seg("技能試験では、教官の隣で教習所内のコースを走る。脱輪や信号無視をすると不合格になる。",
                "In the practical test, you drive the course inside the school with the instructor beside you. Going off the road or ignoring signals means failure.",
                "技能考试教练坐旁边在场内跑一圈。脱轮或闯信号就不合格。"),

            # ── 第二段階 ──
            seg("仮免許を取ると、第二段階に進む。いよいよ一般道路に出て路上教習が始まる。",
                "After getting the provisional license, you move to Stage 2. You finally go out on public roads for on-road training.",
                "拿到临时驾照后进入第二阶段。终于上公共道路进行路上训练了。", True),
            seg("初めて路上に出たときは本当に緊張した。他の車がすぐ横を通るのが怖かった。",
                "I was really nervous the first time I went on the road. It was scary having other cars pass right beside me.",
                "第一次上路真的很紧张。旁边有车经过太害怕了。"),
            seg("右折のタイミング、車線変更、歩行者の確認など、教習所の中とは全然違う。",
                "Timing right turns, changing lanes, checking for pedestrians — it's completely different from inside the school.",
                "右转的时机、变道、确认行人等等，跟场内完全不一样。"),
            seg("高速教習もある。教習車で実際に高速道路を走る。合流するときの加速が難しかった。",
                "There's also highway training. You actually drive on the highway in the training car. Accelerating to merge was difficult.",
                "还有高速公路课。开着教练车实际跑高速。汇入时的加速很难。"),

            # ── 卒業検定 ──
            seg("第二段階が終わると卒業検定がある。路上のコースを走って、安全確認や運転技術を見られる。",
                "After Stage 2, there's the graduation test. You drive a road course while being evaluated on safety checks and driving skills.",
                "第二阶段结束后有毕业考试。在路上跑一圈，考察安全确认和驾驶技术。", True),
            seg("卒業検定に合格すると、教習所を卒業できる。卒業証明書をもらう。",
                "If you pass the graduation test, you can graduate from the driving school. You receive a graduation certificate.",
                "通过毕业考试就能从驾校毕业。拿到毕业证明。"),

            # ── 免許センター ──
            seg("最後に、住んでいる地域の運転免許センターに行って本免許の学科試験を受ける。",
                "Finally, you go to the driver's license center in your area and take the written test for the full license.",
                "最后去所在地区的驾照中心参加正式驾照的笔试。", True),
            seg("九十五問の試験で、合格ラインは九十点以上。教習所で勉強した内容とほぼ同じだが、問題数が多い。",
                "It's a 95-question test with a passing score of 90 or above. The content is almost the same as what you studied at driving school, but there are more questions.",
                "九十五道题，合格线九十分以上。内容跟驾校学的差不多，但题量多。"),
            seg("合格すると、その場で写真を撮って免許証が発行される。やっと運転免許が手に入る。",
                "If you pass, they take your photo on the spot and issue the license. You finally have your driver's license.",
                "通过的话当场拍照发驾照。终于拿到驾照了。"),

            # ── 感想 ──
            seg("初心者マークを車に貼って、初めて一人で運転したときの感動は忘れられない。",
                "I'll never forget the emotion of driving alone for the first time with a beginner's mark on the car.",
                "在车上贴着新手标志第一次一个人开车的感动忘不了。", True),
            seg("教習所に通った三か月間は大変だったが、今では車で自由に出かけられるようになった。頑張ってよかった。",
                "The three months at driving school were tough, but now I can go anywhere freely by car. It was worth the effort.",
                "在驾校的三个月虽然辛苦，但现在能开车自由出行了。努力是值得的。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n3-driving-school dialogue (3幕详细版)
    # ═══════════════════════════════════════════
    {
        "id": "n3-driving-school-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "教習所で運転を習う",
        "titleJp": "教習所で運転を習う",
        "titleEn": "Learning to drive at driving school",
        "titleZh": "在驾校学开车",
        "titleRuby": [],
        "sections": [
            section("入校と初めての技能教習", "Enrollment and first practical lesson", "入校和第一次技能课", "🚗", [
                line("A", "すみません、普通免許のAT限定で入校したいんですが。",
                     "Excuse me, I'd like to enroll for a regular automatic-only license.",
                     "不好意思，想报名普通驾照自动挡的。"),
                line("B", "はい。住民票と身分証明書はお持ちですか？",
                     "OK. Do you have your residence certificate and ID?",
                     "好的。带住民票和身份证明了吗？"),
                line("A", "はい、あります。料金はいくらですか？",
                     "Yes, I have them. How much is the fee?",
                     "带了。费用多少？"),
                line("B", "AT限定で二十八万円です。分割払いもできますよ。",
                     "It's 280,000 yen for automatic only. You can also pay in installments.",
                     "自动挡二十八万日元。也可以分期付款。"),
                line("A", "まず視力検査があるんですよね？眼鏡かけたままでいいですか？",
                     "There's a vision test first, right? Can I keep my glasses on?",
                     "先做视力检查对吧？戴着眼镜行吗？"),
                line("B", "はい、大丈夫です。眼鏡使用の条件が免許に付きますけど。",
                     "Yes, that's fine. A glasses-required condition will be added to your license though.",
                     "可以的。不过驾照上会加注需要眼镜的条件。"),
                line("A", "分かりました。学科と技能はどんなスケジュールですか？",
                     "I see. What's the schedule for classroom and practical lessons?",
                     "明白了。学科课和技能课是什么安排？"),
                line("B", "学科は毎日いくつか開講しています。技能はネットか受付で予約してください。第一段階は場内コースで練習です。",
                     "Classroom lessons are offered several times daily. For practical lessons, book online or at reception. Stage 1 is practice on the in-school course.",
                     "学科课每天有好几节。技能课在网上或前台预约。第一阶段在场内练习。"),
            ]),
            section("技能教習：場内コース", "Practical lesson: in-school course", "技能课：场内练习", "🔰", [
                line("C", "はい、じゃあエンジンをかけてください。まずミラーとシートの位置を確認して。",
                     "OK, start the engine please. First check the mirror and seat position.",
                     "好，请启动发动机。先确认后视镜和座椅位置。"),
                line("A", "はい。……サイドミラーはこのくらいでいいですか？",
                     "OK. ...Is this about right for the side mirror?",
                     "好。……侧后视镜大概这样行吗？"),
                line("C", "もう少し下に向けて。駐車している車の後ろが見えるように。",
                     "Tilt it down a bit more. So you can see behind parked cars.",
                     "再往下调一点。能看到停着的车后面。"),
                line("A", "分かりました。シートベルトを締めて……ブレーキを踏んで、ギアをDに入れて……。",
                     "Got it. Fasten the seatbelt... step on the brake, put it in D...",
                     "明白了。系好安全带……踩刹车，挂D挡……"),
                line("C", "いいですよ。ゆっくりブレーキを離して。アクセルはまだ踏まなくていい。クリープで進みます。",
                     "Good. Slowly release the brake. Don't press the gas yet. It'll move on idle creep.",
                     "好的。慢慢松开刹车。油门先不踩。靠怠速前进。"),
                line("A", "あ、動いた。思ったより速いですね。",
                     "Oh, it's moving. It's faster than I thought.",
                     "啊，动了。比想象中快。"),
                line("C", "次の角を左に曲がって。曲がる前にウインカーを出してね。",
                     "Turn left at the next corner. Put on your turn signal before turning.",
                     "下个弯左转。转弯前打转向灯。"),
                line("A", "左ウインカー……。あ、ハンドルどのくらい切ればいいですか？",
                     "Left signal... Oh, how much should I turn the wheel?",
                     "左转向灯……。啊，方向盘打多少？"),
                line("C", "もう少し大きく切って。内側のポールに当たらないように。そうそう、うまい。",
                     "Turn it a bit more. So you don't hit the inside pole. That's it, good.",
                     "再打大一点。别碰到内侧的杆子。对对，不错。"),
                line("A", "S字カーブはいつ練習しますか？",
                     "When do we practice the S-curve?",
                     "S弯什么时候练？"),
                line("C", "次の時間にやりましょう。今日は直線とカーブの基本をしっかり覚えてください。",
                     "Let's do that next time. Today, make sure to learn the basics of straight lines and curves.",
                     "下次练吧。今天先把直线和弯道的基本功练好。"),
            ]),
            section("仮免試験と路上教習", "Provisional license test and road training", "临时驾照考试和路上训练", "🛣️", [
                line("A", "先生、来週仮免の試験なんですけど、何かアドバイスありますか？",
                     "Instructor, I have the provisional license test next week. Any advice?",
                     "教练，下周临时驾照考试了，有什么建议吗？"),
                line("C", "学科は引っかけ問題に注意。「必ず」とか「絶対に」って書いてある選択肢は、たいてい間違いだから。",
                     "For the written test, watch out for trick questions. Options with words like 'always' or 'absolutely' are usually wrong.",
                     "笔试注意陷阱题。选项里写「一定」「绝对」的基本都是错的。"),
                line("A", "技能試験で一番気をつけることは？",
                     "What should I be most careful about in the practical test?",
                     "技能考试最要注意什么？"),
                line("C", "安全確認。曲がる前、発進する前に必ず左右を確認すること。それと、一時停止線ではしっかり止まる。",
                     "Safety checks. Always check left and right before turning and before starting. Also, come to a complete stop at stop lines.",
                     "安全确认。转弯前、起步前一定确认左右。还有，一时停止线要停稳。"),
                line("A", "脱輪したら即不合格ですか？",
                     "Is it an automatic fail if I go off the road?",
                     "脱轮就直接不合格吗？"),
                line("C", "脱輪は減点が大きいね。でも落ち着いてやれば大丈夫。練習通りにやればいい。",
                     "Going off the road is a big deduction. But if you stay calm you'll be fine. Just do it like you practiced.",
                     "脱轮扣分很重。但冷静下来就没问题。跟平时练的一样就行。"),
                line("A", "仮免取れたら路上に出るんですよね。怖いなあ。",
                     "After getting the provisional license, we go on the road, right? That's scary.",
                     "拿到临时驾照就上路了吧。好害怕。"),
                line("C", "最初はみんな怖いよ。でも路上に出ると一気に上手くなるから。高速教習もあるけど、それは後半のお楽しみだね。",
                     "Everyone's scared at first. But once you're on the road you improve quickly. There's also highway training, but that's something to look forward to later.",
                     "一开始谁都怕。但上了路进步特别快。还有高速课，那是后面的看点了。"),
                line("A", "卒業検定に受かったら、あとは免許センターで学科試験を受けるだけですか？",
                     "After passing the graduation test, I just need to take the written test at the license center?",
                     "通过毕业考试后就只要去驾照中心考笔试了吗？"),
                line("C", "そう。九十五問で九十点以上。受かればその日に免許証がもらえるよ。頑張って。",
                     "That's right. 95 questions, 90 points or above. If you pass, you get your license that day. Good luck.",
                     "对。九十五题九十分以上。通过的话当天就能拿到驾照。加油。"),
            ]),
        ],
    },
]


def main() -> None:
    path = ROOT / "public" / "data" / "ja_articles.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    existing_ids = {item["id"] for item in data["items"]}

    added = 0
    for item in NEW_ITEMS:
        if item["id"] in existing_ids:
            print(f"  skip (exists): {item['id']}")
            continue

        if not item.get("titleRuby"):
            item["titleRuby"] = gr.make_ruby(item["titleWord"])
        item.setdefault("grammar", [])

        data["items"].append(item)
        added += 1
        print(f"  added: {item['id']}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nDone: added {added}, total {len(data['items'])} articles")


if __name__ == "__main__":
    main()
