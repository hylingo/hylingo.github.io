#!/usr/bin/env python3
"""
batch16 → public/data/ja_articles.json

补全缺 dialogue 的 13 个主题:
N4–N3: bento-morning, closet-cleanup, first-bus, first-cooking,
        home-center, sick-day, unpack-boxes, weekend
N5–N3: summer-at-grandpas
N3:    izakaya-party
N3–N2: new-employee, fight-and-makeup
N2:    big-cleanup, fashion

运行: python3 scripts/append_ja_articles_batch16.py
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
    # 1. n4-bento-morning 做便当的早晨
    # ═══════════════════════════════════════════
    {
        "id": "n4-bento-morning-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "お弁当、見せて！",
        "titleJp": "お弁当、見せて！",
        "titleEn": "Show me your bento!",
        "titleZh": "让我看看你的便当！",
        "titleRuby": [],
        "sections": [
            section("お昼の時間", "Lunchtime", "午休时间", "🍱", [
                line("A", "うわ、すごい！お弁当自分で作ったの？",
                     "Wow, amazing! Did you make the bento yourself?",
                     "哇，好厉害！便当自己做的？"),
                line("B", "うん、今朝五時半に起きて作った。眠かったけど。",
                     "Yeah, I woke up at 5:30 this morning to make it. I was sleepy though.",
                     "嗯，今早五点半起来做的。虽然困死了。"),
                line("A", "えー、偉い。私はコンビニのおにぎり……。中身は何？",
                     "Wow, impressive. I just have a convenience store rice ball... What's inside?",
                     "诶——好勤快。我只有便利店饭团……。里面是什么？"),
                line("B", "鶏肉の照り焼きと卵焼き。あと、ぶどう。",
                     "Teriyaki chicken and omelet. And grapes.",
                     "照烧鸡肉和煎蛋卷。还有葡萄。"),
                line("A", "彩りもきれい。写真撮っていい？",
                     "The colors are pretty too. Can I take a picture?",
                     "颜色也好好看。能拍张照吗？"),
                line("B", "いいけど、SNSには上げないでね。そこまでの自信はない。",
                     "Sure, but don't post it on social media. I'm not that confident.",
                     "可以，但别发社交媒体啊。还没那个自信。"),
            ]),
            section("コツを教える", "Sharing tips", "传授秘诀", "📝", [
                line("A", "私もお弁当作りたいんだけど、朝起きられなくて。",
                     "I want to make bentos too, but I can't wake up in the morning.",
                     "我也想做便当，但早上起不来。"),
                line("B", "おかずは夜のうちに作っておくと楽だよ。朝は詰めるだけ。",
                     "It's easier if you make the side dishes the night before. In the morning you just pack them.",
                     "配菜头天晚上做好会轻松很多。早上只要装进去就行。"),
                line("A", "あ、なるほど。ご飯はどうしてるの？",
                     "Oh, I see. What about the rice?",
                     "啊，原来如此。米饭怎么弄？"),
                line("B", "炊飯器のタイマーをセットしておけば、朝炊き立てが食べられる。",
                     "If you set the rice cooker timer, you can have freshly cooked rice in the morning.",
                     "定好电饭锅的定时器，早上就有刚煮好的饭。"),
                line("A", "それなら私にもできそう。来週から挑戦してみようかな。",
                     "I think even I could do that. Maybe I'll try starting next week.",
                     "那我应该也行。下周开始试试吧。"),
                line("B", "がんばって。最初はおにぎりだけでもいいと思うよ。",
                     "Good luck. I think even just rice balls is fine at first.",
                     "加油。一开始光做饭团也挺好的。"),
                line("A", "ありがとう。あ、そのぶどう一個ちょうだい。",
                     "Thanks. Oh, can I have one grape?",
                     "谢谢。啊，给我一颗葡萄呗。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n4-closet-cleanup 衣替え
    # ═══════════════════════════════════════════
    {
        "id": "n4-closet-cleanup-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "衣替えを手伝って",
        "titleJp": "衣替えを手伝って",
        "titleEn": "Help me with the wardrobe switch",
        "titleZh": "帮我换季整理衣服",
        "titleRuby": [],
        "sections": [
            section("夏物をしまう", "Putting away summer clothes", "收夏装", "👕", [
                line("A", "ねえ、急に寒くなったよね。衣替えしなきゃ。手伝ってくれない？",
                     "Hey, it suddenly got cold, right? I need to do the wardrobe switch. Can you help?",
                     "诶，突然变冷了吧。得换季整理衣服了。能帮帮我吗？"),
                line("B", "いいよ。何からやる？",
                     "Sure. Where do we start?",
                     "好啊。先做什么？"),
                line("A", "まず夏の服をたたんで、この箱に入れて。Tシャツとスカートから。",
                     "First fold the summer clothes and put them in this box. Start with T-shirts and skirts.",
                     "先把夏天的衣服叠好放进这个箱子。从T恤和裙子开始。"),
                line("B", "了解。……あれ、このシャツ、襟が黄色くなってない？",
                     "Got it. ...Wait, isn't the collar of this shirt turning yellow?",
                     "收到。……咦，这件衬衫领子是不是发黄了？"),
                line("A", "あー、もう捨てようかな。去年あんまり着なかったし。",
                     "Ah, maybe I should throw it out. I didn't wear it much last year.",
                     "啊——要不扔了吧。去年也没怎么穿。"),
                line("B", "思い切って捨てた方がすっきりするよ。",
                     "You'll feel better if you just get rid of it.",
                     "下定决心扔掉会清爽很多。"),
            ]),
            section("冬物を出す", "Getting out winter clothes", "翻冬装", "🧥", [
                line("A", "次は奥からセーターとコートを出して。",
                     "Next, pull out the sweaters and coats from the back.",
                     "接下来把里面的毛衣和大衣拿出来。"),
                line("B", "うわ、防虫剤の匂いがすごい。一回干した方がいいんじゃない？",
                     "Whoa, the mothball smell is strong. Shouldn't we air them out first?",
                     "呜哇，防虫剂的味道好重。要不先晾一下？"),
                line("A", "そうだね。ベランダに出しとこう。あ、このマフラー去年買ったのに一度も使ってない。",
                     "Good idea. Let's hang them on the balcony. Oh, I bought this scarf last year but never used it.",
                     "也是。挂阳台上吧。啊，这条围巾去年买的一次都没用过。"),
                line("B", "もったいない。今年こそ使いなよ。",
                     "What a waste. Use it this year for sure.",
                     "太浪费了。今年一定用起来。"),
                line("A", "うん。あ、ブーツも出さなきゃ。靴の箱どこだっけ？",
                     "Yeah. Oh, I need to get the boots out too. Where's the shoe box?",
                     "嗯。啊，靴子也要拿出来。鞋盒放哪了？"),
                line("B", "押入れの上の段にあったよ。取ってくる。",
                     "It was on the top shelf of the closet. I'll get it.",
                     "在壁橱上层。我去拿。"),
                line("A", "ありがとう。終わったらお茶にしよう。疲れた。",
                     "Thanks. Let's have tea when we're done. I'm tired.",
                     "谢谢。弄完喝杯茶吧。累了。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-first-bus 初めてバスに乗る
    # ═══════════════════════════════════════════
    {
        "id": "n4-first-bus-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "このバス、港に行きますか？",
        "titleJp": "このバス、港に行きますか？",
        "titleEn": "Does this bus go to the port?",
        "titleZh": "这班车去港口吗？",
        "titleRuby": [],
        "sections": [
            section("バス停で", "At the bus stop", "在公交站", "🚌", [
                line("A", "すみません、このバスは港の方に行きますか？",
                     "Excuse me, does this bus go toward the port?",
                     "不好意思，这班车去港口方向吗？"),
                line("B", "港？えーと、三番のバスなら行きますよ。ここは五番だから、向こうの乗り場ですね。",
                     "The port? Um, bus number 3 goes there. This is number 5, so it's the stop over there.",
                     "港口？嗯，三号线去。这里是五号线，要去对面的站台。"),
                line("A", "あ、間違えてました。ありがとうございます。",
                     "Oh, I was at the wrong stop. Thank you.",
                     "啊，搞错了。谢谢。"),
                line("B", "信号を渡って、横断歩道の先にバス停がありますよ。",
                     "Cross at the light, and the bus stop is just past the crosswalk.",
                     "过红绿灯，人行横道那边就是公交站。"),
                line("A", "料金はいくらぐらいですか？",
                     "How much is the fare?",
                     "车费大概多少？"),
                line("B", "二百五十円くらいかな。ICカードも使えますよ。",
                     "About 250 yen I think. You can use an IC card too.",
                     "大概两百五十日元吧。也能刷交通卡。"),
            ]),
            section("バスの中で", "On the bus", "在车上", "🪟", [
                line("A", "あの、降りるときはどうすればいいですか？",
                     "Um, what do I do when I want to get off?",
                     "那个，下车的时候要怎么做？"),
                line("C", "次の停留所が近くなったら、このボタンを押してください。",
                     "When the next stop is approaching, press this button.",
                     "快到下一站的时候按这个按钮。"),
                line("A", "分かりました。港まであと何分くらいですか？",
                     "Got it. About how many minutes to the port?",
                     "明白了。到港口还有几分钟？"),
                line("C", "十五分くらいですかね。窓から海が見えたら、その次です。",
                     "About fifteen minutes I'd say. When you can see the ocean from the window, it's the next stop.",
                     "大概十五分钟吧。从窗户能看到海的时候，下一站就是。"),
                line("A", "海が目印ですね。ありがとうございます。",
                     "The ocean is the landmark. Thank you.",
                     "以大海为标志。谢谢。"),
                line("C", "初めてこの辺に来たんですか？いい街ですよ。",
                     "Is this your first time in this area? It's a nice town.",
                     "第一次来这边吗？这里是个好地方。"),
                line("A", "はい、出張で来ました。景色がきれいですね。",
                     "Yes, I'm here on a business trip. The scenery is beautiful.",
                     "嗯，来出差的。风景真好看。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 4. n4-first-cooking 初めての自炊
    # ═══════════════════════════════════════════
    {
        "id": "n4-first-cooking-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "卵焼きの作り方",
        "titleJp": "卵焼きの作り方",
        "titleEn": "How to make tamagoyaki",
        "titleZh": "煎蛋卷的做法",
        "titleRuby": [],
        "sections": [
            section("スーパーで", "At the supermarket", "在超市", "🛒", [
                line("A", "日本に来て一週間、ずっとコンビニ弁当だったんだけど、そろそろ自炊したくて。",
                     "It's been a week since I came to Japan, and I've been eating convenience store bentos. I want to start cooking.",
                     "来日本一周了，一直吃便利店便当。想开始自己做饭了。"),
                line("B", "お、いいね。何作るの？",
                     "Oh, nice. What are you going to make?",
                     "哦，不错啊。打算做什么？"),
                line("A", "とりあえず卵焼き。簡単そうだから。何を買えばいい？",
                     "Tamagoyaki for now. It seems easy. What should I buy?",
                     "先做煎蛋卷。看起来简单。要买什么？"),
                line("B", "卵と醤油と砂糖。あと油。お米もいるでしょ？",
                     "Eggs, soy sauce, and sugar. And oil. You need rice too, right?",
                     "鸡蛋、酱油、砂糖。还有油。米也要吧？"),
                line("A", "あ、そうだ。炊飯器はあるけど、お米がない。",
                     "Oh right. I have a rice cooker but no rice.",
                     "啊，对。有电饭锅但没米。"),
                line("B", "じゃあ二キロでいいよ。最初はそんなに使わないから。",
                     "Then 2 kilos is enough. You won't use that much at first.",
                     "那买两公斤就够了。一开始用不了那么多。"),
            ]),
            section("キッチンで", "In the kitchen", "在厨房", "🍳", [
                line("A", "えーと、油を引いて、卵を割って……あれ、殻が入っちゃった。",
                     "Um, put oil in, crack the egg... oops, a shell piece fell in.",
                     "嗯，倒油，打蛋……啊，蛋壳掉进去了。"),
                line("B", "箸でつまんで取って。……そうそう、上手い。",
                     "Pick it out with chopsticks. ...Yeah, nice, good job.",
                     "用筷子夹出来。……对对，不错。"),
                line("A", "醤油はどのくらい入れるの？",
                     "How much soy sauce should I add?",
                     "酱油放多少？"),
                line("B", "少しでいいよ。入れすぎるとしょっぱくなるから。",
                     "Just a little. If you put too much it'll be too salty.",
                     "少放点就好。放多了会太咸。"),
                line("A", "……あ、ちょっと焦げた。",
                     "...Oh, it burnt a little.",
                     "……啊，有点焦了。"),
                line("B", "大丈夫、最初はそんなもん。味はどう？",
                     "It's fine, that's normal for the first time. How does it taste?",
                     "没事，第一次都这样。味道怎么样？"),
                line("A", "……おいしい！お母さんの味とは全然違うけど、自分で作ったから嬉しい。",
                     "...Delicious! It's nothing like my mom's cooking, but I'm happy because I made it myself.",
                     "……好吃！跟妈妈做的完全不一样，但自己做的就是开心。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 5. n4-home-center ホームセンター
    # ═══════════════════════════════════════════
    {
        "id": "n4-home-center-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "ホームセンターで店員に聞く",
        "titleJp": "ホームセンターで店員に聞く",
        "titleEn": "Asking a staff member at the home center",
        "titleZh": "在家居店问店员",
        "titleRuby": [],
        "sections": [
            section("照明と工具", "Lighting and tools", "照明和工具", "💡", [
                line("A", "すみません、LED電球はどこですか？",
                     "Excuse me, where are the LED bulbs?",
                     "不好意思，LED灯泡在哪？"),
                line("B", "照明コーナーは三番通路の奥です。ご案内しましょうか？",
                     "The lighting section is at the back of aisle 3. Shall I show you?",
                     "照明区在三号通道里面。需要带您去吗？"),
                line("A", "お願いします。あと、針と糸も探してるんですけど。",
                     "Yes please. Also, I'm looking for needles and thread.",
                     "麻烦了。另外我还在找针和线。"),
                line("B", "手芸用品は五番通路にあります。ボタン付け用ですか？",
                     "Sewing supplies are in aisle 5. Is it for sewing buttons?",
                     "手工用品在五号通道。是缝扣子用的吗？"),
                line("A", "はい、ズボンのボタンが取れちゃって。",
                     "Yes, a button came off my pants.",
                     "对，裤子扣子掉了。"),
                line("B", "でしたら、こちらのセットが便利ですよ。針と糸とボタンが入ってます。",
                     "In that case, this set is convenient. It has needles, thread, and buttons.",
                     "那这个套装挺方便的。里面有针、线和扣子。"),
            ]),
            section("カーテンを選ぶ", "Choosing curtains", "选窗帘", "🪟", [
                line("A", "あの、カーテンを探してるんですけど、サイズがよく分からなくて。",
                     "Um, I'm looking for curtains, but I'm not sure about the size.",
                     "那个，我想买窗帘，但不太清楚尺寸。"),
                line("B", "窓の幅と高さは測ってきましたか？",
                     "Did you measure the width and height of your window?",
                     "量了窗户的宽度和高度吗？"),
                line("A", "幅は百八十センチで、高さは二百センチくらいです。",
                     "The width is 180 cm and the height is about 200 cm.",
                     "宽一百八十厘米，高两百厘米左右。"),
                line("B", "それなら、このサイズが合いますね。柄はお好みで。",
                     "Then this size should fit. The pattern is up to your preference.",
                     "那这个尺寸合适。花纹看您喜好。"),
                line("A", "この丸い柄のがいいな。遮光カーテンですか？",
                     "I like this round pattern one. Is it a blackout curtain?",
                     "这个圆形花纹的不错。是遮光窗帘吗？"),
                line("B", "はい、一級遮光です。朝日が気になる方にはおすすめですよ。",
                     "Yes, it's grade 1 blackout. I recommend it for anyone bothered by morning sun.",
                     "是的，一级遮光。怕早上阳光的话很推荐。"),
                line("A", "じゃあこれにします。レジはどこですか？",
                     "I'll take this then. Where is the register?",
                     "那就要这个。收银台在哪？"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 6. n4-sick-day 体調を崩した日
    # ═══════════════════════════════════════════
    {
        "id": "n4-sick-day-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "風邪引いたかも",
        "titleJp": "風邪引いたかも",
        "titleEn": "I might have caught a cold",
        "titleZh": "好像感冒了",
        "titleRuby": [],
        "sections": [
            section("会社に電話する", "Calling the office", "给公司打电话", "📞", [
                line("A", "もしもし、田中です。すみません、今朝から熱がありまして、お休みをいただきたいのですが。",
                     "Hello, this is Tanaka. I'm sorry, I've had a fever since this morning and would like to take the day off.",
                     "喂，我是田中。不好意思，从今早开始发烧了，想请个假。"),
                line("B", "大丈夫ですか？熱は何度ですか？",
                     "Are you OK? How high is the fever?",
                     "没事吧？多少度？"),
                line("A", "三十七度八分です。頭も痛くて、鼻も詰まっていて。",
                     "37.8. My head hurts too, and my nose is stuffed.",
                     "三十七度八。头也疼，鼻子也塞了。"),
                line("B", "それは辛いですね。今日の会議は私が代わりに出ますので、ゆっくり休んでください。",
                     "That sounds tough. I'll attend today's meeting in your place, so please rest well.",
                     "那挺难受的。今天的会议我代你出席，好好休息吧。"),
                line("A", "ありがとうございます。申し訳ないです。",
                     "Thank you. I'm sorry for the trouble.",
                     "谢谢。真不好意思。"),
                line("B", "いいえ。お大事に。病院には行ってくださいね。",
                     "Not at all. Take care. Please go to the hospital.",
                     "没关系。保重。记得去医院。"),
            ]),
            section("病院で", "At the hospital", "在医院", "🏥", [
                line("C", "田中さん、どうぞ。今日はどうされましたか？",
                     "Tanaka-san, please come in. What brings you here today?",
                     "田中先生，请进。今天怎么了？"),
                line("A", "朝から頭が痛くて、鼻も詰まっています。熱もあります。",
                     "My head has been hurting since morning, and my nose is stuffed. I have a fever too.",
                     "从早上开始头疼，鼻子也堵。还发烧。"),
                line("C", "のどを見せてください。……少し赤いですね。風邪でしょう。",
                     "Let me see your throat. ...It's a bit red. It's probably a cold.",
                     "让我看看喉咙。……有点红。应该是感冒。"),
                line("A", "薬をもらえますか？",
                     "Can I get some medicine?",
                     "能开药吗？"),
                line("C", "はい、食後に飲む錠剤と、のどのスプレーを出します。水分をたくさん取ってくださいね。",
                     "Yes, I'll prescribe tablets to take after meals and a throat spray. Make sure to drink plenty of fluids.",
                     "好的，开饭后吃的药片和喉咙喷雾。多喝水。"),
                line("A", "分かりました。どのくらいで治りますか？",
                     "Understood. How long until I recover?",
                     "明白了。大概多久能好？"),
                line("C", "二、三日でよくなると思いますよ。しっかり寝てください。",
                     "I think you'll feel better in two or three days. Get plenty of sleep.",
                     "两三天应该就好了。好好睡觉。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 7. n4-unpack-boxes 段ボールを開ける夜
    # ═══════════════════════════════════════════
    {
        "id": "n4-unpack-boxes-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "引っ越しの荷解き",
        "titleJp": "引っ越しの荷解き",
        "titleEn": "Unpacking after moving",
        "titleZh": "搬家后拆箱",
        "titleRuby": [],
        "sections": [
            section("箱を開ける", "Opening boxes", "开箱", "📦", [
                line("A", "やっと荷物届いた……。段ボール十個もある。",
                     "The boxes finally arrived... There are ten of them.",
                     "行李终于到了……。十个纸箱。"),
                line("B", "多いね。どれから開ける？",
                     "That's a lot. Which one do we open first?",
                     "好多啊。先开哪个？"),
                line("A", "まず大きいやつ。掃除機と電子レンジが入ってるはず。",
                     "The big one first. The vacuum cleaner and microwave should be inside.",
                     "先开大的。应该装着吸尘器和微波炉。"),
                line("B", "あ、食器はこっちだね。お皿とお茶碗。……全部無事だ。割れてない。",
                     "Oh, the tableware is in this one. Plates and rice bowls. ...Everything's fine. Nothing broken.",
                     "啊，餐具在这边。盘子和饭碗。……都没事。没碎。"),
                line("A", "よかった。新聞紙でちゃんと包んだからね。",
                     "Good. I wrapped them properly in newspaper.",
                     "太好了。用报纸好好包了。"),
                line("B", "この箱は布団と毛布だ。今夜寝る分だけ先に出そう。",
                     "This box has the futon and blankets. Let's just take out what we need for tonight.",
                     "这箱是被子和毯子。先拿出今晚要用的吧。"),
            ]),
            section("まだ足りないもの", "Still missing things", "还缺的东西", "🛍️", [
                line("A", "あれ、ハンガー買い忘れた。洋服の箱、開けても掛けられない。",
                     "Oh no, I forgot to buy hangers. Even if I open the clothes box, I can't hang anything.",
                     "糟，忘了买衣架。衣服的箱子打开了也挂不了。"),
                line("B", "明日買いに行こう。あと何か足りないものある？",
                     "Let's go buy some tomorrow. Anything else missing?",
                     "明天去买吧。还缺什么？"),
                line("A", "カーテンとスリッパ。あ、ゴミ袋も。",
                     "Curtains and slippers. Oh, and garbage bags.",
                     "窗帘和拖鞋。啊，垃圾袋也要。"),
                line("B", "リストにしとこう。……あ、この小さい箱、何が入ってるの？",
                     "Let's make a list. ...Oh, what's in this small box?",
                     "列个清单吧。……哎，这个小箱子里装的什么？"),
                line("A", "アルバムと人形。実家から持ってきた大切なもの。",
                     "A photo album and a doll. Precious things I brought from home.",
                     "相册和人偶。从老家带来的重要东西。"),
                line("B", "いいね。窓開けて風入れようよ。新しい生活だね。",
                     "Nice. Let's open the window and let some air in. A new life, huh.",
                     "真好。开窗透透气吧。新生活开始了。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 8. n4-weekend 週末の約束
    # ═══════════════════════════════════════════
    {
        "id": "n4-weekend-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "日曜日に買い物に行こう",
        "titleJp": "日曜日に買い物に行こう",
        "titleEn": "Let's go shopping on Sunday",
        "titleZh": "周日去逛街吧",
        "titleRuby": [],
        "sections": [
            section("LINE で約束", "Making plans on LINE", "LINE 约好", "📱", [
                line("A", "明日暇？買い物に行かない？",
                     "Are you free tomorrow? Want to go shopping?",
                     "明天有空吗？去逛街吧？"),
                line("B", "行きたい！どこに行く？",
                     "I'd love to! Where to?",
                     "想去！去哪？"),
                line("A", "新宿はどう？あの大きい本屋にも寄れるし。",
                     "How about Shinjuku? We can stop by that big bookstore too.",
                     "新宿怎么样？还能顺便去那家大书店。"),
                line("B", "いいね。十時に駅で待ち合わせでいい？",
                     "Nice. Shall we meet at the station at 10?",
                     "好啊。十点在车站碰头行吗？"),
                line("A", "うん。あ、天気予報見た？午後から雨っぽいよ。",
                     "Yeah. Oh, did you check the weather forecast? It looks like rain in the afternoon.",
                     "嗯。啊，看天气预报了吗？下午好像要下雨。"),
                line("B", "え、まじ？傘持っていかなきゃ。",
                     "Eh, really? I need to bring an umbrella.",
                     "诶，真的？得带伞。"),
            ]),
            section("新宿で", "In Shinjuku", "在新宿", "🏙️", [
                line("A", "このワンピースかわいくない？試着してみようかな。",
                     "Isn't this dress cute? Maybe I'll try it on.",
                     "这条连衣裙好不好看？试试吧。"),
                line("B", "似合いそう。色もいいし。",
                     "It would look good on you. The color is nice too.",
                     "应该合适。颜色也好。"),
                line("A", "……サイズがちょっと小さかった。残念。",
                     "...The size was a bit small. Too bad.",
                     "……尺码有点小。好可惜。"),
                line("B", "しょうがないよ。お腹空かない？ラーメン食べに行こうよ。",
                     "Can't be helped. Aren't you hungry? Let's go eat ramen.",
                     "没办法。饿了吧？去吃拉面吧。"),
                line("A", "あ、行列ができてる。人気の店みたいだね。",
                     "Oh, there's a line. Looks like a popular place.",
                     "啊，在排队呢。好像是人气店。"),
                line("B", "二十分くらいなら並ぼうよ。友達に教えてもらった店なの。",
                     "If it's about 20 minutes let's wait. A friend told me about this place.",
                     "二十分钟的话排吧。朋友推荐的店。"),
                line("A", "じゃあ並ぼう。……うわ、おいしい！今まで食べた中で一番かも。",
                     "OK let's wait. ...Wow, delicious! Maybe the best I've ever had.",
                     "那就排。……哇，好吃！可能是吃过最好吃的。"),
                line("B", "でしょ？今度はあのカレー屋にも連れてくよ。",
                     "Right? Next time I'll take you to that curry place too.",
                     "对吧？下次带你去那家咖喱店。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 9. n4-summer-at-grandpas 爷爷家的暑假
    # ═══════════════════════════════════════════
    {
        "id": "n4-summer-at-grandpas-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "おじいちゃんの家で",
        "titleJp": "おじいちゃんの家で",
        "titleEn": "At Grandpa's house",
        "titleZh": "在爷爷家",
        "titleRuby": [],
        "sections": [
            section("到着", "Arrival", "到达", "🏡", [
                line("A", "おばあちゃん、久しぶり！大きくなったでしょ？",
                     "Grandma, long time no see! I've gotten bigger, right?",
                     "奶奶，好久不见！长大了吧？"),
                line("B", "あら、本当に大きくなったねえ。おいで、スイカ切ってあるよ。",
                     "Oh my, you really have grown. Come, I've cut some watermelon.",
                     "哎呀，真的长大了。快来，西瓜切好了。"),
                line("A", "やった！おじいちゃんはどこ？",
                     "Yay! Where's Grandpa?",
                     "太好了！爷爷在哪？"),
                line("B", "畑にいるよ。トマトの世話をしてるんだ。",
                     "He's in the field. Taking care of the tomatoes.",
                     "在菜地呢。照看番茄。"),
                line("A", "手伝いに行ってくる！",
                     "I'll go help!",
                     "我去帮忙！"),
                line("B", "帽子かぶってね。熱いから。",
                     "Wear a hat. It's hot.",
                     "戴上帽子。太热了。"),
            ]),
            section("川遊びと花火", "Playing in the river and fireworks", "玩水和放烟花", "🎆", [
                line("C", "お兄ちゃん、川で泳ごうよ！",
                     "Big brother, let's swim in the river!",
                     "哥哥，去河里游泳吧！"),
                line("A", "いいよ。でもお姉ちゃんにも声かけよう。",
                     "Sure. But let's ask our sister too.",
                     "好啊。不过叫上姐姐。"),
                line("C", "近所のおじさんが「気をつけてな」って。",
                     "The neighbor said 'Be careful.'",
                     "邻居大叔说了「小心点」。"),
                line("A", "うん、深いところには行かないようにしよう。",
                     "Yeah, let's not go to the deep parts.",
                     "嗯，别去深的地方。"),
                line("C", "夜は花火するんでしょ？おじいちゃんが買ってくれたの？",
                     "We're doing fireworks tonight, right? Did Grandpa buy them?",
                     "晚上放烟花对吧？爷爷买的？"),
                line("A", "うん。手持ち花火がいっぱいあるって。",
                     "Yeah. He said there are lots of sparklers.",
                     "嗯。说有好多手持烟花。"),
                line("C", "楽しみ！毎年ここに来るの、一番好き。",
                     "I can't wait! Coming here every year is my favorite.",
                     "好期待！每年来这里是我最喜欢的事。"),
                line("A", "俺もだよ。おじいちゃん家の夏が一番いい。",
                     "Me too. Summer at Grandpa's house is the best.",
                     "我也是。在爷爷家过夏天最棒了。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 10. n3-izakaya-party 居酒屋忘年会
    # ═══════════════════════════════════════════
    {
        "id": "n3-izakaya-party-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "忘年会で乾杯",
        "titleJp": "忘年会で乾杯",
        "titleEn": "A toast at the year-end party",
        "titleZh": "忘年会上干杯",
        "titleRuby": [],
        "sections": [
            section("注文と乾杯", "Ordering and toasting", "点单和干杯", "🍻", [
                line("A", "みんな揃ったね。じゃ、とりあえずビールでいい？",
                     "Everyone's here. So, beer for now?",
                     "人到齐了。那先来啤酒行吗？"),
                line("B", "私は日本酒にしようかな。寒いから温かいのが飲みたい。",
                     "I think I'll have sake. It's cold so I want something warm.",
                     "我要日本酒吧。冷，想喝热的。"),
                line("C", "俺はビールで。あ、枝豆と焼き鳥も頼もうよ。",
                     "Beer for me. Oh, let's order edamame and yakitori too.",
                     "我啤酒。啊，毛豆和烤鸡串也点吧。"),
                line("A", "いいね。じゃ、乾杯しよう。今年一年、お疲れ様でした！",
                     "Nice. OK, let's toast. Thank you for a great year!",
                     "好。那来干杯。辛苦了一年！"),
                line("B", "お疲れ様でした！",
                     "Cheers to a great year!",
                     "辛苦了！"),
                line("C", "かんぱーい！",
                     "Cheers!",
                     "干杯——！"),
            ]),
            section("料理を食べながら", "While eating", "边吃边聊", "🍖", [
                line("B", "この焼肉、塩で食べるとおいしいね。",
                     "This grilled meat is good with salt.",
                     "这个烤肉蘸盐吃好好吃。"),
                line("C", "醤油よりさっぱりしてるよな。あ、寿司も来た。",
                     "It's lighter than soy sauce. Oh, the sushi is here too.",
                     "比酱油清爽。啊，寿司也来了。"),
                line("A", "食べすぎちゃいそう。デザートもあるんでしょ？",
                     "I might eat too much. There's dessert too, right?",
                     "要吃多了。还有甜品吧？"),
                line("B", "アイスとケーキだって。甘いものは別腹よ。",
                     "Ice cream and cake apparently. There's always room for dessert.",
                     "冰淇淋和蛋糕。甜食另有一个胃嘛。"),
                line("C", "ジュースおかわりしていい？無料だよね？",
                     "Can I get a refill on juice? It's free, right?",
                     "果汁能续杯吗？免费的吧？"),
                line("A", "うん、飲み放題だよ。……ああ、お腹いっぱい。もう食べられない。",
                     "Yeah, it's all-you-can-drink. ...Ah, I'm stuffed. I can't eat any more.",
                     "嗯，畅饮的。……啊，吃饱了。吃不动了。"),
                line("B", "帰り道の夜風が気持ちよさそう。来年もみんなで来ようね。",
                     "The night breeze on the way home will feel nice. Let's come together again next year.",
                     "回去路上的夜风肯定很舒服。明年也一起来吧。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 11. n3-new-employee 新入社員の最初の一週間
    # ═══════════════════════════════════════════
    {
        "id": "n3-new-employee-dialogue",
        "level": "N3–N2",
        "format": "dialogue",
        "titleWord": "新入社員の研修",
        "titleJp": "新入社員の研修",
        "titleEn": "New employee orientation",
        "titleZh": "新员工培训",
        "titleRuby": [],
        "sections": [
            section("初日の自己紹介", "First day introductions", "第一天自我介绍", "🏢", [
                line("A", "初めまして、本日付で配属になりました山田です。よろしくお願いいたします。",
                     "Nice to meet you, I'm Yamada, assigned here starting today. Please take care of me.",
                     "初次见面，我是今天入职的山田。请多关照。"),
                line("B", "ようこそ。担当の田中です。何でも聞いてね。席はこっちだよ。",
                     "Welcome. I'm Tanaka, your supervisor. Ask me anything. Your desk is over here.",
                     "欢迎。我是负责人田中。什么都可以问。你的位子在这边。"),
                line("A", "ありがとうございます。あの、コピー機はどこにありますか？",
                     "Thank you. Um, where is the copy machine?",
                     "谢谢。那个，复印机在哪？"),
                line("B", "廊下の突き当たり。紙の入れ方、あとで教えるね。",
                     "At the end of the hallway. I'll show you how to load paper later.",
                     "走廊尽头。怎么装纸待会教你。"),
                line("A", "会議室の予約はどうすればいいですか？",
                     "How do I book a meeting room?",
                     "会议室怎么预约？"),
                line("B", "社内システムから予約できるよ。ログインIDは人事からもらった？",
                     "You can book through the internal system. Did you get your login ID from HR?",
                     "通过内部系统预约。登录ID从人事那拿到了吗？"),
            ]),
            section("最初のレポート", "The first report", "第一份报告", "📄", [
                line("A", "田中さん、レポートを書いたんですけど、見ていただけますか？",
                     "Tanaka-san, I wrote a report. Could you take a look?",
                     "田中先生，我写了报告，能帮我看看吗？"),
                line("B", "いいよ。……うーん、内容はいいんだけど、もう少し具体的な数字があるといいかな。",
                     "Sure. ...Hmm, the content is good, but it'd be better with more specific numbers.",
                     "好。……嗯，内容不错，但再加些具体数字就更好了。"),
                line("A", "分かりました。直して再提出します。",
                     "Understood. I'll fix it and resubmit.",
                     "明白了。修改后重新交。"),
                line("B", "最初はみんなそうだよ。俺も赤ペンだらけで返されたから。",
                     "Everyone's like that at first. I got mine back covered in red ink too.",
                     "一开始都这样。我当初也被红笔改得满满的。"),
                line("A", "ちょっと安心しました。来週から一人で会議に出るんですけど、大丈夫ですかね。",
                     "That's a relief. I have to attend meetings alone starting next week though — will I be OK?",
                     "稍微放心了。下周开始我一个人出席会议，能行吗。"),
                line("B", "大丈夫。分からないことはメモして、あとで聞けばいいから。",
                     "You'll be fine. Just take notes on what you don't understand and ask later.",
                     "没问题。不懂的先记下来，事后问就行。"),
                line("A", "はい、頑張ります。",
                     "Yes, I'll do my best.",
                     "好的，我会努力的。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 12. n3-fight-and-makeup 和好朋友吵架
    # ═══════════════════════════════════════════
    {
        "id": "n3-fight-and-makeup-dialogue",
        "level": "N3–N2",
        "format": "dialogue",
        "titleWord": "喧嘩のあとで",
        "titleJp": "喧嘩のあとで",
        "titleEn": "After the fight",
        "titleZh": "吵架之后",
        "titleRuby": [],
        "sections": [
            section("仲間の心配", "A friend's concern", "朋友的担心", "💬", [
                line("C", "ねえ、最近あの二人、話してなくない？",
                     "Hey, haven't those two not been talking lately?",
                     "诶，最近那两个人是不是没说话？"),
                line("A", "……うん。飲み会のとき、冗談のつもりだったんだろうけど、ちょっとひどかったんだよね。",
                     "...Yeah. At the drinking party, it was probably meant as a joke, but it was kind of harsh.",
                     "……嗯。喝酒的时候虽然可能是开玩笑，但有点过分了。"),
                line("C", "相手の前でからかったやつ？みんな笑ってたけど……。",
                     "The one where they teased you in front of everyone? Everyone laughed but...",
                     "当着别人面取笑你那次？大家都笑了但是……"),
                line("A", "言われた側はそう思えなかった。帰り道に「あれはひどくない？」って言ったら、「冗談じゃん」って。",
                     "The person on the receiving end couldn't see it that way. On the way home I said 'wasn't that harsh?' and they said 'it was just a joke.'",
                     "被说的人可不这么想。回去的路上说了句「不觉得过分吗」，结果人家说「开玩笑而已」。"),
                line("C", "それは辛いね。でも、もう一週間でしょ？そろそろ連絡してみたら？",
                     "That's tough. But it's been a week, right? How about reaching out?",
                     "那确实难受。不过已经一周了吧？要不联系一下？"),
                line("A", "……うん、でも向こうから謝ってほしいって気持ちもあって。",
                     "...Yeah, but part of me wants them to apologize first.",
                     "……嗯，但也有种想让对方先道歉的心情。"),
            ]),
            section("仲直り", "Making up", "和好", "☕", [
                line("B", "……ごめん。この前のこと、ずっと気になってた。",
                     "...Sorry. What happened the other day has been on my mind.",
                     "……对不起。上次的事，一直在意着。"),
                line("A", "……こっちも言い方がきつかったかも。",
                     "...I might have been too harsh in how I said it too.",
                     "……我说话方式可能也太冲了。"),
                line("B", "冗談のつもりだったんだけど、傷つけたよね。ほんとにごめん。",
                     "I meant it as a joke, but I hurt you. I'm really sorry.",
                     "本来是想开玩笑的，但伤到你了。真的对不起。"),
                line("A", "……ありがとう。言ってくれて嬉しい。",
                     "...Thank you. I'm glad you said that.",
                     "……谢谢。你能这么说我很高兴。"),
                line("B", "今度から気をつける。……カフェ行かない？おごるから。",
                     "I'll be more careful from now on. ...Want to go to a cafe? My treat.",
                     "以后注意。……去咖啡店吗？我请客。"),
                line("A", "うん。……やっぱり、何でも一番に話すのはお前だよ。",
                     "Yeah. ...After all, you're the first person I tell everything to.",
                     "好。……果然不管什么事，第一个想说的人还是你。"),
                line("B", "……泣くなよ。俺も泣きそうになるから。",
                     "...Don't cry. I'm about to cry too.",
                     "……别哭啊。我也快哭了。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 13. n2-big-cleanup 年末大掃除
    # ═══════════════════════════════════════════
    {
        "id": "n2-big-cleanup-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "年末の大掃除を始めよう",
        "titleJp": "年末の大掃除を始めよう",
        "titleEn": "Let's start the year-end deep cleaning",
        "titleZh": "开始年末大扫除吧",
        "titleRuby": [],
        "sections": [
            section("台所から", "Starting with the kitchen", "从厨房开始", "🧹", [
                line("A", "十二月三十日。そろそろ大掃除やらないとまずくない？",
                     "December 30th. Don't you think we should start the deep cleaning?",
                     "十二月三十号了。不开始大扫除不行了吧？"),
                line("B", "やるか……。どこからやる？",
                     "Let's do it... Where do we start?",
                     "干吧……。从哪开始？"),
                line("A", "台所。シンクの下、いつから開けてないか分からない。",
                     "The kitchen. I don't even know when I last opened under the sink.",
                     "厨房。水槽下面都不知道多久没打开了。"),
                line("B", "うわ、古い瓶と缶が出てきた。中身何これ？開ける？",
                     "Ugh, old bottles and cans. What's in them? Should we open them?",
                     "呜，翻出来旧瓶子和罐头。里面什么啊？要打开吗？"),
                line("A", "怖いからやめて。そのまま捨てよう。",
                     "Scary, don't. Let's just throw them away as is.",
                     "吓人，别开了。直接扔。"),
                line("B", "冷蔵庫の奥にもカビの生えた容器が……。反省するわ。",
                     "There's a moldy container in the back of the fridge too... I feel bad.",
                     "冰箱里面也有发霉的容器……。反省。"),
            ]),
            section("居間と押入れ", "Living room and closet", "客厅和壁橱", "🧽", [
                line("A", "ソファーの隙間からボールペンと切手が出てきたんだけど。",
                     "I found a pen and stamps in the gap of the sofa.",
                     "沙发缝里翻出了圆珠笔和邮票。"),
                line("B", "あ、そのペンずっと探してた！押入れもやろう。",
                     "Oh, I've been looking for that pen! Let's do the closet too.",
                     "啊，那支笔我找了好久！壁橱也收拾吧。"),
                line("A", "座布団と毛布と……これ何？風呂敷に包まれてるけど。",
                     "Floor cushions and blankets and... what's this? It's wrapped in a furoshiki.",
                     "坐垫和毯子和……这是什么？用包袱皮包着的。"),
                line("B", "あ、おばあちゃんの瀬戸物だ。大事にしまっとこう。",
                     "Oh, that's Grandma's ceramics. Let's store it carefully.",
                     "啊，是奶奶的陶瓷器。好好收着。"),
                line("A", "粗大ゴミの袋、もう三つ目だよ。散らかす方は簡単なのにね。",
                     "This is the third bag of bulk garbage already. Making a mess is easy, but cleaning up is hard.",
                     "大件垃圾袋已经第三个了。弄乱容易收拾难。"),
                line("B", "ほんとそれ。……あー、でもすっきりした。年越しそば食べよう。",
                     "So true. ...Ah, but it feels refreshing. Let's eat New Year's Eve soba.",
                     "真的是。……啊，不过清爽多了。吃年越荞麦面吧。"),
                line("A", "いいね。きれいな部屋で新年迎えよう。",
                     "Sounds good. Let's welcome the new year in a clean room.",
                     "好。在干净的房间迎接新年吧。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 14. n2-fashion 穿什么上班
    # ═══════════════════════════════════════════
    {
        "id": "n2-fashion-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "何を着ていけばいい？",
        "titleJp": "何を着ていけばいい？",
        "titleEn": "What should I wear?",
        "titleZh": "穿什么去上班好？",
        "titleRuby": [],
        "sections": [
            section("朝の悩み", "Morning dilemma", "早晨的烦恼", "👔", [
                line("A", "ねえ、今日何着ていこう。会議あるんだけど。",
                     "Hey, what should I wear today? I have a meeting.",
                     "诶，今天穿什么去？有会议。"),
                line("B", "会議ならブラウスとスカートでいいんじゃない？",
                     "For a meeting, a blouse and skirt should be fine, right?",
                     "开会的话衬衫配裙子不就好了？"),
                line("A", "でも寒いんだよね。ワンピースなら一枚で楽だけど、冬は足元が冷える。",
                     "But it's cold. A one-piece dress is easy, but in winter my feet get cold.",
                     "但是冷啊。连衣裙一件搞定倒是方便，但冬天脚冷。"),
                line("B", "ストッキング履けば？あ、伝線すると困るから予備も持っていきなよ。",
                     "Wear stockings? Oh, bring a spare pair in case they run.",
                     "穿丝袜呗？啊，万一跑丝就麻烦了，带双备用的。"),
                line("A", "それもそうか。……足元はスニーカーで通勤して、会社でスリッパに替えよう。",
                     "Good point. ...I'll commute in sneakers and change to slippers at the office.",
                     "也是。……脚上穿运动鞋通勤，到公司换拖鞋。"),
                line("B", "スカーフ巻くと印象変わるよ。この前の紺色のやつ、似合ってた。",
                     "A scarf changes the impression. That navy one the other day looked good on you.",
                     "围条丝巾印象会不一样。前几天那条藏青色的挺好看的。"),
            ]),
            section("おしゃれの楽しみ", "The joy of fashion", "穿搭的乐趣", "💄", [
                line("A", "この前ブローチ付けてったら同僚に褒められてさ。嬉しかった。",
                     "The other day I wore a brooch and a colleague complimented me. I was happy.",
                     "前几天戴了胸针去，同事夸了。好开心。"),
                line("B", "いいじゃん。アクセサリーって気分転換になるよね。",
                     "Nice. Accessories can really change your mood.",
                     "不错嘛。饰品确实能换个心情。"),
                line("A", "口紅の色も服に合わせるの、最近ハマってる。茶色い服にはピンク、黒い服には赤。",
                     "Lately I'm into matching lipstick to my outfit. Pink with brown clothes, red with black.",
                     "最近迷上了口红颜色配衣服。棕色衣服配粉色，黑衣服配红色。"),
                line("B", "おしゃれだね。……でもクリーニング代、増えてない？",
                     "Stylish. ...But hasn't your dry cleaning bill gone up?",
                     "好时髦。……不过干洗费是不是涨了？"),
                line("A", "それは言わないで。毛糸のセーターの手入れも面倒だし。",
                     "Don't remind me. Taking care of wool sweaters is a hassle too.",
                     "别提了。毛衣的保养也麻烦。"),
                line("B", "制服がある会社が羨ましくなる瞬間だよね。",
                     "That's the moment you envy companies with uniforms.",
                     "这时候就羡慕有制服的公司了。"),
                line("A", "でも、何を着るか選べるのは楽しいよ。煩わしい日もあるけど、楽しい日の方が多い。",
                     "But being able to choose what to wear is fun. Some days are annoying, but the fun days outnumber them.",
                     "但是能自己选穿什么还是开心的。虽然有烦的时候，开心的时候更多。"),
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
