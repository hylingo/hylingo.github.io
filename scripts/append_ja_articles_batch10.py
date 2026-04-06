#!/usr/bin/env python3
"""
batch10 → public/data/ja_articles.json

P2: N2生活类×3 (衣物穿搭essay, 家电维修dialogue, 大扫除essay)
P3: 健康医疗×2 (essay+dialogue), 交通出行×2 (essay+dialogue), 工作职场×2 (essay+dialogue)

共9篇

运行: python3 scripts/append_ja_articles_batch10.py
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
        "word": w, "jp": w, "en": en.strip(), "zh": zh.strip(),
        "reading": full_reading(w), "ruby": gr.make_ruby(w),
    }


def enrich_line(speaker: str, word: str, en: str, zh: str) -> dict:
    d = enrich_segment(word, en, zh)
    d["speaker"] = speaker
    return d


def section(heading, heading_en, heading_zh, badge, lines):
    return {
        "badge": badge,
        "headingWord": heading, "headingJp": heading,
        "headingEn": heading_en, "headingZh": heading_zh,
        "lines": [enrich_line(sp, w, e, z) for sp, w, e, z in lines],
    }


NEW_ITEMS: list[dict] = [

    # ===== P2-1: N2 衣物穿搭 (essay) =====
    {
        "id": "n2-fashion-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "制服のない会社で何を着るか",
        "titleJp": "制服のない会社で何を着るか",
        "titleEn": "What to wear at a company with no uniform",
        "titleZh": "没有制服的公司穿什么",
        "titleRuby": [],
        "segments": [
            ("転職先には制服がなく、毎朝何を着るかで悩むようになった。",
             "My new workplace has no uniform, and I started agonizing over what to wear every morning.",
             "新公司没有制服，每天早上开始纠结穿什么。"),
            ("ワンピースなら一枚で決まるので楽だが、冬は寒い。",
             "A dress is easy since it looks put-together by itself, but it's cold in winter.",
             "连衣裙一件就能搞定所以很轻松，但冬天冷。"),
            ("セーターにスカートという組み合わせが一番多い。スカーフを巻くと印象が変わる。",
             "The most common combination is a sweater with a skirt. Wrapping a scarf changes the impression.",
             "毛衣配裙子是最多的搭配。围上围巾印象就不一样了。"),
            ("ブラウスとスーツは会議の日に着る。ストッキングが伝線すると困るので、予備をポケットに入れている。",
             "I wear a blouse and suit on meeting days. Runs in stockings are a problem, so I keep spares in my pocket.",
             "衬衫和西装是开会的日子穿。丝袜走丝就麻烦了，所以口袋里备着替换的。"),
            ("足元はスニーカーで通勤して、会社でスリッパに履き替える。下駄箱に革靴を入れてある。",
             "I commute in sneakers and change into slippers at the office. I keep leather shoes in the shoe cupboard.",
             "穿运动鞋通勤，到公司换拖鞋。鞋柜里放着皮鞋。"),
            ("先日、ブローチを付けてみたら同僚に褒められた。アクセサリーは小さな気分転換になる。",
             "The other day, I tried wearing a brooch and a colleague complimented me. Accessories are a small mood changer.",
             "前几天试着别了个胸针，被同事夸了。饰品是小小的心情转换。"),
            ("クリーニングに出す服が増えて、毛糸のセーターの手入れも面倒だ。",
             "More clothes need dry cleaning, and caring for wool sweaters is also a hassle.",
             "需要送干洗的衣服多了，毛线毛衣的打理也麻烦。"),
            ("口紅の色を服に合わせるのが最近の楽しみだ。茶色い服には落ち着いたピンク、黒い服には赤。",
             "Matching lipstick color to my outfit has become a recent pleasure. Calm pink for brown clothes, red for black.",
             "最近的乐趣是把口红颜色和衣服搭配。棕色衣服配沉稳的粉色，黑色配红色。"),
            ("何を着るかは自分を表す手段の一つだと思う。煩わしいこともあるが、楽しい日の方が多い。",
             "I think what you wear is one way of expressing yourself. It can be bothersome, but most days it's enjoyable.",
             "我觉得穿什么是表达自己的方式之一。虽然有时觉得烦，但开心的日子更多。"),
        ],
    },

    # ===== P2-2: N2 家电维修 (dialogue, 口語化) =====
    {
        "id": "n2-appliance-repair-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "洗濯機が壊れた（夫婦の相談）",
        "titleJp": "洗濯機が壊れた（夫婦の相談）",
        "titleEn": "The washing machine broke (couple discussing)",
        "titleZh": "洗衣机坏了（夫妻商量）",
        "titleRuby": [],
        "sections": [
            section("発見", "Discovery", "发现故障", "🔧", [
                ("A", "ねえ、洗濯機から変な音しない？なんかガタガタって。",
                 "Hey, doesn't the washing machine sound weird? Like a rattling noise.",
                 "诶，洗衣机是不是有奇怪的声音？咔哒咔哒的。"),
                ("B", "あー、昨日からだよ。蛇口のあたりから水も漏れてるっぽい。",
                 "Ah, since yesterday. Looks like water is leaking around the faucet too.",
                 "啊，从昨天开始的。水龙头那边好像也在漏水。"),
                ("A", "マジ？コンセント抜いた方がいいかな。感電したら怖いし。",
                 "Seriously? Should we unplug it? Getting electrocuted would be scary.",
                 "真的假的？要不要拔插头？触电就麻烦了。"),
                ("B", "うん、とりあえず抜こう。扇風機で乾かしとけば大丈夫でしょ。",
                 "Yeah, let's unplug it for now. It should be fine if we dry it with a fan.",
                 "嗯，先拔了。用电扇吹干应该没事。"),
            ]),
            section("修理か買い替えか", "Repair or replace", "修还是换", "💰", [
                ("A", "修理に出すのと買い替えるの、どっちが安いかな。",
                 "Which is cheaper, getting it repaired or buying a new one?",
                 "送修和换新哪个便宜？"),
                ("B", "もう七年使ってるからね。蛍光灯もこの前切れたし、家電って一気に壊れるよね。",
                 "We've had it for seven years already. The fluorescent light also went out recently. Appliances all break at once, don't they?",
                 "都用了七年了。荧光灯前阵子也坏了。家电就是一起坏的。"),
                ("A", "乾電池で動くような小さいのじゃなくて、大物ばっかり壊れるんだよなあ。",
                 "It's not the small battery-powered stuff that breaks, it's always the big ones.",
                 "偏偏不是干电池那种小东西坏，净是大件坏。"),
                ("B", "とりあえずクリーニング屋に持ってくか。掃除機も調子悪いし、ついでに見てもらおう。",
                 "Let's take stuff to the dry cleaner for now. The vacuum's acting up too, might as well get it checked.",
                 "先把衣服送去干洗店吧。吸尘器也不太对劲，顺便让人看看。"),
                ("A", "扇風機はまだ使えるよね？夏までもってほしい。",
                 "The fan still works, right? I hope it lasts until summer.",
                 "电扇还能用吧？希望能撑到夏天。"),
                ("B", "大丈夫。……たぶん。",
                 "It's fine. ...Probably.",
                 "没问题。……大概。"),
            ]),
        ],
    },

    # ===== P2-3: N2 大扫除 (essay) =====
    {
        "id": "n2-big-cleanup-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "年末の大掃除で見つかるもの",
        "titleJp": "年末の大掃除で見つかるもの",
        "titleEn": "Things found during year-end deep cleaning",
        "titleZh": "年末大扫除翻出来的东西",
        "titleRuby": [],
        "segments": [
            ("十二月三十日、重い腰を上げて大掃除を始めた。",
             "December 30th, I finally got off my butt and started the year-end deep cleaning.",
             "十二月三十号，终于下定决心开始大扫除。"),
            ("まず台所。シンクの下から古い瓶と缶が出てきた。中身は不明。怖いので開けずに捨てた。",
             "First the kitchen. Old bottles and cans came out from under the sink. Contents unknown. Too scared to open them, so I threw them away.",
             "先从厨房开始。水槽下面翻出了旧瓶子和罐子。里面什么不知道。怕得不敢打开直接扔了。"),
            ("冷蔵庫の奥にはカビの生えた容器があった。食べ物を粗末にしてしまった。反省。",
             "In the back of the fridge was a moldy container. I wasted food. Reflecting on it.",
             "冰箱深处有个发了霉的容器。糟蹋食物了。反省。"),
            ("居間に移って、ソファーの隙間を探ると、ボールペンと万年筆と切手が出てきた。",
             "Moving to the living room, I searched the gaps in the sofa and found a ballpoint pen, a fountain pen, and stamps.",
             "到了客厅，翻沙发缝隙翻出来了圆珠笔、钢笔和邮票。"),
            ("雑巾で棚を拭き、掃除機をかけ、障子の汚れを落とした。",
             "I wiped the shelves with a rag, vacuumed, and cleaned the stains off the paper sliding doors.",
             "用抹布擦架子、吸地、去掉纸拉门上的脏东西。"),
            ("押入れからは座布団と毛布と草履が出てきた。風呂敷に包まれた古い瀬戸物もあった。",
             "From the closet came cushions, a blanket, and straw sandals. There was also old pottery wrapped in a furoshiki.",
             "壁橱里翻出了坐垫、毛毯和草鞋。还有用包袱皮包着的旧陶器。"),
            ("階段の手すりを磨き、灯油ストーブの周りも清掃した。",
             "I polished the stair railing and cleaned around the kerosene heater.",
             "擦了楼梯扶手，煤油暖炉周围也打扫了。"),
            ("夕方には粗大ゴミの袋が三つできた。散らかす方は簡単なのに、散らかった部屋を片付けるのは大変だ。",
             "By evening I had three bags of oversized garbage. It's easy to make a mess, but cleaning it up is hard.",
             "傍晚攒了三袋大件垃圾。弄乱很简单，收拾起来可费劲了。"),
            ("綺麗になった部屋で年越しそばを食べた。新しい年を気持ちよく迎えられそうだ。",
             "I ate New Year's Eve soba in the clean room. It felt like I could welcome the new year feeling good.",
             "在干干净净的房间里吃了跨年荞麦面。似乎能舒舒服服迎接新年了。"),
        ],
    },

    # ===== P3-1: 健康医疗 (essay) =====
    {
        "id": "n4-sick-day-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "体調を崩した一日",
        "titleJp": "体調を崩した一日",
        "titleEn": "A day when I fell ill",
        "titleZh": "身体不舒服的一天",
        "titleRuby": [],
        "segments": [
            ("朝起きたら頭が痛くて、鼻も詰まっていた。お腹も少し痛い。",
             "When I woke up in the morning, my head hurt and my nose was stuffed. My stomach hurt a little too.",
             "早上起来头疼，鼻子也塞了。肚子也有点痛。"),
            ("熱を測ったら三十七度八分だった。病気かもしれないと思い、会社に電話して休みをもらった。",
             "I took my temperature and it was 37.8. Thinking I might be sick, I called the company and took the day off.",
             "量了体温三十七度八。觉得可能是生病了，打电话给公司请了假。"),
            ("近くの病院に行った。受付で「いつから具合が悪いですか」と聞かれた。",
             "I went to a nearby hospital. At reception they asked 'Since when have you been feeling unwell?'",
             "去了附近的医院。挂号处问「从什么时候开始不舒服的？」。"),
            ("医者に診てもらった。のどと耳を見て、指で背中を叩いた。",
             "I was examined by the doctor. He looked at my throat and ears and tapped my back with his finger.",
             "让医生看了。检查了喉咙和耳朵，用手指敲了敲后背。"),
            ("「風邪ですね。薬を出しますので、しっかり水分を取ってください」と言われた。",
             "'It's a cold. I'll prescribe medicine, so make sure to drink plenty of fluids,' he said.",
             "他说「是感冒。给你开药，请多喝水」。"),
            ("薬局で薬をもらった。食後に飲む錠剤と、のどのスプレーだ。",
             "I got the medicine at the pharmacy. Tablets to take after meals and a throat spray.",
             "在药房拿了药。饭后吃的药片和喉咙喷雾。"),
            ("家に帰って、お湯を飲んで、布団に入った。足が冷たいので靴下を履いたまま寝た。",
             "I went home, drank hot water, and got into the futon. My feet were cold so I slept with socks on.",
             "回家喝了热水，钻进被窝。脚冷就穿着袜子睡了。"),
            ("夕方、少し元気になったのでお粥を作って食べた。味はしなかったが、お腹は落ち着いた。",
             "In the evening, I felt a bit better so I made and ate porridge. I couldn't taste it, but my stomach settled.",
             "傍晚稍微好了点，煮了粥吃。没什么味道，但肚子舒服了。"),
            ("体調が悪いときに一人暮らしだと心細い。でも、こういう日にこそ自分の体を大切にしようと思った。",
             "Living alone when you're feeling unwell is lonely. But it's on days like this that I think I should take care of my body.",
             "身体不好的时候独居很没安全感。但正是这种日子让我想好好珍惜身体。"),
        ],
    },

    # ===== P3-2: 健康医疗 (dialogue, 口語化) =====
    {
        "id": "n4-clinic-friend-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "具合が悪い友達に電話する",
        "titleJp": "具合が悪い友達に電話する",
        "titleEn": "Calling a friend who's feeling unwell",
        "titleZh": "给不舒服的朋友打电话",
        "titleRuby": [],
        "sections": [
            section("電話で様子を聞く", "Checking in by phone", "电话问情况", "📞", [
                ("A", "もしもし、大丈夫？今日学校来なかったから心配してたんだけど。",
                 "Hello, are you OK? I was worried since you didn't come to school today.",
                 "喂，你没事吧？今天没来学校我挺担心的。"),
                ("B", "ごめん、朝から頭が痛くてさ。鼻も止まらなくて。",
                 "Sorry, my head has been hurting since morning. My nose won't stop running either.",
                 "抱歉，从早上开始头疼。鼻涕也止不住。"),
                ("A", "熱は？病院行った？",
                 "Do you have a fever? Did you go to the hospital?",
                 "发烧了吗？去医院了没？"),
                ("B", "三十八度あったから午前中に行ってきた。風邪だって。薬もらったよ。",
                 "It was 38, so I went in the morning. They said it's a cold. Got medicine.",
                 "三十八度，所以上午去了。说是感冒。开了药。"),
                ("A", "お腹は大丈夫？ちゃんとご飯食べた？",
                 "Is your stomach OK? Did you eat properly?",
                 "肚子没事吧？好好吃饭了没？"),
                ("B", "腹痛はないけど、食欲がなくて……。お粥でも作ろうかなって思ってるとこ。",
                 "No stomachache, but I have no appetite... I was just thinking about making porridge.",
                 "肚子不痛，就是没胃口……。正想着要不要煮个粥。"),
            ]),
            section("お見舞い", "Visiting", "去探望", "🍎", [
                ("A", "なんか買ってこうか？果物とか。お見舞いっぽくない？",
                 "Want me to bring something? Like fruit. Isn't that what you do for sick visits?",
                 "要不我给你带点什么？水果什么的。像探病一样。"),
                ("B", "えっ、いいの？じゃあ、みかんとゼリーがあると嬉しい。",
                 "Eh, really? Then I'd be happy with tangerines and jelly.",
                 "诶，可以吗？那有橘子和果冻就好了。"),
                ("A", "了解。あとポカリも買ってく。足りないものある？ティッシュとか。",
                 "Got it. I'll also get Pocari. Need anything else? Tissues or something?",
                 "收到。再买瓶宝矿力。还缺什么不？纸巾之类的。"),
                ("B", "うーん、鼻のかみすぎで鼻が痛い。柔らかいティッシュあったら助かる。",
                 "Hmm, my nose hurts from blowing it too much. Soft tissues would help.",
                 "嗯——鼻子擤太多疼了。有软纸巾就好了。"),
                ("A", "はいはい。じゃ三十分くらいで行くから、ゆっくりしてて。",
                 "OK OK. I'll be there in about 30 minutes, so just rest.",
                 "好好。那三十分钟左右到，你好好休息。"),
                ("B", "ありがとう……ほんとに。一人だと心細かったからさ。",
                 "Thank you... really. I was feeling lonely being alone.",
                 "谢谢……真的。一个人的时候好没安全感。"),
            ]),
        ],
    },

    # ===== P3-3: 交通出行 (essay) =====
    {
        "id": "n4-first-bus-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "初めての土地でバスに乗る",
        "titleJp": "初めての土地でバスに乗る",
        "titleEn": "Riding a bus in an unfamiliar place",
        "titleZh": "在陌生的地方坐公交",
        "titleRuby": [],
        "segments": [
            ("出張先で、駅からホテルまでバスに乗ることになった。",
             "On a business trip, I had to take a bus from the station to the hotel.",
             "出差的地方，从车站到酒店要坐公交。"),
            ("バス停を探すのに手間取った。交差点を渡り、信号を三つ過ぎて、やっと見つけた。",
             "I struggled to find the bus stop. I crossed the intersection, passed three traffic lights, and finally found it.",
             "找公交站费了一番工夫。过了十字路口、经过三个红绿灯，总算找到了。"),
            ("横断歩道を渡る途中で、タクシーが速いスピードで走ってきて驚いた。",
             "While crossing the crosswalk, a taxi came at high speed and startled me.",
             "过人行横道的时候，一辆出租车飞快地开过来吓了一跳。"),
            ("バスが来た。運転手に「このバスは港に行きますか」と聞いた。「行きますよ」と言われて安心した。",
             "The bus came. I asked the driver 'Does this bus go to the port?' He said 'Yes' and I was relieved.",
             "公交来了。问司机「这班车去港口吗？」。他说「去的」我就放心了。"),
            ("窓から外を見ると、東に海が見えた。南には山があり、北に向かって川が流れていた。",
             "Looking out the window, I could see the sea to the east. There were mountains to the south, and a river flowed northward.",
             "从窗户往外看，东边能看到海。南边有山，河流向北流去。"),
            ("駐車場の広い商業施設を過ぎると、入口に「歩行者注意」の看板がある小さな橋を渡った。",
             "After passing a commercial complex with a large parking lot, we crossed a small bridge with a 'Watch for pedestrians' sign at the entrance.",
             "经过停车场很大的商业设施后，过了一座入口处写着「注意行人」的小桥。"),
            ("飛行機の音が聞こえた。近くに空港があるのだろう。自転車に乗った地元の人が手を振ってくれた。",
             "I heard the sound of an airplane. There must be an airport nearby. A local on a bicycle waved at me.",
             "听到了飞机的声音。附近应该有机场。一个骑自行车的当地人朝我挥了挥手。"),
            ("三十分くらいでホテルの前に着いた。自動車よりバスの方が街の様子が見えて楽しい。",
             "I arrived in front of the hotel in about 30 minutes. You can see more of the town from a bus than a car, which is fun.",
             "大约三十分钟到了酒店门前。坐公交比坐小汽车能看到更多街景，更有意思。"),
            ("知らない土地でバスに乗るのは少し不安だったが、新しい発見もあった。",
             "Riding a bus in an unfamiliar place was a little nerve-wracking, but there were also new discoveries.",
             "在陌生的地方坐公交虽然有点不安，但也有新发现。"),
        ],
    },

    # ===== P3-4: 交通出行 (dialogue, 口語化) =====
    {
        "id": "n4-asking-directions-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "道に迷って通行人に聞く",
        "titleJp": "道に迷って通行人に聞く",
        "titleEn": "Getting lost and asking a passerby",
        "titleZh": "迷路了问路人",
        "titleRuby": [],
        "sections": [
            section("交差点で", "At the intersection", "在十字路口", "🗺️", [
                ("A", "すみません、この辺に郵便局ってありますか？",
                 "Excuse me, is there a post office around here?",
                 "不好意思，这附近有邮局吗？"),
                ("B", "郵便局？えーと、この道をまっすぐ行って、二つ目の信号を右に曲がると……あるはず。",
                 "Post office? Um, go straight on this road, turn right at the second light... it should be there.",
                 "邮局？嗯，沿这条路直走，第二个红绿灯右转……应该就有。"),
                ("A", "右ですね。橋を渡りますか？",
                 "Right, got it. Do I cross a bridge?",
                 "右转是吧。要过桥吗？"),
                ("B", "いや、橋は渡らないよ。橋の手前で右。交番の隣にあるから、すぐ分かると思う。",
                 "No, you don't cross the bridge. Turn right before the bridge. It's next to the police box, so I think you'll find it easily.",
                 "不用，不过桥。桥前面右转。就在派出所旁边，一眼就能看到。"),
                ("A", "あ、地下鉄の駅の近くですか？",
                 "Oh, near the subway station?",
                 "啊，在地铁站附近吗？"),
                ("B", "そうそう、駅の出口から歩いて二分くらい。",
                 "Yeah yeah, about two minutes walk from the station exit.",
                 "对对，从站出口走大概两分钟。"),
            ]),
            section("お礼と別れ", "Thanks and goodbye", "道谢和告别", "🙏", [
                ("A", "封筒と切手も買いたいんですけど、郵便局で売ってますかね？",
                 "I also want to buy envelopes and stamps — do they sell them at the post office?",
                 "我还想买信封和邮票，邮局卖吗？"),
                ("B", "うん、売ってるよ。葉書もあるし、手紙に必要なものは大体揃う。",
                 "Yeah, they do. They have postcards too, pretty much everything you need for letters.",
                 "卖的。也有明信片，写信需要的基本都齐。"),
                ("A", "よかった。あと、大使館ってここから遠いですか？",
                 "Great. Also, is the embassy far from here?",
                 "太好了。还有，大使馆离这里远吗？"),
                ("B", "大使館はちょっと遠いかな。バスか地下鉄で二十分くらい。走って行くにはきついよ。",
                 "The embassy is a bit far. About 20 minutes by bus or subway. Too far to walk.",
                 "大使馆有点远。公交或地铁大概二十分钟。走过去太累了。"),
                ("A", "なるほど。ありがとうございます、助かりました！",
                 "I see. Thank you so much, you've been a great help!",
                 "原来如此。非常感谢，帮了大忙！"),
                ("B", "いえいえ。気をつけてね。",
                 "Not at all. Take care.",
                 "哪里哪里。路上小心。"),
            ]),
        ],
    },

    # ===== P3-5: 工作职场 (essay) =====
    {
        "id": "n3-new-employee-essay",
        "level": "N3–N2",
        "format": "essay",
        "titleWord": "新入社員の最初の一週間",
        "titleJp": "新入社員の最初の一週間",
        "titleEn": "A new employee's first week",
        "titleZh": "新员工的第一周",
        "titleRuby": [],
        "segments": [
            ("四月一日、入社式があった。社長の話は長かったが、緊張していたのであまり覚えていない。",
             "April 1st, there was an entrance ceremony. The president's speech was long, but I was so nervous I don't remember much.",
             "四月一号举行了入职仪式。社长的话很长，但因为太紧张没怎么记住。"),
            ("部長に連れられて部署に行くと、課長が待っていた。「担当者の田中です、よろしく」と名刺を渡された。",
             "Led by the department head to the office, the section chief was waiting. 'I'm Tanaka, your contact person, nice to meet you,' he said, handing me a business card.",
             "部长带我到部门，课长在等着。「我是负责人田中，请多关照」说着递了名片。"),
            ("先輩が席の場所と会議室の使い方を教えてくれた。コピー機の紙の入れ方も習った。",
             "A senior colleague showed me my seat and how to use the meeting room. I also learned how to load paper in the copier.",
             "前辈告诉了我座位和会议室的使用方法。也学了怎么给复印机装纸。"),
            ("三日目にして初めて後輩が「先輩」と呼んでくれた。研修で同期に入った人だった。",
             "On the third day, someone called me 'senpai' for the first time. It was someone who joined in the same intake for training.",
             "第三天第一次有人叫我「前辈」。是一起进来培训的同期。"),
            ("事務所には静かなルールがある。電話の声は小さく、キーボードの音も控えめに。",
             "The office has quiet rules. Keep your phone voice low and keyboard sounds modest.",
             "办公室有安静的规矩。打电话声音要小，键盘声也要控制。"),
            ("昼休みに先輩に誘われて食堂に行った。「最初は分からないことだらけだけど、慣れるから」と言われた。",
             "At lunch break, a senior invited me to the cafeteria. 'At first everything is confusing, but you'll get used to it,' they said.",
             "午休被前辈叫去食堂。他说「一开始什么都不懂，但会习惯的」。"),
            ("金曜日、部下として初めてのレポートを課長に提出した。赤ペンがたくさん入って返ってきた。",
             "On Friday, I submitted my first report as a subordinate to the section chief. It came back covered in red pen marks.",
             "周五，作为下属第一次提交报告给课长。改得满篇红字拿回来了。"),
            ("歌手になりたかった十代の自分には想像もできなかった会社員生活。でも、悪くない。",
             "The teenage me who wanted to be a singer couldn't have imagined office life. But it's not bad.",
             "十几岁想当歌手的自己完全想象不到的上班族生活。但还不错。"),
            ("来週からは一人で会議に出る。まだ緊張するが、少しずつ自分の居場所ができてきた気がする。",
             "Starting next week I'll attend meetings alone. I'm still nervous, but I feel like I'm gradually finding my place.",
             "下周开始要一个人参加会议了。还是会紧张，但感觉渐渐有了自己的位置。"),
        ],
    },

    # ===== P3-6: 工作职场 (dialogue, 口語化) =====
    {
        "id": "n3-office-senpai-dialogue",
        "level": "N3–N2",
        "format": "dialogue",
        "titleWord": "先輩に相談する（後輩と先輩）",
        "titleJp": "先輩に相談する（後輩と先輩）",
        "titleEn": "Consulting a senior (junior and senior)",
        "titleZh": "向前辈请教（后辈和前辈）",
        "titleRuby": [],
        "sections": [
            section("仕事の悩み", "Work troubles", "工作烦恼", "💼", [
                ("A", "先輩、ちょっといいですか。相談があるんですけど。",
                 "Senpai, do you have a moment? I have something to discuss.",
                 "前辈，能占用您一会儿吗？有件事想请教。"),
                ("B", "いいよ、どうした？",
                 "Sure, what's up?",
                 "好啊，怎么了？"),
                ("A", "実は、担当者として初めてお客さんに提案したんですけど、全然ダメで……。",
                 "Actually, I made my first proposal to a client as the person in charge, but it was a total flop...",
                 "其实我第一次作为负责人跟客户提方案，结果完全不行……"),
                ("B", "あー、最初はそんなもんだよ。俺も新人のとき、部長にめちゃくちゃ怒られたから。",
                 "Ah, that's how it is at first. When I was new, the department head chewed me out big time.",
                 "啊，一开始都那样。我新人的时候也被部长狠狠骂了一顿。"),
                ("A", "課長にも「もう少し工夫しろ」って言われて。工夫って何すればいいのか分かんなくて。",
                 "The section chief also told me to 'put more thought into it.' I don't even know what that means.",
                 "课长也说「再下点功夫」。我都不知道该怎么下功夫。"),
                ("B", "まあ、具体的に言えば、相手の立場で考えるってことかな。お客さんが何に困ってるかをもっと聞くんだよ。",
                 "Well, specifically it means thinking from the other person's perspective. Listen more to what the client is struggling with.",
                 "嗯，具体来说就是站在对方立场想。多听客户到底在烦什么。"),
            ]),
            section("励まし", "Encouragement", "鼓励", "✊", [
                ("A", "先輩みたいになれるかな……。監督がいないと何もできない感じで。",
                 "Can I become like you, senpai... I feel like I can't do anything without someone supervising.",
                 "我能变得像前辈一样吗……感觉没人带就什么都做不了。"),
                ("B", "なれるって。てか、後輩にそう言われると照れるんだけど。",
                 "You will. Actually, it's embarrassing when a junior says that.",
                 "能的。话说被后辈这么说还挺不好意思的。"),
                ("A", "でも、同期の中で自分が一番できてない気がして。",
                 "But I feel like I'm the worst among my cohort.",
                 "但总觉得同期里面自己是最差的。"),
                ("B", "比べんなって。人材ってのは一人ひとり伸びるタイミングが違うんだよ。三年後に笑ってればいいじゃん。",
                 "Don't compare. Everyone grows at different times. If you're laughing three years from now, that's all that matters.",
                 "别比。人才这东西每个人成长的节奏都不一样。三年后笑着就好了嘛。"),
                ("A", "……ありがとうございます。なんか楽になりました。",
                 "...Thank you. I feel lighter somehow.",
                 "……谢谢。感觉轻松多了。"),
                ("B", "よし、じゃあ飯行こう。腹減ったでしょ。後輩の分は俺がおごるから。",
                 "Alright, let's go eat. You're hungry, right? I'll treat you since you're the junior.",
                 "好，走吃饭。饿了吧。后辈的份我请。"),
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

        enriched_segments = []
        for seg in item.get("segments", []):
            if isinstance(seg, tuple):
                enriched_segments.append(enrich_segment(*seg))
            else:
                enriched_segments.append(seg)
        item["segments"] = enriched_segments

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
