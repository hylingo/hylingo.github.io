#!/usr/bin/env python3
"""
batch4 → public/data/ja_articles.json（用户选定场景）

2 コインランドリー / 3 映画館 / 7 国内線空港 / 13 歯科検診 / 14 眼科・コンタクト / 15 神社・御朱印 / 16 区民プール・体育館

运行: .venv/bin/python scripts/append_ja_articles_batch4.py
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
    # --- コインランドリー ---
    {
        "id": "n4-laundromat-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "初めて一人でコインランドリーに行った夜",
        "titleJp": "初めて一人でコインランドリーに行った夜",
        "titleEn": "The first night I went to the coin laundry alone",
        "titleZh": "第一次晚上独自去自助洗衣店",
        "titleRuby": [],
        "segments": [
            (
                "布団カバーとタオルがかさばり、家の洗濯機では回しきれなくなった。",
                "Duvet covers and towels had piled up; the home washer couldn't handle it.",
                "被套和毛巾堆太多，家用洗衣机洗不下了。",
            ),
            (
                "駅から歩いて三分の店は、ガラス越しに洗濯機の列が見えた。",
                "The shop three minutes from the station showed a row of machines through the glass.",
                "从车站走三分钟的店，透过玻璃能看到一排洗衣机。",
            ),
            (
                "両替機に千円札を入れると、百円玉が勢いよく落ちてきた。",
                "I fed a 1,000-yen bill into the changer; 100-yen coins clattered out.",
                "把千元钞塞进换币机，百元硬币哗啦啦掉下来。",
            ),
            (
                "洗剤は自動投入の機械を選び、コースは標準にした。",
                "I picked a machine with auto detergent and chose the standard course.",
                "选了自动加洗衣液的机器，程序用标准档。",
            ),
            (
                "ドラムの中に服を押し込み、扉を閉めるとロック音がした。",
                "I stuffed the laundry in, closed the door, and heard it lock.",
                "把衣服塞进滚筒，关门时咔哒一声锁上。",
            ),
            (
                "残り時間を見ながらスマホをいじっていたら、隣の人に「乾燥は上ですよ」と教えられた。",
                'While killing time on my phone, the person next to me said, "Dryers are upstairs."',
                "刷手机等时间，旁边有人告诉我「烘干在上面」。",
            ),
            (
                "乾燥機は高温にすると縮むと聞いたことがあり、中温で四十分にセットした。",
                "I'd heard high heat can shrink clothes, so I set medium for forty minutes.",
                "听说高温会缩水，设成中温四十分钟。",
            ),
            (
                "ふわっと温かいタオルを畳むと、洗濯物が終わった実感が湧いた。",
                "Folding warm fluffy towels, I really felt the laundry was done.",
                "叠起松软温热的毛巾，才觉得洗衣真的结束了。",
            ),
            (
                "最後にゴミを捨て、床に落ちた糸くずだけ拾って帰った。",
                "I threw away trash, picked up a bit of lint on the floor, and left.",
                "最后扔了垃圾，捡起地上一点线头就走了。",
            ),
        ],
    },
    {
        "id": "n4-laundromat-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "コインランドリーで店員に聞く",
        "titleJp": "コインランドリーで店員に聞く",
        "titleEn": "Asking staff at the coin laundry",
        "titleZh": "在自助洗衣店问店员",
        "titleRuby": [],
        "sections": [
            section(
                "使い方",
                "How to use",
                "用法",
                "🧺",
                [
                    (
                        "B",
                        "すみません、初めてなんですが、この洗濯機、洗剤はどこに入れますか。",
                        "Excuse me, it's my first time—where does detergent go in this washer?",
                        "不好意思，第一次来，这台洗衣机洗衣液倒哪里？",
                    ),
                    (
                        "A",
                        "それは自動投入タイプなので、ここにコインを入れてスタートだけで大丈夫です。",
                        "That one's auto-dose, so just put in coins and press start.",
                        "那台是自动投放的，投币按开始就行。",
                    ),
                    (
                        "B",
                        "四十分コースで十分ですか。毛布一枚なんですが。",
                        "Is the forty-minute course enough? It's one blanket.",
                        "四十分钟够吗？是一条毛毯。",
                    ),
                    (
                        "A",
                        "かさばりますね。六十分の方が安心だと思います。乾燥は二階ですよ。",
                        "It's bulky. I'd go with sixty minutes. Dryers are on the second floor.",
                        "比较厚。六十分钟更稳妥。烘干在二楼。",
                    ),
                ],
            ),
            section(
                "乾燥",
                "Drying",
                "烘干",
                "🌪️",
                [
                    (
                        "B",
                        "乾燥機、百円で何分回りますか。",
                        "How many minutes per 100 yen on the dryer?",
                        "烘干机一百日元能转几分钟？",
                    ),
                    (
                        "A",
                        "百円で十分です。足りなければ追加で入れてください。",
                        "Ten minutes per 100 yen. Add more coins if you need longer.",
                        "一百日元十分钟。不够再投币。",
                    ),
                    (
                        "B",
                        "服を取り忘れないように、アラームセットしておきます。",
                        "I'll set an alarm so I don't forget my clothes.",
                        "我设个闹钟免得忘拿衣服。",
                    ),
                    (
                        "A",
                        "いいですね。閉店は二十三時なので、それまでに乾燥も終わらせてくださいね。",
                        "Good idea. We close at eleven, so please finish drying by then.",
                        "好主意。我们十一点关门，请在这之前烘干完。",
                    ),
                ],
            ),
        ],
    },
    # --- 映画館 ---
    {
        "id": "n4-cinema-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "平日割引で映画を見に行った",
        "titleJp": "平日割引で映画を見に行った",
        "titleEn": "I went to see a movie on a weekday discount",
        "titleZh": "用平日折扣去看了电影",
        "titleRuby": [],
        "segments": [
            (
                "気になっていた作品が、平日の昼割で安くなっているのをアプリで見つけた。",
                "On the app I found a film I'd wanted to see cheaper on a weekday matinee.",
                "在 App 上看到想看的片平日白天有折扣。",
            ),
            (
                "当日、QRコードをかざして発券し、ロビーに入った。",
                "That day I scanned a QR code for my ticket and entered the lobby.",
                "当天扫二维码取票进了大厅。",
            ),
            (
                "ポップコーンの列が長く、上映十五分前に並び直した。",
                "The popcorn line was long; I got back in line fifteen minutes before showtime.",
                "爆米花队很长，开演前十五分钟又去排。",
            ),
            (
                "塩味のSサイズと、小さめの飲み物のセットにした。",
                "I got a small salted popcorn and a small drink set.",
                "点了小份咸爆米花加小杯饮料套餐。",
            ),
            (
                "客席は真ん中よりやや前で、首が疲れない位置だった。",
                "My seat was slightly forward of center—easy on the neck.",
                "座位比正中间稍靠前，脖子不累。",
            ),
            (
                "予告編が三本作続けて流れ、観客のざわめきが少しずつ静かになった。",
                "Three trailers played in a row and the audience slowly quieted.",
                "连着放了三个预告，观众渐渐静下来。",
            ),
            (
                "本編が始まると、スマホは必ずマナーモードにしていた。",
                "When the feature started, my phone was already on silent.",
                "正片开始手机早就静音了。",
            ),
            (
                "字幕に引っ張られすぎないよう、一度目は日本語だけを追った。",
                "To avoid clinging to subtitles, the first time through I followed only the Japanese.",
                "怕太依赖字幕，第一遍只跟日语。",
            ),
            (
                "終わったあと、エンドロールの音楽が残り香のように耳に残った。",
                "After it ended, the end-credit music lingered like an aftertaste.",
                "散场后片尾音乐像余味一样留在耳边。",
            ),
        ],
    },
    {
        "id": "n4-cinema-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "映画館の窓口で",
        "titleJp": "映画館の窓口で",
        "titleEn": "At the movie theater box office",
        "titleZh": "在电影院售票处",
        "titleRuby": [],
        "sections": [
            section(
                "チケット",
                "Tickets",
                "票",
                "🎬",
                [
                    (
                        "B",
                        "すみません、十八時十分からの「海辺の町」、まだ空いてますか。",
                        'Excuse me, is "The Seaside Town" at 6:10 p.m. still available?',
                        "请问六点十分的《海边小镇》还有票吗？",
                    ),
                    (
                        "A",
                        "はい、後ろの方の席がございます。一般で千八百円です。",
                        "Yes, we have seats toward the back. General admission is 1,800 yen.",
                        "有，后排还有。全价一千八百日元。",
                    ),
                    (
                        "B",
                        "平日割引は使えますか。アプリのクーポンです。",
                        "Can I use the weekday discount? It's an app coupon.",
                        "能用平日折扣吗？App 上的券。",
                    ),
                    (
                        "A",
                        "かしこまりました。こちらをご提示ください。千四百円になります。",
                        "Certainly. Please show this screen. That will be 1,400 yen.",
                        "好的。请出示这个画面。一千四百日元。",
                    ),
                ],
            ),
            section(
                "座席と注意",
                "Seating and notices",
                "座位与须知",
                "🍿",
                [
                    (
                        "B",
                        "座席は自分で選べますか。",
                        "Can I choose my seat?",
                        "座位可以自己选吗？",
                    ),
                    (
                        "A",
                        "はい、この画面で空いている席をタップしてください。通路側がよろしいですか。",
                        "Yes, tap an open seat on this screen. Would you like an aisle seat?",
                        "可以，在屏幕上点空位。要靠过道吗？",
                    ),
                    (
                        "B",
                        "お願いします。あと、ポップコーンは別ですか。",
                        "Yes, please. Is popcorn separate?",
                        "要。爆米花另外买吗？",
                    ),
                    (
                        "A",
                        "はい、売店でお並びください。上映は十七時五十分から入場できます。",
                        "Yes, please line up at the concession. You may enter from 5:50 p.m.",
                        "是的，请在小卖部排队。五点五十可以进场。",
                    ),
                ],
            ),
        ],
    },
    # --- 国内線空港 ---
    {
        "id": "n3-airport-domestic-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "国内線で福岡へ行く朝",
        "titleJp": "国内線で福岡へ行く朝",
        "titleEn": "A morning flight to Fukuoka on a domestic line",
        "titleZh": "乘国内线去福冈的早晨",
        "titleRuby": [],
        "segments": [
            (
                "朝早めに空港に着き、まずモニターで航空会社とカウンターを確認した。",
                "I arrived at the airport early and first checked the airline and counter on the monitor.",
                "一早到机场，先在屏幕上确认航空公司和柜台。",
            ),
            (
                "預け荷物は一つだけにして、機内持ち込みはリュックにまとめた。",
                "I had only one checked bag and put carry-on items in my backpack.",
                "托运只带一件，随身物品塞进双肩包。",
            ),
            (
                "セルフチェックイン端末で搭乗券を発行し、長い列を避けられた。",
                "I printed my boarding pass at a self check-in kiosk and skipped the long line.",
                "在自助值机打了登机牌，躲开了长队。",
            ),
            (
                "保安検査の前に飲み物を飲み干すのを忘れず、ペットボトルを空にした。",
                "Before security I remembered to finish my drink and emptied the bottle.",
                "安检前记得把饮料喝完，塑料瓶倒空。",
            ),
            (
                "ベルトと腕時計をトレーに乗せ、人混みの中をゆっくり進んだ。",
                "I put my belt and watch on the tray and moved slowly through the crowd.",
                "腰带手表放进托盘，在人群里慢慢往前挪。",
            ),
            (
                "搭乗口に着くと、まだ「搭乗開始前」と表示されていて、椅子に腰を下ろした。",
                "At the gate it still said \"Boarding not yet begun,\" so I sat down.",
                "到登机口还显示「尚未开始登机」，先坐下。",
            ),
            (
                "アナウンスで優先搭乗のあと一般が呼ばれ、列に並んだ。",
                "After priority boarding was called for general boarding, I joined the line.",
                "广播先优先登机再一般登机，我排队。",
            ),
            (
                "座席は通路側で、離陸のあと少し耳が詰まった。",
                "My seat was on the aisle; after takeoff my ears felt a bit blocked.",
                "座位靠过道，起飞后耳朵有点闷。",
            ),
            (
                "雲の上に出ると、窓の外がまぶしくてサンシェードを下ろした。",
                "Above the clouds the window glare was bright, so I lowered the shade.",
                "飞到云上窗外刺眼，拉下了遮阳板。",
            ),
            (
                "着陸直前、係員がシートベルト着用を英語と日本語で告げた。",
                "Just before landing, the crew announced seat belts in English and Japanese.",
                "降落前乘务员用日英双语提醒系好安全带。",
            ),
        ],
    },
    {
        "id": "n3-airport-domestic-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "空港のカウンターで預け荷物",
        "titleJp": "空港のカウンターで預け荷物",
        "titleEn": "Checking a bag at the airport counter",
        "titleZh": "在机场柜台托运行李",
        "titleRuby": [],
        "sections": [
            section(
                "手続き",
                "Procedure",
                "手续",
                "✈️",
                [
                    (
                        "B",
                        "こんにちは。福岡行きの〇〇航空、搭乗手続きをお願いします。",
                        "Hello. I'd like to check in for flight OO to Fukuoka, please.",
                        "你好。办去福冈的〇〇航空登机手续。",
                    ),
                    (
                        "A",
                        "ありがとうございます。パスポートまたは身分証をお願いいたします。",
                        "Thank you. May I see your passport or ID?",
                        "谢谢。请出示护照或身份证件。",
                    ),
                    (
                        "B",
                        "はい、運転免許証です。預け荷物はこのスーツケース一つです。",
                        "Here's my driver's license. One suitcase to check.",
                        "给，驾照。托运行李就这一件行李箱。",
                    ),
                    (
                        "A",
                        "かしこまりました。中に電池やライターはお入りですか。",
                        "Understood. Any batteries or lighters inside?",
                        "好的。里面有电池或打火机吗？",
                    ),
                ],
            ),
            section(
                "制限品",
                "Restricted items",
                "限制物品",
                "🧳",
                [
                    (
                        "B",
                        "ノートパソコンは機内持ち込みにします。",
                        "I'll carry my laptop on board.",
                        "笔记本电脑我随身带。",
                    ),
                    (
                        "A",
                        "ありがとうございます。お荷物は二十三キロまで無料です。こちらが預り票です。",
                        "Thank you. Baggage is free up to 23 kg. Here is your claim tag.",
                        "谢谢。行李二十三公斤以内免费。这是托运条。",
                    ),
                    (
                        "B",
                        "搭乗口は何番でしょうか。",
                        "Which gate is it?",
                        "登机口是几号？",
                    ),
                    (
                        "A",
                        "ただいま十二番です。変更があればアナウンスいたします。保安検査はお早めにお願いします。",
                        "It's gate twelve for now. We'll announce any changes. Please go through security early.",
                        "目前是十二号。若有变更会广播。请尽早过安检。",
                    ),
                ],
            ),
        ],
    },
    # --- 歯科 ---
    {
        "id": "n4-dental-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "半年ぶりの歯のクリーニング",
        "titleJp": "半年ぶりの歯のクリーニング",
        "titleEn": "A teeth cleaning after six months",
        "titleZh": "时隔半年的洗牙",
        "titleRuby": [],
        "segments": [
            (
                "健康保険が使える歯科医院を選び、前日にネットで予約を入れた。",
                "I picked a dental clinic that takes health insurance and booked online the day before.",
                "选了能用医保的牙科，前一天网上预约。",
            ),
            (
                "受付で保険証を出すと、問診票に「前回から変わった薬はありますか」とあった。",
                "At reception I showed my insurance card; the form asked if any medications had changed.",
                "在接待处出示保险证，问诊表问「上次以来药物有无变化」。",
            ),
            (
                "診療室の椅子に寝かされ、鏡で口の中を見せてもらいながら説明を聞いた。",
                "Reclined in the chair, I listened to explanations while they showed my mouth in a mirror.",
                "躺在诊疗椅上，对着镜子听讲解。",
            ),
            (
                "スケーラーの音がジーと鳴り、歯石が取れていく感触が不思議だった。",
                "The scaler buzzed; the feeling of tartar coming off was odd.",
                "洁牙器嗡嗡响，牙结石被刮掉的感觉很奇妙。",
            ),
            (
                "歯茎から少し血が出たが、問題ない範囲だと言われた。",
                "A little blood from the gums, but they said it was within normal range.",
                "牙龈有点出血，说在正常范围。",
            ),
            (
                "磨き残しが多いのは奥歯の裏だと指摘され、ブラシの当て方を実演してもらった。",
                "They said I miss the backs of molars most and demonstrated how to angle the brush.",
                "指出大牙内侧刷得不够，示范了牙刷角度。",
            ),
            (
                "フッ素のジェルを塗られ、しばらくうがいは控えるよう言われた。",
                "Fluoride gel was applied; I was told not to rinse for a while.",
                "涂了含氟凝胶，说暂时别漱口。",
            ),
            (
                "会計は窓口で三分の一負担で済み、次は半年後の予約を取った。",
                "I paid my 30% share at the counter and made the next appointment in six months.",
                "柜台付三成，约了半年后。",
            ),
            (
                "舌で歯をなぞると、さっきまでと違うつるつる感が気持ちよかった。",
                "Running my tongue over my teeth, the new smoothness felt good.",
                "用舌头舔牙齿，滑溜溜的触感很舒服。",
            ),
        ],
    },
    {
        "id": "n4-dental-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "歯科衛生士さんと（クリーニング）",
        "titleJp": "歯科衛生士さんと（クリーニング）",
        "titleEn": "With the dental hygienist (cleaning)",
        "titleZh": "与牙科卫生士（洗牙）",
        "titleRuby": [],
        "sections": [
            section(
                "始まり",
                "Starting",
                "开始",
                "🦷",
                [
                    (
                        "A",
                        "では、今日はクリーニングですね。痛いところがあったら手を挙げてくださいね。",
                        "Today we're doing a cleaning. Raise your hand if anything hurts.",
                        "今天是洗牙。疼的话请举手。",
                    ),
                    (
                        "B",
                        "はい、わかりました。",
                        "Okay, I will.",
                        "好的，知道了。",
                    ),
                    (
                        "A",
                        "ここ、歯石が少し付いています。水、かけますよ。",
                        "There's a bit of tartar here. I'll spray some water.",
                        "这里有点牙结石。要喷水了。",
                    ),
                ],
            ),
            section(
                "アドバイス",
                "Advice",
                "建议",
                "✨",
                [
                    (
                        "A",
                        "仕上げました。磨き残しは右の奥歯の外側が多いです。こういうふうに当てると届きやすいです。",
                        "All done. You miss the outer side of the right molars most. Angling like this reaches better.",
                        "好了。右边大牙外侧刷得少。这样斜一点比较好刷到。",
                    ),
                    (
                        "B",
                        "気をつけます。フロスは毎日した方がいいですか。",
                        "I'll be careful. Should I floss every day?",
                        "我会注意。牙线要每天用吗？",
                    ),
                    (
                        "A",
                        "理想は毎日ですが、週に何回かでも効果があります。",
                        "Daily is ideal, but even a few times a week helps.",
                        "最好每天，一周几次也有用。",
                    ),
                    (
                        "B",
                        "ありがとうございます。次は半年後でよいですか。",
                        "Thank you. Should I come back in six months?",
                        "谢谢。下次还是半年后吗？",
                    ),
                    (
                        "A",
                        "はい、また先生の診察とセットで予約を取ってください。",
                        "Yes—please book together with the dentist's exam.",
                        "是的，请和医生检查一起预约。",
                    ),
                ],
            ),
        ],
    },
    # --- 眼科 ---
    {
        "id": "n4-eye-clinic-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "コンタクトの装用時間を相談しに",
        "titleJp": "コンタクトの装用時間を相談しに",
        "titleEn": "Visiting the eye clinic to ask about contact lens wear time",
        "titleZh": "去眼科咨询隐形眼镜佩戴时间",
        "titleRuby": [],
        "segments": [
            (
                "画面に長時間向く仕事が続き、夕方になると目が乾いてコンタクトが気になるようになった。",
                "Staring at screens all day, by evening my eyes felt dry and my contacts bothered me.",
                "长时间看屏幕的工作持续一阵，傍晚眼睛发干、隐形眼镜别扭。",
            ),
            (
                "眼科を検索し、コンタクト処方もしているクリニックに予約した。",
                "I searched for an eye clinic that prescribes contacts and made an appointment.",
                "搜了能开隐形眼镜处方的眼科并预约。",
            ),
            (
                "視力検査では、かな文字とランドルト環を交互に見せられた。",
                "During the vision test I alternated reading kana and Landolt C rings.",
                "查视力时交替看假名和兰氏环。",
            ),
            (
                "眼圧の測定は息を止めすぎないよう、軽くあごを乗せるだけで済んだ。",
                "For eye pressure I just rested my chin lightly without holding my breath too long.",
                "测眼压只需轻托下巴，不用憋太久气。",
            ),
            (
                "先生に症状を話すと、乾きやすいタイプのレンズや、滴眼液の種類の話が出た。",
                "When I described my symptoms, we discussed drier-eye-friendly lenses and types of eye drops.",
                "跟医生说完症状，聊到不易干的镜片和眼药水种类。",
            ),
            (
                "装用時間は八時間を目安にし、長引く日はメガネに切り替えるよう勧められた。",
                "They advised aiming for about eight hours of wear and switching to glasses on long days.",
                "建议佩戴以八小时为参考，长的日子改戴眼镜。",
            ),
            (
                "レンズを外す前に手を洗うことと、ケースの溶液は毎日取り換えることを念押しされた。",
                "They stressed washing hands before removing lenses and changing solution daily.",
                "强调摘镜前要洗手，镜盒护理液每天更换。",
            ),
            (
                "帰りに薬局で人工涙液を買い、デスクの引き出しに一本忍ばせた。",
                "On the way home I bought artificial tears and stashed a bottle in my desk drawer.",
                "回家路上在药妆店买了人工泪液，塞一瓶进抽屉。",
            ),
            (
                "目は我慢比べではないと、少し肩の力が抜けた気がした。",
                "Eyes aren't a contest of endurance—I felt my shoulders relax a little.",
                "觉得眼睛不是比谁更能扛，肩膀松了一点。",
            ),
        ],
    },
    {
        "id": "n4-eye-clinic-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "眼科の受付と診察",
        "titleJp": "眼科の受付と診察",
        "titleEn": "Reception and exam at the eye clinic",
        "titleZh": "眼科接待与看诊",
        "titleRuby": [],
        "sections": [
            section(
                "受付",
                "Reception",
                "接待",
                "👁️",
                [
                    (
                        "B",
                        "予約の山田です。コンタクトの相談と視力検査をお願いしたいです。",
                        "I have an appointment, Yamada. I'd like to consult about contacts and get a vision check.",
                        "预约的山田。想咨询隐形眼镜并查视力。",
                    ),
                    (
                        "A",
                        "ありがとうございます。保険証と、お持ちのコンタクトの処方箋はありますか。",
                        "Thank you. Your insurance card and any current contact lens prescription?",
                        "谢谢。保险证和现有的隐形眼镜处方有吗？",
                    ),
                    (
                        "B",
                        "処方箋は去年のものですが……。",
                        "I have one from last year...",
                        "处方是去年的……",
                    ),
                    (
                        "A",
                        "では本日、再検査のうえで処方を更新する場合があります。問診票に目の症状をご記入ください。",
                        "We may update your prescription after today's exam. Please note your eye symptoms on the form.",
                        "今天复查后可能会更新处方。请在问诊表填写眼部症状。",
                    ),
                ],
            ),
            section(
                "診察",
                "Exam",
                "看诊",
                "🔍",
                [
                    (
                        "A",
                        "目が乾くのはいつからですか。コンタクトは一日何時間くらいですか。",
                        "When did the dryness start? How many hours a day do you wear contacts?",
                        "眼睛发干从什么时候开始的？隐形眼镜一天戴几小时？",
                    ),
                    (
                        "B",
                        "ここ一か月、夕方からです。仕事中は十時間くらいつけています。",
                        "For the past month, from evening on. About ten hours during work.",
                        "这一个月，从傍晚开始。上班时大概戴十小时。",
                    ),
                    (
                        "A",
                        "わかりました。涙液が少なめですね。装用時間を短くするか、酸素透過性の高いレンズに変えましょう。",
                        "I see. Your tear film is a bit low. Shorten wear time or switch to higher-oxygen lenses.",
                        "明白了。泪液偏少。缩短佩戴时间或换成高透氧镜片吧。",
                    ),
                    (
                        "B",
                        "滴眼液は市販のでよいですか。",
                        "Are over-the-counter drops okay?",
                        "眼药水买市售的可以吗？",
                    ),
                    (
                        "A",
                        "防腐剤フリーのものを選んでください。処方のものも出せます。",
                        "Choose preservative-free drops. We can prescribe some as well.",
                        "选不含防腐剂的。也可以开处方眼药水。",
                    ),
                ],
            ),
        ],
    },
    # --- 神社 ---
    {
        "id": "n3-shrine-goshuin-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "初めて御朱印をいただいた日",
        "titleJp": "初めて御朱印をいただいた日",
        "titleEn": "The day I received a goshuin for the first time",
        "titleZh": "第一次领到御朱印的那天",
        "titleRuby": [],
        "segments": [
            (
                "友人に勧められ、近所の神社に御朱印帳を持って行った。",
                "A friend suggested I take a goshuin book to a nearby shrine.",
                "朋友推荐，带着朱印帐去了附近神社。",
            ),
            (
                "手水舎では、まず柄杓で左手、右手、口元と順番を間違えないようゆっくり行った。",
                "At the chozuya I slowly followed the order—left hand, right hand, mouth—so I wouldn't mix it up.",
                "在手水舍用柄杓先左后右再漱口，慢慢做怕顺序错。",
            ),
            (
                "本殿の前で二礼二拍手一礼をし、鐘は鳴らさず静かに祈った。",
                "Before the main hall I bowed twice, clapped twice, bowed once, and prayed quietly without ringing the bell.",
                "在本殿前二拜二拍手一拜，没敲钟静静祈祷。",
            ),
            (
                "社務所の小さな窓口には「御朱印」と書かれた札がかかっていた。",
                "A small shrine office window had a sign reading \"Goshuin.\"",
                "社务所小窗口挂着写「御朱印」的牌子。",
            ),
            (
                "朱印帳を差し出すと、書き手の人が日付と社名を墨で書き始めた。",
                "When I handed over my book, the scribe began brushing the date and shrine name in ink.",
                "递上朱印帐，书写的人开始用墨写日期和社名。",
            ),
            (
                "直書きは数分かかり、そのあいだ他の参拝客も静かに列をなしていた。",
                "Direct stamping and calligraphy took a few minutes; other visitors waited quietly in line.",
                "直书要几分钟，期间其他参拜者静静排队。",
            ),
            (
                "出来上がった印は、思ったより力強くて、紙に少しにじみがあるのが味だった。",
                "The finished seal was bolder than I'd expected; slight bleed on the paper felt like character.",
                "成品比想象有力，纸上略晕开反而有味道。",
            ),
            (
                "お守りの棚では、健康守と交通安全守が並び、説明を読んでから一つ選んだ。",
                "On the omamori shelf were health and traffic-safety charms; I read the labels and chose one.",
                "御守架子上有健康守和交通安全守，看完说明选了一个。",
            ),
            (
                "帰り道、朱印帳を開いて何度も見返し、旅の記録にも似た満足感があった。",
                "Walking home I opened the book again and again; it felt like a travel log's satisfaction.",
                "回家路上反复翻开朱印帐，有点像旅行记录的满足感。",
            ),
        ],
    },
    {
        "id": "n3-shrine-goshuin-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "神社の社務所で",
        "titleJp": "神社の社務所で",
        "titleEn": "At the shrine office window",
        "titleZh": "在神社社务所",
        "titleRuby": [],
        "sections": [
            section(
                "御朱印",
                "Goshuin",
                "御朱印",
                "⛩️",
                [
                    (
                        "B",
                        "すみません、御朱印をお願いしたいのですが。",
                        "Excuse me, I'd like a goshuin, please.",
                        "你好，想求御朱印。",
                    ),
                    (
                        "A",
                        "ありがとうございます。朱印帳はお持ちですか。それとも紙でのお渡しにしますか。",
                        "Thank you. Do you have a goshuin book, or would you like it on a loose sheet?",
                        "谢谢。带朱印帐了吗？还是要写在单张纸上？",
                    ),
                    (
                        "B",
                        "朱印帳があります。直書きをお願いします。",
                        "I have a book. Direct writing, please.",
                        "带了。请直书。",
                    ),
                    (
                        "A",
                        "かしこまりました。三百円になります。少々お待ちください。",
                        "Certainly. That will be 300 yen. One moment, please.",
                        "好的。三百日元。请稍等。",
                    ),
                ],
            ),
            section(
                "お守り",
                "Omamori",
                "御守",
                "🎋",
                [
                    (
                        "B",
                        "あと、お守りは健康と仕事運、どちらがよいでしょうか。",
                        "Also, for an omamori, health or work luck—which would be better?",
                        "还有御守，健康和事业运哪种比较好？",
                    ),
                    (
                        "A",
                        "どちらもご用意がございます。一年ほどお持ちいただき、あとお焚き上げにお戻しください。",
                        "We have both. Please keep it about a year, then return it for ritual burning.",
                        "两种都有。请佩戴一年左右，之后送回焚烧供养。",
                    ),
                    (
                        "B",
                        "分かりました。では健康守を一つお願いします。",
                        "Understood. I'll take one health charm, please.",
                        "明白了。那就要一个健康守。",
                    ),
                    (
                        "A",
                        "ありがとうございます。心を込めてお授けいたします。",
                        "Thank you. We offer it with our prayers.",
                        "谢谢。诚心为您授与。",
                    ),
                ],
            ),
        ],
    },
    # --- 区民プール ---
    {
        "id": "n4-sports-pool-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "区民プールで泳ぐ土曜の午後",
        "titleJp": "区民プールで泳ぐ土曜の午後",
        "titleEn": "Swimming at the public pool on a Saturday afternoon",
        "titleZh": "周六下午在区民泳池游泳",
        "titleRuby": [],
        "segments": [
            (
                "暑さが続く週末、区の体育館のプールが安いと聞いて初めて行ってみた。",
                "On a hot weekend I tried the ward sports-center pool for the first time—I'd heard it was cheap.",
                "酷暑周末听说区立体育馆泳池便宜，第一次去。",
            ),
            (
                "窓口で入館料を払い、リストバンド型の入場券を手首にはめた。",
                "I paid at the counter and wore a wristband-style ticket.",
                "窗口付入馆费，戴上腕带式入场券。",
            ),
            (
                "プール利用にはメッシュキャップが必須で、忘れずに百均で買っておいて正解だった。",
                "A mesh swim cap was required—buying one at the 100-yen shop beforehand was the right call.",
                "游泳必须戴网泳帽，提前在百元店买好对了。",
            ),
            (
                "更衣室はロッカーに百円玉が要り、鍵を回すとコインが返ってくるタイプだった。",
                "The locker needed a 100-yen coin; turning the key returned the coin.",
                "更衣室储物柜要投百元硬币，转钥匙会退回那种。",
            ),
            (
                "シャワーで体を流してからプールサイドへ出ると、子どもの授業と一般が区切られていた。",
                "After a shower I reached the poolside; kids' lessons and general swim were separated.",
                "淋浴后出来到池边，儿童课和一般泳区是分开的。",
            ),
            (
                "水は思ったより冷たく、足首からゆっくり慣らして入った。",
                "The water was colder than expected; I eased in from the ankles.",
                "水比想的凉，从脚踝慢慢适应。",
            ),
            (
                "クロールで何往復かすると、肩のこりが少しほどけた。",
                "A few laps of crawl loosened my shoulder tension a bit.",
                "自由泳几个来回，肩膀僵劲松了些。",
            ),
            (
                "休憩時間に笛が鳴り、全員プールから上がるルールだと知った。",
                "A whistle blew for break time—I learned everyone had to get out of the pool.",
                "休息哨一响，才知道要全员上岸。",
            ),
            (
                "帰りの自販機でスポーツドリンクを買い、夏の午後の消耗を取り戻した。",
                "I bought a sports drink from a vending machine on the way out and recovered from the summer afternoon drain.",
                "出门在自动贩卖机买运动饮料，补回夏日午后的消耗。",
            ),
        ],
    },
    {
        "id": "n4-sports-pool-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "区民プールの窓口で",
        "titleJp": "区民プールの窓口で",
        "titleEn": "At the public pool counter",
        "titleZh": "在区民泳池窗口",
        "titleRuby": [],
        "sections": [
            section(
                "入場",
                "Entry",
                "入场",
                "🏊",
                [
                    (
                        "B",
                        "すみません、大人一人、一般プールを利用したいです。",
                        "Excuse me, one adult for general pool use, please.",
                        "你好，大人一位，用一般泳池。",
                    ),
                    (
                        "A",
                        "ありがとうございます。五百円になります。メッシュキャップはお持ちですか。",
                        "Thank you. That will be 500 yen. Do you have a mesh swim cap?",
                        "谢谢。五百日元。带网泳帽了吗？",
                    ),
                    (
                        "B",
                        "はい、あります。タオルはプールサイドに持ち込めますか。",
                        "Yes, I do. Can I bring a towel poolside?",
                        "带了。毛巾能带到池边吗？",
                    ),
                    (
                        "A",
                        "はい、ただし水中には入れないでください。ロッカーはコイン式です。",
                        "Yes, but please don't take it into the water. Lockers are coin-operated.",
                        "可以，但不要带进水里。储物柜是投币式。",
                    ),
                ],
            ),
            section(
                "ルール",
                "Rules",
                "规则",
                "📣",
                [
                    (
                        "B",
                        "泳げる時間は何時までですか。",
                        "What time does swimming end?",
                        "可以游到几点？",
                    ),
                    (
                        "A",
                        "本日は十七時三十分までです。十五分前に休憩の笛が鳴ります。",
                        "Today until 5:30 p.m. A break whistle blows fifteen minutes before.",
                        "今天到五点半。结束前十五分钟有休息哨。",
                    ),
                    (
                        "B",
                        "分かりました。飛び込みは禁止ですか。",
                        "Understood. Is diving banned?",
                        "知道了。禁止跳水吗？",
                    ),
                    (
                        "A",
                        "はい、このプールは飛び込み禁止です。足元にお気をつけてお楽しみください。",
                        "Yes, no diving in this pool. Mind your step and enjoy.",
                        "是的，本池禁止跳水。请注意脚下，祝您愉快。",
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
