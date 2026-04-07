#!/usr/bin/env python3
"""
batch21 → public/data/ja_articles.json

生活实用 + 家庭亲情对话:
1. n4-home-center dialogue (家居店买日用品)
2. n3-moving-unpack dialogue (新家拆箱)
3. n3-closet-organize dialogue (换季整理衣柜)
4. n4-supermarket dialogue (超市挑食材)
5. n3-cooking-class essay (开始上烹饪课)
6. n3-family-dinner dialogue (家人吃晚饭聊天)
7. n4-call-grandma dialogue (给奶奶打电话)
8. n3-siblings-childhood dialogue (兄弟聊小时候)

运行: python3 scripts/append_ja_articles_batch21.py
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
    # 1. 家居店买日用品 dialogue
    # ═══════════════════════════════════════════
    {
        "id": "n4-home-center-dialogue",
        "level": "N5–N4",
        "format": "dialogue",
        "titleWord": "ホームセンターで日用品を買う",
        "titleJp": "ホームセンターで日用品を買う",
        "titleEn": "Buying daily necessities at a home center",
        "titleZh": "在家居店买日用品",
        "titleRuby": [],
        "sections": [
            section("洗面台のコーナー", "Washroom corner", "洗漱台区域", "🪥", [
                line("A", "歯ブラシ、どれにする？いっぱいあるね。",
                     "Which toothbrush? There are so many.",
                     "牙刷选哪个？好多啊。"),
                line("B", "やわらかいのがいいな。この青いの、よさそう。",
                     "I'd like a soft one. This blue one looks good.",
                     "我想要软的。这个蓝色的看着不错。"),
                line("A", "じゃあ、私はこのピンクのにする。お揃いだね。",
                     "Then I'll get this pink one. We'll match.",
                     "那我选这个粉色的。配对了呢。"),
                line("B", "タオルも買わなきゃ。古いのはもう硬くなっちゃった。",
                     "We need to buy towels too. The old ones are already stiff.",
                     "毛巾也得买。旧的已经硬了。"),
                line("A", "この厚いタオル、気持ちよさそう。触ってみて。",
                     "This thick towel looks comfy. Feel it.",
                     "这条厚毛巾看着很舒服。你摸摸看。"),
            ]),
            section("キッチン用品", "Kitchen supplies", "厨房用品", "🍳", [
                line("B", "あ、お皿のコーナーだ。白いお皿がほしいんだよね。",
                     "Oh, the plate section. I want a white plate.",
                     "啊，是盘子区。我想要白色的盘子。"),
                line("A", "この丸いのはどう？シンプルでいいと思う。",
                     "How about this round one? I think it's nice and simple.",
                     "这个圆的怎么样？简单又好看。"),
                line("B", "うん、五つ買おう。家族みんなの分。",
                     "Yeah, let's get five. Enough for the whole family.",
                     "嗯，买五个吧。一家人都够。"),
                line("A", "ラップとか、ゴミ袋もいるよね。あっちの棚にあるかな。",
                     "We also need plastic wrap and garbage bags, right? Maybe on that shelf over there.",
                     "保鲜膜和垃圾袋也需要吧。那边的架子上有没有。"),
                line("B", "あった。ゴミ袋は大きいのと小さいの、両方買おう。",
                     "Found them. Let's buy both large and small garbage bags.",
                     "找到了。垃圾袋大的小的都买吧。"),
            ]),
            section("お会計", "Checkout", "结账", "💰", [
                line("A", "けっこう買ったね。かごが重い！",
                     "We bought a lot. The basket is heavy!",
                     "买了不少呢。篮子好重！"),
                line("B", "お金、足りるかな。全部でいくらだろう。",
                     "Do we have enough money? I wonder how much it all costs.",
                     "钱够不够呢。总共多少钱啊。"),
                line("A", "大丈夫。カードで払えるから。",
                     "It's fine. We can pay by card.",
                     "没事。可以刷卡。"),
                line("B", "お釣り、いらないね。ちょうどだった。",
                     "No change needed. It was exact.",
                     "不用找零了。刚好。"),
                line("A", "袋に入れよう。エコバッグ持ってきてよかった。",
                     "Let's put them in the bag. Glad we brought the eco bag.",
                     "装进袋子吧。带了环保袋真好。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. 新家拆箱 dialogue
    # ═══════════════════════════════════════════
    {
        "id": "n3-moving-unpack-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "引っ越し先で段ボールを開ける",
        "titleJp": "引っ越し先で段ボールを開ける",
        "titleEn": "Unpacking boxes at the new place",
        "titleZh": "在新家拆快递箱",
        "titleRuby": [],
        "sections": [
            section("リビング", "Living room", "客厅", "📦", [
                line("A", "やっと引っ越し終わった！段ボール、すごい数だね。",
                     "We finally finished moving! So many boxes.",
                     "终于搬完了！纸箱好多啊。"),
                line("B", "まず家具の場所を決めよう。冷蔵庫はキッチンのここでいい？",
                     "Let's decide where to put the furniture first. Is the fridge OK here in the kitchen?",
                     "先决定家具的位置吧。冰箱放厨房这里行吗？"),
                line("A", "うん、コンセントが近いからそこがいい。",
                     "Yeah, the outlet is close so that's good.",
                     "嗯，插座近，放那里好。"),
                line("B", "洗濯機は？お風呂の隣に置くスペースあるかな。",
                     "What about the washing machine? Is there room to put it next to the bathroom?",
                     "洗衣机呢？浴室旁边有空间放吗？"),
                line("A", "ギリギリ入りそう。測ってみよう。",
                     "Looks like it'll barely fit. Let's measure.",
                     "勉强放得下的样子。量一下吧。"),
            ]),
            section("キッチン", "Kitchen", "厨房", "🍽️", [
                line("B", "この段ボール、「キッチン」って書いてある。開けるね。",
                     "This box says 'Kitchen'. I'll open it.",
                     "这箱子写着'厨房'。我打开了。"),
                line("A", "電子レンジ、ちゃんと動くかな。引っ越しで壊れてないといいけど。",
                     "I hope the microwave still works. I hope it didn't break during the move.",
                     "微波炉还能用吗。搬家别搞坏了就好。"),
                line("B", "大丈夫そう。掃除機も出しておこう。床がほこりだらけだよ。",
                     "Looks fine. Let's get out the vacuum too. The floor is dusty.",
                     "看着没问题。吸尘器也拿出来吧。地板全是灰。"),
                line("A", "天井にクモの巣がある！やだー。",
                     "There's a spider web on the ceiling! Gross!",
                     "天花板上有蜘蛛网！好恶心！"),
                line("B", "あはは。まず掃除してから片付けよう。",
                     "Haha. Let's clean first, then organize.",
                     "哈哈。先打扫再收拾吧。"),
            ]),
            section("夕方", "Evening", "傍晚", "🌇", [
                line("A", "だいぶ片付いたね。疲れた〜。",
                     "We've organized a lot. I'm tired.",
                     "收拾了不少了。累死了〜"),
                line("B", "まだ段ボール半分も残ってるけどね。",
                     "We still have half the boxes left though.",
                     "不过纸箱还剩一半呢。"),
                line("A", "今日はもう休もう。明日また頑張ろう。",
                     "Let's rest for today. We'll try hard again tomorrow.",
                     "今天就歇了吧。明天再加油。"),
                line("B", "布団どこだっけ？段ボールに入ったままだ。",
                     "Where's the futon? It's still in a box.",
                     "被子在哪来着？还在纸箱里呢。"),
                line("A", "あはは、それだけは先に出さなきゃ。",
                     "Haha, we need to take that out first.",
                     "哈哈，那个得先拿出来才行。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. 换季整理衣柜 dialogue
    # ═══════════════════════════════════════════
    {
        "id": "n3-closet-organize-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "衣替えでクローゼットを整理する",
        "titleJp": "衣替えでクローゼットを整理する",
        "titleEn": "Organizing the closet for the season change",
        "titleZh": "换季整理衣柜",
        "titleRuby": [],
        "sections": [
            section("冬服をしまう", "Putting away winter clothes", "收起冬装", "🧥", [
                line("A", "もう暖かくなってきたから、冬服をしまおうよ。",
                     "It's gotten warm, so let's put away the winter clothes.",
                     "已经暖和起来了，把冬装收起来吧。"),
                line("B", "うん。このジャケット、今年あんまり着なかったな。",
                     "Yeah. I didn't wear this jacket much this year.",
                     "嗯。这件夹克今年没怎么穿过。"),
                line("A", "捨てる？それとも取っておく？",
                     "Throw it away? Or keep it?",
                     "扔掉？还是留着？"),
                line("B", "まだきれいだし、来年着るかも。しまっておこう。",
                     "It's still clean, and I might wear it next year. I'll keep it.",
                     "还挺干净的，明年说不定穿。收起来吧。"),
                line("A", "この上着はもう古いから、捨ててもいいんじゃない？",
                     "This coat is old, so maybe it's OK to toss?",
                     "这件外套旧了，扔了也行吧？"),
            ]),
            section("夏服を出す", "Bringing out summer clothes", "拿出夏装", "👕", [
                line("B", "Tシャツ、去年のまだあるかな。",
                     "I wonder if I still have my T-shirts from last year.",
                     "T恤，去年的还有吗。"),
                line("A", "あったあった。でも黄色くなってるよ、これ。",
                     "Found them. But this one turned yellow.",
                     "有有。不过这件发黄了。"),
                line("B", "うわ、ほんとだ。洗濯機で洗ってもダメかな。",
                     "Wow, really. I wonder if even the washing machine can't fix it.",
                     "哇，真的。用洗衣机洗也不行吗。"),
                line("A", "ワンピース、これ去年買ったやつだよね。かわいい。",
                     "This dress — you bought it last year, right? It's cute.",
                     "连衣裙，这是去年买的那条吧。好看。"),
                line("B", "うん、お気に入り。大事にしまってたの。",
                     "Yeah, it's my favorite. I kept it carefully.",
                     "嗯，我最喜欢的。小心收着的。"),
            ]),
            section("整理完了", "Done organizing", "整理完毕", "✨", [
                line("A", "やっと全部入った！クローゼットがすっきりした。",
                     "Everything's in! The closet is so tidy now.",
                     "终于全放进去了！衣柜清爽多了。"),
                line("B", "物干しに夏服かけておこう。風を通したいし。",
                     "Let's hang the summer clothes on the drying rack. I want to air them out.",
                     "把夏装挂晾衣架上吧。透透风。"),
                line("A", "器用だね、たたみ方上手。",
                     "You're skillful. You fold clothes well.",
                     "你好利索啊，叠衣服真好看。"),
                line("B", "母に教わったの。うちの母、不器用だけどたたむのだけは上手なんだ。",
                     "My mom taught me. She's clumsy, but she's great at folding.",
                     "我妈教的。我妈虽然笨手笨脚，但叠衣服特别厉害。"),
                line("A", "いいお母さんだね。",
                     "That's a nice mom.",
                     "真是个好妈妈。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 4. 超市挑食材 dialogue
    # ═══════════════════════════════════════════
    {
        "id": "n4-supermarket-dialogue",
        "level": "N5–N4",
        "format": "dialogue",
        "titleWord": "友達とスーパーで食材を選ぶ",
        "titleJp": "友達とスーパーで食材を選ぶ",
        "titleEn": "Choosing ingredients at the supermarket with friends",
        "titleZh": "和朋友在超市挑食材",
        "titleRuby": [],
        "sections": [
            section("野菜コーナー", "Vegetable corner", "蔬菜区", "🥬", [
                line("A", "今夜は何作る？",
                     "What are we making tonight?",
                     "今晚做什么？"),
                line("B", "カレーはどう？簡単だし、おいしいよ。",
                     "How about curry? It's easy and delicious.",
                     "咖喱怎么样？简单又好吃。"),
                line("A", "いいね！じゃあ、にんじんとじゃがいもと玉ねぎ。",
                     "Sounds good! Then carrots, potatoes, and onions.",
                     "好啊！那就胡萝卜、土豆和洋葱。"),
                line("B", "あ、お肉も。豚肉と牛肉、どっちがいい？",
                     "Oh, we need meat too. Pork or beef?",
                     "啊，肉也要。猪肉和牛肉，你选哪个？"),
                line("A", "豚肉にしよう。安いし。",
                     "Let's go with pork. It's cheaper.",
                     "选猪肉吧。便宜。"),
            ]),
            section("飲み物と調味料", "Drinks and seasonings", "饮料和调味料", "🧂", [
                line("B", "お茶も買っておく？冷蔵庫に何もないよね。",
                     "Should we buy tea too? There's nothing in the fridge.",
                     "茶也买点？冰箱里啥也没有吧。"),
                line("A", "うん、お茶とお水。あと、お酒も？",
                     "Yeah, tea and water. And alcohol too?",
                     "嗯，茶和水。还有，酒也要？"),
                line("B", "今日はやめておこう。明日仕事だから。",
                     "Let's skip that today. I have work tomorrow.",
                     "今天算了吧。明天要上班。"),
                line("A", "調味料は？塩とか、ある？",
                     "What about seasonings? Do we have salt?",
                     "调味料呢？有盐吗？"),
                line("B", "塩はあるけど、カレーのルーを買わなきゃ。",
                     "We have salt, but we need to buy curry roux.",
                     "盐有，但咖喱块得买。"),
            ]),
            section("レジで", "At the register", "收银台", "🧾", [
                line("A", "全部で千五百円くらいかな。",
                     "I think it's about 1,500 yen total.",
                     "总共大概一千五百日元吧。"),
                line("B", "半分ずつ出そう。割り勘ね。",
                     "Let's split it evenly. Going Dutch.",
                     "一人一半吧。AA制。"),
                line("A", "うん。お釣りは私がもらうね。",
                     "OK. I'll take the change.",
                     "嗯。找的零钱我拿了。"),
                line("B", "袋いりますか？って聞かれたよ。いらないよね？",
                     "They asked if we need a bag. We don't, right?",
                     "问要不要袋子呢。不用吧？"),
                line("A", "うん、エコバッグあるから大丈夫。帰ろう！",
                     "Yeah, we have an eco bag so it's fine. Let's go home!",
                     "嗯，有环保袋没问题。回家吧！"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 5. 开始上烹饪课 essay
    # ═══════════════════════════════════════════
    {
        "id": "n3-cooking-class-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "料理教室に通い始める",
        "titleJp": "料理教室に通い始める",
        "titleEn": "Starting cooking classes",
        "titleZh": "开始上烹饪课",
        "titleRuby": [],
        "segments": [
            seg("先月から、駅前の料理教室に通い始めた。",
                "Starting last month, I began attending a cooking class near the station.",
                "上个月开始，我去车站附近的料理教室上课了。", True),
            seg("ずっと料理が苦手で、コンビニ弁当ばかり食べていた。",
                "I was always bad at cooking and only ate convenience store bentos.",
                "一直不擅长做饭，净吃便利店的便当。"),
            seg("友達に「自分で作った方が安いし健康だよ」と言われて、やっと決心した。",
                "A friend told me 'It's cheaper and healthier to cook yourself,' and I finally made up my mind.",
                "朋友说'自己做又便宜又健康'，我终于下定决心了。"),
            seg("最初の授業は、だしの取り方だった。",
                "The first class was about how to make dashi stock.",
                "第一节课是熬高汤。", True),
            seg("昆布とかつお節でだしを取るのは初めてだった。",
                "It was my first time making dashi from kombu and bonito flakes.",
                "用昆布和柴鱼片熬汤还是头一回。"),
            seg("先生が「だしは料理の基本ですよ」と笑顔で教えてくれた。",
                "The teacher smiled and said 'Dashi is the foundation of cooking.'",
                "老师笑着告诉我'高汤是料理的基础'。"),
            seg("二回目の授業では、野菜の切り方を習った。",
                "In the second class, I learned how to cut vegetables.",
                "第二节课学了蔬菜的切法。", True),
            seg("にんじんを薄く切るのが難しくて、先生に何度も見てもらった。",
                "Cutting carrots thinly was difficult, so I had the teacher watch me many times.",
                "把胡萝卜切薄好难，让老师看了好几次。"),
            seg("胡椒と塩で味付けして、シンプルな炒め物を作った。",
                "I seasoned with pepper and salt and made a simple stir-fry.",
                "用胡椒和盐调味，做了一道简单的炒菜。"),
            seg("自分で作った料理は、なんだかとてもおいしかった。",
                "The food I made myself somehow tasted really good.",
                "自己做的菜，怎么说呢，特别好吃。"),
            seg("三回目は煮物に挑戦した。",
                "The third time, I challenged myself with simmered dishes.",
                "第三次挑战了炖菜。", True),
            seg("大根と鶏肉を鍋に入れて、酢と醤油で煮る。",
                "Put daikon and chicken in a pot and simmer with vinegar and soy sauce.",
                "把白萝卜和鸡肉放进锅里，用醋和酱油炖。"),
            seg("弱火でゆっくり煮ると、味がしっかり染み込む。",
                "Simmering slowly on low heat lets the flavor soak in well.",
                "小火慢慢炖，味道就能彻底渗进去。"),
            seg("「料理って楽しいかも」と、少し思えるようになった。",
                "I started to feel that maybe cooking is actually fun.",
                "开始觉得'做菜说不定还挺有意思的'。"),
            seg("来月はスープとアイスクリームを作るらしい。楽しみだ。",
                "Next month, we'll apparently make soup and ice cream. I'm looking forward to it.",
                "听说下个月做汤和冰淇淋。好期待。", True),
            seg("レシピも少しずつ増えてきた。小麦粉を使ったお菓子にも挑戦してみたい。",
                "My recipes are gradually increasing too. I want to try sweets using flour.",
                "食谱也在慢慢增加。也想挑战用面粉做点心。"),
            seg("まだまだ下手だけど、食費も減って、体の調子もよくなった気がする。",
                "I'm still not great, but my food expenses have gone down and I feel healthier.",
                "虽然还是不太行，但伙食费少了，身体好像也好起来了。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 6. 家人吃晚饭聊天 dialogue (亲情)
    # ═══════════════════════════════════════════
    {
        "id": "n3-family-dinner-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "家族で晩ご飯を食べながら話す",
        "titleJp": "家族で晩ご飯を食べながら話す",
        "titleEn": "Chatting over dinner with family",
        "titleZh": "一家人边吃晚饭边聊天",
        "titleRuby": [],
        "sections": [
            section("いただきます", "Let's eat", "开饭啦", "🍚", [
                line("母", "はい、今日は肉じゃがだよ。たくさん作ったから、おかわりしてね。",
                     "Here, today it's nikujaga. I made a lot, so have seconds.",
                     "来，今天是肉炖土豆。做了很多，多吃点。"),
                line("父", "おお、うまそうだな。いただきます。",
                     "Oh, looks delicious. Let's eat.",
                     "哦，看着好好吃。开动了。"),
                line("子", "いただきます！お母さん、これ、味がすごく染みてる。",
                     "Let's eat! Mom, the flavor is really soaked in.",
                     "开动了！妈妈，这个入味了好好吃。"),
                line("母", "朝から煮てたからね。お父さんの好きな味付けにしたの。",
                     "I was simmering it since morning. I seasoned it the way your dad likes.",
                     "从早上就开始炖了嘛。按你爸喜欢的味道调的。"),
                line("父", "ありがとう。やっぱり家のご飯が一番だよ。",
                     "Thank you. Home cooking really is the best.",
                     "谢谢。还是家里的饭最好吃。"),
            ]),
            section("学校のこと", "About school", "聊聊学校", "📖", [
                line("母", "そういえば、学校はどう？最近忙しいの？",
                     "By the way, how's school? Have you been busy lately?",
                     "对了，学校怎么样？最近忙吗？"),
                line("子", "うん、テストが多くて大変。でも友達と一緒に勉強してるから楽しいよ。",
                     "Yeah, there are lots of tests so it's tough. But I study with friends so it's fun.",
                     "嗯，考试多挺累的。不过和朋友一起学习很开心。"),
                line("父", "友達は大事だよ。大人になっても付き合える友達を作りなさい。",
                     "Friends are important. Make friends you can keep even as an adult.",
                     "朋友很重要。要交那种长大了也能来往的朋友。"),
                line("子", "うん。お父さんも高校の友達とまだ会ってるもんね。",
                     "Yeah. You still meet your high school friends, right, Dad?",
                     "嗯。爸爸也还跟高中同学见面呢。"),
                line("父", "そうだよ。来月も一緒に釣りに行く予定だ。",
                     "That's right. We're planning to go fishing together next month too.",
                     "是啊。下个月还打算一起去钓鱼。"),
            ]),
            section("お風呂の順番", "Bath order", "洗澡顺序", "🛁", [
                line("母", "ご飯の後、お風呂の順番、どうする？",
                     "After dinner, who takes a bath first?",
                     "吃完饭，洗澡顺序怎么排？"),
                line("子", "私、先に入っていい？明日早いんだ。",
                     "Can I go first? I have to be up early tomorrow.",
                     "我先洗行吗？明天起得早。"),
                line("父", "いいよ。じゃあ、お父さんは最後でいい。",
                     "Sure. I'll go last then.",
                     "好呀。那爸爸最后洗。"),
                line("母", "お父さん、いつも最後だね。ありがとう。",
                     "Dad, you're always last. Thank you.",
                     "爸爸总是最后。谢谢你。"),
                line("父", "家族のためだからな。さて、もう一杯お茶をもらおうかな。",
                     "It's for the family. Now, can I get another cup of tea?",
                     "为了家人嘛。那，再给我倒杯茶呗。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 7. 给奶奶打电话 dialogue (亲情)
    # ═══════════════════════════════════════════
    {
        "id": "n4-call-grandma-dialogue",
        "level": "N5–N4",
        "format": "dialogue",
        "titleWord": "おばあちゃんに電話をかける",
        "titleJp": "おばあちゃんに電話をかける",
        "titleEn": "Calling grandma on the phone",
        "titleZh": "给奶奶打电话",
        "titleRuby": [],
        "sections": [
            section("もしもし", "Hello", "喂", "📞", [
                line("孫", "もしもし、おばあちゃん？元気？",
                     "Hello, Grandma? How are you?",
                     "喂，奶奶？身体好吗？"),
                line("祖母", "あら、久しぶりだねえ。元気だよ。あなたは？",
                     "Oh, it's been a while. I'm fine. How about you?",
                     "哎呀，好久没打了。我挺好的。你呢？"),
                line("孫", "元気だよ。最近ちょっと忙しくて、なかなか電話できなくて、ごめんね。",
                     "I'm fine. I've been a bit busy lately and couldn't call, sorry.",
                     "我也好。最近有点忙，没来得及打电话，对不起。"),
                line("祖母", "いいのいいの。声が聞けてうれしいよ。",
                     "It's OK, it's OK. I'm happy to hear your voice.",
                     "没事没事。能听到你的声音就高兴了。"),
                line("孫", "おじいちゃんも元気？",
                     "Is Grandpa doing well too?",
                     "爷爷也好吗？"),
                line("祖母", "元気だよ。毎日散歩してるよ。",
                     "He's fine. He takes a walk every day.",
                     "好着呢。每天都去散步。"),
            ]),
            section("近況を話す", "Catching up", "聊近况", "💬", [
                line("孫", "おばあちゃん、最近何してるの？",
                     "Grandma, what have you been up to lately?",
                     "奶奶，最近在干嘛呢？"),
                line("祖母", "庭で花を育ててるよ。今年はひまわりがきれいに咲いたの。",
                     "I'm growing flowers in the garden. The sunflowers bloomed beautifully this year.",
                     "在院子里种花呢。今年向日葵开得可好了。"),
                line("孫", "いいなあ。写真送ってよ。",
                     "That's nice. Send me a photo.",
                     "真好啊。给我发照片嘛。"),
                line("祖母", "おばあちゃん、写真の送り方、わからないんだよ。",
                     "Grandma doesn't know how to send photos.",
                     "奶奶不会发照片啊。"),
                line("孫", "今度帰ったとき、教えるよ。簡単だから。",
                     "I'll teach you next time I visit. It's easy.",
                     "下次回去的时候教你。很简单的。"),
                line("祖母", "ほんと？楽しみだねえ。",
                     "Really? I look forward to it.",
                     "真的？那太好了。"),
            ]),
            section("また来るね", "I'll visit again", "下次回去看你", "🏠", [
                line("孫", "お盆に帰るつもりだから、また会えるよ。",
                     "I plan to go back during Obon, so we can see each other.",
                     "盂兰盆节打算回去，到时候又能见面了。"),
                line("祖母", "うれしい！おばあちゃん、あなたの好きなお菓子作って待ってるからね。",
                     "I'm so happy! Grandma will make your favorite sweets and wait for you.",
                     "太高兴了！奶奶给你做你爱吃的点心等着你。"),
                line("孫", "やった！おばあちゃんのお菓子、世界一おいしいもん。",
                     "Yay! Grandma's sweets are the best in the world.",
                     "太好了！奶奶做的点心是世界上最好吃的。"),
                line("祖母", "大げさだよ。でも、ありがとうね。体に気をつけてね。",
                     "You're exaggerating. But thank you. Take care of yourself.",
                     "你也太夸张了。不过谢谢你。注意身体。"),
                line("孫", "おばあちゃんもね。じゃあ、また電話するね。おやすみ。",
                     "You too, Grandma. I'll call again. Good night.",
                     "奶奶也是。那我再打给你。晚安。"),
                line("祖母", "おやすみ。いい夢見てね。",
                     "Good night. Sweet dreams.",
                     "晚安。做个好梦。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 8. 兄弟聊小时候 dialogue (亲情)
    # ═══════════════════════════════════════════
    {
        "id": "n3-siblings-childhood-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "兄弟で子供の頃の話をする",
        "titleJp": "兄弟で子供の頃の話をする",
        "titleEn": "Siblings talking about childhood",
        "titleZh": "兄弟俩聊小时候的事",
        "titleRuby": [],
        "sections": [
            section("昔の写真", "Old photos", "老照片", "📷", [
                line("兄", "この写真、覚えてる？おじいさんの家で撮ったやつ。",
                     "Do you remember this photo? The one taken at Grandpa's house.",
                     "这张照片，你还记得吗？在爷爷家拍的。"),
                line("弟", "あ、これ！おばあさんが作ってくれたカレー、すごくおいしかったよね。",
                     "Oh, this one! The curry Grandma made was really delicious.",
                     "啊，这张！奶奶做的咖喱，超好吃的。"),
                line("兄", "お前、おかわり三回もしてたぞ。おばあさん、笑ってたよ。",
                     "You had three helpings. Grandma was laughing.",
                     "你添了三碗呢。奶奶都笑了。"),
                line("弟", "だって本当においしかったんだもん。また食べたいな。",
                     "Because it was really delicious. I want to eat it again.",
                     "因为真的很好吃嘛。好想再吃一次。"),
                line("兄", "今度一緒に作ってみるか。レシピ、母さんが知ってるはずだ。",
                     "Shall we try making it together next time? Mom should know the recipe.",
                     "下次一起做试试？食谱妈妈应该知道。"),
            ]),
            section("夏休みの思い出", "Summer vacation memories", "暑假的回忆", "🌻", [
                line("弟", "夏休み、毎年おじいさんの家に行ってたよね。",
                     "We went to Grandpa's house every summer vacation, didn't we.",
                     "暑假每年都去爷爷家吧。"),
                line("兄", "川で遊んだり、虫を捕まえたり。毎日が冒険だった。",
                     "Playing in the river, catching bugs. Every day was an adventure.",
                     "在河里玩啊、抓虫子啊。每天都是冒险。"),
                line("弟", "兄ちゃん、一回川に落ちて、お母さんにめちゃくちゃ怒られたよね。",
                     "Bro, you fell into the river once and Mom was super mad.",
                     "哥你有一次掉河里了，被妈妈狠狠骂了吧。"),
                line("兄", "あはは、そうだった。お父さんが「男の子はそんなもんだ」って言ってくれたけど。",
                     "Haha, that's right. Dad said 'That's just how boys are,' though.",
                     "哈哈，是啊。爸爸说'男孩子就是这样的'帮我说话了。"),
                line("弟", "お父さん、優しかったよね。怒るのはいつもお母さんだった。",
                     "Dad was kind, wasn't he. It was always Mom who got angry.",
                     "爸爸很温柔呢。生气的总是妈妈。"),
            ]),
            section("大人になって", "Now that we're grown up", "长大以后", "🍺", [
                line("兄", "あの頃は早く大人になりたかったけど、今は子供の頃に戻りたいよ。",
                     "Back then I wanted to grow up fast, but now I want to go back to being a kid.",
                     "那时候想快点长大，现在却想回到小时候。"),
                line("弟", "わかる。でも、大人になったから、こうやって一緒に酒が飲めるじゃん。",
                     "I know. But because we grew up, we can drink together like this.",
                     "懂。但正因为长大了，才能这样一起喝酒啊。"),
                line("兄", "それもそうだな。お前と飲むの、楽しいよ。",
                     "That's true. Drinking with you is fun.",
                     "也是。跟你喝酒挺开心的。"),
                line("弟", "今度、家族みんなで集まらない？お盆とか。",
                     "How about we all get together next time? Like during Obon.",
                     "下次全家聚一聚？盂兰盆节什么的。"),
                line("兄", "いいね。おじいさんとおばあさんも喜ぶだろうし。母さんに連絡しておくよ。",
                     "Good idea. Grandpa and Grandma would be happy too. I'll contact Mom.",
                     "好啊。爷爷奶奶也会高兴的。我跟妈妈说一声。"),
                line("弟", "楽しみだな。子供の頃みたいに、みんなで花火しよう。",
                     "I'm looking forward to it. Let's do fireworks together, like when we were kids.",
                     "好期待。像小时候一样，大家一起放烟花吧。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 9. 父亲退休那天 dialogue (N2 亲情)
    # ═══════════════════════════════════════════
    {
        "id": "n2-father-retirement-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "お父さんの退職の日",
        "titleJp": "お父さんの退職の日",
        "titleEn": "The day Dad retires",
        "titleZh": "爸爸退休的那天",
        "titleRuby": [],
        "sections": [
            section("帰宅", "Coming home", "到家", "🏠", [
                line("父", "ただいま。今日で、会社は最後だった。",
                     "I'm home. Today was my last day at the company.",
                     "我回来了。今天是在公司的最后一天了。"),
                line("母", "おかえりなさい。長い間、本当にお疲れ様でした。",
                     "Welcome home. Thank you for all your hard work over the years.",
                     "你回来了。这么多年，真的辛苦了。"),
                line("娘", "お父さん、三十五年間も同じ会社に勤めたんだよね。すごいよ。",
                     "Dad, you worked at the same company for 35 years, right? That's amazing.",
                     "爸爸，在同一家公司干了三十五年呢。太厉害了。"),
                line("父", "あっという間だったよ。入社した頃が、つい昨日のことのようだ。",
                     "It went by in a flash. It feels like just yesterday when I joined.",
                     "一晃就过去了。刚入职的时候仿佛就在昨天。"),
                line("母", "新入社員の頃、毎晩遅くまで残業してたわよね。心配だった。",
                     "When you were a new employee, you worked overtime every night. I was worried.",
                     "刚入职那会儿，每天加班到很晚。我当时好担心。"),
            ]),
            section("振り返り", "Looking back", "回顾", "📖", [
                line("父", "辛いこともあったけど、家族がいたから頑張れた。",
                     "There were hard times, but I could persevere because I had my family.",
                     "也有辛苦的时候，但因为有家人才能坚持下来。"),
                line("娘", "お父さんが頑張ってくれたおかげで、私は大学にも行けたし、留学もできた。感謝してる。",
                     "Thanks to your hard work, I could go to college and study abroad. I'm grateful.",
                     "多亏了爸爸的努力，我才能上大学、去留学。很感激。"),
                line("父", "そう言ってもらえると、報われるよ。",
                     "Hearing you say that makes it all worth it.",
                     "你这么说，我觉得一切都值了。"),
                line("母", "ボーナスが出ない年もあったし、リストラの噂が出た時期もあったわね。",
                     "There were years without bonuses, and times when there were layoff rumors.",
                     "也有没发奖金的年份，也有过裁员传闻的时候。"),
                line("父", "あの頃は妥協せずに踏ん張ったのが正解だった。逃げなくてよかった。",
                     "Not compromising and holding firm back then was the right call. Glad I didn't run.",
                     "那时候没有妥协、咬牙坚持下来是对的。没有逃跑真好。"),
            ]),
            section("これから", "From now on", "今后", "🌅", [
                line("娘", "これからどうするの？何かやりたいこと、ある？",
                     "What are you going to do from now on? Anything you want to do?",
                     "今后打算怎么办？有什么想做的吗？"),
                line("父", "実は、ずっと蓄えてきたお金で、母さんと旅行に行きたいと思ってる。",
                     "Actually, I've been thinking of using the money I've saved up to travel with your mom.",
                     "其实，我一直想用攒下来的钱，和你妈妈去旅行。"),
                line("母", "え、本当？初めて聞いた。どこに行きたいの？",
                     "Really? This is the first I've heard. Where do you want to go?",
                     "诶，真的？头一次听你说。想去哪？"),
                line("父", "京都。結婚する前に二人で行った場所を、もう一度回りたいんだ。",
                     "Kyoto. I want to revisit the places we went together before we got married.",
                     "京都。想再走一遍结婚前我们俩一起去过的地方。"),
                line("母", "……うれしい。楽しみにしてるね。",
                     "...I'm so happy. I'll look forward to it.",
                     "……好开心。我等着。"),
                line("娘", "いいなあ。お父さん、お母さん、ゆっくり楽しんできてね。",
                     "How nice. Dad, Mom, take your time and enjoy it.",
                     "真好啊。爸爸妈妈，好好享受吧。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 10. 母亲的便当 essay (N2 亲情)
    # ═══════════════════════════════════════════
    {
        "id": "n2-mothers-bento-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "母の弁当",
        "titleJp": "母の弁当",
        "titleEn": "Mom's bento",
        "titleZh": "妈妈的便当",
        "titleRuby": [],
        "segments": [
            seg("小学校から高校まで、母は毎日弁当を作ってくれた。",
                "From elementary to high school, my mom made me a bento every day.",
                "从小学到高中，妈妈每天都给我做便当。", True),
            seg("朝五時に起きて、台所に立つ母の後ろ姿を、寝ぼけた目で何度も見た。",
                "I saw her back standing in the kitchen at 5 AM with sleepy eyes many times.",
                "早上五点起床站在厨房里的妈妈的背影，我迷迷糊糊地看过很多次。"),
            seg("当時はそれが当たり前だと思っていた。感謝の気持ちなんて、まるでなかった。",
                "At the time I thought it was normal. I had no sense of gratitude at all.",
                "当时觉得那是理所当然的。完全没有感激的心情。"),
            seg("高校の頃、友達にからかわれたことがある。",
                "In high school, I was teased by my friends once.",
                "高中时，被朋友取笑过一次。", True),
            seg("「まだ親に弁当作ってもらってるの？」と笑われた。",
                "They laughed and said, 'You still have your parents make your bento?'",
                "\"你还让父母给你做便当啊?\"被他们嘲笑了。"),
            seg("恥ずかしくなって、「明日からコンビニで買うから、もう作らなくていい」と母に言った。",
                "I felt embarrassed and told my mom, 'I'll buy from the convenience store starting tomorrow, so you don't need to make it anymore.'",
                "我觉得丢人，跟妈妈说'明天开始在便利店买，不用做了'。"),
            seg("母は「そう」とだけ言って、少し寂しそうに笑った。",
                "Mom just said 'I see' and smiled a little sadly.",
                "妈妈只说了句'这样啊'，有点落寞地笑了。"),
            seg("大学に入って一人暮らしを始めた。",
                "I started college and began living alone.",
                "上了大学开始一个人住。", True),
            seg("自炊してみて初めて、毎日弁当を作ることがどれほど大変か分かった。",
                "Only after trying to cook for myself did I realize how hard it is to make a bento every day.",
                "自己做饭后才第一次明白，每天做便当有多不容易。"),
            seg("献立を考え、買い物をし、朝早く起きて調理する。それを何年も続けていたのだ。",
                "Planning the menu, shopping, waking up early to cook. She did this for years.",
                "想菜单、买食材、一大早起来做饭。这样持续了好多年。"),
            seg("栄養のバランスも考えて、彩りよく詰めてくれていた。",
                "She also considered nutritional balance and packed it colorfully.",
                "还考虑了营养均衡，搭配得色彩丰富。"),
            seg("去年の正月に実家に帰ったとき、母に「あの頃はごめん」と伝えた。",
                "When I went home last New Year's, I told my mom 'I'm sorry about back then.'",
                "去年过年回老家时，我跟妈妈说了'那时候对不起'。", True),
            seg("母は「覚えてたの？」と驚いて、それから泣いた。",
                "Mom was surprised and said 'You remembered?' and then she cried.",
                "妈妈吃惊地说'你还记得啊?'然后哭了。"),
            seg("「あなたが元気でいてくれれば、それだけで十分よ」と言ってくれた。",
                "She said, 'As long as you're healthy, that's enough for me.'",
                "她说'只要你健健康康的，对我来说就够了'。"),
            seg("今でも時々、あの弁当の味を思い出す。卵焼きの甘さ、梅干しの酸っぱさ。",
                "Even now, I sometimes remember the taste of those bentos. The sweetness of tamagoyaki, the sourness of umeboshi.",
                "到现在偶尔还会想起那个便当的味道。玉子烧的甜、梅干的酸。", True),
            seg("もう二度と食べられない味ではないけれど、母が作ってくれたあの味は、きっと一生忘れない。",
                "It's not a taste I can never have again, but the flavor she made will surely stay with me forever.",
                "虽然不是再也吃不到的味道，但妈妈做的那个味道，大概一辈子都忘不了。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 11. 女儿出嫁前夜 dialogue (N2 亲情)
    # ═══════════════════════════════════════════
    {
        "id": "n2-daughter-wedding-eve-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "娘が嫁ぐ前の夜",
        "titleJp": "娘が嫁ぐ前の夜",
        "titleEn": "The night before the daughter's wedding",
        "titleZh": "女儿出嫁前一晚",
        "titleRuby": [],
        "sections": [
            section("リビングで", "In the living room", "在客厅", "🌙", [
                line("娘", "お母さん、まだ起きてたの？",
                     "Mom, you're still up?",
                     "妈妈，你还没睡？"),
                line("母", "うん。なんだか眠れなくて。明日のこと考えちゃって。",
                     "Yeah. I just can't sleep. I keep thinking about tomorrow.",
                     "嗯。怎么也睡不着。一直在想明天的事。"),
                line("娘", "私も。ちょっと緊張してる。",
                     "Me too. I'm a little nervous.",
                     "我也是。有点紧张。"),
                line("母", "あなたが生まれた日のこと、まだ覚えてるよ。小さくて、ずっと泣いてた。",
                     "I still remember the day you were born. You were tiny and cried all the time.",
                     "你出生那天我还记得。小小的，一直在哭。"),
                line("娘", "お母さん、その話何回目？",
                     "Mom, how many times have you told that story?",
                     "妈你这故事讲几遍了？"),
                line("母", "何回でも言うわよ。だって、本当にうれしかったんだもの。",
                     "I'll say it as many times as I want. Because I was truly happy.",
                     "多少遍都要讲。因为真的太高兴了。"),
            ]),
            section("思い出話", "Reminiscing", "回忆", "💭", [
                line("娘", "小さい頃、お母さんの隣じゃないと寝られなかったの、覚えてる？",
                     "Do you remember? When I was little, I couldn't sleep unless I was next to you.",
                     "小时候不在妈妈旁边就睡不着，你还记得吗？"),
                line("母", "覚えてるよ。手をつないで、歌を歌ってあげたわ。",
                     "Of course. I held your hand and sang to you.",
                     "记得呀。牵着你的手给你唱歌。"),
                line("娘", "反抗期の頃は、ひどいこと言ってごめんね。「うるさい」とか「ほっといて」とか。",
                     "Sorry for saying horrible things during my rebellious phase. Like 'shut up' and 'leave me alone.'",
                     "叛逆期的时候说了很过分的话，对不起。什么'烦死了''别管我'之类的。"),
                line("母", "あの頃は辛かったけど、いつか分かってくれるって信じてた。",
                     "Those times were hard, but I believed you'd understand someday.",
                     "那段时间很难受，但我一直相信你总有一天会理解的。"),
                line("娘", "今なら分かる。全部、私のためだったんだよね。",
                     "Now I understand. It was all for my sake.",
                     "现在懂了。全都是为了我。"),
            ]),
            section("明日へ", "Toward tomorrow", "面向明天", "💐", [
                line("母", "明日からは、新しい家族と暮らすのね。寂しくなるわ。",
                     "Starting tomorrow, you'll live with your new family. I'll be lonely.",
                     "明天开始，你就和新的家人一起生活了。会寂寞的。"),
                line("娘", "お母さん、泣かないでよ。私もつられちゃう。",
                     "Mom, don't cry. You'll make me cry too.",
                     "妈妈别哭啊。我也跟着要哭了。"),
                line("母", "ごめんごめん。でもね、幸せになってね。それだけが願いよ。",
                     "Sorry, sorry. But please be happy. That's my only wish.",
                     "对不起对不起。不过，要幸福哦。这是我唯一的愿望。"),
                line("娘", "うん。お母さんみたいな、あたたかい家庭を作りたい。",
                     "Yeah. I want to make a warm home like you did.",
                     "嗯。我想建一个像妈妈一样温暖的家。"),
                line("母", "……ありがとう。さあ、明日に備えて寝ましょう。おやすみ。",
                     "...Thank you. Now, let's sleep to prepare for tomorrow. Good night.",
                     "……谢谢。好了，为了明天早点睡吧。晚安。"),
                line("娘", "おやすみ、お母さん。……今まで育ててくれて、ありがとう。",
                     "Good night, Mom. ...Thank you for raising me all this time.",
                     "晚安，妈妈。……谢谢你一直以来的养育。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 12. 家族旅行の宿泊 dialogue
    # ═══════════════════════════════════════════
    {
        "id": "n3-family-trip-hotel-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "家族旅行で温泉旅館に泊まる",
        "titleJp": "家族旅行で温泉旅館に泊まる",
        "titleEn": "Staying at a hot spring inn on a family trip",
        "titleZh": "家庭旅行住温泉旅馆",
        "titleRuby": [],
        "sections": [
            section("予約", "Reservation", "预约", "📱", [
                line("母", "夏休み、どこか泊まりに行かない？",
                     "Shall we go stay somewhere for summer vacation?",
                     "暑假去哪住一晚怎么样？"),
                line("父", "いいね。温泉旅館はどう？ゆっくりできるし。",
                     "Good idea. How about a hot spring inn? We can relax.",
                     "好啊。温泉旅馆怎么样？可以好好放松。"),
                line("子", "温泉！行きたい！宿泊費はいくらくらい？",
                     "Hot spring! I want to go! How much is the accommodation?",
                     "温泉！想去！住宿费大概多少？"),
                line("父", "一泊二食付きで、一人一万五千円くらいかな。",
                     "About 15,000 yen per person with dinner and breakfast included.",
                     "含两餐的话，大概一个人一万五千日元。"),
                line("母", "じゃあ、来週予約しておくね。人気の旅館はすぐ埋まっちゃうから。",
                     "Then I'll make a reservation next week. Popular inns fill up quickly.",
                     "那我下周预约吧。热门的旅馆一下就订满了。"),
            ]),
            section("チェックイン", "Check-in", "办入住", "🏨", [
                line("母", "すみません、今日から一泊で予約した田中です。",
                     "Excuse me, we're the Tanaka family with a one-night reservation starting today.",
                     "您好，我们是预约了今天起住一晚的田中。"),
                line("係", "お待ちしておりました。お部屋は二階の和室でございます。",
                     "We've been expecting you. Your room is a Japanese-style room on the second floor.",
                     "恭候您了。您的房间是二楼的和式房间。"),
                line("子", "わあ、畳だ！広い！",
                     "Wow, tatami! It's spacious!",
                     "哇，榻榻米！好大！"),
                line("父", "窓から山が見えるぞ。いい眺めだなあ。",
                     "You can see the mountains from the window. What a great view.",
                     "从窗户能看到山。景色真好啊。"),
                line("母", "浴衣も用意してあるね。みんなで着よう。",
                     "They have yukata prepared too. Let's all wear them.",
                     "浴衣也准备好了。大家一起穿吧。"),
            ]),
            section("温泉と夕食", "Hot spring and dinner", "温泉和晚餐", "♨️", [
                line("父", "いやー、温泉最高だった。疲れが全部取れた気がする。",
                     "Man, the hot spring was amazing. I feel like all my fatigue is gone.",
                     "哎呀，温泉太棒了。感觉疲劳全消了。"),
                line("子", "お腹すいた！夕食は何時から？",
                     "I'm hungry! What time is dinner?",
                     "肚子饿了！晚饭几点开始？"),
                line("母", "六時からだって。もうすぐだよ。",
                     "They said from 6 o'clock. It's almost time.",
                     "说是六点开始。快到了。"),
                line("子", "すごい！お刺身も天ぷらもある！豪華だね。",
                     "Amazing! There's sashimi and tempura! So luxurious.",
                     "好厉害！有刺身还有天妇罗！好豪华啊。"),
                line("父", "旅館の食事は特別だからな。たくさん食べなさい。",
                     "Inn food is special. Eat plenty.",
                     "旅馆的饭菜是特别的嘛。多吃点。"),
                line("母", "幸せだね、家族みんなでこうやって食べられるのは。",
                     "It's such a blessing, being able to eat together as a family like this.",
                     "真幸福啊，一家人能这样一起吃饭。"),
            ]),
            section("翌朝", "The next morning", "第二天早上", "🌅", [
                line("子", "もう帰るの？もう一泊したいなあ。",
                     "We're leaving already? I want to stay one more night.",
                     "这就回去了？好想再住一晚。"),
                line("父", "また来よう。今度はもっと長く泊まろう。",
                     "Let's come again. Next time we'll stay longer.",
                     "下次再来吧。下次住久一点。"),
                line("母", "お土産も買って帰ろうね。おばあちゃんにも何か選ぼう。",
                     "Let's buy souvenirs too. Let's pick something for Grandma as well.",
                     "买点特产回去吧。也给奶奶选点什么。"),
                line("子", "楽しかった！来年も絶対来ようね。",
                     "It was so fun! Let's definitely come again next year.",
                     "好开心！明年一定要再来。"),
                line("父", "ああ、約束だ。家族旅行は毎年の恒例にしよう。",
                     "Yeah, it's a promise. Let's make the family trip an annual tradition.",
                     "嗯，说好了。家庭旅行每年都要有。"),
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
