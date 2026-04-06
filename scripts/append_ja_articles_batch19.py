#!/usr/bin/env python3
"""
batch19 → public/data/ja_articles.json

医疗词汇覆盖补充 (6篇):
1. n3-hospital-visit (住院探病) essay + dialogue
2. n3-health-checkup (健康体检) essay + dialogue
3. n3-sports-injury (运动受伤) essay + dialogue

目标覆盖: 入院、退院、注射、手術、骨折、治療、回復、看護婦、患者、医師、
身長、栄養、太る、痩せる、ダイエット、血液、血圧、心臓、診断、
サッカー、野球、試合、けが、骨、頭痛、マッサージ、危険、テニス 等

运行: python3 scripts/append_ja_articles_batch19.py
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
    # 1. n3-hospital-visit 住院探病
    # ═══════════════════════════════════════════
    {
        "id": "n3-hospital-visit-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "友達が入院した",
        "titleJp": "友達が入院した",
        "titleEn": "My friend was hospitalized",
        "titleZh": "朋友住院了",
        "titleRuby": [],
        "segments": [
            seg("先週、友達のケンが交通事故でけがをして入院した。バイクに乗っていて、車とぶつかったらしい。",
                "Last week, my friend Ken was injured in a traffic accident and hospitalized. He was riding a motorcycle and apparently collided with a car.",
                "上周朋友健因为交通事故受伤住院了。骑摩托车的时候好像跟汽车撞了。", True),
            seg("病院に電話したら、看護師さんが「面会は午後二時からです」と教えてくれた。",
                "When I called the hospital, a nurse told me 'Visiting hours start at 2 PM.'",
                "打电话去医院，护士告诉我「探视时间从下午两点开始」。"),
            seg("お見舞いに果物とスポーツ雑誌を持っていった。ケンは野球が好きだから喜ぶだろう。",
                "I brought fruit and a sports magazine to visit him. Ken likes baseball so he'd be happy.",
                "探病带了水果和体育杂志。健喜欢棒球所以应该会高兴。"),
            seg("病室に入ると、ケンは右足にギプスをつけてベッドに横になっていた。骨折だそうだ。",
                "When I entered the room, Ken was lying on the bed with a cast on his right leg. Apparently it was a fracture.",
                "进了病房，健右脚打着石膏躺在床上。说是骨折了。", True),
            seg("「手術は終わったよ。骨にボルトを入れたんだ」とケンが言った。痛そうだが、声は元気だった。",
                "'The surgery is done. They put a bolt in the bone,' Ken said. It looked painful, but his voice was cheerful.",
                "健说「手术做完了。骨头里打了螺丝」。看着疼，但声音挺精神。"),
            seg("医師の話では、治療は順調で、二週間ほどで退院できる見込みだとい��。",
                "According to the doctor, the treatment is going well and he's expected to be discharged in about two weeks.",
                "医生说治疗很顺利，预��两周左右能出院。"),
            seg("毎日注射があって、それが一番嫌だとケンは笑った。「針が苦手なんだよ」。",
                "He gets an injection every day, and Ken laughed that that's the worst part. 'I'm bad with needles.'",
                "每天要打针，健笑着说那是最讨厌的。「我怕针」。", True),
            seg("看護師さんがとても親切で、患者さん一人ひとりに声をかけているのが印象的だった。",
                "The nurses were very kind, and it was impressive how they spoke to each patient individually.",
                "护士非常亲切，给每个患者都打招呼让人印象深刻。"),
            seg("隣のベッドのおじいさんは転んで腰の骨を折ったそうだ。リハビリを頑張っていた。",
                "The old man in the next bed apparently fell and broke a bone in his hip. He was working hard at rehabilitation.",
                "隔壁床的老爷爷说是摔倒骨折了腰。在努力做康复训练。"),
            seg("帰り道、健康でいられることのありがたさを改めて感じた。ケンの回復を祈っている。",
                "On the way home, I felt grateful again for being healthy. I'm praying for Ken's recovery.",
                "回去的路上重新感受到健康的可贵。祝健早日康复。", True),
        ],
    },

    {
        "id": "n3-hospital-visit-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "お見舞いに行く",
        "titleJp": "お見舞いに行く",
        "titleEn": "Going to visit a patient",
        "titleZh": "去探病",
        "titleRuby": [],
        "sections": [
            section("病室で", "In the hospital room", "在病房", "🏥", [
                line("A", "ケン、大丈夫？事故って聞いてびっくりしたよ。",
                     "Ken, are you OK? I was shocked when I heard about the accident.",
                     "健，没事吧？听说出事了吓了一跳。"),
                line("B", "ありがとう。骨折したけど、手術は終わったから。あとは治療しながら回復を待つだけ。",
                     "Thanks. I fractured a bone, but the surgery is done. Now I just wait to recover while getting treatment.",
                     "谢谢。骨折了但手术做完了。接下来边治疗边等恢复。"),
                line("A", "手術って怖くなかった？",
                     "Wasn't the surgery scary?",
                     "手术不害怕吗？"),
                line("B", "麻酔かけられたから何も感じなかった。ただ、毎日の注射が痛くてさ。",
                     "They gave me anesthesia so I didn't feel anything. But the daily injections hurt.",
                     "打了麻药什么都没感觉。就是每天打针疼。"),
                line("A", "いつ退院できそう？",
                     "When can you be discharged?",
                     "什么时候能出院？"),
                line("B", "医師は二週間くらいって言ってた。看護師さんが優しいのが救いだよ。",
                     "The doctor said about two weeks. The nurses being so kind is a saving grace.",
                     "医生说大概两周。护士人好是唯一的安慰。"),
            ]),
            section("退院の話", "Talking about discharge", "聊出院", "🎉", [
                line("A", "退院したら何したい？",
                     "What do you want to do after you're discharged?",
                     "出院了想干什么？"),
                line("B", "まず焼肉。病院の食事は栄養バランスはいいんだけど、味が薄くてさ。",
                     "Barbecue first. The hospital food is nutritionally balanced, but it's bland.",
                     "先吃烤肉。医院饭菜营养均衡是挺好的，但味道太淡了。"),
                line("A", "あはは。リハビリは大変？",
                     "Haha. Is rehabilitation tough?",
                     "哈哈。康复训练辛苦吗？"),
                line("B", "最初は痛かったけど、だんだん足が動くようになってきた。患者同士で励まし合ってるよ。",
                     "It hurt at first, but gradually my leg is starting to move. The patients encourage each other.",
                     "一开始疼，但慢慢地脚能动了。患者之间互相鼓励。"),
                line("A", "よかった。これ、野球雑誌。暇つぶしに。",
                     "Good to hear. Here, a baseball magazine. To kill time.",
                     "太好了。给你，棒球杂志。打发时间用。"),
                line("B", "おー、ありがとう！入院生活で一番嬉しいのはお見舞いだな。",
                     "Oh, thanks! The best part of being in the hospital is the visitors.",
                     "哦——谢谢！住院最开心的就是有人来看了。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n3-health-checkup 健康体检
    # ═══════════════════════════════════════════
    {
        "id": "n3-health-checkup-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "健康診断を受ける",
        "titleJp": "健康診断を受ける",
        "titleEn": "Getting a health checkup",
        "titleZh": "做健康体检",
        "titleRuby": [],
        "segments": [
            seg("会社の健康診断の日が来た。毎年この時期になると少し緊張する。",
                "The day of the company health checkup has come. I get a little nervous every year around this time.",
                "公司体检的日子到了。每年��这个时候都有点紧张。", True),
            seg("まず受付で名前を言って、問診票を出した。身長と体重を測る。",
                "First I said my name at reception and submitted the questionnaire. Then height and weight were measured.",
                "先在前台报了名，交了问诊表。测了身高和体重。"),
            seg("去年より二キロ太っていた。最近ダイエットをサボっていたから当然だ。",
                "I was two kilos heavier than last year. It's no surprise since I've been slacking on my diet lately.",
                "比去年胖了两公斤。最近减肥偷懒了所以理所当然。"),
            seg("次は血圧。看護師さんが腕にカフを巻いて測ってくれた。「少し高めですね」と言われた。",
                "Next was blood pressure. The nurse wrapped a cuff around my arm and measured it. 'It's a bit high,' she said.",
                "接下来量血压。护士在手臂上缠上袖带测了。她说「有点偏高」。", True),
            seg("血液検査では注射器で血を採られた。針が刺さる瞬間、思わず目をそらした。",
                "For the blood test, they drew blood with a syringe. The moment the needle went in, I instinctively looked away.",
                "验血的时候用注射器抽了血。针扎进去的瞬间不由自主地把眼睛移开了。"),
            seg("心臓の検査では、胸に何枚かのシールを貼って、心電図を取った。",
                "For the heart exam, they stuck several patches on my chest and took an ECG.",
                "心脏检查的时候在胸口贴了好几片贴片，做了心电图。"),
            seg("視力検査と聴力検査も受けた。視力が少し落ちていた。スマホの見すぎだろう。",
                "I also had vision and hearing tests. My vision had dropped a bit. Probably from looking at my phone too much.",
                "还做了视力和听力检查。视力稍微下降了。大概是手机看太多了。", True),
            seg("最後に医師の診断があった。「全体的には問題ありませんが、血圧と体重は気をつけましょう」。",
                "Finally there was the doctor's diagnosis. 'Overall there are no problems, but let's watch the blood pressure and weight.'",
                "最后是医生的诊断。「总体没问题，但要注意血压和体重」。"),
            seg("「塩分を控えて、適度な運動を心がけてください。栄養バランスのいい食事も大切です」と言われた。",
                "'Try to reduce salt and exercise moderately. A nutritionally balanced diet is also important,' I was told.",
                "他说「控制盐分，注意适度运动。营养均衡的饮食也很重要」。"),
            seg("帰り道、今日からちゃんと運動しようと思った。去年も同じことを思ったが、今年こそ続けたい。",
                "On the way home, I resolved to exercise properly starting today. I thought the same thing last year, but this year I want to stick with it.",
                "回去的路上下决心从今天开始好好运动。去年也想过一样的事，但今年一定要坚持。", True),
        ],
    },

    {
        "id": "n3-health-checkup-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "健康診断の結果",
        "titleJp": "健康診断の結果",
        "titleEn": "Health checkup results",
        "titleZh": "体检结果",
        "titleRuby": [],
        "sections": [
            section("検査を受ける", "Getting tested", "做检查", "🩺", [
                line("A", "すみません、健康診断の受付はこちらですか？",
                     "Excuse me, is this the reception for the health checkup?",
                     "不好意思，体检在这里登记吗？"),
                line("B", "はい。問診票は記入されましたか？",
                     "Yes. Have you filled out the questionnaire?",
                     "是的。问诊表填好了吗？"),
                line("A", "はい、こちらです。",
                     "Yes, here it is.",
                     "填好了，在这。"),
                line("B", "では、まず身長と体重を測りますね。……百七十二センチ、七十五キロです。",
                     "OK, first let me measure your height and weight. ...172 cm, 75 kg.",
                     "那先量身高体重。……一百七十二厘米，七十五公斤。"),
                line("A", "去年より太りましたか？",
                     "Have I gained weight since last year?",
                     "比去年胖了吗？"),
                line("B", "二キロ増えていますね。次は血圧です。腕を出してください。",
                     "You've gained two kilos. Next is blood pressure. Please hold out your arm.",
                     "涨了两公斤。接下来量血压。请伸出手臂。"),
            ]),
            section("結果を聞く", "Hearing the results", "听结果", "📋", [
                line("C", "血液検査の結果ですが、コレステロールが少し高いです。",
                     "Regarding the blood test results, your cholesterol is a bit high.",
                     "血液检查的结果，胆固醇有点高。"),
                line("A", "やっぱり……。心臓は大丈夫ですか？",
                     "I figured... Is my heart OK?",
                     "果然……。心脏没事吧？"),
                line("C", "心電図は正常です。ただ、このまま太り続けると危険ですよ。",
                     "The ECG is normal. However, if you keep gaining weight it could be dangerous.",
                     "心电图正常。不过继续胖下去就危险了。"),
                line("A", "ダイエットした方がいいですか。",
                     "Should I go on a diet?",
                     "需要减肥吗。"),
                line("C", "急に痩せる必要はありません。栄養バランスを意識して、週に二、三回運動してください。",
                     "You don't need to lose weight suddenly. Be mindful of nutritional balance and exercise two to three times a week.",
                     "不需要突然变瘦。注意营养均衡，每周运动两三次。"),
                line("A", "分かりました。まずは走ることから始めてみます。",
                     "Understood. I'll start with running first.",
                     "明白了。先从跑步开始试试。"),
                line("C", "いいですね。来年の診断で改善されていることを期待しています。",
                     "Sounds good. I hope to see improvement at next year's checkup.",
                     "不错。期待明年体检能有改善。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n3-sports-injury 运动受伤
    # ═══════════════════════════════════════════
    {
        "id": "n3-sports-injury-essay",
        "level": "N3–N2",
        "format": "essay",
        "titleWord": "サッカーの試合で怪我をした",
        "titleJp": "サッカーの試合で怪我をした",
        "titleEn": "I got injured in a soccer match",
        "titleZh": "足球比赛受伤了",
        "titleRuby": [],
        "segments": [
            seg("日曜日、会社のサッカーチームの試合があった。相手は隣の会社のチームで、毎年やっている。",
                "On Sunday, there was a match for the company soccer team. The opponent was the team from the neighboring company — we play every year.",
                "周日公司足球队有比赛。对手是隔壁公司的队，每年都踢。", True),
            seg("前半は順調だった。チームメイトのパスがうまくつながって、一点を先制した。",
                "The first half went well. Our teammate's passes connected nicely and we scored first.",
                "上半场很顺利。队友的传球衔接得好，先得了一分。"),
            seg("問題は後半だった。相手の選手とボールを争ったとき、足が絡まって転んだ。",
                "The problem was the second half. When I was fighting for the ball with an opposing player, our legs got tangled and I fell.",
                "问题出在下半场。和对方球员争球的时候脚绊在一起摔倒了。"),
            seg("右足の膝を強く打った。立とうとしたが、痛くて立てなかった。これは危険だと思った。",
                "I hit my right knee hard. I tried to stand but the pain was too much. I thought this was bad.",
                "右膝盖撞得很重。想站起来但疼得站不住。觉得这下危险了。", True),
            seg("チームメイトが肩を貸してくれて、ベンチまで運んでもらった。",
                "A teammate lent me a shoulder and helped me to the bench.",
                "队友扶着我，把我搀到替补席。"),
            seg("頭痛はなかったが、膝が腫れてきた。マネージャーが氷で冷やしてくれた。",
                "I didn't have a headache, but my knee started swelling. The manager iced it for me.",
                "没有头疼，但膝盖肿起来了。经理帮忙用冰敷了。"),
            seg("念のため病院に行った。レントゲンを撮ったら、骨には異常がなかった。靭帯を少し傷めたらしい。",
                "Just in case, I went to the hospital. After X-rays, there was nothing wrong with the bone. Apparently I slightly injured a ligament.",
                "为了保险去了医院。拍了X光片骨头没问题。好像韧带轻微损伤。", True),
            seg("医師に「二週間は運動を控えてください」と言われた。テニスの約束もキャンセルした。",
                "The doctor told me 'Please refrain from exercise for two weeks.' I also canceled my tennis plans.",
                "医生说「两周内避免运动」。网球的约也取消了。"),
            seg("スポーツは楽しいが、怪我の危険は常にある。ストレッチとウォームアップを怠ってはいけないと反省した。",
                "Sports are fun, but there's always a risk of injury. I reflected that I shouldn't neglect stretching and warming up.",
                "运动虽然开心但总有受伤的风险。反省了一下不能偷懒不做拉伸和热身。"),
            seg("来月の試合には間に合うように、マッサージとリハビリを続けている。早く治って野球の応援にも行きたい。",
                "I'm continuing massage and rehabilitation so I can make it in time for next month's match. I want to recover quickly and go cheer at baseball games too.",
                "继续做按摩和康复训练争取赶上下个月的比赛。想快点好了去看棒球比赛加油。", True),
        ],
    },

    {
        "id": "n3-sports-injury-dialogue",
        "level": "N3–N2",
        "format": "dialogue",
        "titleWord": "試合で怪我した話",
        "titleJp": "試合で怪我した話",
        "titleEn": "Talking about getting injured in a match",
        "titleZh": "聊比赛受伤的事",
        "titleRuby": [],
        "sections": [
            section("月曜の朝", "Monday morning", "周一早上", "🏢", [
                line("A", "え、足どうしたの？びっこ引いてない？",
                     "Wait, what happened to your leg? Are you limping?",
                     "诶，你脚怎么了？一瘸一拐的。"),
                line("B", "昨日サッカーの試合で怪我しちゃって。膝をやられた。",
                     "I got injured in a soccer match yesterday. Hurt my knee.",
                     "昨天足球比赛受伤了。膝盖撞了。"),
                line("A", "うわ、大丈夫？骨折？",
                     "Ouch, are you OK? Fracture?",
                     "哇，没事吧？骨折了？"),
                line("B", "骨は大丈夫。靭帯をちょっと傷めたみたい。病院でレントゲン撮ってもらった。",
                     "The bone is fine. Seems like I slightly injured a ligament. Got X-rays at the hospital.",
                     "骨头没事。韧带好像轻微损伤。去医院拍了片子。"),
                line("A", "試合中に転んだの？",
                     "Did you fall during the match?",
                     "比赛中摔的？"),
                line("B", "相手の選手と足が絡まってさ。立てなくて、チームメイトに運んでもらった。",
                     "My legs got tangled with an opposing player. I couldn't stand so my teammates carried me.",
                     "和对方球员脚绊在一起了。站不起来，队友把我扶过去的。"),
            ]),
            section("治療と回復", "Treatment and recovery", "治疗和恢复", "💪", [
                line("A", "医者に何て言われた？",
                     "What did the doctor say?",
                     "医生怎么说？"),
                line("B", "二週間は運動禁止。マッサージとリハビリを続けてって。",
                     "No exercise for two weeks. Keep doing massage and rehabilitation.",
                     "两周禁止运动。继续做按摩和康复。"),
                line("A", "テニスの約束、来週あったよね。",
                     "We had tennis plans next week, right?",
                     "下周约的网球呢。"),
                line("B", "キャンセルした。残念だけど仕方ない。危険を冒してもっとひどくなったら困るし。",
                     "Canceled it. It's a shame but can't be helped. I don't want to risk making it worse.",
                     "取消了。可惜但没办法。冒险弄得更严重就麻烦了。"),
                line("A", "ストレッチちゃんとしてた？",
                     "Were you doing proper stretches?",
                     "有好好做拉伸吗？"),
                line("B", "……正直、サボってた。やっぱり準備運動は大事だね。",
                     "...Honestly, I'd been skipping them. Warmups really are important.",
                     "……说实话偷懒了。果然热身很重要。"),
                line("A", "来月の試合には間に合いそう？",
                     "Think you'll make it for next month's match?",
                     "赶得上下个月的比赛吗？"),
                line("B", "頑張って回復するよ。野球のシーズンも始まるし、早く治したい。",
                     "I'll work hard to recover. Baseball season is starting too, so I want to heal fast.",
                     "努力恢复。棒球赛季也要开始了，想快点好。"),
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
