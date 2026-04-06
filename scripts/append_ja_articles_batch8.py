#!/usr/bin/env python3
"""
batch8 → public/data/ja_articles.json

P0: 5篇纯N5短文 + 3篇生活用品 + 3篇食物料理
共 11 篇 (essay only, dialogues in batch9)

运行: python3 scripts/append_ja_articles_batch8.py
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

    # ===== 1. 纯N5: 自我介绍 =====
    {
        "id": "n5-self-intro-essay",
        "level": "N5",
        "format": "essay",
        "titleWord": "わたしのこと",
        "titleJp": "わたしのこと",
        "titleEn": "About me",
        "titleZh": "关于我",
        "titleRuby": gr.make_ruby("わたしのこと"),
        "segments": [
            enrich_segment(
                "わたしの名前はリンです。二十歳の留学生です。",
                "My name is Rin. I'm a twenty-year-old international student.",
                "我叫琳。是二十岁的留学生。"),
            enrich_segment(
                "中国から来ました。今、東京に住んでいます。",
                "I came from China. I live in Tokyo now.",
                "从中国来的。现在住在东京。"),
            enrich_segment(
                "毎年、お正月には両親に電話します。",
                "Every year, I call my parents at New Year's.",
                "每年新年都会给父母打电话。"),
            enrich_segment(
                "誕生日は三月三日です。クリスマスも大好きです。",
                "My birthday is March 3rd. I also love Christmas.",
                "我的生日是三月三号。也很喜欢圣诞节。"),
            enrich_segment(
                "映画を見ることと、歌を歌うことが好きです。",
                "I like watching movies and singing songs.",
                "喜欢看电影和唱歌。"),
            enrich_segment(
                "ギターも少し弾けます。下手ですが、楽しいです。",
                "I can also play guitar a little. I'm not good, but it's fun.",
                "也会弹一点吉他。虽然不好，但很开心。"),
            enrich_segment(
                "絵を描くのはつまらないので、あまりしません。",
                "Drawing is boring to me, so I don't do it much.",
                "画画觉得无聊，所以不怎么画。"),
            enrich_segment(
                "日本語はまだ難しいですが、毎日勉強しています。いつも辞書を使います。",
                "Japanese is still hard, but I study every day. I always use a dictionary.",
                "日语还很难，但每天都在学。总是用词典。"),
            enrich_segment(
                "将来は日本の会社で働きたいです。りっぱな会社員になりたいです。",
                "In the future, I want to work at a Japanese company. I want to become a fine office worker.",
                "将来想在日本的公司工作。想成为出色的公司职员。"),
        ],
    },

    # ===== 2. 纯N5: 我的家人 =====
    {
        "id": "n5-my-family-essay",
        "level": "N5",
        "format": "essay",
        "titleWord": "わたしの家族",
        "titleJp": "わたしの家族",
        "titleEn": "My family",
        "titleZh": "我的家人",
        "titleRuby": gr.make_ruby("わたしの家族"),
        "segments": [
            enrich_segment(
                "わたしの家族は六人です。両親と兄と姉と弟がいます。",
                "My family has six people. I have parents, an older brother, an older sister, and a younger brother.",
                "我家有六口人。有父母、哥哥、姐姐和弟弟。"),
            enrich_segment(
                "お父さんは会社員です。毎日ネクタイをして、背広を着て出かけます。",
                "My father is a company employee. Every day he puts on a tie and suit and goes out.",
                "爸爸是公司职员。每天系上领带穿上西装出门。"),
            enrich_segment(
                "お母さんは料理が上手です。お母さんの晩ご飯はいつもおいしいです。",
                "My mother is a good cook. Her dinner is always delicious.",
                "妈妈做菜很好。妈妈做的晚饭总是很好吃。"),
            enrich_segment(
                "お兄さんは男の人の中で一番背が高いです。お姉さんはとても綺麗です。",
                "My older brother is the tallest among the men. My older sister is very pretty.",
                "哥哥在家里男性中个子最高。姐姐非常漂亮。"),
            enrich_segment(
                "弟はまだ小さい男の子で、毎日うるさいです。でも、大好きです。",
                "My younger brother is still a small boy and is noisy every day. But I love him.",
                "弟弟还是个小男孩，每天都很吵。但是我很喜欢他。"),
            enrich_segment(
                "おじいさんとおばあさんは田舎に住んでいます。",
                "My grandfather and grandmother live in the countryside.",
                "爷爷和奶奶住在乡下。"),
            enrich_segment(
                "夏休みにはいつも兄弟みんなで遊びに行きます。",
                "In summer vacation, all the siblings always go visit them together.",
                "暑假总是兄弟姐妹一起去玩。"),
            enrich_segment(
                "おじさんとおばさんも来ます。大勢で食べる晩御飯はとても楽しいです。",
                "Our uncle and aunt come too. Eating dinner with a lot of people is very fun.",
                "叔叔和阿姨也来。一大家子吃晚饭非常开心。"),
            enrich_segment(
                "家族は大切です。来年も再来年もずっと元気でいてほしいです。",
                "Family is important. I hope they stay healthy next year and the year after that, always.",
                "家人很重要。希望明年、后年、一直都健健康康。"),
        ],
    },

    # ===== 3. 纯N5: 一天的生活 =====
    {
        "id": "n5-my-day-essay",
        "level": "N5",
        "format": "essay",
        "titleWord": "わたしの一日",
        "titleJp": "わたしの一日",
        "titleEn": "My day",
        "titleZh": "我的一天",
        "titleRuby": gr.make_ruby("わたしの一日"),
        "segments": [
            enrich_segment(
                "月曜日から金曜日まで学校があります。土曜日と日曜日は休みです。",
                "I have school from Monday to Friday. Saturday and Sunday are days off.",
                "周一到周五有课。周六和周日休息。"),
            enrich_segment(
                "朝六時に起きます。すぐにお風呂に入って、シャワーを浴びます。",
                "I wake up at 6 AM. I get in the bath right away and take a shower.",
                "早上六点起床。马上进浴室淋浴。"),
            enrich_segment(
                "朝ご飯はパンと卵とお茶です。紅茶を飲む日もあります。",
                "Breakfast is bread, eggs, and tea. Some days I drink black tea.",
                "早餐是面包、鸡蛋和茶。也有喝红茶的日子。"),
            enrich_segment(
                "八時に家を出ます。地下鉄で学校に行きます。交差点を渡って、橋を越えます。",
                "I leave home at 8. I go to school by subway. I cross the intersection and go over the bridge.",
                "八点出门。坐地铁去学校。过十字路口，过桥。"),
            enrich_segment(
                "学校ではテストがあったり、作文を書いたりします。質問があれば先生に聞きます。",
                "At school, I take tests, write compositions, and such. If I have questions, I ask the teacher.",
                "在学校有考试、写作文等。有问题就问老师。"),
            enrich_segment(
                "昼ご飯は学校の食堂で食べます。今日は牛肉と果物でした。",
                "I eat lunch at the school cafeteria. Today it was beef and fruit.",
                "午餐在学校食堂吃。今天是牛肉和水果。"),
            enrich_segment(
                "午後の授業が終わると、図書館で勉強します。鉛筆とペンとノートを使います。",
                "When afternoon classes end, I study at the library. I use pencils, pens, and notebooks.",
                "下午的课结束后在图书馆学习。用铅笔、笔和笔记本。"),
            enrich_segment(
                "夕方、スーパーで買い物をします。豚肉と鶏肉と卵を買いました。",
                "In the evening, I go shopping at the supermarket. I bought pork, chicken, and eggs.",
                "傍晚在超市购物。买了猪肉、鸡肉和鸡蛋。"),
            enrich_segment(
                "晩ご飯を作って食べます。そして、少しテレビを見て、寝ます。",
                "I cook and eat dinner. Then I watch a little TV and go to bed.",
                "做晚饭吃。然后看一会儿电视就睡了。"),
            enrich_segment(
                "だんだん日本の生活に慣れてきました。毎日忙しいですが、楽しいです。",
                "I'm gradually getting used to life in Japan. Every day is busy, but fun.",
                "渐渐习惯了日本的生活。每天很忙，但很开心。"),
        ],
    },

    # ===== 4. 纯N5: 我的房间 =====
    {
        "id": "n5-my-room-essay",
        "level": "N5",
        "format": "essay",
        "titleWord": "わたしの部屋",
        "titleJp": "わたしの部屋",
        "titleEn": "My room",
        "titleZh": "我的房间",
        "titleRuby": gr.make_ruby("わたしの部屋"),
        "segments": [
            enrich_segment(
                "わたしの部屋は小さいですが、綺麗に片付けています。",
                "My room is small, but I keep it tidy.",
                "我的房间虽然小，但收拾得很干净。"),
            enrich_segment(
                "ベッドは窓の近くにあります。机と椅子はベッドの横にあります。",
                "The bed is near the window. The desk and chair are next to the bed.",
                "床在窗户旁边。桌子和椅子在床边。"),
            enrich_segment(
                "本棚にはたくさんの本と辞書があります。",
                "On the bookshelf, there are many books and dictionaries.",
                "书架上有很多书和词典。"),
            enrich_segment(
                "台所は小さいです。冷蔵庫の中には卵と果物が入っています。",
                "The kitchen is small. Inside the fridge there are eggs and fruit.",
                "厨房很小。冰箱里放着鸡蛋和水果。"),
            enrich_segment(
                "お手洗いの近くに石鹸とハンカチがあります。",
                "Near the restroom, there is soap and a handkerchief.",
                "厕所旁边有肥皂和手帕。"),
            enrich_segment(
                "電気をつけると明るいです。消すと暗いです。",
                "When I turn on the light, it's bright. When I turn it off, it's dark.",
                "开灯就亮。关灯就暗。"),
            enrich_segment(
                "冬はストーブをつけます。部屋がすぐに暖かくなります。",
                "In winter, I turn on the heater. The room gets warm right away.",
                "冬天开暖炉。房间马上就暖和了。"),
            enrich_segment(
                "窓の外には花が見えます。暖かい日は窓を開けます。風が吹くと気持ちがいいです。",
                "I can see flowers outside the window. On warm days I open the window. When the wind blows, it feels nice.",
                "从窗户可以看到花。暖和的日子会开窗。风一吹很舒服。"),
            enrich_segment(
                "この部屋は狭いですが、とても好きです。",
                "This room is narrow, but I like it very much.",
                "这个房间虽然窄，但我很喜欢。"),
        ],
    },

    # ===== 5. 纯N5: 喜欢的食物 =====
    {
        "id": "n5-food-i-like-essay",
        "level": "N5",
        "format": "essay",
        "titleWord": "好きな食べ物",
        "titleJp": "好きな食べ物",
        "titleEn": "Food I like",
        "titleZh": "喜欢的食物",
        "titleRuby": gr.make_ruby("好きな食べ物"),
        "segments": [
            enrich_segment(
                "わたしは食べることが大好きです。嫌いな食べ物はほとんどありません。",
                "I love eating. There is almost no food I dislike.",
                "我非常喜欢吃东西。几乎没有讨厌的食物。"),
            enrich_segment(
                "朝ご飯にはいつもパンとバターと卵を食べます。お茶か紅茶を飲みます。",
                "For breakfast, I always eat bread, butter, and eggs. I drink tea or black tea.",
                "早餐总是吃面包、黄油和鸡蛋。喝茶或红茶。"),
            enrich_segment(
                "昼ご飯は学校の食堂で食べます。醤油をかけたお米が好きです。",
                "I eat lunch at the school cafeteria. I like rice with soy sauce.",
                "午餐在学校食堂吃。喜欢浇了酱油的米饭。"),
            enrich_segment(
                "日本の牛肉はとてもおいしいです。豚肉も鶏肉も好きです。",
                "Japanese beef is very delicious. I also like pork and chicken.",
                "日本的牛肉非常好吃。猪肉和鸡肉也喜欢。"),
            enrich_segment(
                "果物の中ではみかんが一番好きです。",
                "Among fruits, I like tangerines the most.",
                "水果里面最喜欢橘子。"),
            enrich_segment(
                "お菓子も好きです。でも、甘いものを食べすぎると、お腹が痛くなります。",
                "I also like sweets. But if I eat too many sweet things, my stomach hurts.",
                "也喜欢点心。但是甜的吃太多肚子会痛。"),
            enrich_segment(
                "まずい食べ物はあまり食べたくないです。でも、お湯をかけるだけのラーメンは時々食べます。",
                "I don't really want to eat bad-tasting food. But I sometimes eat instant ramen that you just pour hot water on.",
                "难吃的东西不太想吃。不过只要浇热水的方便面偶尔会吃。"),
            enrich_segment(
                "晩ご飯はいつも自分で作ります。茶碗にお米を入れて、おかずはスプーンとフォークとナイフで食べます。",
                "I always cook dinner myself. I put rice in a bowl and eat the side dishes with a spoon, fork, and knife.",
                "晚饭总是自己做。把米饭盛到碗里，配菜用勺子、叉子和刀吃。"),
            enrich_segment(
                "日本に来てから、色々な食べ物を食べました。お酒も少し飲めるようになりました。",
                "Since coming to Japan, I've eaten various foods. I've also become able to drink a little alcohol.",
                "来日本之后吃了各种各样的食物。也变得能喝一点酒了。"),
        ],
    },

    # ===== 6. 生活用品: 换季整理衣柜 =====
    {
        "id": "n4-closet-cleanup-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "衣替えの日",
        "titleJp": "衣替えの日",
        "titleEn": "The day of seasonal wardrobe switch",
        "titleZh": "换季整理衣服的一天",
        "titleRuby": gr.make_ruby("衣替えの日"),
        "segments": [
            enrich_segment(
                "十月に入って急に寒くなった。そろそろ衣替えをしなければと思い、日曜日の朝からクローゼットを開けた。",
                "It suddenly got cold in October. Thinking I should do the seasonal wardrobe switch, I opened the closet on Sunday morning.",
                "进入十月突然变冷了。想着该换季整理衣服了，周日早上打开了衣柜。"),
            enrich_segment(
                "まず、夏の洋服を出す。シャツやTシャツ、スカート、薄いズボンを一枚ずつたたんだ。",
                "First, I took out the summer clothes. I folded shirts, T-shirts, skirts, and thin pants one by one.",
                "先把夏天的衣服拿出来。衬衫、T恤、裙子、薄裤子一件件叠好。"),
            enrich_segment(
                "次に秋冬の服を手前に移す。セーター、コート、厚い靴下、下着も確認した。",
                "Next, I moved the autumn and winter clothes to the front. I also checked sweaters, coats, thick socks, and underwear.",
                "接着把秋冬的衣服移到前面。毛衣、大衣、厚袜子、内衣也确认了。"),
            enrich_segment(
                "靴も入れ替えた。サンダルをしまい、スニーカーとブーツを出した。",
                "I also switched the shoes. I put away the sandals and brought out sneakers and boots.",
                "鞋子也换了。收起凉鞋，拿出运动鞋和靴子。"),
            enrich_segment(
                "ついでに鞄の中身も整理した。古いハンカチとティッシュが出てきた。",
                "While I was at it, I organized the contents of my bag. Old handkerchiefs and tissues came out.",
                "顺便也整理了包里的东西。翻出了旧手帕和纸巾。"),
            enrich_segment(
                "帽子のコーナーも片付けた。黒い帽子と青いキャップを残して、あとは箱に入れた。",
                "I also tidied up the hat section. I kept a black hat and a blue cap, and put the rest in a box.",
                "帽子区域也收拾了。留下黑色帽子和蓝色鸭舌帽，其他装进箱子。"),
            enrich_segment(
                "指輪やアクセサリーは小さな箱にまとめた。ネックレスが絡まっていて、ほどくのに時間がかかった。",
                "I gathered the rings and accessories in a small box. A necklace was tangled and it took time to undo.",
                "戒指和饰品收到小盒子里。项链缠在一起，解了好久。"),
            enrich_segment(
                "ポケットの中からマッチとテープが出てきた。何に使ったのか覚えていない。",
                "A match and some tape came out from a pocket. I don't remember what I used them for.",
                "口袋里翻出了火柴和胶带。不记得用来干什么了。"),
            enrich_segment(
                "午後三時、ようやく終わった。床に座って、すっきりしたクローゼットを眺めた。",
                "At 3 PM, I was finally done. I sat on the floor and looked at the neat closet.",
                "下午三点终于弄完了。坐在地上看着整洁的衣柜。"),
            enrich_segment(
                "丈夫なスーツも見つかった。来週の面接に着ていこう。",
                "I also found a sturdy suit. I'll wear it to next week's interview.",
                "还找到了一套结实的西装。下周面试穿去吧。"),
        ],
    },

    # ===== 7. 生活用品: 家居店买日用品 =====
    {
        "id": "n4-home-center-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "ホームセンターで買い物",
        "titleJp": "ホームセンターで買い物",
        "titleEn": "Shopping at the home center",
        "titleZh": "在家居店购物",
        "titleRuby": gr.make_ruby("ホームセンターで買い物"),
        "segments": [
            enrich_segment(
                "引っ越したばかりで、足りないものがたくさんある。日曜日にホームセンターへ行った。",
                "I just moved and need a lot of things. I went to the home center on Sunday.",
                "刚搬完家，缺的东西太多了。周日去了家居店。"),
            enrich_segment(
                "まず照明コーナーへ向かった。部屋の電球が切れていたので、新しいのを二つ買った。",
                "First I headed to the lighting section. The light bulbs in my room were dead, so I bought two new ones.",
                "先去了照明区。房间的灯泡坏了，买了两个新的。"),
            enrich_segment(
                "次にキッチン用品。石鹸、歯ブラシ、ゴミ袋、ティッシュ。カゴがすぐいっぱいになった。",
                "Next, kitchen supplies. Soap, toothbrush, garbage bags, tissues. The basket was full in no time.",
                "接着是厨房用品。肥皂、牙刷、垃圾袋、纸巾。购物篮一下子就满了。"),
            enrich_segment(
                "工具コーナーで針と糸も見つけた。ズボンのボタンが取れたので、自分で縫おうと思う。",
                "I also found needles and thread in the tool section. A button came off my pants, so I'll sew it myself.",
                "工具区还找到了针和线。裤子扣子掉了，准备自己缝。"),
            enrich_segment(
                "コンセントが足りないので、延長コードを買った。スイッチ付きで便利だ。",
                "I didn't have enough outlets, so I bought an extension cord. It has a switch, which is convenient.",
                "插座不够用，买了延长线。带开关的，很方便。"),
            enrich_segment(
                "ペンキを見て、壁を塗りたくなったが、賃貸だからやめた。",
                "I saw some paint and wanted to paint the walls, but gave up since it's a rental.",
                "看到油漆想刷墙，但因为是租的房子就算了。"),
            enrich_segment(
                "電池とテープも忘れずに買った。時計とリモコンに使う。",
                "I also made sure to buy batteries and tape. For the clock and the remote control.",
                "电池和胶带也没忘了买。用在时钟和遥控器上。"),
            enrich_segment(
                "最後にカーテンを選んだ。丸い柄のものが気に入った。",
                "Finally, I chose curtains. I liked one with a round pattern.",
                "最后选了窗帘。喜欢上了圆形图案的。"),
            enrich_segment(
                "道具を揃えると、新しい部屋がだんだん自分の場所になっていく気がする。",
                "When you get the right tools, the new room gradually starts to feel like your own place.",
                "把东西置办齐了，新房间感觉渐渐变成自己的地方了。"),
        ],
    },

    # ===== 8. 生活用品: 引っ越し先で段ボールを開ける =====
    {
        "id": "n4-unpack-boxes-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "段ボールを開ける夜",
        "titleJp": "段ボールを開ける夜",
        "titleEn": "The night of unpacking boxes",
        "titleZh": "拆快递箱的夜晚",
        "titleRuby": gr.make_ruby("段ボールを開ける夜"),
        "segments": [
            enrich_segment(
                "引っ越しの荷物が届いた。部屋の真ん中に段ボールが十個並んでいる。",
                "The moving shipment arrived. Ten cardboard boxes are lined up in the middle of the room.",
                "搬家的行李到了。房间正中间摆着十个纸箱。"),
            enrich_segment(
                "まず大きな箱を開けた。中には掃除機と電子レンジが入っていた。",
                "I opened the big box first. Inside were a vacuum cleaner and a microwave.",
                "先打开了大箱子。里面是吸尘器和微波炉。"),
            enrich_segment(
                "洗濯機は業者が設置してくれた。冷蔵庫はもう台所に置いてある。",
                "The movers installed the washing machine. The fridge is already in the kitchen.",
                "洗衣机搬家公司帮忙装好了。冰箱已经放在厨房了。"),
            enrich_segment(
                "次の箱からは食器が出てきた。お皿とスプーンとフォークとナイフと茶碗。割れていなくてよかった。",
                "Tableware came out of the next box. Plates, spoons, forks, knives, and rice bowls. Glad nothing was broken.",
                "下一个箱子是餐具。盘子、勺子、叉子、刀和饭碗。没碎真是太好了。"),
            enrich_segment(
                "三番目の箱には布団と毛布と枕。今夜寝る分だけ先にベッドに敷いた。",
                "The third box had a futon, blanket, and pillow. I laid out just enough for tonight on the bed.",
                "第三个箱子是被子、毛毯和枕头。先把今晚要用的铺到了床上。"),
            enrich_segment(
                "洋服の箱はまだ開けていない。ハンガーを買い忘れた。",
                "I haven't opened the clothes box yet. I forgot to buy hangers.",
                "装衣服的箱子还没开。忘了买衣架。"),
            enrich_segment(
                "小さな箱にはアルバムと人形が入っていた。実家から持ってきた大切なものだ。",
                "A small box had a photo album and a doll. Precious things I brought from home.",
                "小箱子里是相册和人偶。从老家带来的重要东西。"),
            enrich_segment(
                "ソファーは明日届く。今夜は床に座布団を敷いて座る。",
                "The sofa arrives tomorrow. Tonight I'll sit on a cushion on the floor.",
                "沙发明天到。今晚在地上铺坐垫坐。"),
            enrich_segment(
                "窓を開けると、涼しい風が入ってきた。新しい生活が始まる気がした。",
                "When I opened the window, cool air came in. It felt like a new life was beginning.",
                "打开窗户，凉风吹了进来。感觉新生活要开始了。"),
        ],
    },

    # ===== 9. 食物料理: 初めて自炊する留学生 =====
    {
        "id": "n4-first-cooking-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "初めての自炊",
        "titleJp": "初めての自炊",
        "titleEn": "Cooking for the first time",
        "titleZh": "第一次自己做饭",
        "titleRuby": gr.make_ruby("初めての自炊"),
        "segments": [
            enrich_segment(
                "日本に来て一週間、ずっとコンビニの弁当を食べていた。そろそろ自炊しようと思った。",
                "For a week since coming to Japan, I'd been eating convenience store bentos. I thought it was time to cook.",
                "来日本一周，一直吃便利店便当。想着差不多该自己做饭了。"),
            enrich_segment(
                "スーパーで米と卵と醤油と砂糖を買った。油とお酒も買った。",
                "At the supermarket, I bought rice, eggs, soy sauce, and sugar. I also bought oil and sake.",
                "在超市买了米、鸡蛋、酱油和砂糖。也买了油和料酒。"),
            enrich_segment(
                "家に帰って、まず炊飯器でお米を炊いた。三十分くらい待つ。",
                "I went home and first cooked rice in the rice cooker. Wait about thirty minutes.",
                "回到家先用电饭锅煮米饭。等了大约三十分钟。"),
            enrich_segment(
                "フライパンに油を引いて、卵を割った。醤油を少しかけて、卵焼きを作った。",
                "I put oil in the frying pan and cracked the eggs. I added a little soy sauce and made a rolled omelet.",
                "在平底锅里倒油，打了鸡蛋。加了点酱油，做了煎蛋卷。"),
            enrich_segment(
                "茶碗にご飯を入れて、お皿に卵焼きを乗せた。スプーンもフォークも出したが、結局箸で食べた。",
                "I put rice in a bowl and placed the omelet on a plate. I got out a spoon and fork too, but ended up eating with chopsticks.",
                "把饭盛到碗里，煎蛋卷放到盘子上。勺子叉子也拿出来了，最后还是用筷子吃了。"),
            enrich_segment(
                "味は……まずくはないが、お母さんの料理とは全然違う。",
                "The taste... it wasn't bad, but it was nothing like my mother's cooking.",
                "味道嘛……不难吃，但跟妈妈做的完全不一样。"),
            enrich_segment(
                "食べ終わって、お湯で食器を洗った。包丁は今日は使わなかった。",
                "After eating, I washed the dishes with hot water. I didn't use the knife today.",
                "吃完用热水洗了碗碟。今天没用菜刀。"),
            enrich_segment(
                "明日は豆腐と豚肉で何か作ってみよう。",
                "Tomorrow I'll try making something with tofu and pork.",
                "明天用豆腐和猪肉试试做点什么吧。"),
            enrich_segment(
                "自分で作ると、食べ物を大切にする気持ちが分かる。",
                "When you cook yourself, you understand the feeling of valuing food.",
                "自己动手做了才知道珍惜食物的心情。"),
        ],
    },

    # ===== 10. 食物料理: お弁当を作る朝 =====
    {
        "id": "n4-bento-morning-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "お弁当を作る朝",
        "titleJp": "お弁当を作る朝",
        "titleEn": "The morning I make a bento",
        "titleZh": "做便当的早晨",
        "titleRuby": gr.make_ruby("お弁当を作る朝"),
        "segments": [
            enrich_segment(
                "朝五時半に目覚ましが鳴った。今日はお弁当を作る日だ。",
                "The alarm rang at 5:30 AM. Today is a bento-making day.",
                "早上五点半闹钟响了。今天是做便当的日子。"),
            enrich_segment(
                "まず弁当箱を出して、おかずの材料を並べる。卵、鶏肉、野菜。",
                "First, I take out the bento box and line up the ingredients. Eggs, chicken, vegetables.",
                "先拿出便当盒，把配菜材料摆好。鸡蛋、鸡肉、蔬菜。"),
            enrich_segment(
                "フライパンで鶏肉を焼く。醤油と砂糖で味をつける。",
                "I fry the chicken in a pan. I season it with soy sauce and sugar.",
                "用平底锅煎鸡肉。用酱油和砂糖调味。"),
            enrich_segment(
                "卵は甘い卵焼きにした。ちょっと焦げたが、まあいい。",
                "I made the eggs into a sweet omelet. It's a little burnt, but oh well.",
                "鸡蛋做成了甜蛋卷。稍微焦了一点，算了。"),
            enrich_segment(
                "炊飯器のお米を弁当箱に詰めて、おかずを横に並べた。",
                "I packed the rice from the rice cooker into the bento box and arranged the side dishes next to it.",
                "把电饭锅里的米饭装进便当盒，配菜摆在旁边。"),
            enrich_segment(
                "小さいカップにデザートの果物を入れた。今日はぶどうにした。",
                "I put dessert fruit in a small cup. Today I chose grapes.",
                "在小杯里放了甜品水果。今天选的是葡萄。"),
            enrich_segment(
                "ナイフでチーズを切って、すきまに入れた。彩りがよくなった。",
                "I cut cheese with a knife and tucked it in the gaps. The colors looked better.",
                "用刀切了奶酪塞进空隙。颜色好看多了。"),
            enrich_segment(
                "蓋をして、ゴムで止めて、鞄に入れた。食べるのが楽しみだ。",
                "I put on the lid, secured it with a rubber band, and put it in my bag. I can't wait to eat it.",
                "盖上盖子、用皮筋固定、放进包里。好期待吃的时候。"),
            enrich_segment(
                "食堂で買うより安いし、自分で作ると好きなおかずを入れられる。",
                "It's cheaper than buying at the cafeteria, and when I make it myself I can put in the side dishes I like.",
                "比在食堂买便宜，而且自己做可以放喜欢的菜。"),
            enrich_segment(
                "お弁当を開けたとき、朝の頑張りを思い出してうれしくなる。",
                "When I open the bento, I remember the morning effort and feel happy.",
                "打开便当的时候，想起早上的努力就很开心。"),
        ],
    },

    # ===== 11. 食物料理: 居酒屋で忘年会 =====
    {
        "id": "n3-izakaya-party-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "居酒屋での忘年会",
        "titleJp": "居酒屋での忘年会",
        "titleEn": "Year-end party at an izakaya",
        "titleZh": "在居酒屋的忘年会",
        "titleRuby": gr.make_ruby("居酒屋での忘年会"),
        "segments": [
            enrich_segment(
                "十二月の金曜日、職場の忘年会が居酒屋であった。",
                "On a Friday in December, our office year-end party was held at an izakaya.",
                "十二月的一个周五，单位的忘年会在居酒屋举办。"),
            enrich_segment(
                "メニューを見ながら、まず飲み物を決める。日本酒、ワイン、ビール。わたしはビールにした。",
                "Looking at the menu, we first decide on drinks. Sake, wine, beer. I chose beer.",
                "看着菜单先选饮品。日本酒、葡萄酒、啤酒。我选了啤酒。"),
            enrich_segment(
                "乾杯のあと、料理が次々に運ばれてきた。",
                "After the toast, dishes were brought out one after another.",
                "干杯之后，菜一道道端上来了。"),
            enrich_segment(
                "焼肉、寿司、餃子。テーブルがあっという間にいっぱいになった。",
                "Grilled meat, sushi, gyoza. The table was full in no time.",
                "烤肉、寿司、饺子。桌子一转眼就摆满了。"),
            enrich_segment(
                "焼肉は塩で食べた。醤油よりさっぱりしていておいしい。",
                "I ate the grilled meat with salt. It's lighter than soy sauce and delicious.",
                "烤肉蘸盐吃。比酱油清淡，好吃。"),
            enrich_segment(
                "日本酒を一杯だけ飲んでみた。辛いが、魚に合う。",
                "I tried just one cup of sake. It's dry, but it goes well with fish.",
                "尝了一杯日本酒。辣辣的，但配鱼很搭。"),
            enrich_segment(
                "デザートにはアイスクリームとケーキが出た。甘いものは別腹だ。",
                "For dessert, ice cream and cake came out. There's always room for sweets.",
                "甜品上了冰淇淋和蛋糕。甜食是装在另一个胃里的。"),
            enrich_segment(
                "ジュースを追加で頼んだ。おかわりは無料だった。",
                "I ordered more juice. Refills were free.",
                "又加了果汁。续杯是免费的。"),
            enrich_segment(
                "食べすぎてお腹がいっぱいだ。隣の先輩も「もう食べられない」と笑っていた。",
                "I ate too much and was stuffed. The senior next to me was laughing saying 'I can't eat any more.'",
                "吃太多撑死了。旁边的前辈也笑着说「吃不下了」。"),
            enrich_segment(
                "帰り道、冬の夜風が気持ちよかった。来年もみんなで来たい。",
                "On the way home, the winter night breeze felt nice. I want to come again with everyone next year.",
                "回去的路上，冬夜的风很舒服。明年也想大家一起来。"),
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

        # Convert raw tuple segments to enriched dicts
        enriched_segments = []
        for seg in item.get("segments", []):
            if isinstance(seg, tuple):
                enriched_segments.append(enrich_segment(*seg))
            else:
                enriched_segments.append(seg)
        item["segments"] = enriched_segments

        # Enrich titleRuby if empty
        if not item.get("titleRuby"):
            item["titleRuby"] = gr.make_ruby(item["titleWord"])

        # Add grammar field
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
