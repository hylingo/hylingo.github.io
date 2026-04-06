#!/usr/bin/env python3
"""
batch13 → public/data/ja_articles.json

第1轮重写C: 3组场景 (6篇)
- n4-supermarket (超市购物)
- n4-restaurant (餐厅吃饭)
- n4-cafe-work (咖啡店办公)

运行: python3 scripts/append_ja_articles_batch13.py
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
    # 1. n4-supermarket 超市购物
    # ═══════════════════════════════════════════
    {
        "id": "n4-supermarket-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "閉店間際のスーパーで買い物する",
        "titleJp": "閉店間際のスーパーで買い物する",
        "titleEn": "Shopping at the supermarket right before closing",
        "titleZh": "快打烊时在超市购物",
        "titleRuby": [],
        "segments": [
            seg("仕事が終わって、スーパーに寄った。もう夜の八時半で、閉店は九時だ。",
                "After work I stopped by the supermarket. It was already 8:30 PM, and they close at nine.",
                "下班后顺路去了超市。已经晚上八点半了，九点关门。", True),
            seg("冷蔵庫の中がほとんど空だったので、まとめて買い物をしなければならない。",
                "The fridge was nearly empty, so I needed to do a big grocery run.",
                "冰箱里几乎空了，得一次性多买点。"),
            seg("入り口に「本日のお買い得」と書かれた看板があった。卵が十個で百九十八円。安い。",
                "At the entrance there was a sign saying 'Today's Deals.' Eggs were 198 yen for ten. Cheap.",
                "入口有块写着「今日特价」的牌子。鸡蛋十个一百九十八日元。便宜。"),
            seg("カゴを取って、まず野菜コーナーに向かった。キャベツとにんじんとたまねぎを入れた。今週はカレーを作るつもりだ。",
                "I grabbed a basket and headed to the vegetable section first. I put in cabbage, carrots, and onions. I plan to make curry this week.",
                "拿了个篮子，先去了蔬菜区。放了卷心菜、胡萝卜和洋葱。这周打算做咖喱。"),
            seg("じゃがいもも必要だと思い出して、戻って二つ取った。カレーにじゃがいもがないと寂しい。",
                "I remembered I needed potatoes too and went back to grab two. Curry without potatoes feels incomplete.",
                "想起来还需要土豆，回去拿了两个。咖喱没有土豆总觉得缺点什么。", True),
            seg("肉売り場に行くと、閉店前の値引きシールが貼られていた。豚肉が三割引、鶏もも肉が半額になっている。",
                "At the meat section, discount stickers had been applied before closing. Pork was 30% off, chicken thigh was half price.",
                "到了肉类区，打烊前的折扣贴纸已经贴上了。猪肉七折，鸡腿肉半价。"),
            seg("半額の鶏肉を二パック取った。一パックは冷凍すれば来週も使える。",
                "I grabbed two packs of the half-price chicken. If I freeze one pack, I can use it next week too.",
                "拿了两盒半价鸡肉。冻一盒下周还能用。"),
            seg("お惣菜コーナーも値引きが始まっていた。コロッケが三個で百五十円。今日の夕飯はこれでいい。",
                "The deli section had also started discounting. Croquettes were 150 yen for three. This will do for tonight's dinner.",
                "熟食区也开始打折了。炸肉饼三个一百五十日元。今晚的晚饭就它了。"),
            seg("隣の棚にはサラダも半額で並んでいた。ポテトサラダを一つ追加した。",
                "On the shelf next to it, salads were also half price. I added a potato salad.",
                "旁边的架子上沙拉也半价了。加了一份土豆沙拉。", True),
            seg("飲み物の棚で麦茶を探したが、売り切れだった。仕方なくウーロン茶にした。",
                "I looked for barley tea on the drink shelf, but it was sold out. I settled for oolong tea instead.",
                "在饮料货架上找麦茶，卖完了。只好换了乌龙茶。"),
            seg("ついでに牛乳とヨーグルトも取った。朝ごはん用に毎週買っている。",
                "I also grabbed milk and yogurt while I was at it. I buy them every week for breakfast.",
                "顺便拿了牛奶和酸奶。每周都买来当早饭。"),
            seg("レジに並ぶと、前に三人いた。みんなカゴがいっぱいだ。閉店前はみんな考えることが同じらしい。",
                "When I lined up at the register, three people were ahead of me. Everyone's baskets were full. Seems everyone thinks alike before closing.",
                "排收银台前面有三个人。大家篮子都满满的。快打烊时大家想的都一样。", True),
            seg("セルフレジが空いていたので、そちらに移った。最近はセルフレジの方が早いことが多い。",
                "The self-checkout was open so I moved over. Recently self-checkout is often faster.",
                "自助收银台空着就过去了。最近自助收银往往更快。"),
            seg("店員が「袋はご利用ですか」と聞いた。エコバッグを持ってきたので「大丈夫です」と答えた。",
                "The clerk asked 'Would you like a bag?' I brought my eco bag so I said 'I'm fine.'",
                "店员问「需要袋子吗」。带了环保袋就说「不用了」。"),
            seg("合計で千八百円ほどだった。値引きのおかげで、普段より五百円くらい安く済んだ。",
                "The total was about 1,800 yen. Thanks to discounts, it was about 500 yen cheaper than usual.",
                "总共大概一千八百日元。多亏了打折，比平时便宜了五百日元左右。"),
            seg("エコバッグに詰めていると、店内放送が流れた。「まもなく閉店のお時間です。お買い忘れはございませんか」。",
                "As I was packing my eco bag, an announcement played. 'We will be closing soon. Have you forgotten anything?'",
                "正往环保袋里装东西，店内广播响了。「即将到打烊时间。有没有忘买的东西」。", True),
            seg("急いで店を出た。外はもう暗くて、少し肌寒かった。エコバッグが重くて、肩にずっしり来る。",
                "I hurried out of the store. It was already dark outside and a bit chilly. The eco bag was heavy on my shoulder.",
                "赶紧出了店。外面已经黑了，有点凉。环保袋沉甸甸地压着肩膀。"),
            seg("家に帰って冷蔵庫に食材をしまった。鶏肉は一パック分をラップに包んで冷凍庫に入れた。",
                "I got home and put the groceries in the fridge. I wrapped one pack of chicken in plastic wrap and put it in the freezer.",
                "到家后把食材放进冰箱。鸡肉一盒用保鲜膜包好放进了冷冻室。"),
            seg("コロッケをレンジで温めて食べた。スーパーの惣菜だけど、揚げたてみたいでおいしかった。",
                "I microwaved the croquettes and ate them. They're just supermarket deli food, but they tasted like they were freshly fried.",
                "用微波炉热了炸肉饼吃了。虽然是超市熟食，但像刚炸的一样好吃。", True),
            seg("ポテトサラダも開けた。半額で買ったけど、味は全然問題ない。むしろ手作りよりうまい。",
                "I opened the potato salad too. I bought it half price but the taste was perfectly fine. Better than homemade, even.",
                "土豆沙拉也打开了。虽然半价买的，味道完全没问题。甚至比自己做的好吃。"),
            seg("閉店間際の買い物は値引きが多くてお得だが、品切れも多い。早く行くか遅く行くか、毎回迷う。",
                "Shopping right before closing has lots of discounts so it's a good deal, but many things are sold out. I can never decide whether to go early or late.",
                "快打烊时购物折扣多很划算，但缺货也多。每次都纠结早去还是晚去。"),
            seg("明日は早めに来て、ちゃんと麦茶を買おう。",
                "Tomorrow I'll come early and properly buy barley tea.",
                "明天早点来，好好买上麦茶。"),
        ],
    },

    {
        "id": "n4-supermarket-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "スーパーでばったり会う",
        "titleJp": "スーパーでばったり会う",
        "titleEn": "Running into someone at the supermarket",
        "titleZh": "在超市偶遇",
        "titleRuby": [],
        "sections": [
            section("偶然の再会", "Chance meeting", "偶然碰面", "🛒", [
                line("A", "あれ、田中さん？こんなところで会うなんて。",
                     "Huh, Tanaka-san? Fancy meeting you here.",
                     "咦，田中？在这遇到你了。"),
                line("B", "あ、久しぶり！このスーパーよく来るの？",
                     "Oh, long time no see! Do you come to this supermarket often?",
                     "啊，好久不见！你经常来这个超市吗？"),
                line("A", "うん、閉店前が狙い目なんだよね。値引きシール貼ってあるから。",
                     "Yeah, right before closing is the sweet spot. They put discount stickers on.",
                     "嗯，快打烊的时候来比较好。会贴折扣贴纸。"),
                line("B", "わかる！私も半額シール目当てで来たの。見て、この鶏肉、半額だよ。",
                     "I know! I came for the half-price stickers too. Look, this chicken is half off.",
                     "懂！我也是冲着半价贴纸来的。你看，这鸡肉半价。"),
                line("A", "おお、いいな。俺もさっき二パック取った。一つ冷凍する。",
                     "Nice. I grabbed two packs too. I'll freeze one.",
                     "哦，不错。我也拿了两盒。冻一盒。"),
                line("B", "考えること一緒だね。あ、お惣菜のコロッケも安くなってるよ。",
                     "We think alike. Oh, the deli croquettes are discounted too.",
                     "想法一样啊。啊，熟食区的炸肉饼也便宜了。"),
            ]),
            section("買い物の相談", "Shopping chat", "聊购物", "🥕", [
                line("A", "田中さん、自炊してるんだ？料理できるイメージなかったけど。",
                     "Tanaka-san, you cook for yourself? I didn't picture you as a cook.",
                     "田中你自己做饭啊？没想到你会做饭。"),
                line("B", "失礼な！まあ、簡単なものだけだけどね。カレーとか炒め物とか。",
                     "How rude! Well, only simple stuff. Curry, stir-fry, things like that.",
                     "好过分！嘛，只做简单的。咖喱啊炒菜什么的。"),
                line("A", "あ、俺も今週カレー作るつもり。にんじんとたまねぎ買った。",
                     "Oh, I'm planning to make curry this week too. Got carrots and onions.",
                     "啊，我这周也打算做咖喱。买了胡萝卜和洋葱。"),
                line("B", "じゃがいもは？カレーにじゃがいも入れない派？",
                     "What about potatoes? Are you the no-potatoes-in-curry type?",
                     "土豆呢？你是咖喱不放土豆派？"),
                line("A", "あ、忘れてた！ちょっと取ってくる。",
                     "Oh, I forgot! Let me go grab some.",
                     "啊，忘了！我去拿一下。"),
                line("B", "ふふ、危なかった。あとルーはどこのがおすすめ？いつも同じやつ買っちゃうんだけど。",
                     "Haha, that was close. Also which brand of roux do you recommend? I always buy the same one.",
                     "呵呵，好险。还有咖喱块你推荐哪个牌子？我老买同一种。"),
                line("A", "俺はジャワカレーの中辛。辛すぎず、ちょうどいいんだよね。",
                     "I go with Java Curry medium hot. Not too spicy, just right.",
                     "我用爪哇咖喱中辣的。不会太辣，刚刚好。"),
            ]),
            section("レジと帰り道", "Checkout and heading home", "结账和回家", "🏠", [
                line("B", "あ、もう閉店五分前だ。急いでレジ行こう。",
                     "Oh, it's five minutes until closing. Let's hurry to the register.",
                     "啊，离打烊还有五分钟了。赶紧去收银台。"),
                line("A", "袋持ってきた？",
                     "Did you bring a bag?",
                     "带袋子了吗？"),
                line("B", "あ、忘れた……。三円の袋もらおうかな。",
                     "Oh, I forgot... I'll get the three-yen bag I guess.",
                     "啊，忘了……买个三日元的袋子吧。"),
                line("A", "エコバッグ、二つ持ってるから一つ貸すよ。",
                     "I have two eco bags so I'll lend you one.",
                     "我有两个环保袋，借你一个。"),
                line("B", "ありがとう、助かる！今度返すね。",
                     "Thanks, that helps! I'll return it next time.",
                     "谢谢，太好了！下次还你。"),
                line("A", "いいよ、今度コーヒーおごってくれたら。",
                     "It's fine, just treat me to coffee next time.",
                     "没事，下次请我喝杯咖啡就行。"),
                line("B", "了解。じゃあ、また閉店前に会うかもね。",
                     "Deal. Well, maybe we'll meet again before closing time.",
                     "收到。那说不定又会在打烊前碰到。"),
                line("A", "はは、そうかも。じゃ、気をつけて。",
                     "Haha, maybe so. Well, take care.",
                     "哈哈，说不定。那路上小心。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n4-restaurant 餐厅吃饭
    # ═══════════════════════════════════════════
    {
        "id": "n4-restaurant-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "初めての居酒屋で注文する",
        "titleJp": "初めての居酒屋で注文する",
        "titleEn": "Ordering at an izakaya for the first time",
        "titleZh": "第一次在居酒屋点餐",
        "titleRuby": [],
        "segments": [
            seg("会社の同僚に誘われて、駅の近くの居酒屋に行った。初めての店だったので少し緊張した。",
                "A colleague from work invited me to an izakaya near the station. It was my first time at this place so I was a bit nervous.",
                "被公司同事约了去车站附近的居酒屋。第一次去那家店，有点紧张。", True),
            seg("入り口は小さくて、のれんをくぐって入る。中は思ったより広かった。",
                "The entrance was small, and you enter by ducking under a noren curtain. Inside was more spacious than expected.",
                "入口很小，掀开门帘进去。里面比想象中宽敞。"),
            seg("「二名です」と言うと、店員が「カウンターでもよろしいですか」と聞いた。「大丈夫です」と答えた。",
                "I said 'Two people' and the staff asked 'Is the counter OK?' I said 'That's fine.'",
                "说了「两位」，店员问「吧台可以吗」。回答说「可以」。"),
            seg("席に着くと、おしぼりとメニューが出てきた。メニューは壁にも手書きで貼ってある。今日のおすすめは鯵の刺身らしい。",
                "Once seated, we were given wet towels and menus. The menu was also handwritten on the wall. Today's special seems to be horse mackerel sashimi.",
                "坐下后拿到了湿毛巾和菜单。墙上也贴着手写的菜单。今日推荐好像是竹荚鱼刺身。", True),
            seg("まず「とりあえず生ビール二つ」と頼んだ。居酒屋ではこれが定番の最初の注文らしい。",
                "First we ordered 'two draft beers to start.' This is apparently the standard first order at an izakaya.",
                "先点了「先来两杯生啤」。居酒屋好像都是这样开场的。"),
            seg("つまみは枝豆と冷やしトマトにした。同僚は「焼き鳥の盛り合わせも頼もうよ」と言った。",
                "For snacks we got edamame and chilled tomatoes. My colleague said 'Let's order the grilled chicken skewer platter too.'",
                "小菜点了毛豆和冰番茄。同事说「也点个烤鸡肉串拼盘吧」。"),
            seg("焼き鳥は塩とタレが選べる。塩三本、タレ三本の盛り合わせを注文した。",
                "The yakitori could be ordered with salt or sauce. We ordered a platter of three salt and three sauce skewers.",
                "烤鸡肉串可以选盐味或酱汁。点了盐味三串酱汁三串的拼盘。"),
            seg("ビールが来て乾杯した。「お疲れさまです」。冷たいビールが喉を通るとき、今日の疲れが消えていくようだった。",
                "The beer came and we toasted. 'Cheers to a hard day's work.' As the cold beer went down my throat, the day's fatigue seemed to melt away.",
                "啤酒来了干杯。「辛苦了」。冰啤酒过喉的时候，今天的疲劳好像都消失了。", True),
            seg("枝豆をつまみながら仕事の話をした。来月のプロジェクトのことや、上司の愚痴。",
                "We chatted about work while picking at edamame. About next month's project and complaining about the boss.",
                "一边吃毛豆一边聊工作。下个月的项目啊，吐槽上司啊。"),
            seg("焼き鳥が来た。炭火で焼いてあって、香ばしい匂いがした。塩の方がシンプルでおいしい。",
                "The yakitori arrived. Grilled over charcoal, it smelled savory. The salt ones were simpler and tastier.",
                "烤鸡肉串来了。用炭火烤的，闻着好香。盐味的更简单更好吃。"),
            seg("カウンターの向こうで大将が焼き鳥を焼いている。煙がもくもく上がって、いい雰囲気だ。",
                "Behind the counter the chef was grilling yakitori. Smoke billowed up, creating a great atmosphere.",
                "吧台那边师傅在烤鸡肉串。烟雾腾腾的，气氛很好。", True),
            seg("二杯目はハイボールにした。メニューに「角ハイボール」と書いてあったので、それにした。",
                "For my second drink I went with a highball. The menu said 'Kaku Highball' so I ordered that.",
                "第二杯换了威士忌苏打。菜单上写着「角High Ball」，就点了那个。"),
            seg("同僚は日本酒を頼んでいた。「この店、日本酒の種類が多いんだよ」と嬉しそうだった。",
                "My colleague ordered sake. 'This place has lots of kinds of sake,' he said happily.",
                "同事点了日本酒。「这家店日本酒种类很多呢」一脸高兴。"),
            seg("追加で刺身の盛り合わせとだし巻き卵を頼んだ。だし巻き卵はふわふわで、出汁の味がしっかりしていた。",
                "We added a sashimi platter and rolled egg with dashi. The egg was fluffy with a rich dashi flavor.",
                "又加点了刺身拼盘和日式鸡蛋卷。鸡蛋卷松松软软的，高汤味道很浓。"),
            seg("刺身はマグロとサーモンとハマチの三種盛りだった。ワサビを少しつけて醤油で食べる。新鮮でうまい。",
                "The sashimi was a three-kind platter of tuna, salmon, and yellowtail. I dipped it in soy sauce with a touch of wasabi. Fresh and delicious.",
                "刺身是金枪鱼、三文鱼和鰤鱼三拼。蘸一点芥末用酱油吃。新鲜好吃。", True),
            seg("隣の席の常連客が大将と楽しそうに話していた。こういう雰囲気が居酒屋のいいところだ。",
                "The regular at the next seat was chatting happily with the chef. This kind of atmosphere is what makes izakayas great.",
                "旁边座位的老顾客和师傅聊得很开心。这种氛围就是居酒屋的好处。"),
            seg("気づいたら二時間経っていた。会計を頼むと、一人三千五百円ほどだった。割り勘にした。",
                "Before I knew it, two hours had passed. When we asked for the bill, it was about 3,500 yen per person. We split it.",
                "不知不觉过了两小时。结账一个人大概三千五百日元。AA了。", True),
            seg("レジで「ごちそうさまでした」と言うと、店員が「またお越しください」と笑った。",
                "At the register I said 'Thank you for the meal' and the staff smiled saying 'Please come again.'",
                "收银台说了「谢谢招待」，店员笑着说「欢迎再来」。"),
            seg("外に出ると、夜風が気持ちよかった。少し酔っていたが、歩けないほどではない。",
                "Stepping outside, the night breeze felt nice. I was a little tipsy but not too drunk to walk.",
                "出来后晚风很舒服。有点醉但还走得了路。"),
            seg("帰り道、「また来月も行こうよ」と同僚が言った。いい店を見つけた。",
                "On the way back, my colleague said 'Let's come again next month.' We found a good spot.",
                "回去路上同事说「下个月也来吧」。找到了家好店。"),
            seg("家に着いて歯を磨きながら、今度は友達も誘おうと思った。",
                "Arriving home and brushing my teeth, I thought I'd invite friends next time.",
                "到家刷牙的时候，想着下次也叫朋友来。"),
        ],
    },

    {
        "id": "n4-restaurant-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "居酒屋でわいわい",
        "titleJp": "居酒屋でわいわい",
        "titleEn": "Having a blast at the izakaya",
        "titleZh": "居酒屋热闹一番",
        "titleRuby": [],
        "sections": [
            section("席に着く", "Taking a seat", "入座", "🍺", [
                line("A", "お、いい感じの店じゃん。カウンターでいい？",
                     "Oh, this is a nice place. Counter OK?",
                     "哦，这店不错嘛。吧台行吗？"),
                line("B", "うん、全然いいよ。メニューどこだろ……あ、壁に書いてあるんだ。",
                     "Yeah, totally fine. Where's the menu... Oh, it's on the wall.",
                     "嗯，完全可以。菜单在哪……啊，写在墙上了。"),
                line("A", "とりあえず生二つでよくない？",
                     "Shall we just start with two drafts?",
                     "先来两杯生啤？"),
                line("B", "もちろん。あと枝豆と……焼き鳥も頼もうよ。塩とタレ、どっちがいい？",
                     "Of course. Plus edamame and... let's order yakitori too. Salt or sauce, which do you prefer?",
                     "当然。再来毛豆和……烤鸡肉串也点吧。盐味还是酱汁？"),
                line("A", "迷うなー。半々にしない？塩三本、タレ三本で。",
                     "Hmm tough call. How about half and half? Three salt, three sauce.",
                     "纠结。各半怎么样？盐味三串酱汁三串。"),
                line("B", "いいね、それで。すみませーん、注文いいですか？",
                     "Sounds good. Excuse me, can we order?",
                     "好，就这样。不好意思，可以点单吗？"),
            ]),
            section("飲みながら", "While drinking", "边喝边聊", "🍶", [
                line("A", "かんぱーい。ぷはー、やっぱ仕事の後のビールは最高だな。",
                     "Cheers! Ahh, beer after work really is the best.",
                     "干杯！哈——果然下班后的啤酒最棒了。"),
                line("B", "ほんとそれ。今日めちゃくちゃ忙しかったもん。会議三つもあってさ。",
                     "So true. Today was insanely busy. I had three meetings.",
                     "就是说。今天忙死了。开了三个会。"),
                line("A", "うわ、きつ。俺は部長に資料やり直せって言われて、二回も作り直したよ。",
                     "Ugh, brutal. My department head told me to redo the materials, and I had to remake them twice.",
                     "哇，惨。我被部长说资料重做，改了两遍。"),
                line("B", "あるある。あ、焼き鳥来たよ。おー、炭火の匂いがいいね。",
                     "Yeah that happens. Oh, the yakitori is here. Ooh, smells great, that charcoal aroma.",
                     "经常的事。啊，烤鸡肉串来了。哦，炭火味好香。"),
                line("A", "塩うまっ。シンプルだけど、こっちの方が好きかも。",
                     "The salt ones are great! Simple but I might prefer these.",
                     "盐味好吃！虽然简单，但可能更喜欢这个。"),
                line("B", "タレも捨てがたいけどね。次なに飲む？俺はハイボールにしよっかな。",
                     "But the sauce ones are hard to give up. What are you drinking next? I'm thinking highball.",
                     "酱汁的也舍不得。下一杯喝什么？我要威士忌苏打吧。"),
                line("A", "じゃ俺も。あとさ、だし巻き卵って気になるんだけど。",
                     "Then me too. Also, the rolled dashi egg looks interesting.",
                     "那我也来一杯。还有日式鸡蛋卷好像不错。"),
                line("B", "絶対頼もう。ここ手作りっぽいし、期待できるよ。",
                     "Definitely order it. This place looks like they make it by hand, so it should be good.",
                     "必须点。这家看着是手做的，值得期待。"),
            ]),
            section("会計", "Paying the bill", "结账", "💴", [
                line("A", "やばっ、もう十時じゃん。そろそろ帰らないと。",
                     "Whoa, it's already ten. We should head out soon.",
                     "糟，都十点了。该回去了。"),
                line("B", "ほんとだ。すみません、お会計お願いします。",
                     "You're right. Excuse me, check please.",
                     "真的。不好意思，结账。"),
                line("A", "いくらだった？",
                     "How much was it?",
                     "多少钱？"),
                line("B", "全部で七千円ちょっと。一人三千五百円でいい？",
                     "Just over 7,000 yen total. Is 3,500 each OK?",
                     "总共七千出头。一人三千五百行吗？"),
                line("A", "オッケー。PayPayで送ろうか？",
                     "OK. Shall I send it via PayPay?",
                     "好。用PayPay转给你？"),
                line("B", "現金あるから大丈夫。ごちそうさまでしたー。",
                     "I have cash so it's fine. Thanks for the meal!",
                     "有现金没事。谢谢招待——"),
                line("A", "うまかったね。来月もここにしない？",
                     "That was good. Wanna come here again next month?",
                     "好吃。下个月还来这家？"),
                line("B", "賛成。今度は刺身もちゃんと頼もうね。",
                     "Agreed. Let's properly order sashimi next time too.",
                     "赞成。下次要好好点刺身。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-cafe-work 咖啡店办公
    # ═══════════════════════════════════════════
    {
        "id": "n4-cafe-work-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "カフェでリモートワークする",
        "titleJp": "カフェでリモートワークする",
        "titleEn": "Working remotely at a cafe",
        "titleZh": "在咖啡店远程办公",
        "titleRuby": [],
        "segments": [
            seg("今日は在宅勤務の日だが、家だと集中できない。洗濯物やテレビが気になってしまう。",
                "Today is a work-from-home day, but I can't concentrate at home. I get distracted by laundry and the TV.",
                "今天是居家办公日，但在家无法集中。总是在意洗的衣服和电视。", True),
            seg("昨日も家で仕事をしたが、午後はほとんど進まなかった。ソファで寝てしまった。",
                "I worked from home yesterday too, but barely made progress in the afternoon. I fell asleep on the sofa.",
                "昨天也在家办公，但下午几乎没推进。在沙发上睡着了。"),
            seg("気分を変えるために、駅前のカフェに行くことにした。電源とWi-Fiがある店を選んだ。",
                "To change the mood, I decided to go to a cafe near the station. I chose one with power outlets and Wi-Fi.",
                "为了换个心情，决定去车站前的咖啡店。选了有插座和Wi-Fi的店。"),
            seg("十時に着いた。平日の午前中なのに、意外と混んでいた。同じようにパソコンを開いている人が多い。",
                "I arrived at ten. Despite being a weekday morning, it was surprisingly crowded. Many people were on laptops like me.",
                "十点到了。虽然是工作日上午，意外地人不少。跟我一样开着电脑的人很多。"),
            seg("カウンターでホットのカフェラテを注文した。四百八十円。ついでにマフィンも一つ頼んだ。",
                "At the counter I ordered a hot cafe latte. 480 yen. I also added a muffin.",
                "在柜台点了杯热拿铁。四百八十日元。顺便还点了一个松饼。", True),
            seg("窓際の席が空いていたので、そこに座った。コンセントが近くて助かる。",
                "A window seat was open so I sat there. The outlet was nearby, which was helpful.",
                "靠窗的位子空着，就坐了那里。插座在旁边，真方便。"),
            seg("パソコンを開いて、会社のVPNに接続した。Wi-Fiの速度を測ると、十分な速さだった。",
                "I opened my laptop and connected to the company VPN. The Wi-Fi speed was fast enough.",
                "打开电脑连了公司VPN。测了一下Wi-Fi速度，够快的。"),
            seg("まずメールを確認した。昨日の会議のメモが来ていたので、内容を読んで返信した。",
                "First I checked my email. Minutes from yesterday's meeting had come, so I read them and replied.",
                "先查了邮件。昨天会议的纪要发过来了，看了看回复了。", True),
            seg("午前中はメールの返信と資料の作成をした。カフェの適度な雑音が、かえって集中を助けてくれる。",
                "In the morning I replied to emails and created documents. The moderate background noise of the cafe actually helped me focus.",
                "上午回了邮件、做了资料。咖啡店适度的嘈杂声反而帮助集中。"),
            seg("十二時にオンライン会議があった。イヤホンをして、小さい声で話した。周りに聞こえないように気をつけた。",
                "I had an online meeting at noon. I put in earphones and spoke quietly, being careful not to be overheard.",
                "十二点有线上会议。戴着耳机小声说话。注意不让周围的人听到。"),
            seg("カメラはオフにした。カフェにいることがバレると、サボっていると思われるかもしれない。",
                "I turned off the camera. If they found out I was at a cafe, they might think I was slacking off.",
                "把摄像头关了。要是被发现在咖啡店，可能会被觉得在偷懒。"),
            seg("会議が終わって、お昼ごはんにサンドイッチを買い足した。カフェのランチは少し高いけど、移動しなくていいのが楽だ。",
                "After the meeting I bought a sandwich for lunch. Cafe lunches are a bit expensive, but not having to move is convenient.",
                "会议结束后又买了个三明治当午饭。咖啡店的午餐虽然有点贵，但不用挪地方很省事。", True),
            seg("午後は企画書を書いた。家にいるときより、明らかにはかどった。",
                "In the afternoon I wrote a proposal. I was clearly more productive than at home.",
                "下午写了企划书。明显比在家效率高。"),
            seg("三時ごろ、二杯目のコーヒーを注文した。一杯だけで何時間も座っているのは申し訳ない気がする。",
                "Around three I ordered a second coffee. I felt bad sitting for hours with just one drink.",
                "三点左右又点了一杯咖啡。只点一杯坐好几个小时总觉得不好意思。"),
            seg("隣の席の人がイヤホンなしで動画を見始めた。少しうるさかったが、我慢した。",
                "The person next to me started watching a video without earphones. It was a bit noisy, but I put up with it.",
                "旁边的人开始不戴耳机看视频。有点吵，但忍了。", True),
            seg("四時半に企画書が完成した。上司にメールで送って、返事を待つ。",
                "At 4:30 I finished the proposal. I emailed it to my boss and waited for a reply.",
                "四点半企划书写完了。发邮件给上司，等回复。"),
            seg("五時に仕事を終えて、パソコンを閉じた。合計で七時間もいた。",
                "I finished work at five and closed my laptop. I'd been there for a total of seven hours.",
                "五点结束工作关了电脑。总共待了七个小时。"),
            seg("コーヒー二杯とマフィンとサンドイッチで、千五百円くらい使った。コワーキングスペースより安いかもしれない。",
                "Two coffees, a muffin, and a sandwich came to about 1,500 yen. Maybe cheaper than a coworking space.",
                "两杯咖啡加松饼和三明治，花了大概一千五百日元。可能比共享办公空间便宜。", True),
            seg("店を出るとき、店員に「ありがとうございました」と言われた。長居したのに嫌な顔をされなかったのがありがたい。",
                "When I left the staff said 'Thank you.' I was grateful they didn't look annoyed despite my long stay.",
                "出门时店员说了「谢谢光临」。待了这么久也没被嫌弃，很感激。"),
            seg("帰り道、明日も来ようかと思ったが、さすがに毎日は店に悪い。週に一回くらいがちょうどいいだろう。",
                "On the way home I thought about coming again tomorrow, but going every day would be too much for the cafe. Once a week seems about right.",
                "回去路上想着明天也来，但天天来对店家不好。一周一次刚刚好吧。"),
            seg("家に帰って、妻に「今日はすごくはかどった」と報告した。「じゃあ毎日カフェに行けば？」と笑われた。",
                "I got home and told my wife 'I was super productive today.' She laughed and said 'Then why not go to a cafe every day?'",
                "到家跟妻子说「今天效率超高」。被笑着说「那你每天去咖啡店不就好了」。"),
        ],
    },

    {
        "id": "n4-cafe-work-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "カフェで隣の人と話す",
        "titleJp": "カフェで隣の人と話す",
        "titleEn": "Chatting with the person next to me at the cafe",
        "titleZh": "在咖啡店和旁边的人聊天",
        "titleRuby": [],
        "sections": [
            section("席が近い", "Sitting close", "座得近", "☕", [
                line("A", "すみません、この席って電源使えますか？",
                     "Excuse me, can I use the outlet at this seat?",
                     "不好意思，这个座位能用插座吗？"),
                line("B", "ああ、使えますよ。ここの下にありますよ。",
                     "Yeah, you can. It's down here.",
                     "能用的。在这下面。"),
                line("A", "ありがとうございます。よかった、充電やばくて。",
                     "Thank you. Good, my battery was about to die.",
                     "谢谢。太好了，快没电了。"),
                line("B", "分かります。カフェで仕事するとき、電源ないと死にますよね。",
                     "I know. When working at a cafe, you're dead without an outlet.",
                     "懂的。在咖啡店办公没插座就完了。"),
                line("A", "ですよね。ここ、Wi-Fiも速いですか？",
                     "Right. Is the Wi-Fi fast here too?",
                     "是吧。这里Wi-Fi快吗？"),
                line("B", "まあまあですね。ビデオ会議はちょっと厳しいかもしれないけど、普通の作業なら大丈夫です。",
                     "It's decent. Video calls might be a stretch, but it's fine for regular work.",
                     "还行。视频会议可能有点勉强，但一般工作没问题。"),
                line("A", "なるほど。会議は一回あるんですけど、音声だけにしようかな。",
                     "I see. I have one meeting, but maybe I'll just do audio only.",
                     "原来如此。有一个会议，那就只开语音吧。"),
            ]),
            section("仕事の話", "Talking about work", "聊工作", "💻", [
                line("B", "リモートワークですか？いいですね。うちの会社はまだ週一しか在宅できなくて。",
                     "Remote work? Nice. My company still only allows one day of WFH a week.",
                     "远程办公吗？真好。我们公司每周还只能居家一天。"),
                line("A", "うちは週二です。でも家だと全然集中できないんですよ。テレビとかベッドとか誘惑が多くて。",
                     "We get two days. But I can't concentrate at home at all. Too many temptations like TV and the bed.",
                     "我们每周两天。但在家根本集中不了。电视啊床什么的诱惑太多。"),
                line("B", "あー、めっちゃ分かります。俺もそれでカフェに逃げてきたタイプです。",
                     "Ah, I totally get that. I'm the type who escapes to cafes for that reason too.",
                     "啊，太懂了。我也是因为这个跑来咖啡店的。"),
                line("A", "ここ、適度にうるさいのがいいんですよね。静かすぎると逆に落ち着かない。",
                     "The moderate noise here is nice. When it's too quiet I actually can't relax.",
                     "这里适度吵吵的挺好。太安静了反而静不下心来。"),
                line("B", "分かる。図書館は静かすぎて、自分のタイピング音が気になっちゃう。",
                     "I know. The library is too quiet — I get self-conscious about my own typing sounds.",
                     "懂。图书馆太安静了，会在意自己的打字声。"),
                line("A", "あはは、それありますよね。",
                     "Haha, that's so true.",
                     "哈哈，确实有。"),
            ]),
            section("帰りぎわ", "About to leave", "准备走了", "🚶", [
                line("B", "あ、もう五時だ。そろそろ帰ろうかな。",
                     "Oh, it's already five. I should probably head home.",
                     "啊，都五点了。差不多该回去了。"),
                line("A", "俺も五時で終わりにします。今日、めっちゃはかどりました。",
                     "Me too, I'll wrap up at five. I was super productive today.",
                     "我也五点收工。今天效率超高。"),
                line("B", "ですよね。家にいるより三倍くらい進んだ気がする。",
                     "Right? I feel like I got three times as much done as I would at home.",
                     "是吧。感觉比在家效率高三倍。"),
                line("A", "コーヒー代は仕事の投資だと思えば安いもんですよね。",
                     "If you think of coffee money as an investment in work, it's cheap.",
                     "咖啡钱当是对工作的投资就很便宜了。"),
                line("B", "そうそう。あ、そういえば、この辺だと二丁目のコーヒーショップもいいですよ。席が広くて。",
                     "Exactly. Oh by the way, the coffee shop on 2-chome around here is good too. The seats are spacious.",
                     "没错。啊对了，这附近二丁目的咖啡店也不错。座位宽敞。"),
                line("A", "へえ、今度行ってみます。教えてくれてありがとうございます。",
                     "Oh really, I'll try it next time. Thanks for telling me.",
                     "是吗，下次去看看。谢谢告诉我。"),
                line("B", "いえいえ。じゃ、お互い頑張りましょう。お疲れさまです。",
                     "Not at all. Well, let's both keep at it. Good work today.",
                     "哪里。那一起加油吧。辛苦了。"),
                line("A", "お疲れさまでーす。",
                     "Good work!",
                     "辛苦了——"),
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
