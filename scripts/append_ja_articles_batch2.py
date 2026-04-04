#!/usr/bin/env python3
"""
追加精读日语文章 batch2 → public/data/ja_articles.json（单行 JSON）。

依赖: .venv 中 pip install 'fugashi[unidic-lite]'
运行: .venv/bin/python scripts/append_ja_articles_batch2.py

主题（短文 + 对话成对）:
- 引越し後の区役所手続き (N4–N3)
- 子どもの発熱・小児科 (N4–N3)
- 電車遅延・駅での案内 (N3)
- 仕事の依頼を婉曲に断る (N3)
- 配送トラブルのクレーム電話 (N2 敬語)
- 週報を短く書くコツ (N3)
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
    return {
        "badge": badge,
        "headingWord": heading,
        "headingJp": heading,
        "headingEn": heading_en,
        "headingZh": heading_zh,
        "lines": [enrich_line(sp, w, e, z) for sp, w, e, z in lines],
    }


NEW_ITEMS: list[dict] = [
    # --- 区役所 ---
    {
        "id": "n4-ward-office-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "引っ越して初めての区役所で",
        "titleJp": "引っ越して初めての区役所で",
        "titleEn": "At the ward office right after moving",
        "titleZh": "搬家后第一次去区役所",
        "titleRuby": [],
        "segments": [
            (
                "新しいマンションに引っ越してから一週間、手続きの山に圧倒されそうだった。",
                "A week after moving into a new apartment, I felt overwhelmed by all the paperwork.",
                "搬进新公寓一周，手续堆成山，快被压垮。",
            ),
            (
                "まず区役所の窓口で転入届を出し、新しい住所を登録した。",
                "First I submitted a change-of-address form at the ward office counter and registered my new address.",
                "先在区役所窗口提交迁入登记，登记了新地址。",
            ),
            (
                "前の市区町村で使っていたマイナンバーカードは、そのまま有効だと教えてもらった。",
                "I was told my My Number card from my previous municipality remains valid as is.",
                "被告知之前市区町村用的个人编号卡可以继续用。",
            ),
            (
                "勤め先の社会保険に入るまでのあいだは、国民健康保険に加入する必要があった。",
                "Until I joined my employer's social insurance, I needed to enroll in National Health Insurance.",
                "在加入公司的社会保险之前，必须先加入国民健康保险。",
            ),
            (
                "収入の申告用紙に少し迷いながら記入し、初回の保険料の目安を聞いた。",
                "I filled out the income declaration form with some hesitation and asked roughly what the first premium would be.",
                "略带犹豫填了收入申报表，并问了首次保费的大致金额。",
            ),
            (
                "支払いは口座振替にすると手間が減るので、その用紙もまとめてもらった。",
                "Paying by bank transfer would save hassle, so I received those forms together.",
                "听说账户扣款省事，一并拿了扣款用的表格。",
            ),
            (
                "ゴミの出し方の冊子と、区の防災アプリの案内も手渡された。",
                "I was also handed a booklet on trash rules and a flyer for the ward's disaster-prep app.",
                "还拿到垃圾分类小册子和区防灾 App 的介绍。",
            ),
            (
                "職員の説明は早口だったが、分からないときは同じ窓口に戻ってよいと言われて安心した。",
                "The clerk spoke quickly, but hearing I could come back to the same counter if I was unsure reassured me.",
                "职员讲得很快，但说不懂可以再来同一窗口，我安心了些。",
            ),
            (
                "窓口が混んでいたので、番号札を取って一時間ほど待った。",
                "The counter was crowded, so I took a ticket and waited about an hour.",
                "窗口人多，取了号等了一小时左右。",
            ),
            (
                "手続きが一通り終わると、住民票の写しが必要なら隣の機械も使えると案内された。",
                "When the procedures were done, I was told I could use the machine next door if I needed a copy of my resident record.",
                "手续办完后，被告知若需要住民票复印件可用旁边的机器。",
            ),
            (
                "帰り道、区のウェブサイトにも同じことが書いてあることを確認し、メモを取った。",
                "On the way home I checked the ward website for the same information and took notes.",
                "回家路上在区网站核对同样内容并做了笔记。",
            ),
            (
                "複雑に見えたが、一つずつ窓口で聞けば進むと実感した。",
                "It looked complicated, but I felt that asking step by step at the counter keeps things moving.",
                "看起来很复杂，但体会到只要一步步在窗口问就能办下去。",
            ),
        ],
    },
    {
        "id": "n4-ward-office-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "区役所の窓口で（転入・保険）",
        "titleJp": "区役所の窓口で（転入・保険）",
        "titleEn": "At the ward office counter (move-in and insurance)",
        "titleZh": "在区役所窗口（迁入与保险）",
        "titleRuby": [],
        "sections": [
            section(
                "呼び出し",
                "Called to the counter",
                "叫号",
                "🎫",
                [
                    (
                        "A",
                        "三十六番の方、ご利用窓口へどうぞ。",
                        "Number 36, please come to the service counter.",
                        "三十六号，请到办事窗口。",
                    ),
                    (
                        "B",
                        "はい。あの、転入届と国民健康保険の手続きをしたいのですが。",
                        "Yes. I'd like to submit my move-in form and enroll in National Health Insurance.",
                        "您好。我想办迁入登记和国民健康保险。",
                    ),
                    (
                        "A",
                        "かしこまりました。まずこちらの転入届にご記入ください。筆記用具はそちらにございます。",
                        "Certainly. Please fill out this move-in form first. Writing utensils are over there.",
                        "好的。请先填写这张迁入表。文具在那边。",
                    ),
                    (
                        "B",
                        "すみません、マイナンバーカードのコピーも必要でしょうか。",
                        "Excuse me, do I need a copy of my My Number card?",
                        "请问需要个人编号卡的复印件吗？",
                    ),
                    (
                        "A",
                        "お持ちでしたら両面のコピーを一枚お願いします。なければ本日は番号の確認だけで進められます。",
                        "If you have one, please provide a single double-sided copy. If not, we can proceed today with just the number verification.",
                        "有的话请交一张正反面复印件。没有的话今天先核对号码也可以办理。",
                    ),
                ],
            ),
            section(
                "書類の確認",
                "Checking documents",
                "核对材料",
                "📄",
                [
                    (
                        "A",
                        "ご記入ありがとうございます。旧住所と引越し日、確認できました。",
                        "Thank you for filling this out. I've confirmed your old address and moving date.",
                        "谢谢填写。旧地址和搬家日期已确认。",
                    ),
                    (
                        "B",
                        "保険証は会社の社会保険のものがまだ届いていないのですが……。",
                        "My company health insurance card hasn't arrived yet...",
                        "公司的医保卡还没寄到……",
                    ),
                    (
                        "A",
                        "では、しばらくの間は国民健康保険に加入の手続きになります。こちらに署名をお願いいたします。",
                        "Then you'll enroll in National Health Insurance for the time being. Please sign here.",
                        "那先办一段时间国民健康保险。请在这里签名。",
                    ),
                ],
            ),
            section(
                "保険料",
                "Premiums",
                "保费",
                "💴",
                [
                    (
                        "B",
                        "初回のお支払いは、だいたいいつ頃になりますか。",
                        "Roughly when will the first payment be due?",
                        "第一次缴费大概在什么时候？",
                    ),
                    (
                        "A",
                        "翌月の二十日前後に納付書が届きます。口座振替にされますか、それとも納付書でしょうか。",
                        "A payment slip arrives around the 20th of the following month. Will you use bank transfer or pay by slip?",
                        "下个月二十号左右会收到缴费单。要账户扣款还是用缴费单？",
                    ),
                    (
                        "B",
                        "振替にします。口座番号はここに書けばよいですか。",
                        "Bank transfer. Do I write the account number here?",
                        "扣款。账户号写在这里可以吗？",
                    ),
                    (
                        "A",
                        "はい、その通りです。後日届く用紙に押印のうえ、ご返送ください。",
                        "Yes, exactly. Please stamp and return the form when it arrives.",
                        "是的。日后寄来的表格请盖章后寄回。",
                    ),
                ],
            ),
            section(
                "締め",
                "Closing",
                "结束",
                "✅",
                [
                    (
                        "B",
                        "今日、ほかに済ませておくことはありますか。",
                        "Is there anything else I should take care of today?",
                        "今天还有别的要一并办的吗？",
                    ),
                    (
                        "A",
                        "本日のご用件は以上で大丈夫です。ゴミ収集の冊子は入口の棚にもございます。",
                        "That completes today's tasks. Trash-collection booklets are also on the shelf at the entrance.",
                        "今天就是这些。垃圾分类册子入口架子上也有。",
                    ),
                    (
                        "B",
                        "丁寧にご説明いただき、ありがとうございました。",
                        "Thank you for explaining everything so clearly.",
                        "讲解得很清楚，谢谢您。",
                    ),
                ],
            ),
        ],
    },
    # --- 小児科 ---
    {
        "id": "n4-child-fever-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "夜中に子どもの熱が出た夜",
        "titleJp": "夜中に子どもの熱が出た夜",
        "titleEn": "The night my child ran a fever",
        "titleZh": "孩子半夜发烧的那晚",
        "titleRuby": [],
        "segments": [
            (
                "午前二時ごろ、五歳の娘が「のどが痛い」と泣きながら起きた。",
                'Around 2 a.m., my five-year-old daughter woke up crying, "My throat hurts."',
                "凌晨两点左右，五岁的女儿哭着醒来，说喉咙痛。",
            ),
            (
                "額に手を当てると、はっきり熱があるのが分かった。",
                "When I touched her forehead, it was clearly hot.",
                "一摸额头，明显在发烧。",
            ),
            (
                "体温計で測ると三十八度五分で、冷たいタオルで脇と首を冷やした。",
                "The thermometer read 38.5°C; I cooled her armpits and neck with a cool towel.",
                "体温计三十八度五，用凉毛巾敷腋下和脖子。",
            ),
            (
                "すぐに小児科の夜間窓口の電話番号を検索し、症状と飲ませている薬をメモした。",
                "I looked up the pediatric night hotline, noting her symptoms and any medicine she'd taken.",
                "马上查夜间儿科咨询电话，记下症状和已服用的药。",
            ),
            (
                "電話では「呼吸が苦しそうなら救急を」と言われ、様子を見ながら朝まで待つことにした。",
                'They said, "Call emergency care if breathing seems hard," so we watched her until morning.',
                "电话里说若呼吸困难要打急救，我们观察情况等到天亮。",
            ),
            (
                "朝になっても熱が下がらなかったので、予約の取れる小児科へ連れて行った。",
                "Her fever hadn't gone down by morning, so I took her to a pediatric clinic that took appointments.",
                "早上烧还没退，带她去能预约的小儿科。",
            ),
            (
                "受付で「昨夜から熱が続いています」と伝え、母子手帳を見せた。",
                'At reception I said, "She\'s had a fever since last night," and showed her mother-child health handbook.',
                "在接待处说「从昨晚一直发烧」，出示母子手册。",
            ),
            (
                "先生はのどと耳を見て、軽い風邪だろうと説明してくれた。",
                "The doctor checked her throat and ears and explained it was likely a mild cold.",
                "医生看了喉咙和耳朵，说是轻微感冒。",
            ),
            (
                "解熱剤と、のどの痛みを和らげるシロップが出た。",
                "We got fever reducer and syrup to soothe her sore throat.",
                "开了退烧药和缓解喉咙痛的糖浆。",
            ),
            (
                "家に帰ってからは、こまめに水分を飲ませ、様子を記録した。",
                "Back home I had her drink often and kept a log of how she was doing.",
                "回家后少量多次补水，并记录情况。",
            ),
            (
                "夕方には三十七度台まで下がり、ごはんを少し食べた。",
                "By evening her temperature was in the 37s and she ate a little rice.",
                "傍晚降到三十七度多，吃了一点饭。",
            ),
            (
                "子どもの熱は親の心まで揺さぶるが、落ち着いて連絡先を確認しておくことが大切だと思った。",
                "A child's fever shakes a parent's nerves, but I felt it's vital to stay calm and know whom to call.",
                "孩子发烧牵动父母的心，但觉得冷静并事先弄清联系方式很重要。",
            ),
        ],
    },
    {
        "id": "n4-child-fever-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "小児科で（母と先生）",
        "titleJp": "小児科で（母と先生）",
        "titleEn": "At pediatrics (mother and doctor)",
        "titleZh": "在儿科（母亲与医生）",
        "titleRuby": [],
        "sections": [
            section(
                "受付",
                "Reception",
                "接待",
                "🏥",
                [
                    (
                        "B",
                        "すみません、昨夜から五歳の子どもが熱があって……。予約なしでもよいでしょうか。",
                        "Excuse me, my five-year-old has had a fever since last night... Can we come without an appointment?",
                        "不好意思，孩子五岁，从昨晚发烧……没预约可以吗？",
                    ),
                    (
                        "A",
                        "かしこまりました。お子さまのお名前と生年月日をお願いします。母子手帳はお持ちですか。",
                        "Certainly. Your child's name and date of birth, please. Do you have the mother-child handbook?",
                        "好的。请告诉我孩子的姓名和出生日期。带母子手册了吗？",
                    ),
                    (
                        "B",
                        "はい、こちらです。熱は三十八度五分くらいで、朝から下がりません。",
                        "Yes, here. Her fever is around 38.5°C and hasn't gone down since morning.",
                        "带了。烧大概三十八度五，从早上一直没退。",
                    ),
                    (
                        "A",
                        "ありがとうございます。では診察室までお通ししますので、そちらでお待ちください。",
                        "Thank you. We'll show you to the exam room; please wait there.",
                        "谢谢。请去诊室等候。",
                    ),
                ],
            ),
            section(
                "診察",
                "Exam",
                "看诊",
                "🩺",
                [
                    (
                        "A",
                        "では、のどを見せてもらいますね。あー、してごらん。",
                        "Let me look at your throat. Can you say \"ah\"?",
                        "看一下喉咙。来，啊——。",
                    ),
                    (
                        "B",
                        "（子ども）あー……。",
                        '(Child) Ahh...',
                        "（孩子）啊——……",
                    ),
                    (
                        "A",
                        "いい子だね。少し赤いけれど、今のところ大きな心配はなさそうです。咳は出ますか。",
                        "Good girl. It's a bit red, but nothing too worrying for now. Any cough?",
                        "真乖。有点红，目前看来不用太担心。咳嗽吗？",
                    ),
                    (
                        "B",
                        "ときどき、乾いた咳が出ます。",
                        "Sometimes a dry cough.",
                        "偶尔干咳。",
                    ),
                ],
            ),
            section(
                "説明",
                "Explanation",
                "说明",
                "💊",
                [
                    (
                        "A",
                        "では解熱剤と、のどの痛み用のシロップを出します。食後に飲ませてください。",
                        "I'll prescribe fever medicine and syrup for the throat. Give them after meals.",
                        "开退烧药和喉咙用的糖浆。请饭后服用。",
                    ),
                    (
                        "B",
                        "熱が三十九度を超えたら、すぐに連絡した方がよいでしょうか。",
                        "Should I call right away if her temperature goes over 39?",
                        "若超过三十九度要马上联系吗？",
                    ),
                    (
                        "A",
                        "はい、落ち着かない、水も飲めないときは、遠慮なく受診してください。",
                        "Yes—if she's restless or can't drink water, please come in without hesitation.",
                        "是的——若烦躁不安或喝不进水，请尽快就诊。",
                    ),
                ],
            ),
            section(
                "帰り",
                "Leaving",
                "离开",
                "🙏",
                [
                    (
                        "B",
                        "説明がとても分かりやすくて助かりました。ありがとうございました。",
                        "Your explanation was very clear—thank you so much.",
                        "说明很清楚，帮了大忙。谢谢您。",
                    ),
                    (
                        "A",
                        "お大事に。様子を見て、悪化したらまたいらしてください。",
                        "Take care. Watch how she does, and come back if it gets worse.",
                        "多保重。注意观察，加重请再来。",
                    ),
                ],
            ),
        ],
    },
    # --- 電車遅延 ---
    {
        "id": "n3-train-delay-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "遅延が続く朝の通勤電車で",
        "titleJp": "遅延が続く朝の通勤電車で",
        "titleEn": "On a delayed commuter train one morning",
        "titleZh": "在延误不断的早高峰电车里",
        "titleRuby": [],
        "segments": [
            (
                "朝のラッシュのあいだ、車内アナウンスが何度も流れた。",
                "During the morning rush, announcements played again and again inside the train.",
                "早高峰里，车内广播播了一遍又一遍。",
            ),
            (
                "「人身事故の影響で、前の駅で列車の運転を見合わせております」と聞こえた。",
                'We heard, "Due to an incident involving a person, train service is suspended ahead."',
                "听到「因人身事故影响，前方车站暂停运行」。",
            ),
            (
                "ドアの前に立ったまま二十分ほど動かず、スマホの路線情報は真っ赤だった。",
                "Standing by the doors, we didn't move for about twenty minutes; the transit app map was all red.",
                "堵在门前二十分钟不动，手机线路图一片红。",
            ),
            (
                "隣の人が小声で「今日の会議、間に合うかな」とつぶやいた。",
                'Someone next to me muttered, "I wonder if I\'ll make the meeting today."',
                "旁边有人小声说「今天的会议能赶上吗」。",
            ),
            (
                "私も上司に遅刻の連絡を入れるべきか迷い、一文だけ下書きを作った。",
                "I too debated whether to message my boss about being late and drafted a single sentence.",
                "我也在想要不要给上司发迟到说明，先写了一句草稿。",
            ),
            (
                "やっと徐行が始まると、また別の理由で五分ほど足止めされた。",
                "When we finally crept forward, we were held up another five minutes for a different reason.",
                "终于开始慢行，又因别的原因停了五分钟。",
            ),
            (
                "駅に着いたとき、ホームの電光掲示板には「遅延・順次運転再開」と出ていた。",
                "On the platform, the electronic board read \"Delayed—service resuming in order.\"",
                "到站时站台电光屏写着「延误·依次恢复运行」。",
            ),
            (
                "改札外の案内所には列ができ、駅員が一つずつ別ルートを説明していた。",
                "A line formed at the info desk outside the gates; staff explained alternate routes one by one.",
                "闸外问讯处排起队，站员逐个说明绕行路线。",
            ),
            (
                "私は急行に乗り換えるより、遅れを吸収できる地下鉄の方が早いと判断した。",
                "I judged the subway would absorb the delay faster than waiting for an express transfer.",
                "判断换急行不如改坐地铁能吃掉延误。",
            ),
            (
                "会社には「電車遅延のため十五分ほど遅れます」と送り、返信は「了解」とだけ返ってきた。",
                'I texted work, "About 15 minutes late due to train delays," and got back only "OK."',
                "给公司发「电车延误约迟到十五分钟」，回复只有「了解」。",
            ),
            (
                "遅延証明書はアプリで取得でき、人事に提出する手間も減っている。",
                "Delay certificates can be pulled from an app now, which saves HR paperwork.",
                "延误证明可在 App 上开，少了不少交人事的麻烦。",
            ),
            (
                "予定どおりにいかない朝ほど、情報を短く共有することが助けになると実感した。",
                "On mornings when nothing goes to plan, I felt that sharing updates briefly really helps.",
                "越是不按计划的早晨，越体会到简短共享信息有多管用。",
            ),
        ],
    },
    {
        "id": "n3-train-delay-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "遅延時、ホームで駅員に聞く",
        "titleJp": "遅延時、ホームで駅員に聞く",
        "titleEn": "Asking station staff on the platform during a delay",
        "titleZh": "延误时在站台问站员",
        "titleRuby": [],
        "sections": [
            section(
                "状況を確認",
                "Checking the situation",
                "确认情况",
                "🚃",
                [
                    (
                        "B",
                        "すみません、この中央線、あとどのくらいで動き出す見込みですか。",
                        "Excuse me, any idea when this Chuo Line train will start moving again?",
                        "请问这条中央线大概还要多久能开？",
                    ),
                    (
                        "A",
                        "現在、前駅での確認作業のため、運転を見合わせております。再開の見込みはまだ申し上げられません。",
                        "Service is suspended for checks at the station ahead. We cannot yet say when it will resume.",
                        "因前方车站正在确认，暂停运行。恢复时间尚无法告知。",
                    ),
                    (
                        "B",
                        "会社に遅刻するので、遅延証明書はどこで取れますか。",
                        "I'll be late for work—where can I get a delay certificate?",
                        "上班要迟到了，延误证明在哪里领？",
                    ),
                    (
                        "A",
                        "改札外の案内所のほか、当社のアプリの「遅延証明」からも取得できます。",
                        "Besides the info desk outside the gates, you can use our app's \"delay certificate\" section.",
                        "闸外问讯处可以，本公司 App 的「延误证明」也能下载。",
                    ),
                ],
            ),
            section(
                "乗り換え",
                "Transfer options",
                "换乘",
                "🔀",
                [
                    (
                        "B",
                        "新宿まで行きたいのですが、別の路線の方が早いでしょうか。",
                        "I need to get to Shinjuku—would another line be faster?",
                        "我要去新宿，换别的线会不会更快？",
                    ),
                    (
                        "A",
                        "このあと順次再開する見込みですが、お急ぎでしたら地下鉄各線への乗り換え口はあちらです。",
                        "We expect service to resume in order, but if you're in a hurry, the subway transfer gates are that way.",
                        "预计会依次恢复，若赶时间地铁各线的换乘口在那边。",
                    ),
                    (
                        "B",
                        "定期はこの会社のままで入れますか。",
                        "Can I enter with this company's commuter pass?",
                        "用这家公司的定期券能进吗？",
                    ),
                    (
                        "A",
                        "相互乗り入れの区間であればご利用いただけます。詳しくは路線図をご覧ください。",
                        "You may use it within mutual through-service sections. Please see the route map for details.",
                        "在互通区间内可以使用。详情请查看路线图。",
                    ),
                ],
            ),
            section(
                "締め",
                "Closing",
                "结束",
                "🙇",
                [
                    (
                        "B",
                        "分かりました。急いで乗り換えてみます。ありがとうございます。",
                        "Understood. I'll try transferring quickly. Thank you.",
                        "明白了。我赶快去换乘。谢谢。",
                    ),
                    (
                        "A",
                        "お足元にお気をつけて。本日はご迷惑をおかけしております。",
                        "Mind your step. We apologize for the inconvenience today.",
                        "请注意脚下。今天给您添麻烦了。",
                    ),
                ],
            ),
        ],
    },
    # --- 依頼を断る ---
    {
        "id": "n3-decline-request-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "無理な依頼には、理由と代案を添えて",
        "titleJp": "無理な依頼には、理由と代案を添えて",
        "titleEn": "For unreasonable requests, add a reason and an alternative",
        "titleZh": "对做不到的请求，附上理由和替代方案",
        "titleRuby": [],
        "segments": [
            (
                "同僚から、締切が重なる週にだけ追加の資料作成を頼まれた。",
                "A colleague asked me to prepare extra materials on a week when deadlines already piled up.",
                "同事在截止扎堆的那周，拜托我额外做资料。",
            ),
            (
                "断るのは悪い気がしたが、そのまま引き受けると自分のタスクが全部遅れると分かっていた。",
                "Saying no felt bad, but I knew taking it on would delay all of my own tasks.",
                "拒绝心里过意不去，但接下来自己的任务全会拖晚。",
            ),
            (
                "まず「今週は〇〇の納期が三つ重なっていて、品質を落とさずに足すのが難しい」と事実を短く伝えた。",
                'First I briefly stated the fact: "This week three deadlines for XX overlap, so it\'s hard to add work without cutting quality."',
                "先简短说明事实：「这周有三个〇〇的截稿叠在一起，不降低质量很难再加」。",
            ),
            (
                "次に「来週の火曜なら二時間ほどなら手伝える」と、具体的な代案を出した。",
                'Then I offered a concrete alternative: "If it can wait until Tuesday next week, I can help for about two hours."',
                "再给出具体替代：「若可延到下周二，我能帮大约两小时」。",
            ),
            (
                "相手は一瞬むっとした顔をしたが、自分の依頼が急だったことを認めてくれた。",
                "They looked annoyed for a moment but admitted their request had been sudden.",
                "对方一时面露不悦，但承认自己的请求太急。",
            ),
            (
                "「代案がないノー」は関係を切るように聞こえやすいと、後から読んだ本に書いてあった。",
                'A book I read later said a "no" with no alternative often sounds like burning bridges.',
                "后来看书上写：没有替代方案的拒绝容易像撕破脸。",
            ),
            (
                "すべてを飲み込むのではなく、優先順位を言語化することが、長い目で見れば信頼につながる。",
                "Putting priorities into words instead of swallowing everything builds trust in the long run.",
                "不是全盘硬扛，而是把优先级说清楚，长远看反而积累信任。",
            ),
            (
                "もちろん相手の立場もあるので、トーンは低めに、メールなら一文目に感謝を入れるようにしている。",
                "Of course they have their side too, so I keep my tone low, and in emails I start with thanks.",
                "当然也要体谅对方，所以语气放低，邮件第一句会写感谢。",
            ),
            (
                "断ったあと、本当に来週手伝えたときにちゃんと時間を空けておくことが大事だと思う。",
                "I think it's important to actually keep the time open if you said you'd help next week.",
                "觉得拒绝之后，若说下周帮，就一定要真的留出时间。",
            ),
            (
                "小さな約束を守り続けるほうが、無理して失敗するより印象がよい。",
                "Keeping small promises leaves a better impression than overpromising and failing.",
                "守住小承诺比硬答应然后搞砸印象更好。",
            ),
            (
                "依頼を断る練習は、自分の仕事の幅を知る練習でもある。",
                "Practicing to decline is also practice in knowing your own bandwidth.",
                "练习拒绝也是练习摸清自己的工作容量。",
            ),
            (
                "完璧に気持ちよく終わらなくても、誠実さは伝わると信じている。",
                "Even if it doesn't end perfectly smoothly, I believe sincerity gets through.",
                "即便不能皆大欢喜，我相信诚意能传达到。",
            ),
        ],
    },
    {
        "id": "n3-decline-request-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "急な追加タスクを断る（同僚同士）",
        "titleJp": "急な追加タスクを断る（同僚同士）",
        "titleEn": "Declining a sudden extra task (between coworkers)",
        "titleZh": "拒绝临时加任务（同事之间）",
        "titleRuby": [],
        "sections": [
            section(
                "依頼",
                "The request",
                "请求",
                "📥",
                [
                    (
                        "A",
                        "ねえ、来週の企画書、金曜までに私の分の資料まとめ、手伝ってくれない？急に上から言われて。",
                        "Hey, can you help compile my part of the proposal deck by Friday? It just came from above.",
                        "喂，企划书我那份资料周五前能帮我整理吗？上面突然派的。",
                    ),
                    (
                        "B",
                        "ごめん、今週は〇〇のレビューと△△の納品が三つ重なってて、今日から手を出すのが難しいんだ。",
                        "Sorry, this week three things overlap—XX review and two △△ deliveries—so I can't really jump in today.",
                        "抱歉，这周〇〇评审和△△交货叠了三件，今天起很难再插一手。",
                    ),
                ],
            ),
            section(
                "理由と代案",
                "Reason and alternative",
                "理由与替代",
                "⚖️",
                [
                    (
                        "B",
                        "品質落として雑に渡すのは嫌だから、今週中は無理。来週の火曜午後なら二時間くらいなら一緒にやれる。",
                        "I don't want to hand in sloppy work, so this week is impossible. Tuesday afternoon next week I could work on it with you for about two hours.",
                        "不想降质量糊弄，所以这周不行。下周二下午可以一起弄两小时左右。",
                    ),
                    (
                        "A",
                        "うーん、金曜が厳しいか。テンプレだけ先に共有してもらえる？そこに私が文章入れる形なら何とかなるかも。",
                        "Hmm, Friday's tight. Could you share the template first? If I just drop text in, I might manage.",
                        "嗯，周五是紧。能先把模板给我吗？我只填文字的话也许能搞定。",
                    ),
                    (
                        "B",
                        "それなら今すぐ共有する。書式だけ合わせておけば、あとはあなたのペースで埋められるはず。",
                        "I can share that right now. Match the format and you should be able to fill the rest at your pace.",
                        "那我现在就共享。格式对齐后你应该能按自己的节奏填完。",
                    ),
                ],
            ),
            section(
                "合意",
                "Agreement",
                "共识",
                "🤝",
                [
                    (
                        "A",
                        "助かる。上には「一部テンプレ協力」とだけ伝えておくね。",
                        "That helps. I'll tell my boss only that I got template help.",
                        "帮大忙了。我跟上面就说「部分模板有人协助」。",
                    ),
                    (
                        "B",
                        "了解。無理に全部背負わなくてよかった。",
                        "Got it. Glad I didn't have to carry the whole thing.",
                        "好。不用硬扛全部真好。",
                    ),
                ],
            ),
        ],
    },
    # --- クレーム電話 N2 ---
    {
        "id": "n2-complaint-call-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "届かなかった荷物の配送を問い合わせた日",
        "titleJp": "届かなかった荷物の配送を問い合わせた日",
        "titleEn": "The day I called about a package that never arrived",
        "titleZh": "打电话询问未送达包裹的那天",
        "titleRuby": [],
        "segments": [
            (
                "ネットで注文した荷物が、追跡では配達済みになっているのに玄関にないことに気づいた。",
                "I noticed my online order showed \"delivered\" on tracking but wasn't at my door.",
                "发现网购包裹追踪显示已送达，门口却没有。",
            ),
            (
                "再配達の連絡をしようとしたが、業者の自動音声が複雑で、人に繋がるまでに時間がかかった。",
                "I tried to arrange redelivery, but the IVR was complex and it took time to reach a person.",
                "想联系再配送，自动语音很复杂，接通人工花了很久。",
            ),
            (
                "オペレーターには、注文番号と配送完了の日時を伝え、置き配指定がなかったことも説明した。",
                "I gave the operator the order number and delivery timestamp and explained I'd requested no doorstep drop-off.",
                "向接线员报了订单号和送达时间，并说明没选门口留置。",
            ),
            (
                "「大変ご迷惑をおかけしております」と何度も謝られ、状況を調べるので少々お待ちくださいと言われた。",
                'I was apologized to repeatedly—"We\'re very sorry for the inconvenience"—and asked to wait while they checked.',
                "对方多次道歉并说正在核实请稍等。",
            ),
            (
                "五分ほど保留音のあと、近隣の配送センターで荷物が見つかったとの連絡が入った。",
                "After about five minutes on hold, they said the package had been found at a nearby depot.",
                "听了约五分钟保留音乐后，说在附近配送中心找到了包裹。",
            ),
            (
                "当日中に再配達できるが、時間帯は指定できないと告げられた。",
                "They said it could be redelivered the same day but the time slot couldn't be chosen.",
                "告知可当天再送，但无法指定时段。",
            ),
            (
                "怒りたい気持ちもあったが、電話の相手は個人ではなく手続きの窓口だと思い直した。",
                "Part of me wanted to be angry, but I reminded myself the person on the phone wasn't the one at fault.",
                "虽想发火，但转念觉得电话那头只是流程窗口不是个人恩怨。",
            ),
            (
                "事実を短く、番号をゆっくり読み上げるだけで、やり取りはだいぶスムーズになった。",
                "Keeping facts brief and reading numbers slowly made the exchange much smoother.",
                "事实说简短、号码慢慢念，沟通顺畅很多。",
            ),
            (
                "夜、ようやく届いた箱を開け、中身に傷がないか確認した。",
                "When the box finally arrived that evening, I opened it and checked the contents weren't damaged.",
                "晚上终于收到箱子，打开检查里面有没有损坏。",
            ),
            (
                "トラブルは起きるものだと割り切り、次からは置き配を使わない設定に変えた。",
                "I accepted that trouble happens sometimes and switched settings so packages aren't left unattended.",
                "想通纠纷难免，之后改成不用门口留置。",
            ),
            (
                "敬語だらけの会話に疲れたが、相手の定型句に合わせて答えると気持ちが楽になった。",
                "The all-keigo conversation was tiring, but matching their set phrases made it easier emotionally.",
                "全程敬语很累，但顺着对方的套话回答心里轻松些。",
            ),
        ],
    },
    {
        "id": "n2-complaint-call-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "配送センターに電話で問い合わせる",
        "titleJp": "配送センターに電話で問い合わせる",
        "titleEn": "Calling the delivery center to inquire",
        "titleZh": "致电配送中心询问",
        "titleRuby": [],
        "sections": [
            section(
                "オープニング",
                "Opening",
                "开场",
                "📞",
                [
                    (
                        "A",
                        "お電話ありがとうございます。配送センターの田中でございます。お問い合わせ番号をお願いできますでしょうか。",
                        "Thank you for calling. This is Tanaka at the delivery center. May I have your inquiry number, please?",
                        "感谢您的来电。我是配送中心的田中。请问您的查询号码是？",
                    ),
                    (
                        "B",
                        "はい、注文番号はABの十二の三十四でございます。追跡では本日十四時に配達済みとなっておりますが、届いておりません。",
                        "Yes—the order number is AB-1234. Tracking shows delivered today at 2 p.m., but I haven't received it.",
                        "订单号是 AB1234。追踪显示今天十四点已送达，但我没收到。",
                    ),
                    (
                        "A",
                        "かしこまりました。大変ご迷惑をおかけいたしております。お客様のお名前とお電話番号をお伺いしてもよろしいでしょうか。",
                        "Understood. We apologize for the inconvenience. May I have your name and phone number?",
                        "明白了。非常抱歉。请问您的姓名和电话号码？",
                    ),
                ],
            ),
            section(
                "確認",
                "Verification",
                "核实",
                "🔍",
                [
                    (
                        "B",
                        "山田太郎でございます。電話番号は〇九〇の……でございます。置き配の指定はしておりません。",
                        "This is Taro Yamada. My number is 090-... I did not request unattended delivery.",
                        "我是山田太郎。电话是 090……没有指定门口留置。",
                    ),
                    (
                        "A",
                        "ありがとうございます。ただいま担当の者に確認いたしますので、少々お待ちくださいませ。",
                        "Thank you. I will confirm with the person in charge; please wait a moment.",
                        "谢谢。我现在向负责人确认，请稍候。",
                    ),
                    (
                        "A",
                        "お待たせいたしました。近隣のセンターにて荷物を確認できました。本日中に再配達を手配いたします。",
                        "Thank you for waiting. We located your package at a nearby depot. We will arrange redelivery today.",
                        "让您久等了。已在附近中心找到包裹。今天内安排再配送。",
                    ),
                ],
            ),
            section(
                "条件と締め",
                "Conditions and closing",
                "条件与收尾",
                "📦",
                [
                    (
                        "B",
                        "時間帯の指定は可能でしょうか。",
                        "Is it possible to specify a time window?",
                        "可以指定时段吗？",
                    ),
                    (
                        "A",
                        "申し訳ございません、本日の再配達につきましては時間帯のご指定を承っておりません。",
                        "We apologize; for same-day redelivery we cannot accept a time-slot request.",
                        "抱歉，当天的再配送无法指定时段。",
                    ),
                    (
                        "B",
                        "承知いたしました。それでは、玄関先でのお渡しをお願いいたします。",
                        "Understood. Please hand it to me at the door.",
                        "知道了。那就请送到门口当面交接。",
                    ),
                    (
                        "A",
                        "かしこまりました。本日は貴重なお時間をいただき、ありがとうございました。",
                        "Certainly. Thank you for your time today.",
                        "好的。感谢您今天抽出宝贵时间。",
                    ),
                ],
            ),
        ],
    },
    # --- 週報 ---
    {
        "id": "n3-weekly-report-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "週報は長ければよいわけではない",
        "titleJp": "週報は長ければよいわけではない",
        "titleEn": "A weekly report isn't better just because it's long",
        "titleZh": "周报并不是越长越好",
        "titleRuby": [],
        "segments": [
            (
                "新しい職場では、毎週金曜に短い週報を提出することが決まっていた。",
                "At my new job, we were to submit a short weekly report every Friday.",
                "新工作规定每周五交一份简短的周报。",
            ),
            (
                "最初は丁寧さを見せたくて、やったことをすべて箇条書きにし、三ページ近くになった。",
                "At first I wanted to look thorough and listed everything I'd done—nearly three pages.",
                "起初想显得认真，把做的事全列成条目，将近三页。",
            ),
            (
                "上司から返ってきたコメントは「次週のリスクだけ一行でよい」という短い一文だった。",
                "My boss's comment came back as one short line: \"Just one line on next week's risks is enough.\"",
                "上司批注只有一句：「下周风险写一行就行」。",
            ),
            (
                "長さは努力の証しではなく、読む人の時間を奪うと気づいた。",
                "I realized length isn't proof of effort—it steals the reader's time.",
                "意识到长度不是努力的证明，而是在占读者时间。",
            ),
            (
                "それ以降は、完了したこと・進行中・詰まりどころの三行に圧縮するフォーマットにした。",
                "After that I used a three-line format: done, in progress, and blockers.",
                "之后改成三行：已完成、进行中、卡点。",
            ),
            (
                "数字は一つだけ入れるようにし、「商談三件、うち一件成約」のように事実を置いた。",
                "I added just one numeric fact, like \"three sales talks, one closed.\"",
                "数字只放一个，如「商谈三件，成交一件」。",
            ),
            (
                "詰まりどころには、すでに試したことと、次に欲しい支援を書くと、会話が早く進んだ。",
                "Under blockers, listing what I'd tried and what help I needed sped up conversations.",
                "在卡点里写已尝试的和需要的支援，对话推进更快。",
            ),
            (
                "週報は記録であると同時に、来週の会話の予告編にもなる。",
                "A weekly report is both a record and a trailer for next week's discussion.",
                "周报既是记录，也是下周沟通的预告。",
            ),
            (
                "テンプレートを共有した同僚も、同じように短く揃えてくれた。",
                "Colleagues I shared the template with also kept theirs short.",
                "分享模板的同事也把周报缩短了。",
            ),
            (
                "「読まれている実感」は文字数より、返信の速さと具体性で感じる。",
                "I feel \"someone read this\" from reply speed and specificity, not word count.",
                "「被认真读了」的感觉来自回复速度和针对性，不是字数。",
            ),
            (
                "週報を書く時間は十五分以内を目標にし、残りは実作業に回すようにした。",
                "I aimed to finish the report in under fifteen minutes and spend the rest on real work.",
                "目标十五分钟写完周报，其余时间留给实干。",
            ),
        ],
    },
    {
        "id": "n3-weekly-report-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "金曜、上司と週報を確認する",
        "titleJp": "金曜、上司と週報を確認する",
        "titleEn": "Friday: reviewing the weekly report with your manager",
        "titleZh": "周五与上司确认周报",
        "titleRuby": [],
        "sections": [
            section(
                "フィードバック",
                "Feedback",
                "反馈",
                "📋",
                [
                    (
                        "A",
                        "今週の週報、三行にまとまっていて読みやすかった。詰まりどころの「レビュー待ち」、誰待ちかだけ書いておいて。",
                        "This week's report was easy to read in three lines. For the blocker \"waiting on review,\" note whose review.",
                        "这周周报三行很易读。卡点「等评审」请写清在等谁。",
                    ),
                    (
                        "B",
                        "了解です。デザインチームの佐藤さん待ちに修正します。",
                        "Got it. I'll change it to waiting on Sato from design.",
                        "好的。改成等设计组的佐藤。",
                    ),
                ],
            ),
            section(
                "来週",
                "Next week",
                "下周",
                "📅",
                [
                    (
                        "A",
                        "来週の目標は、リリース準備で言うとどこまで行きたい？",
                        "For release prep next week, how far do you want to get?",
                        "下周发布准备想推进到哪里？",
                    ),
                    (
                        "B",
                        "ステージング環境での最終確認まで終わらせたいです。ブロッカーが出たら月曜の朝一で共有します。",
                        "I want to finish final checks on staging. If blockers appear I'll flag them first thing Monday morning.",
                        "想做完预发环境的最终确认。若有阻塞周一一早同步。",
                    ),
                    (
                        "A",
                        "いいね。週報にもその一行、入れておいて。",
                        "Good. Put that one line in the weekly report too.",
                        "好。周报里也写上这一行。",
                    ),
                ],
            ),
            section(
                "締め",
                "Closing",
                "收尾",
                "☕",
                [
                    (
                        "B",
                        "短く書くほうが、逆に議論がはっきりしますね。",
                        "Writing shorter actually makes the discussion clearer.",
                        "越短写清楚，讨论反而更明确。",
                    ),
                    (
                        "A",
                        "そうそう。長い週報は、誰も最後まで読んでないことが多いからね。",
                        "Exactly. Long reports often never get read to the end.",
                        "对啊。太长的周报往往没人读完。",
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
