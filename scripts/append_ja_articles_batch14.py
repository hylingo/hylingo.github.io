#!/usr/bin/env python3
"""
batch14 → public/data/ja_articles.json

第1轮重写D: 3组场景 (6篇)
- n4-laundromat (自助洗衣店)
- n4-hair-salon (理发店)
- n4-cinema (电影院)

运行: python3 scripts/append_ja_articles_batch14.py
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
    # 1. n4-laundromat 自助洗衣店
    # ═══════════════════════════════════════════
    {
        "id": "n4-laundromat-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "コインランドリーで布団を洗う",
        "titleJp": "コインランドリーで布団を洗う",
        "titleEn": "Washing a futon at the coin laundry",
        "titleZh": "在自助洗衣店洗被子",
        "titleRuby": [],
        "segments": [
            seg("週末、天気がよかったので、冬の間に使った布団を洗おうと思った。",
                "It was nice weather on the weekend, so I thought I'd wash the futon I used during winter.",
                "周末天气不错，想把冬天用的被子洗一下。", True),
            seg("うちの洗濯機は小さくて布団が入らない。コインランドリーに行くしかない。",
                "Our washing machine is too small for a futon. I have no choice but to go to the coin laundry.",
                "家里的洗衣机太小放不下被子。只能去自助洗衣店。"),
            seg("近所のコインランドリーは歩いて五分のところにある。大きな袋に布団を詰めて持っていった。",
                "The coin laundry in the neighborhood is a five-minute walk away. I stuffed the futon into a big bag and carried it there.",
                "附近的自助洗衣店走五分钟就到。把被子塞进大袋子里带过去了。"),
            seg("店に入ると、洗濯機と乾燥機がずらりと並んでいた。大型の洗濯機は三台あった。",
                "When I entered, washing machines and dryers were lined up in rows. There were three large washing machines.",
                "进了店，洗衣机和烘干机排成一排。大型洗衣机有三台。", True),
            seg("使い方が分からなかったので、壁に貼ってある説明書を読んだ。まず洗濯物を入れて、お金を入れて、ボタンを押す。",
                "I didn't know how to use them, so I read the instructions posted on the wall. First put in laundry, insert money, press the button.",
                "不会用，看了贴在墙上的说明。先放衣物，投币，按按钮。"),
            seg("大型の洗濯機は一回千円だった。百円玉を十枚入れた。両替機がなかったら困るところだった。",
                "The large washing machine was 1,000 yen per load. I put in ten 100-yen coins. I would've been in trouble without the change machine.",
                "大型洗衣机一次一千日元。投了十个一百日元硬币。幸好有兑换机，不然就麻烦了。"),
            seg("洗濯が始まると、布団がぐるぐる回り始めた。窓から中が見えるので、なんとなく見てしまう。",
                "When the wash started, the futon began spinning round and round. You can see inside through the window, so I found myself watching.",
                "洗衣机启动后被子开始转圈圈。从窗口能看到里面，就不由自主地看着。", True),
            seg("洗濯は四十分かかる。待っている間、持ってきた本を読んだ。",
                "The wash takes forty minutes. While waiting, I read the book I brought.",
                "洗涤需要四十分钟。等的时候看了带来的书。"),
            seg("ベンチに座っていると、おばさんが入ってきて隣の洗濯機を使い始めた。「布団ですか？大きいの洗うの大変ですよね」と話しかけてきた。",
                "While sitting on the bench, a woman came in and started using the machine next to mine. 'A futon? Washing big things is tough, isn't it,' she said.",
                "坐在长椅上的时候，一位大妈进来用了旁边的洗衣机。「洗被子啊？洗大件真不容易呢」她搭话说。"),
            seg("「ここの乾燥機は強力だから、布団もちゃんと乾きますよ」と教えてくれた。常連さんらしい。",
                "She told me 'The dryers here are powerful, so futons dry properly.' She seemed to be a regular.",
                "「这里的烘干机功率大，被子也能烘干」她告诉我。看来是常客。", True),
            seg("洗濯が終わって、布団を乾燥機に移した。乾燥は六十分で五百円。",
                "The wash finished and I moved the futon to the dryer. Drying was 500 yen for sixty minutes.",
                "洗好后把被子搬到烘干机。烘干六十分钟五百日元。"),
            seg("乾燥を待つ間、近くのコンビニでコーヒーを買ってきた。のんびりした土曜日の過ごし方だ。",
                "While waiting for the dryer, I went to the nearby convenience store and bought a coffee. A relaxing way to spend a Saturday.",
                "等烘干的时候去附近便利店买了杯咖啡。悠闲的周六。"),
            seg("六十分後、乾燥機を開けた。布団はふわふわになっていた。太陽に干すより仕上がりがいい気がする。",
                "After sixty minutes I opened the dryer. The futon was fluffy. It seemed to come out better than sun-drying.",
                "六十分钟后打开烘干机。被子变得蓬蓬松松。感觉比晒太阳效果还好。", True),
            seg("しかし少し湿っている部分があったので、もう十分だけ追加した。百円追加。",
                "But there was a slightly damp spot, so I added ten more minutes. Another 100 yen.",
                "不过有个地方还有点潮，又加了十分钟。追加一百日元。"),
            seg("今度はちゃんと乾いた。布団を袋に詰めて、家に持ち帰った。",
                "This time it was properly dry. I stuffed the futon back in the bag and took it home.",
                "这次完全干了。把被子塞回袋子里带回了家。"),
            seg("布団を敷いて触ってみると、ふかふかで気持ちいい。洗いたてのいい匂いがする。",
                "When I laid out the futon and touched it, it was soft and comfortable. It smelled fresh and clean.",
                "铺好被子摸了摸，蓬蓬的好舒服。有刚洗好的清香。", True),
            seg("合計で千六百円かかった。クリーニングに出すと三千円以上するから、だいぶ安い。",
                "It cost 1,600 yen in total. Dry cleaning would cost over 3,000, so this was much cheaper.",
                "总共花了一千六百日元。送去干洗要三千日元以上，便宜多了。"),
            seg("シーツと枕カバーも洗濯機で洗って干した。寝室が丸ごときれいになった感じがする。",
                "I also washed the sheets and pillowcases in our washing machine and hung them to dry. It feels like the whole bedroom got clean.",
                "床单和枕套也用家里洗衣机洗了晾起来。感觉整个卧室都焕然一新了。"),
            seg("季節の変わり目には布団を洗うと気持ちがいい。次は梅雨の前にまた行こうと思う。",
                "Washing the futon at the change of seasons feels great. I think I'll go again before the rainy season.",
                "换季洗洗被子心情很好。下次打算梅雨前再去一趟。"),
            seg("今夜はきれいな布団でぐっすり眠れそうだ。",
                "Tonight I should sleep soundly in a clean futon.",
                "今晚应该能在干净的被子里睡个好觉。"),
        ],
    },

    {
        "id": "n4-laundromat-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "コインランドリーで困る",
        "titleJp": "コインランドリーで困る",
        "titleEn": "Having trouble at the coin laundry",
        "titleZh": "在自助洗衣店遇到困难",
        "titleRuby": [],
        "sections": [
            section("使い方が分からない", "Can't figure it out", "不会用", "🧺", [
                line("A", "すみません、この洗濯機の使い方が分からなくて……。初めて来たんですけど。",
                     "Excuse me, I can't figure out how to use this machine... It's my first time here.",
                     "不好意思，这个洗衣机不会用……第一次来。"),
                line("B", "ああ、大丈夫ですよ。何を洗いたいんですか？",
                     "Oh, no problem. What are you trying to wash?",
                     "没事的。你要洗什么？"),
                line("A", "布団なんですけど、どの洗濯機を使えばいいですか？",
                     "A futon — which machine should I use?",
                     "被子，该用哪台洗衣机？"),
                line("B", "布団なら一番大きいやつですね。あの奥の三台。",
                     "For a futon, the biggest ones. Those three in the back.",
                     "被子的话用最大的那种。后面那三台。"),
                line("A", "お金はいくらかかりますか？",
                     "How much does it cost?",
                     "要多少钱？"),
                line("B", "洗濯だけなら千円です。乾燥は別で、十分百円。布団だと六十分くらい必要ですよ。",
                     "Washing alone is 1,000 yen. Drying is separate, 100 yen per ten minutes. For a futon you'll need about sixty minutes.",
                     "光洗的话一千日元。烘干另算，十分钟一百日元。被子的话需要六十分钟左右。"),
                line("A", "結構かかりますね。両替機ってありますか？千円札しかなくて。",
                     "That adds up. Is there a change machine? I only have thousand-yen bills.",
                     "还挺贵的。有兑换机吗？只有千元纸币。"),
                line("B", "入り口の横にありますよ。あと洗剤は自動で出るから、持ってこなくて大丈夫です。",
                     "It's next to the entrance. Also detergent is dispensed automatically so you don't need to bring any.",
                     "入口旁边有。还有洗涤剂是自动投放的，不用自己带。"),
            ]),
            section("待ち時間", "Waiting time", "等待时间", "📖", [
                line("A", "四十分って結構長いですね。みなさんどうやって待ってるんですか？",
                     "Forty minutes is pretty long. How does everyone pass the time?",
                     "四十分钟还挺长的。大家都怎么打发时间的？"),
                line("B", "私はいつも本持ってきますよ。あとスマホで動画見てる人も多いですね。",
                     "I always bring a book. Also many people watch videos on their phones.",
                     "我总是带本书。也有很多人看手机视频。"),
                line("A", "一回家に帰ってもいいんですかね？",
                     "Would it be OK to go home and come back?",
                     "回家一趟也行吗？"),
                line("B", "大丈夫ですよ。ただ、終わったらすぐ取り出してくださいね。次の人が待ってることもあるので。",
                     "Sure. But please take it out right away when it's done. Other people might be waiting.",
                     "没问题。但结束了请马上拿出来。可能有人在等着用。"),
                line("A", "そうですよね。じゃあ近くのコンビニ行ってきます。",
                     "Right. I'll go to the convenience store nearby then.",
                     "也是。那我去趟附近的便利店。"),
                line("B", "あ、あそこのコンビニのコーヒーおいしいですよ。おすすめです。",
                     "Oh, the coffee at that convenience store is good. I recommend it.",
                     "啊，那家便利店的咖啡挺好喝的。推荐。"),
            ]),
            section("乾燥の確認", "Checking the drying", "确认烘干", "✨", [
                line("A", "あの、乾燥六十分やったんですけど、ちょっとまだ湿ってる気がするんですよね……。",
                     "Um, I dried it for sixty minutes but I feel like it's still a bit damp...",
                     "那个，烘了六十分钟，但感觉还有点潮……"),
                line("B", "あー、布団は厚いから中まで乾きにくいんですよね。もう十分くらい追加した方がいいかも。",
                     "Ah yeah, futons are thick so it's hard for the inside to dry. Maybe add about ten more minutes.",
                     "啊，被子厚嘛里面不容易干。再追加十分钟比较好。"),
                line("A", "やっぱりそうですか。百円追加しますね。",
                     "I thought so. I'll add another 100 yen.",
                     "果然是这样。追加一百日元。"),
                line("B", "コツがあって、途中で一回出してひっくり返すと均等に乾きますよ。",
                     "Here's a tip — if you take it out once in the middle and flip it, it dries more evenly.",
                     "有个窍门，中途拿出来翻一下会烘得更均匀。"),
                line("A", "えー、そうなんですか。知らなかった。次からそうします。",
                     "Oh really? I didn't know that. I'll do that next time.",
                     "诶，是吗。不知道。下次试试。"),
                line("B", "慣れたら簡単ですよ。月に一回くらい来ると布団もいつもふかふかですよ。",
                     "Once you get used to it, it's easy. Come about once a month and your futon will always be fluffy.",
                     "习惯了就简单了。一个月来一次被子就一直蓬松的。"),
                line("A", "いいですね。ありがとうございます、すごく助かりました。",
                     "Sounds good. Thank you so much, you were a huge help.",
                     "不错。太感谢了，帮了大忙。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n4-hair-salon 理发店
    # ═══════════════════════════════════════════
    {
        "id": "n4-hair-salon-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "三か月ぶりに美容院に行く",
        "titleJp": "三か月ぶりに美容院に行く",
        "titleEn": "Going to the hair salon after three months",
        "titleZh": "时隔三个月去美容院",
        "titleRuby": [],
        "segments": [
            seg("髪が伸びて、前髪が目にかかるようになった。もう三か月も美容院に行っていない。",
                "My hair has grown out and my bangs are getting in my eyes. I haven't been to the salon in three months.",
                "头发长了，刘海都遮到眼睛了。已经三个月没去美容院了。", True),
            seg("いつもの美容院にネットで予約を入れた。土曜日の午後二時。担当は前回と同じ人を指名した。",
                "I made a reservation online at my usual salon. Saturday at 2 PM. I requested the same stylist as last time.",
                "在常去的美容院网上预约了。周六下午两点。指定了上次的同一个发型师。"),
            seg("美容院に着くと、受付の人が「お待ちしていました」と言ってくれた。席に案内された。",
                "When I arrived at the salon, the receptionist said 'We've been expecting you.' I was shown to my seat.",
                "到了美容院，前台说「恭候您了」。被带到了座位。"),
            seg("大きな鏡の前に座ると、美容師が来て「今日はどうしますか」と聞いた。",
                "Sitting in front of the large mirror, the stylist came and asked 'What would you like today?'",
                "坐在大镜子前面，发型师过来问「今天怎么剪」。", True),
            seg("「全体的に短くして、前髪は眉毛くらいにしてください」と伝えた。",
                "I said 'Please cut it shorter overall, and my bangs to about eyebrow length.'",
                "「整体剪短一些，刘海到眉毛左右」。"),
            seg("スマホで見つけた写真を見せた。「こんな感じにしたいんですけど」。美容師は「いいですね、似合うと思いますよ」と言った。",
                "I showed a photo I found on my phone. 'I'd like something like this.' The stylist said 'That looks great, I think it'll suit you.'",
                "给他看了手机上找到的照片。「想剪成这样」。发型师说「不错，应该很适合你」。"),
            seg("まずシャンプー台に案内された。お湯の温度を聞かれて、「ちょうどいいです」と答えた。",
                "First I was taken to the shampoo station. They asked about the water temperature, and I said 'It's just right.'",
                "先被带去了洗头台。问了水温，回答「刚刚好」。", True),
            seg("頭を洗ってもらうのは気持ちいい。プロの手つきは全然違う。力加減がちょうどよくて、眠くなりそうだった。",
                "Having your head washed feels great. A professional's touch is completely different. The pressure was just right and I nearly fell asleep.",
                "让人洗头很舒服。专业的手法就是不一样。力度刚刚好，差点睡着。"),
            seg("席に戻ると、カットが始まった。美容師はハサミを素早く動かしていく。",
                "Back at my seat, the cutting began. The stylist moved the scissors swiftly.",
                "回到座位上开始剪了。发型师迅速地动着剪刀。"),
            seg("鏡を見ると、髪がどんどん短くなっていく。切られた髪が床に落ちていくのを見ると、少しさっぱりした気分になる。",
                "Looking in the mirror, my hair was getting shorter and shorter. Watching the cut hair fall to the floor made me feel refreshed.",
                "看着镜子头发越来越短。看着剪下来的头发落到地上，感觉清爽了不少。", True),
            seg("「最近お仕事忙しいですか」と美容師に聞かれた。美容院での会話は苦手だが、適当に答えた。",
                "'Have you been busy with work recently?' the stylist asked. I'm not good at salon small talk, but I answered casually.",
                "「最近工作忙吗」发型师问。我不擅长在美容院聊天，但随便回答了几句。"),
            seg("カットが終わると、今度はドライヤーで乾かしてくれた。ワックスを少しつけて、形を整えてくれた。",
                "After the cut, they blow-dried my hair. They applied a little wax and styled it.",
                "剪完后用吹风机吹干。抹了一点发蜡，整了整形状。"),
            seg("仕上がりを見て、「いい感じですね」と思った。写真に近い雰囲気になった。",
                "Looking at the finished result, I thought 'This looks good.' It had a vibe similar to the photo.",
                "看了成品觉得「不错嘛」。跟照片的感觉很接近。", True),
            seg("美容師が後ろを手鏡で見せてくれた。「後ろもきれいに揃ってますね」。満足だ。",
                "The stylist showed me the back with a hand mirror. 'The back is neatly trimmed too.' I was satisfied.",
                "发型师用手镜给我看了后面。「后面也修得很整齐」。很满意。"),
            seg("会計は四千五百円だった。カットとシャンプーのセット料金だ。",
                "The bill was 4,500 yen. That's the set price for a cut and shampoo.",
                "费用是四千五百日元。剪发加洗头的套餐价。"),
            seg("次回の予約を聞かれたが、「また連絡します」と答えた。毎回同じことを言ってしまう。",
                "They asked about my next appointment, but I said 'I'll contact you later.' I always say the same thing.",
                "问了下次预约，回答「再联系」。每次都这么说。"),
            seg("店を出ると、風が首筋に当たって涼しかった。髪を切ると、風の感じ方が変わる。",
                "Stepping out of the shop, the wind hit my neck and felt cool. After a haircut, you feel the wind differently.",
                "出了店，风吹到脖子上很凉快。剪完头发风的感觉都不一样了。", True),
            seg("駅のトイレの鏡で、もう一度自分の髪を確認した。やっぱりいい感じだ。",
                "In the station bathroom mirror, I checked my hair once more. It definitely looks good.",
                "在车站厕所的镜子里又看了一下头发。果然不错。"),
            seg("家に帰ると妻が「あ、切ったんだ。さっぱりしたね」と言った。気づいてもらえると嬉しい。",
                "When I got home, my wife said 'Oh, you got a haircut. You look refreshed.' It's nice when someone notices.",
                "到家后妻子说「啊，剪了。清爽了呢」。被注意到就很开心。"),
            seg("次は二か月後くらいに行こう。三か月は少し放置しすぎだった。",
                "I'll go again in about two months. Three months was a bit too long to leave it.",
                "下次两个月左右去吧。三个月还是拖太久了。"),
        ],
    },

    {
        "id": "n4-hair-salon-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "美容院で注文する",
        "titleJp": "美容院で注文する",
        "titleEn": "Ordering at the hair salon",
        "titleZh": "在美容院说怎么剪",
        "titleRuby": [],
        "sections": [
            section("カウンセリング", "Consultation", "沟通", "💇", [
                line("A", "今日はどうされますか？",
                     "What would you like today?",
                     "今天怎么剪？"),
                line("B", "えーと、全体的にちょっと短くしたいんですけど。あと前髪が長くなっちゃって。",
                     "Um, I'd like it a bit shorter overall. And my bangs have gotten too long.",
                     "嗯，整体想短一点。还有刘海太长了。"),
                line("A", "どのくらい切りますか？三センチくらい？",
                     "How much should I take off? About three centimeters?",
                     "剪多少？三厘米左右？"),
                line("B", "うーん、もうちょっと切ってほしいかな。五センチくらい？あ、これ参考の写真なんですけど。",
                     "Hmm, I'd like a bit more off. About five centimeters? Oh, here's a reference photo.",
                     "嗯，再多剪点。五厘米？啊，这是参考的照片。"),
                line("A", "ああ、いいですね。すっきりした感じで。お客様の髪質だと似合うと思いますよ。",
                     "Oh, that's nice. A clean look. I think it'll suit your hair type.",
                     "啊，不错。很利落的感觉。以您的发质应该很合适。"),
                line("B", "ほんとですか？じゃあこんな感じでお願いします。あ、横は耳にかからないくらいで。",
                     "Really? Then please do it like this. Oh, and the sides shouldn't cover my ears.",
                     "真的吗？那就按这个来。啊，两边不要盖住耳朵。"),
                line("A", "分かりました。カラーはどうされますか？",
                     "Got it. How about coloring?",
                     "好的。要染色吗？"),
                line("B", "今日はカットだけでお願いします。",
                     "Just a cut today, please.",
                     "今天只剪就好。"),
            ]),
            section("カット中", "During the cut", "剪发中", "✂️", [
                line("A", "最近お仕事忙しいですか？",
                     "Have you been busy with work lately?",
                     "最近工作忙吗？"),
                line("B", "まあ、それなりに。年度末でバタバタしてて、やっと落ち着いたんで来れました。",
                     "Well, reasonably. It was hectic around the end of the fiscal year, so I finally got a chance to come.",
                     "算是吧。年末忙得不行，终于消停了才来。"),
                line("A", "三か月ぶりですもんね。結構伸びてましたね。",
                     "It's been three months, right? It really grew out.",
                     "三个月了吧。长了不少。"),
                line("B", "ですよね。もっとこまめに来なきゃとは思うんですけど、つい後回しにしちゃって。",
                     "Right. I keep telling myself to come more often, but I always put it off.",
                     "是啊。想着要勤快点来，但总是拖。"),
                line("A", "お客様の髪、くせが少しあるので、ここをすいて軽くしますね。",
                     "Your hair has a slight wave, so I'll thin it out here to lighten it.",
                     "您的头发有点自来卷，这里打薄一下。"),
                line("B", "はい、お任せします。いつもセットしにくいんですよね、そこ。",
                     "OK, I'll leave it to you. That part is always hard to style.",
                     "好的，交给你了。那里每次都不好打理。"),
            ]),
            section("仕上げ", "Finishing up", "最后整理", "💈", [
                line("A", "はい、こんな感じになりました。後ろも見ますか？",
                     "OK, here's how it turned out. Want to see the back?",
                     "好，剪成这样了。要看后面吗？"),
                line("B", "お願いします。……うん、いい感じです。写真に近いですね。",
                     "Please. ...Yeah, it looks good. Close to the photo.",
                     "麻烦了。……嗯，不错。跟照片很像。"),
                line("A", "ワックスつけますか？普段使ってますか？",
                     "Shall I put some wax on? Do you usually use it?",
                     "要抹发蜡吗？平时用吗？"),
                line("B", "休みの日は使わないんですけど、仕事の日は少しだけ。今日はお願いします。",
                     "I don't use it on days off, but a little on work days. Yes please today.",
                     "休息日不用，上班时抹一点。今天帮我抹一下。"),
                line("A", "少しだけつけて、自然な感じにしますね。……はい、これでどうですか？",
                     "I'll put on just a little for a natural look. ...There, how's this?",
                     "抹一点点，弄成自然的感觉。……好，这样怎么样？"),
                line("B", "完璧です。ありがとうございます。次はもうちょっと早めに来ますね。",
                     "Perfect. Thank you. I'll come a bit earlier next time.",
                     "完美。谢谢。下次早点来。"),
                line("A", "お待ちしてます。次回ご予約も取れますけど、どうされますか？",
                     "We'll be waiting. You can also book your next appointment now — would you like to?",
                     "恭候您。下次也可以现在预约，怎么样？"),
                line("B", "えーと……また連絡します。いつもすみません。",
                     "Um... I'll contact you later. Sorry, I always say that.",
                     "嗯……再联系吧。每次都不好意思。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-cinema 电影院
    # ═══════════════════════════════════════════
    {
        "id": "n4-cinema-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "久しぶりに映画館で映画を見る",
        "titleJp": "久しぶりに映画館で映画を見る",
        "titleEn": "Watching a movie at the cinema after a long time",
        "titleZh": "久违地在电影院看电影",
        "titleRuby": [],
        "segments": [
            seg("最近話題のアニメ映画があって、ずっと気になっていた。友達も「すごくよかった」と言っていた。",
                "There's been a popular anime movie recently that I'd been curious about. My friend said 'It was amazing.'",
                "最近有部很火的动画电影，一直很在意。朋友也说「特别好看」。", True),
            seg("映画館で見るのは半年ぶりだ。最近はサブスクで見ることが多くて、わざわざ映画館に行くことが減った。",
                "It's been half a year since I last saw a movie in a theater. Lately I watch mostly on streaming, so I rarely bother going to the cinema.",
                "半年没去电影院了。最近都是看流媒体，特意去电影院的次数少了。"),
            seg("でも友達が「これは絶対映画館で見た方がいい。音がすごい」と言うので、行くことにした。",
                "But my friend said 'You absolutely should see this one in theaters. The sound is incredible,' so I decided to go.",
                "但朋友说「这部一定要在电影院看。音效太厉害了」，就决定去了。"),
            seg("ネットでチケットを予約した。土曜日の夕方の回を選んだ。席は真ん中あたりを取った。",
                "I booked tickets online. I chose the Saturday evening showing and picked seats around the middle.",
                "网上订了票。选了周六傍晚的场次。座位选了中间附近。", True),
            seg("映画館に着いたのは上映の三十分前だった。ロビーはかなり混んでいた。",
                "I arrived thirty minutes before showtime. The lobby was quite crowded.",
                "到电影院的时候离开场还有三十分钟。大厅相当拥挤。"),
            seg("発券機でチケットを発行した。QRコードをかざすだけで簡単だった。",
                "I printed my ticket at the kiosk. Just scanning the QR code — it was easy.",
                "在取票机上出了票。扫一下二维码就行，很简单。"),
            seg("売店でポップコーンとコーラを買った。Mサイズのセットで七百円。映画館の値段は高い。",
                "I bought popcorn and a cola at the snack bar. A medium combo for 700 yen. Cinema prices are steep.",
                "在卖品部买了爆米花和可乐。中号套餐七百日元。电影院价格就是贵。", True),
            seg("でも映画にポップコーンは欠かせない。塩味にした。キャラメル味と迷ったが、いつも塩味を選んでしまう。",
                "But popcorn is essential for movies. I went with salt flavor. I debated caramel but always end up choosing salt.",
                "但看电影不能没有爆米花。选了盐味。和焦糖味纠结了一下，但每次都选盐味。"),
            seg("スクリーン番号を確認して、六番に向かった。入り口でチケットを見せて中に入る。",
                "I checked the screen number and headed to screen six. I showed my ticket at the entrance and went in.",
                "确认了放映厅号码，去了六号厅。在入口出示了票进去了。"),
            seg("中は暗くて、予告編が流れていた。席を見つけて座った。座り心地がよくて、リクライニングもできる。",
                "Inside it was dark and trailers were playing. I found my seat and sat down. The seat was comfortable and could recline.",
                "里面很暗，正在放预告片。找到座位坐下了。座位很舒服，还能调角度。", True),
            seg("上映が始まった。最初の数分で引き込まれた。画面が大きくて迫力がある。",
                "The movie began. I was drawn in within the first few minutes. The big screen was powerful.",
                "电影开始了。开头几分钟就被吸引了。画面好大好震撼。"),
            seg("音響もすごかった。友達が言っていた通りだ。家のテレビでは味わえない臨場感がある。",
                "The sound was incredible too. Just like my friend said. There's an immersive feeling you can't get from a TV at home.",
                "音效也很厉害。跟朋友说的一样。有在家电视体会不到的临场感。"),
            seg("途中で泣きそうになったが、周りの人もすすり泣いていたので安心した。",
                "I almost cried partway through, but others around me were sniffling too, so I felt OK.",
                "中间差点哭了，但周围也有人在抽泣，就安心了。", True),
            seg("気づいたらポップコーンを全部食べてしまっていた。映画に集中すると手が止まらない。",
                "Before I knew it I'd eaten all the popcorn. When I focus on a movie my hands don't stop.",
                "不知不觉爆米花全吃完了。一集中看电影手就停不下来。"),
            seg("二時間の映画はあっという間だった。エンドロールが流れても、すぐには立てなかった。",
                "The two-hour movie flew by. Even when the credits rolled, I couldn't get up right away.",
                "两个小时的电影一眨眼就过了。字幕出来了也一时站不起来。"),
            seg("明るくなって周りを見ると、みんな同じ余韻に浸っているようだった。",
                "When the lights came on and I looked around, everyone seemed to be basking in the same afterglow.",
                "灯亮了看看周围，大家好像都沉浸在同样的余韻里。", True),
            seg("映画館を出て、すぐに友達にメッセージを送った。「見てきた。最高だった」。",
                "Leaving the cinema, I immediately messaged my friend. 'Just watched it. It was the best.'",
                "走出电影院，马上给朋友发了消息。「看了。太棒了」。"),
            seg("友達はすぐに返事をくれた。「でしょ？あのシーン、やばかったよね」。どのシーンのことか、すぐに分かった。",
                "My friend replied right away. 'Right? That scene was insane.' I knew exactly which scene they meant.",
                "朋友马上回了。「吧？那个场景太绝了」。我立刻知道说的是哪个场景。"),
            seg("帰りの電車の中で、映画のサントラを聴いた。場面が目に浮かんでくる。",
                "On the train home, I listened to the movie soundtrack. The scenes came flooding back.",
                "回去的电车上听了电影的原声带。画面浮现在眼前。", True),
            seg("やっぱり映画は映画館で見るのがいい。サブスクは便利だが、あの大画面と音響は特別だ。",
                "Movies really are best in a theater. Streaming is convenient, but that big screen and sound are special.",
                "电影果然还是在电影院看好。流媒体方便，但那个大银幕和音效是不一样的。"),
            seg("来月も気になる映画がある。今度は妻と一緒に見に行こうと思う。",
                "There's another movie I'm curious about next month. I think I'll go see it with my wife.",
                "下个月也有部在意的电影。下次打算和妻子一起去看。"),
        ],
    },

    {
        "id": "n4-cinema-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "映画を見に行こう",
        "titleJp": "映画を見に行こう",
        "titleEn": "Let's go see a movie",
        "titleZh": "一起去看电影吧",
        "titleRuby": [],
        "sections": [
            section("チケットを取る", "Getting tickets", "买票", "🎬", [
                line("A", "ねえ、あのアニメ映画もう見た？",
                     "Hey, have you seen that anime movie yet?",
                     "诶，那部动画电影看了吗？"),
                line("B", "まだ。気になってるんだけど、一人で行くのもなんかなーと思って。",
                     "Not yet. I'm interested but going alone feels a bit...",
                     "还没。一直想看，但一个人去总觉得……"),
                line("A", "じゃあ一緒に行かない？土曜の夕方とかどう？",
                     "Then wanna go together? How about Saturday evening?",
                     "那一起去？周六傍晚怎么样？"),
                line("B", "いいね！チケットはネットで取れる？",
                     "Sounds good! Can we get tickets online?",
                     "好啊！票能网上买吗？"),
                line("A", "うん、アプリで取った方が席も選べるし楽だよ。真ん中らへんがいいよね？",
                     "Yeah, it's easier to use the app since you can pick seats. Middle area good?",
                     "嗯，用App买还能选座，方便。中间附近好吧？"),
                line("B", "うん。あ、ポップコーンセットのクーポンもあるみたいだよ。",
                     "Yeah. Oh, looks like there's a popcorn set coupon too.",
                     "好。啊，好像还有爆米花套餐的优惠券。"),
                line("A", "マジ？使おう使おう。映画にポップコーンは絶対でしょ。",
                     "Seriously? Let's use it. Popcorn at the movies is a must.",
                     "真的？用用用。看电影必须有爆米花。"),
            ]),
            section("映画館にて", "At the cinema", "在电影院", "🍿", [
                line("B", "わー、結構混んでるね。人気あるんだなあ。",
                     "Wow, it's pretty crowded. It must be popular.",
                     "哇，人好多。真有人气。"),
                line("A", "だね。あ、先にポップコーン買おうよ。並んでる間に上映始まったら嫌だし。",
                     "Yeah. Hey, let's buy popcorn first. I don't want the movie to start while we're still in line.",
                     "是啊。先去买爆米花吧。排着排着开场就麻烦了。"),
                line("B", "塩とキャラメル、どっちにする？",
                     "Salt or caramel — which one?",
                     "盐味还是焦糖？"),
                line("A", "俺は塩派。キャラメルは甘すぎるんだよね。",
                     "I'm team salt. Caramel is too sweet for me.",
                     "我选盐味。焦糖太甜了。"),
                line("B", "じゃあ私はキャラメルにしよ。たまにはね。",
                     "Then I'll go with caramel. As a treat.",
                     "那我选焦糖。偶尔嘛。"),
                line("A", "お、もう入れるみたいだよ。チケット出して。",
                     "Oh, looks like we can go in now. Get your ticket out.",
                     "哦，好像可以进了。票拿出来。"),
                line("B", "ここの席だよね。わ、リクライニングできるんだ。すごい。",
                     "Our seats are here, right? Oh wow, they recline. Amazing.",
                     "是这个座位吧。哇，还能调角度。厉害。"),
            ]),
            section("映画の後", "After the movie", "看完之后", "🌙", [
                line("B", "やばい、めっちゃよかった……。あのラストのシーンで泣いちゃった。",
                     "That was incredible... I cried at that last scene.",
                     "太棒了……最后那个场景哭了。"),
                line("A", "俺も。隣でおじさんも泣いてたよ。",
                     "Me too. The guy next to me was crying too.",
                     "我也是。旁边的大叔也在哭。"),
                line("B", "音響がすごかったよね。あの戦闘シーン、お腹に響いた。",
                     "The sound was amazing, right? That battle scene — I felt it in my stomach.",
                     "音效太厉害了。那个战斗场景，肚子都在震。"),
                line("A", "やっぱ映画館で見てよかったわ。サブスクだとあの迫力は出ないもん。",
                     "Glad we watched it in theaters. You can't get that impact on streaming.",
                     "果然在电影院看对了。流媒体出不来那种震撼。"),
                line("B", "ほんとそれ。あ、来月も新作出るみたいだよ。実写のやつ。",
                     "So true. Oh, a new movie is coming out next month too. A live-action one.",
                     "真的。啊，下个月好像也有新片。真人版的。"),
                line("A", "また行こうよ。今度は飯も食べに行かない？映画のあとのご飯って最高じゃん。",
                     "Let's go again. Wanna grab dinner too this time? Eating after a movie is the best.",
                     "再去吧。下次也去吃饭？看完电影去吃饭最棒了。"),
                line("B", "いいね！じゃあ来月も予定空けとく。",
                     "Sounds great! I'll keep my schedule open next month then.",
                     "好啊！那下个月留着时间。"),
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
