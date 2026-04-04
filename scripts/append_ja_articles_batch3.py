#!/usr/bin/env python3
"""
batch3 → public/data/ja_articles.json（单行 JSON）

场景与 batch1/batch2 及原有篇目不重复：
美容院、スーパー精算、図書館、ビジネスホテルチェックイン、実家への電話、カフェで作業

运行: .venv/bin/python scripts/append_ja_articles_batch3.py
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
    # --- 美容院 ---
    {
        "id": "n4-hair-salon-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "久しぶりに美容院へ行った日",
        "titleJp": "久しぶりに美容院へ行った日",
        "titleEn": "The day I finally went to the hair salon after a long break",
        "titleZh": "隔了许久去理发店的那天",
        "titleRuby": [],
        "segments": [
            (
                "髪が伸びっぱなしで、鏡を見るたびに後回しにしてきた。",
                "My hair had grown out; every time I looked in the mirror I kept putting it off.",
                "头发一直留长，每次照镜子都往后拖。",
            ),
            (
                "ネットで近所の店を探し、写真の雰囲気が好みそうなところに電話で予約した。",
                "I searched online for a nearby shop and booked by phone at a place whose photos looked like my style.",
                "在网上找附近的店，看照片合口味就打电话预约了。",
            ),
            (
                "当日、シャンプーの香りが漂う店内で、担当の人が笑顔で声をかけてくれた。",
                "That day, inside the shop smelling of shampoo, the stylist greeted me with a smile.",
                "当天店里飘着洗发水味，店员笑着跟我打招呼。",
            ),
            (
                "「どんな感じにしますか」と聞かれ、襟足は短め、前は目にかからないくらいと伝えた。",
                'Asked, "How would you like it?" I said shorter at the nape and bangs not in my eyes.',
                "被问想剪成什么样，我说后颈短一点、刘海别挡眼睛。",
            ),
            (
                "写真を見せながら「だいたいこんなイメージです」と言うと、分かりやすいですねと言ってもらえた。",
                'When I showed a photo and said, "Roughly this image," they said that made it clear.',
                "拿照片说「大概这种感觉」，对方说那就清楚了。",
            ),
            (
                "カットのあいだ、旅行の話で少し盛り上がり、緊張がほどけた。",
                "During the cut we chatted a bit about travel and I relaxed.",
                "剪发时聊了会儿旅行，没那么紧张了。",
            ),
            (
                "ドライヤーの熱でうとうとしかけて、自分で苦笑いした。",
                "The dryer heat almost put me to sleep; I smiled wryly at myself.",
                "吹风机热得差点睡着，自己苦笑了一下。",
            ),
            (
                "仕上がりを見て、思ったより軽くて歩きやすいと感じた。",
                "Seeing the result, it felt lighter and easier to move than I'd expected.",
                "看完成果，比想象中轻快、利落。",
            ),
            (
                "会計はカードも使えて、次回は何週間空けたらいいかも教えてもらった。",
                "I could pay by card, and they told me how many weeks to wait before the next visit.",
                "可以刷卡，还问了下次隔几周来比较好。",
            ),
            (
                "店を出て風が首に触れると、いつもと違う感触が新鮮だった。",
                "Leaving the shop, the wind on my neck felt fresh and different.",
                "出店风碰到后颈，触感新鲜。",
            ),
            (
                "自分の身だしなみを後回しにしすぎないよう、カレンダーに丸を付けた。",
                "I circled a date on the calendar so I wouldn't keep putting self-care last.",
                "在日历上画圈，提醒自己别总把打理自己放最后。",
            ),
        ],
    },
    {
        "id": "n4-hair-salon-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "美容院で（カットの相談）",
        "titleJp": "美容院で（カットの相談）",
        "titleEn": "At the salon (consulting on a cut)",
        "titleZh": "在理发店（商量怎么剪）",
        "titleRuby": [],
        "sections": [
            section(
                "着席",
                "At the chair",
                "入座",
                "💇",
                [
                    (
                        "A",
                        "本日はご予約の山田様ですね。お荷物、こちらのかごにどうぞ。",
                        "You're Yamada with an appointment today. Please put your bag in this basket.",
                        "是预约的山田女士吧。包请放在这个篮子里。",
                    ),
                    (
                        "B",
                        "ありがとうございます。実は三か月ぶりなので、だいぶ伸びちゃって。",
                        "Thank you. It's actually been three months, so it's grown a lot.",
                        "谢谢。其实三个月没剪了，长了不少。",
                    ),
                    (
                        "A",
                        "大丈夫ですよ。今日はどんな雰囲気に近づけたいですか。",
                        "No worries. What kind of style or look would you like today?",
                        "没关系。今天想剪什么样的发型？",
                    ),
                ],
            ),
            section(
                "要望",
                "Requests",
                "要求",
                "✂️",
                [
                    (
                        "B",
                        "後ろはすっきり、横は耳が隠れるくらいがいいです。前髪は眉毛にかからない長さで。",
                        "I'd like the back neat, the sides long enough to cover my ears, and bangs not touching my eyebrows.",
                        "后面清爽，两侧盖到耳朵就行。刘海别盖住眉毛。",
                    ),
                    (
                        "A",
                        "かしこまりました。この写真、イメージに近いですか。",
                        "Got it. Is this photo close to what you want?",
                        "好的。这张照片接近您想要的吗？",
                    ),
                    (
                        "B",
                        "はい、だいたいそれで。あまり短くしすぎないでくださいね。",
                        "Yes, roughly that. Please don't cut it too short.",
                        "对，差不多。别剪太短哦。",
                    ),
                ],
            ),
            section(
                "仕上げ",
                "Finishing",
                "收尾",
                "✨",
                [
                    (
                        "A",
                        "どうぞ鏡をご覧ください。ボリューム、調整しましょうか。",
                        "Please look in the mirror. Would you like me to adjust the fullness?",
                        "请看镜子。要调整一下蓬松度吗？",
                    ),
                    (
                        "B",
                        "いい感じです。このままで大丈夫です。",
                        "Looks good. This is fine as is.",
                        "挺好的。就这样可以。",
                    ),
                    (
                        "A",
                        "ありがとうございます。スタイリングは、乾かしたあとにこのワックスを少量つけると形がキープしやすいです。",
                        "Thank you. After drying, a little of this wax helps hold the shape.",
                        "谢谢。吹干后抹一点这个发蜡比较容易定型。",
                    ),
                    (
                        "B",
                        "教えてくださって助かります。また来ますね。",
                        "Thanks for explaining—I'll come again.",
                        "您这么说我好办多了。我会再来的。",
                    ),
                ],
            ),
        ],
    },
    # --- スーパー ---
    {
        "id": "n4-supermarket-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "夕方のスーパーで買い物して",
        "titleJp": "夕方のスーパーで買い物して",
        "titleEn": "Grocery shopping at the supermarket one evening",
        "titleZh": "傍晚在超市买东西",
        "titleRuby": [],
        "segments": [
            (
                "仕事帰り、冷蔵庫が空に近いことに気づいて駅前の店に寄った。",
                "After work I noticed the fridge was almost empty and stopped by the store in front of the station.",
                "下班发现冰箱快空了，顺路去车站前的店。",
            ),
            (
                "野菜売り場では、半額シールのパックを見つけて思わず手が伸びた。",
                "In the produce section I spotted half-price packs and reached for them instinctively.",
                "在蔬菜区看到半价贴，忍不住伸手拿。",
            ),
            (
                "レジの列が二つあって、カゴの少ない方に並ぶクセがついている。",
                "There were two checkout lines; I'm in the habit of joining the one with smaller baskets.",
                "有两条收银队，我习惯排篮子少的那条。",
            ),
            (
                "自分の番が近づくと、ポイントカードを探して財布の奥から引っ張り出した。",
                "As my turn neared, I dug my points card from deep in my wallet.",
                "快轮到我时翻钱包深处找积分卡。",
            ),
            (
                "袋は五円だが、エコバッグを出すのが遅れて、少し慌てた。",
                "Bags cost five yen, but I was slow getting my eco-bag out and flustered a bit.",
                "塑料袋五日元，但环保袋拿慢了，有点慌。",
            ),
            (
                "レジの人が「お弁当、温めますか」と聞いてくれて、助かった。",
                'The cashier asked, "Shall I heat your bento?" which saved me.',
                "收银员问「便当要加热吗」，帮了大忙。",
            ),
            (
                "会計が終わると、釣り銭トレーに小銭が滑り込む音がした。",
                "When payment finished, coins slid into the change tray with a clink.",
                "结完账，零钱滑进托盘的声音很清楚。",
            ),
            (
                "袋を両手で持ち直し、エスカレーターへ向かった。",
                "I readjusted the bags in both hands and headed for the escalator.",
                "双手拎好袋子走向扶梯。",
            ),
            (
                "家に着いてレシートを見ると、思ったより牛乳が高くなっていた。",
                "Home, checking the receipt, milk had gone up more than I'd thought.",
                "到家看小票，牛奶比想的涨了不少。",
            ),
            (
                "それでも冷蔵庫が満たされる安心感は、小さな達成感みたいだった。",
                "Still, the relief of a full fridge felt like a small accomplishment.",
                "但冰箱被填满的安心感，像一点小成就。",
            ),
        ],
    },
    {
        "id": "n4-supermarket-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "レジで（袋とポイント）",
        "titleJp": "レジで（袋とポイント）",
        "titleEn": "At the register (bags and points)",
        "titleZh": "在收银台（袋子和积分）",
        "titleRuby": [],
        "sections": [
            section(
                "会計前",
                "Before paying",
                "结账前",
                "🛒",
                [
                    (
                        "A",
                        "お待たせいたしました。ポイントカードはお持ちですか。",
                        "Sorry for the wait. Do you have a points card?",
                        "让您久等了。有积分卡吗？",
                    ),
                    (
                        "B",
                        "はい、こちらです。あ、あとレジ袋、一枚お願いします。",
                        "Yes, here. Oh, one shopping bag, please.",
                        "有，这张。还要一个塑料袋。",
                    ),
                    (
                        "A",
                        "かしこまりました。お弁当とお味噌汁、温めますか。",
                        "Certainly. Shall I heat the bento and the miso soup?",
                        "好的。便当和味噌汤要加热吗？",
                    ),
                    (
                        "B",
                        "味噌汁だけお願いします。",
                        "Just the miso soup, please.",
                        "只要味噌汤，谢谢。",
                    ),
                ],
            ),
            section(
                "支払い",
                "Payment",
                "付款",
                "💳",
                [
                    (
                        "A",
                        "一千二百八十八円になります。お支払いはカードでよろしいですか。",
                        "That will be 1,288 yen. Will you pay by card?",
                        "一共一千二百八十八日元。刷卡可以吗？",
                    ),
                    (
                        "B",
                        "はい、タッチ決済で。",
                        "Yes, contactless, please.",
                        "嗯，闪付。",
                    ),
                    (
                        "A",
                        "ありがとうございます。レシートは必要ですか。",
                        "Thank you. Do you need a receipt?",
                        "谢谢。需要小票吗？",
                    ),
                    (
                        "B",
                        "大丈夫です。",
                        "No, I'm fine.",
                        "不用了。",
                    ),
                ],
            ),
            section(
                "締め",
                "Closing",
                "结束",
                "🙏",
                [
                    (
                        "A",
                        "お買い上げありがとうございます。足元にお気をつけてお帰りください。",
                        "Thank you for your purchase. Mind your step on the way home.",
                        "谢谢惠顾。路上请小心。",
                    ),
                    (
                        "B",
                        "ありがとうございました。",
                        "Thank you.",
                        "谢谢。",
                    ),
                ],
            ),
        ],
    },
    # --- 図書館 ---
    {
        "id": "n3-library-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "市立図書館で予約本を受け取って",
        "titleJp": "市立図書館で予約本を受け取って",
        "titleEn": "Picking up a reserved book at the city library",
        "titleZh": "在市立图书馆取预约的书",
        "titleRuby": [],
        "segments": [
            (
                "新刊が市立図書館のサイトに載るたびに、予約ボタンを押すのが楽しみになっていた。",
                "Whenever new books hit the city library site, tapping reserve had become a small pleasure.",
                "市立图书馆网站一上新书，按预约成了一种小期待。",
            ),
            (
                "今回は長めの小説で、在庫が一冊しかないため順番待ちになった。",
                "This time it was a long novel with only one copy, so I had to wait my turn.",
                "这次是长篇，馆藏只有一本，得排队。",
            ),
            (
                "メールで「受け取り可能」と来た日、仕事の帰りに立ち寄った。",
                "The day the email said it was ready, I stopped by after work.",
                "收到「可取书」邮件那天，下班顺路去。",
            ),
            (
                "自動貸出機の前で並んでいると、前の人が延長の仕方で職員に聞いていた。",
                "Waiting at the self-checkout, the person ahead was asking staff how to renew.",
                "在自助借书机排队时，前面的人在问怎么续借。",
            ),
            (
                "自分の番では、会員カードをかざすだけで本が出てきて、手軽さに驚いた。",
                "At my turn, I just tapped my card and the book came out—surprised how easy it was.",
                "轮到我只要刷会员卡书就出来了，没想到这么省事。",
            ),
            (
                "閲覧席は窓際が空いていて、しばらく目次だけ読んでから帰った。",
                "A window seat in the reading area was free; I skimmed the table of contents before leaving.",
                "阅览区靠窗有空位，翻了一会儿目录才走。",
            ),
            (
                "貸出期間は二週間だが、厚い本なので延長を検討しようとメモした。",
                "Loan period is two weeks, but since it's thick I noted to consider renewing.",
                "借期两周，书很厚，记下来考虑续借。",
            ),
            (
                "図書館の空気は、少し冷えていて集中しやすかった。",
                "The library air was a bit cool and easy to focus in.",
                "图书馆有点凉，容易集中。",
            ),
            (
                "家に帰り、カバーに書店の値段が印刷されているのを見て、税金の使い道を実感した。",
                "Home, seeing the printed bookstore price on the cover, I felt how taxes get used.",
                "回家看到封底印着书店定价，真切感到税金用在了哪里。",
            ),
            (
                "無料だからこそ、期限と他の読者への配慮を守りたいと思う。",
                "Because it's free, I want to respect deadlines and other readers.",
                "正因为免费，更想守期限、体谅别的读者。",
            ),
        ],
    },
    {
        "id": "n3-library-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "図書館のカウンターで",
        "titleJp": "図書館のカウンターで",
        "titleEn": "At the library counter",
        "titleZh": "在图书馆柜台",
        "titleRuby": [],
        "sections": [
            section(
                "予約の本",
                "Reserved book",
                "预约书",
                "📚",
                [
                    (
                        "B",
                        "すみません、予約してあった本を取りに来たのですが。",
                        "Excuse me, I came to pick up a book I'd reserved.",
                        "你好，我来取预约的书。",
                    ),
                    (
                        "A",
                        "会員番号をお願いします。お名前もフルネームで。",
                        "Your member number, please. And your full name.",
                        "请报会员号。还有全名。",
                    ),
                    (
                        "B",
                        "〇九の十二の三十四です。山田花子です。",
                        "091234. Hanako Yamada.",
                        "091234。山田花子。",
                    ),
                    (
                        "A",
                        "ありがとうございます。こちらがご予約の本です。二週間が返却期限です。",
                        "Thank you. Here is your reserved book. It's due back in two weeks.",
                        "谢谢。这是您预约的书。两周内请归还。",
                    ),
                ],
            ),
            section(
                "延長について",
                "About renewal",
                "续借",
                "🔄",
                [
                    (
                        "B",
                        "もし読み終わらなかったら、延長はアプリからでよいですか。",
                        "If I don't finish, can I renew from the app?",
                        "若读不完，可以在 App 上续借吗？",
                    ),
                    (
                        "A",
                        "はい、誰かが予約していなければ、開館日のうちに操作いただけます。",
                        "Yes, if no one else has reserved it, you can do it on any open day.",
                        "可以，只要没人预约，在开馆日内操作即可。",
                    ),
                    (
                        "B",
                        "分かりました。紛失した場合は、すぐに連絡すればよいですか。",
                        "Understood. If I lose it, should I contact you right away?",
                        "明白了。若弄丢要马上联系吗？",
                    ),
                    (
                        "A",
                        "はい。できるだけ早めに窓口または電話でお知らせください。",
                        "Yes. Please let us know at the counter or by phone as soon as you can.",
                        "是的。请尽快到窗口或电话联系。",
                    ),
                ],
            ),
        ],
    },
    # --- ホテル ---
    {
        "id": "n3-hotel-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "出張でビジネスホテルにチェックインして",
        "titleJp": "出張でビジネスホテルにチェックインして",
        "titleEn": "Checking into a business hotel on a work trip",
        "titleZh": "出差入住商务酒店",
        "titleRuby": [],
        "segments": [
            (
                "地方の取引先へ行くため、前泊で駅近のビジネスホテルを取っていた。",
                "For a client visit out of town, I'd booked a business hotel near the station the night before.",
                "要去外地见客户，提前订了车站附近的商务酒店过夜。",
            ),
            (
                "フロントには小さな荷物しか持たずに並び、予約名を告げた。",
                "I lined up at the front desk with only a small bag and gave my reservation name.",
                "只拎小包在前台排队，报了预约姓名。",
            ),
            (
                "身分証の提示を求められ、免許証をスライドして渡した。",
                "They asked for ID; I slid my license across.",
                "要出示证件，把驾照递过去。",
            ),
            (
                "部屋は禁煙のシングルで、朝食付きかどうかを確認された。",
                "The room was a non-smoking single; they confirmed whether breakfast was included.",
                "房间是无烟单人间，对方确认是否含早餐。",
            ),
            (
                "朝はバイキングだが、開始が六時半からだと聞いて安心した。",
                "Breakfast was a buffet starting at 6:30, which sounded fine.",
                "早餐是自助，听说六点半开始，放心了。",
            ),
            (
                "カードキーを受け取り、エレベーターで三階へ上がった。",
                "I took the card key and rode the elevator to the third floor.",
                "拿了房卡乘电梯上三楼。",
            ),
            (
                "部屋はコンパクトだったが、デスクの明るさとWi-Fiの貼り紙が仕事向きだった。",
                "The room was compact, but the desk light and Wi-Fi notice felt work-friendly.",
                "房间不大，但台灯亮度和 Wi‑Fi 说明很适合干活。",
            ),
            (
                "浴槽は浅めで、長湯よりさっと温まる用途だと分かった。",
                "The tub was shallow—better for a quick warm-up than a long soak.",
                "浴缸偏浅，适合泡一下暖身而不是久泡。",
            ),
            (
                "夜、薄いカーテン越しに街の灯りが入り、どこにでもある旅先の夜の匂いがした。",
                "At night, city light seeped through thin curtains— that anywhere-on-a-trip feeling.",
                "夜里薄窗帘透进街灯，有那种到哪都一样的出差夜晚感。",
            ),
            (
                "翌朝、混み合う前に食堂へ行き、味噌汁で胃を整えて会議へ向かった。",
                "Next morning I hit the dining hall before the rush, settled my stomach with miso soup, and headed to the meeting.",
                "第二天早上赶在人多前进餐厅，用味噌汤垫胃去开会。",
            ),
        ],
    },
    {
        "id": "n3-hotel-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "フロントでチェックイン",
        "titleJp": "フロントでチェックイン",
        "titleEn": "Checking in at the front desk",
        "titleZh": "在前台办理入住",
        "titleRuby": [],
        "sections": [
            section(
                "予約確認",
                "Reservation check",
                "确认预约",
                "🏨",
                [
                    (
                        "B",
                        "こんばんは。山田で予約しているのですが。",
                        "Good evening. I have a reservation under Yamada.",
                        "晚上好，我姓山田，有预约。",
                    ),
                    (
                        "A",
                        "山田様、ご来館ありがとうございます。おひとり様でいらっしゃいますね。",
                        "Mr./Ms. Yamada, thank you for staying with us. Just one guest, correct?",
                        "山田先生，欢迎入住。一位入住对吗？",
                    ),
                    (
                        "B",
                        "はい、シングル禁煙、朝食付きのプランです。",
                        "Yes, non-smoking single with breakfast.",
                        "对，无烟单人间含早餐。",
                    ),
                ],
            ),
            section(
                "手続き",
                "Procedure",
                "手续",
                "🪪",
                [
                    (
                        "A",
                        "ありがとうございます。身分証明書を一件お願いいたします。",
                        "Thank you. May I see one form of ID, please?",
                        "谢谢。请出示一种身份证件。",
                    ),
                    (
                        "B",
                        "はい、免許証です。チェックアウトは十一時でよかったでしょうか。",
                        "Here's my license. Checkout is at eleven, right?",
                        "给，驾照。退房是十一点对吧？",
                    ),
                    (
                        "A",
                        "はい、十一時です。延長をご希望の場合は、空室状況を確認のうえご案内いたします。",
                        "Yes, eleven o'clock. If you need a late checkout, we'll check availability.",
                        "是的，十一点。若要延迟退房我们会视空房情况安排。",
                    ),
                ],
            ),
            section(
                "案内",
                "Directions",
                "说明",
                "🔑",
                [
                    (
                        "A",
                        "こちらがカードキーでございます。朝食会場は一階レストラン、六時半オープンです。",
                        "Here is your card key. Breakfast is on the first floor; the restaurant opens at 6:30.",
                        "这是房卡。早餐在一楼餐厅，六点半开。",
                    ),
                    (
                        "B",
                        "分かりました。荷物はこのまま部屋へ持ち込んで大丈夫ですか。",
                        "Understood. Can I take my bags straight to the room?",
                        "好的。行李可以直接带进房间吗？",
                    ),
                    (
                        "A",
                        "はい、どうぞ。お疲れのところ、お気をつけてお上がりください。",
                        "Yes, please go ahead. You must be tired—please take care on your way up.",
                        "可以，请便。您辛苦了，上楼请小心。",
                    ),
                ],
            ),
        ],
    },
    # --- 実家への電話 ---
    {
        "id": "n3-family-phone-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "母に電話して、近況を話した夜",
        "titleJp": "母に電話して、近況を話した夜",
        "titleEn": "The night I called my mother and caught up",
        "titleZh": "晚上给妈妈打电话聊近况",
        "titleRuby": [],
        "segments": [
            (
                "週末でもないのに、ふと実家の母の声が聞きたくなった。",
                "Even though it wasn't the weekend, I suddenly wanted to hear my mom's voice.",
                "不是周末，却突然想听老家妈妈的声音。",
            ),
            (
                "仕事が一段落した九時ごろにかけたら、すぐに出て「どうしたの」と言われた。",
                "I called around nine when work had settled; she picked up right away and said, \"What's wrong?\"",
                "九点工作告一段落打过去，她马上接起来问「怎么了」。",
            ),
            (
                "別に用件はない、元気にしてるかなと思って、と正直に言うと笑われた。",
                'When I said honestly, "No real reason—I just wondered how you were," she laughed.',
                "老实说「没什么事，就想问你好吗」，她笑了。",
            ),
            (
                "最近の仕事は忙しいが楽しい、食事はだいたい自分で作っていると伝えた。",
                "I told her work had been busy but fun, and I mostly cooked for myself.",
                "说最近工作忙但开心，饭大体自己做。",
            ),
            (
                "母は「野菜は足りてる？」と決まって聞いてくる。",
                'My mother always asks, "Are you eating enough vegetables?"',
                "妈妈照例问「蔬菜够吗」。",
            ),
            (
                "冷凍のミックス野菜を常備している話をすると、少し安心したような返事が返ってきた。",
                "When I mentioned keeping frozen mixed vegetables on hand, she sounded a little relieved.",
                "说常备冷冻混合菜，她听起来放心了点。",
            ),
            (
                "父は早く寝たらしく、代わりに出てきて一言だけ「体に気をつけろ」と言った。",
                "Dad had apparently gone to bed early; he came on for one line: \"Take care of yourself.\"",
                "爸爸好像早睡，接过来只说了一句「注意身体」。",
            ),
            (
                "故郷の天気はまだ暑いとのことで、エアコンの話で盛り上がった。",
                "They said it was still hot back home, and we got into a chat about air conditioning.",
                "说老家还热，聊了几句空调。",
            ),
            (
                "長電話になりそうだったので、そろそろ切るねと言うと、向こうから先に謝られた。",
                "When I said I should hang up before it turned into a long call, they apologized first.",
                "我说快别打太长了，对方反倒先道歉。",
            ),
            (
                "電話を切ったあと、静かな部屋に戻っても、なぜか胸のあたりが温かかった。",
                "After hanging up, even back in my quiet room, my chest felt oddly warm.",
                "挂电话回到安静的房间，胸口却莫名暖暖的。",
            ),
        ],
    },
    {
        "id": "n3-family-phone-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "実家の母と電話で",
        "titleJp": "実家の母と電話で",
        "titleEn": "On the phone with Mom back home",
        "titleZh": "和在老家的妈妈通电话",
        "titleRuby": [],
        "sections": [
            section(
                "出だし",
                "Opening",
                "开头",
                "📱",
                [
                    (
                        "B",
                        "もしもし、母？今、話して大丈夫？",
                        "Hello, Mom? Is it okay to talk now?",
                        "喂，妈？现在方便聊吗？",
                    ),
                    (
                        "A",
                        "もちろん。どうしたの、そんな時間に。",
                        "Of course. What's up at this hour?",
                        "当然。这个点打来怎么了？",
                    ),
                    (
                        "B",
                        "別に悪いことじゃないよ。なんとなく声が聞きたくて。",
                        "Nothing bad. I just felt like hearing your voice.",
                        "没什么事。就是想听听你声音。",
                    ),
                ],
            ),
            section(
                "近況",
                "Catching up",
                "近况",
                "💬",
                [
                    (
                        "A",
                        "そっか。仕事はどう？無理してない？",
                        "I see. How's work? You're not overdoing it?",
                        "这样啊。工作怎么样？没勉强自己吧？",
                    ),
                    (
                        "B",
                        "忙しいけど、チームの人もいいし、なんとかなってる。残業は週に二日くらい。",
                        "Busy, but the team is nice—managing. Overtime maybe twice a week.",
                        "忙，但同事人不错，还能撑。加班一周大概两天。",
                    ),
                    (
                        "A",
                        "そう。ご飯はちゃんと食べてる？",
                        "Okay. Are you eating proper meals?",
                        "哦。饭有好好吃吗？",
                    ),
                    (
                        "B",
                        "うん、週末に作り置きして、平日は温めて食べてる。",
                        "Yeah, I meal-prep on weekends and reheat on weekdays.",
                        "嗯，周末做好冷藏，平日热一下吃。",
                    ),
                ],
            ),
            section(
                "締め",
                "Closing",
                "收尾",
                "🌙",
                [
                    (
                        "A",
                        "分かった。体調崩したらすぐ連絡しなさいよ。",
                        "Got it. Call right away if you feel unwell.",
                        "知道了。身体不舒服马上打电话啊。",
                    ),
                    (
                        "B",
                        "うん、ありがとう。また近いうちにかけるね。",
                        "Yeah, thanks. I'll call again soon.",
                        "嗯，谢谢。过阵子再打。",
                    ),
                    (
                        "A",
                        "待ってるから。おやすみ。",
                        "I'll be here. Good night.",
                        "我等着。晚安。",
                    ),
                ],
            ),
        ],
    },
    # --- カフェ ---
    {
        "id": "n4-cafe-work-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "カフェの角の席で資料を読む午後",
        "titleJp": "カフェの角の席で資料を読む午後",
        "titleEn": "An afternoon reading materials at a corner cafe table",
        "titleZh": "午后在咖啡馆角落座位看资料",
        "titleRuby": [],
        "segments": [
            (
                "在宅と出社のあいだを行き来するようになって、集中したいときだけカフェを借りることが増えた。",
                "Switching between remote and office work, I more often \"borrow\" a cafe only when I need to focus.",
                "远程和坐班换来换去之后，想专心时就更常去咖啡馆待着。",
            ),
            (
                "角の壁際の席は電源があり、半日いても罪悪感が少ない。",
                "The corner wall seat has an outlet, so even a half-day stay feels less guilty.",
                "靠墙角落有插座，待半天也没那么内疚。",
            ),
            (
                "最初にドリンクを注文し、二杯目からはおかわり割引になる店だった。",
                "First you order a drink; from the second cup there was a refill discount.",
                "先点一杯，第二杯起有续杯折扣。",
            ),
            (
                "イヤホンで落ち着いた音楽を流し、PDFを縦スクロールしながら読み進めた。",
                "I played calm music on headphones and scrolled through a PDF.",
                "耳机里放轻音乐，竖着划 PDF 往下读。",
            ),
            (
                "隣の人がオンライン会議をしていて、自分のマイクは必ずミュートにした。",
                "The next table was on a video call; I kept my mic muted.",
                "邻桌在开在线会，我把麦克风一直静音。",
            ),
            (
                "おかわりを取りに立つタイミングで、ストレッチも兼ねて背筋を伸ばした。",
                "When I got up for a refill, I stretched and straightened my back.",
                "起来续杯时顺便伸个懒腰。",
            ),
            (
                "カップの底に残った氷がカラカラ鳴り、そろそろ帰る頃だと知らせていた。",
                "Ice clinking at the bottom of the cup told me it was time to head home.",
                "杯底冰块哐当响，像在提醒该走了。",
            ),
            (
                "会計のあと、店員に「お世話になりました」と言うと、笑顔で頭を下げてくれた。",
                'After paying, when I said, "Thanks for having me," the staff smiled and bowed.',
                "结账时说「打扰了」，店员笑着点头。",
            ),
            (
                "外に出ると日が傾き、画面にばかり向いていた目が少し楽になった。",
                "Outside, the sun was lower; my screen-tired eyes felt a bit better.",
                "出门太阳偏西，盯屏幕盯累的眼睛轻松了点。",
            ),
        ],
    },
    {
        "id": "n4-cafe-work-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "カフェで注文とおかわり",
        "titleJp": "カフェで注文とおかわり",
        "titleEn": "Ordering and a refill at a cafe",
        "titleZh": "在咖啡馆点单与续杯",
        "titleRuby": [],
        "sections": [
            section(
                "初注文",
                "First order",
                "第一次点单",
                "☕",
                [
                    (
                        "A",
                        "いらっしゃいませ。店内でお召し上がりですか。",
                        "Welcome. Will you be staying in?",
                        "欢迎光临。堂食吗？",
                    ),
                    (
                        "B",
                        "はい。角の席、電源使ってもいいですか。",
                        "Yes. May I use the outlet at the corner seat?",
                        "嗯。角落座位可以用电源吗？",
                    ),
                    (
                        "A",
                        "はい、壁側のブースでしたらご利用いただけます。ドリンクはいかがですか。",
                        "Yes, you can use them at the wall-side booths. What would you like to drink?",
                        "可以，靠墙卡座都能用。要喝点什么？",
                    ),
                    (
                        "B",
                        "アイスカフェラテのミディアムをお願いします。砂糖はなしで。",
                        "Iced cafe latte, medium, please. No sugar.",
                        "冰拿铁中杯。不加糖。",
                    ),
                ],
            ),
            section(
                "おかわり",
                "Refill",
                "续杯",
                "🧊",
                [
                    (
                        "B",
                        "すみません、おかわりお願いします。ホットのアメリカーノに変えてもいいですか。",
                        "Excuse me, a refill please. Can I switch to a hot Americano?",
                        "不好意思，续杯。可以改成热美式吗？",
                    ),
                    (
                        "A",
                        "かしこまりました。おかわりは五十円引きになりますね。お席までお持ちします。",
                        "Certainly. Refills are fifty yen off. I'll bring it to your seat.",
                        "好的。续杯减五十日元。给您送到座位。",
                    ),
                    (
                        "B",
                        "ありがとうございます。あと一時間ほど居ても大丈夫ですか。",
                        "Thanks. Is it okay if I stay about another hour?",
                        "谢谢。再待一小时左右可以吗？",
                    ),
                    (
                        "A",
                        "はい、ラッシュ前でしたら大丈夫です。混み始めたら一声おかけください。",
                        "Yes, as long as it's before the rush. If it gets crowded, please let us know.",
                        "可以，高峰前没问题。若开始挤了请跟我们说一声。",
                    ),
                ],
            ),
            section(
                "会計",
                "Paying",
                "结账",
                "💴",
                [
                    (
                        "B",
                        "お会計お願いします。",
                        "Check, please.",
                        "买单。",
                    ),
                    (
                        "A",
                        "ありがとうございました。またのご来店お待ちしております。",
                        "Thank you. We hope to see you again.",
                        "谢谢惠顾。欢迎再来。",
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
