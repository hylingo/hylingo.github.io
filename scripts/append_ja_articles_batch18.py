#!/usr/bin/env python3
"""
batch18 → public/data/ja_articles.json

修复问题文章:
1. 重写 n3-tokyo-day-essay (缩到20句)
2. 重写 n2-moving-essay (缩到20句)
3. 补写 n4-weekend-essay
4. 补写 n3-decline-request-dialogue
5. 补写 n2-moving-dialogue (分幕)

运行: python3 scripts/append_ja_articles_batch18.py
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


# ── Articles to REPLACE (remove old, add new) ──
REPLACE_IDS = ["n3-tokyo-day-essay", "n2-moving-essay"]

NEW_ITEMS: list[dict] = [

    # ═══════════════════════════════════════════
    # 1. n3-tokyo-day-essay (重写, 20句)
    # ═══════════════════════════════════════════
    {
        "id": "n3-tokyo-day-essay",
        "level": "N5–N3",
        "format": "essay",
        "titleWord": "東京での一日",
        "titleJp": "東京での一日",
        "titleEn": "A day in Tokyo",
        "titleZh": "在东京的一天",
        "titleRuby": [],
        "segments": [
            seg("わたしの名前はリンです。中国から来た留学生で、今東京の小さなアパートに住んでいます。",
                "My name is Rin. I'm a student from China, and I live in a small apartment in Tokyo.",
                "我叫琳。是从中国来的留学生，现在住在东京一间小公寓里。", True),
            seg("朝六時半に起きて、シャワーを浴びてから朝ご飯を食べます。今朝はトーストと目玉焼きでした。",
                "I wake up at 6:30, take a shower, and eat breakfast. This morning it was toast and a fried egg.",
                "早上六点半起床，洗了澡吃早饭。今天早上吃的吐司和煎蛋。"),
            seg("七時半に家を出ます。駅まで歩いて十分。朝の電車はとても混んでいて、いつも立ちっぱなしです。",
                "I leave home at 7:30. It's a ten-minute walk to the station. The morning train is very crowded and I always have to stand.",
                "七点半出门。走到车站十分钟。早上的电车很挤，总是站着。"),
            seg("イヤホンでポッドキャストを聞いていると、満員電車もちょっと楽になります。",
                "Listening to podcasts with my earbuds makes the packed train a bit more bearable.",
                "戴耳机听播客的话，满员电车也能好受一点。", True),
            seg("学校に着くと、クラスメートのジェームズがいつも冗談を言って笑わせてくれます。",
                "When I get to school, my classmate James always cracks jokes and makes me laugh.",
                "到了学校，同学詹姆斯总是讲笑话逗大家笑。"),
            seg("今日の授業は文法が難しかったけど、先生の説明が分かりやすかったので助かりました。",
                "Today's grammar lesson was tough, but the teacher's explanation was easy to follow, which helped.",
                "今天语法课很难，但老师讲得很清楚帮了大忙。"),
            seg("お昼は学校の近くの定食屋で食べました。魚と味噌汁と漬物のセットで六百円。",
                "I ate lunch at a set-meal restaurant near school. A set of fish, miso soup, and pickles for 600 yen.",
                "午饭在学校附近的定食店吃的。鱼、味噌汤和腌菜的套餐六百日元。", True),
            seg("おばさんが「日本語上手になったね」と言ってくれて、嬉しかったです。",
                "The lady there said 'Your Japanese has gotten better,' which made me happy.",
                "老板娘说「日语进步了嘛」，很开心。"),
            seg("午後はアルバイトです。駅前のコンビニで週に三回働いています。",
                "In the afternoon I have my part-time job. I work at a convenience store near the station three times a week.",
                "下午去打工。每周在车站前的便利店工作三次。"),
            seg("最初は敬語が大変でしたが、今はだいぶ慣れました。レジの操作もスムーズになってきました。",
                "Keigo was hard at first, but I've gotten used to it. I've gotten smoother at the register too.",
                "一开始敬语很难，但现在已经习惯多了。收银操作也越来越顺了。", True),
            seg("店長は優しい人で、忙しいときでも怒らないので、安心して働けます。",
                "The manager is a kind person and doesn't get angry even when it's busy, so I can work without worry.",
                "店长人很好，忙的时候也不发火，能安心工作。"),
            seg("バイトが終わって、スーパーで豆腐と卵を買いました。今夜は自炊します。",
                "After work, I bought tofu and eggs at the supermarket. Tonight I'll cook for myself.",
                "下班后在超市买了豆腐和鸡蛋。今晚自己做饭。"),
            seg("帰り道、夕焼けがきれいでした。東京のビルの間から見える空が好きです。",
                "On the way home, the sunset was beautiful. I like the sky you can see between Tokyo's buildings.",
                "回家路上晚霞很美。喜欢从东京大楼之间看到的天空。", True),
            seg("夜、部屋で宿題をしてから、国の家族にビデオ電話をしました。",
                "At night, after doing homework in my room, I video-called my family back home.",
                "晚上在房间做完作业后，给国内的家人打了视频电话。"),
            seg("お母さんが「ちゃんと食べてる？」と心配してくれました。毎回同じことを聞かれます。",
                "My mom asked 'Are you eating properly?' She asks the same thing every time.",
                "妈妈担心地问「好好吃饭了吗」。每次都问同样的话。"),
            seg("ことばが通じなくて困ることもあるし、寂しくなることもあります。",
                "Sometimes I have trouble communicating, and sometimes I feel lonely.",
                "有时候语言不通会困扰，有时候也会寂寞。", True),
            seg("でも、新しいことばを覚えるたびに、世界が少し広くなる気がします。",
                "But every time I learn a new word, I feel like the world gets a little bigger.",
                "但每学会一个新词，就觉得世界变大了一点。"),
            seg("来月は日本語能力試験があります。N3に合格したいです。",
                "Next month is the JLPT. I want to pass N3.",
                "下个月有日语能力考试。想通过N3。"),
            seg("忙しいけど、充実した毎日です。明日も頑張ります。",
                "It's busy, but every day is fulfilling. I'll do my best tomorrow too.",
                "虽然忙，但每天都很充实。明天也加油。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n2-moving-essay (重写, 20句)
    # ═══════════════════════════════════════════
    {
        "id": "n2-moving-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "引っ越しで変わったこと",
        "titleJp": "引っ越しで変わったこと",
        "titleEn": "What changed after moving",
        "titleZh": "搬家后变化的事",
        "titleRuby": [],
        "segments": [
            seg("最近、引っ越しをした。前のアパートには四年住んでいたから、荷物の量が自分でも驚くほどだった。",
                "I recently moved. I'd lived in the previous apartment for four years, so the amount of stuff surprised even me.",
                "最近搬了家。在前一间公寓住了四年，行李多得连自己都吃惊。", True),
            seg("「いつか使うかもしれない」と取っておいたものが押し入れの奥から次々と出てきた。三年前のヨガマット、大学の教科書。",
                "Things I'd kept 'just in case' kept emerging from the back of the closet. A yoga mat from three years ago, university textbooks.",
                "「说不定以后用得上」而留着的东西从壁橱深处一个接一个冒出来。三年前的瑜伽垫、大学课本。"),
            seg("引っ越しの理由は、上の階の生活音だった。毎晩ドタドタと足音がして、寝不足が続いていた。",
                "The reason for moving was the noise from upstairs. Footsteps thudded every night, and I'd been chronically sleep-deprived.",
                "搬家的原因是楼上的生活噪音。每晚咚咚的脚步声，一直睡不好。"),
            seg("管理会社に相談しても状況は変わらず、限界を感じて引っ越しを決めた。",
                "Even after consulting the management company, nothing changed. I felt I'd reached my limit and decided to move.",
                "跟管理公司反映了也没改善，觉得到极限了就决定搬家。", True),
            seg("新しい部屋は駅から遠くなったが、近くに大きな公園がある。朝、窓を開けると木の匂いがする。",
                "The new place is farther from the station, but there's a large park nearby. When I open the window in the morning, I can smell the trees.",
                "新房子离车站远了，但附近有大公园。早上开窗能闻到树木的味道。"),
            seg("引っ越しで一番面倒だったのは役所の手続きだった。転出届、転入届、マイナンバーの住所変更。",
                "The most annoying part of moving was the paperwork at city hall. Move-out notice, move-in notice, My Number address change.",
                "搬家最麻烦的是去政府办手续。迁出证明、迁入证明、个人编号地址变更。"),
            seg("全部まとめてやると丸一日かかる。平日しか受け付けていないので、仕事を休む必要があった。",
                "Doing it all at once takes a full day. It's only available on weekdays, so I had to take time off work.",
                "全部一起办的话要花整整一天。只有工作日受理，得请假。", True),
            seg("なぜオンラインでできないのかと、窓口で待ちながら何度も思った。",
                "I kept thinking 'why can't this be done online' while waiting at the counter.",
                "在窗口排队的时候反复想，为什么不能网上办。"),
            seg("それでも、新しい部屋での生活は気に入っている。休みの日は公園を散歩するのが習慣になった。",
                "Still, I like life in the new place. Going for walks in the park on days off has become a habit.",
                "不过还是很喜欢新房子的生活。休息日去公园散步成了习惯。", True),
            seg("先週、ベンチに座っていたら隣のおばあさんに話しかけられた。この公園の桜は五十年以上前に植えられたものらしい。",
                "Last week, sitting on a bench, the lady next to me started talking. The cherry trees in this park were apparently planted over 50 years ago.",
                "上周坐在长椅上，旁边的老奶奶跟我搭话。说这公园的樱花树是五十多年前种的。"),
            seg("こういう何気ない会話が、新しい街に馴染んでいく感覚をくれる。",
                "These casual conversations give me the feeling of gradually fitting into the new town.",
                "这种不经意的对话让人感觉在渐渐融入新的街区。"),
            seg("スーパーもようやく開拓してきた。駅前のチェーン店は品揃えがいいが高い。",
                "I've finally explored the supermarkets too. The chain store by the station has good selection but is pricey.",
                "超市也终于摸清了。车站前的连锁店品种齐全但贵。", True),
            seg("一本裏の商店街の八百屋は野菜が新鮮で安い。自分なりの「生活圏」ができてくると、その街に住んでいる実感が湧く。",
                "The greengrocer on the back street has fresh, cheap vegetables. As I build my own 'living zone,' I start to feel like I really live here.",
                "后面商店街的菜店蔬菜新鲜又便宜。渐渐有了自己的「生活圈」，就有了住在这里的实感。"),
            seg("自炊も前よりするようになった。前のアパートはキッチンが狭すぎて、まな板を置くスペースすらなかった。",
                "I cook more than before too. The old apartment's kitchen was too small — there wasn't even room for a cutting board.",
                "自己做饭也比以前多了。前面公寓厨房太小，连放砧板的地方都没有。"),
            seg("新しいキッチンは少し広いので、この前初めて肉じゃがに挑戦してみた。煮込みすぎてじゃがいもが全部溶けた。",
                "The new kitchen is a bit bigger, so I tried making nikujaga for the first time. I simmered it too long and all the potatoes dissolved.",
                "新厨房大了一点，前几天第一次挑战做肉炖土豆。炖过头了土豆全化了。", True),
            seg("見た目はひどかったが、味は意外と悪くなかった。",
                "It looked terrible, but the taste was surprisingly not bad.",
                "卖相很差，但味道意外地还行。"),
            seg("夜、ベランダに出ると、遠くにマンションの明かりが見える。それぞれの窓の向こうに、それぞれの生活がある。",
                "At night, when I step onto the balcony, I can see apartment lights in the distance. Behind each window, there's a different life.",
                "晚上走到阳台上，远处能看到公寓楼的灯光。每扇窗户后面都有各自的生活。"),
            seg("場所が変わるだけで、見えるものも考えることも変わる。たかが引っ越しだけど、自分にとっては大きなリセットだった。",
                "Just by changing places, what you see and what you think about changes. It's just a move, but for me it was a big reset.",
                "只是换了个地方，看到的东西和想的事情就不一样了。虽然只是搬家，但对我来说是一次很大的重启。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-weekend-essay 周末（配合已有dialogue）
    # ═══════════════════════════════════════════
    {
        "id": "n4-weekend-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "友達と新宿に行った日",
        "titleJp": "友達と新宿に行った日",
        "titleEn": "The day I went to Shinjuku with a friend",
        "titleZh": "和朋友去新宿的那天",
        "titleRuby": [],
        "segments": [
            seg("土曜日の夜、友達のユキからLINEが来た。「明日暇？買い物に行かない？」。",
                "Saturday night, I got a LINE message from my friend Yuki. 'Free tomorrow? Want to go shopping?'",
                "周六晚上朋友优纪发来LINE。「明天有空吗？去逛街？」。", True),
            seg("新宿に行くことにした。大きい本屋にも寄りたかったし、ちょうど服も見たかった。",
                "We decided to go to Shinjuku. I wanted to stop by the big bookstore and was also looking for clothes.",
                "决定去新宿。想去大书店，正好也想看衣服。"),
            seg("天気予報を見たら午後から雨が降りそうだったので、傘を持って出かけた。",
                "The weather forecast said it might rain in the afternoon, so I brought an umbrella.",
                "看天气预报说下午可能下雨，就带着伞出了门。"),
            seg("十時に駅で待ち合わせた。ユキはもう来ていて、「早いね」と笑った。",
                "We met at the station at 10. Yuki was already there and laughed, saying 'You're early.'",
                "十点在车站碰头。优纪已经到了，笑着说「好早啊」。", True),
            seg("電車に乗って新宿に向かった。日曜なのに電車は空いていた。",
                "We took the train to Shinjuku. The train was empty despite it being Sunday.",
                "坐电车去新宿。明明是周日电车却挺空。"),
            seg("まず服屋に入った。赤いワンピースがかわいくて、試着してみた。",
                "First we went into a clothing store. I found a cute red dress and tried it on.",
                "先进了服装店。看到一件红色连衣裙很好看，试穿了一下。"),
            seg("でもサイズが小さくて、もう一つ大きいのはないかと聞いたが、それしかなかった。残念だった。",
                "But the size was too small. I asked if they had a bigger one, but that was all they had. Too bad.",
                "但尺码小了。问有没有大一号的，说只有这个。好可惜。", True),
            seg("お昼になってラーメン屋に入った。店の前に行列ができていて、二十分ほど並んだ。",
                "At noon we went to a ramen shop. There was a line out front and we waited about twenty minutes.",
                "到了中午去拉面店。门口排着队，等了大约二十分钟。"),
            seg("ユキが友達に教えてもらった店で、食べてみたらすごくおいしかった。今まで食べた中で一番かもしれない。",
                "It was a place a friend told Yuki about. When we tried it, it was incredibly good. Maybe the best I've ever had.",
                "是优纪朋友推荐的店，一吃超好吃。可能是吃过最好吃的。"),
            seg("午後は本屋に行った。日本語の小説を買いたかったけど、どれが自分のレベルに合うか分からなかった。",
                "In the afternoon we went to the bookstore. I wanted to buy a Japanese novel but didn't know which one suited my level.",
                "下午去了书店。想买日语小说，但不知道哪本适合自己的水平。", True),
            seg("ユキが「この作家の本は読みやすいって聞いたよ」と勧めてくれた。少し読んでみたら大丈夫そうだったので買った。",
                "Yuki recommended one: 'I heard this author's books are easy to read.' I tried reading a bit and it seemed fine, so I bought it.",
                "优纪推荐说「听说这个作家的书很好读」。翻了一下觉得能读就买了。"),
            seg("本屋を出たら雨が降り始めていた。ユキは傘を持ってきていなかった。",
                "When we left the bookstore, it had started raining. Yuki hadn't brought an umbrella.",
                "走出书店雨已经下起来了。优纪没带伞。"),
            seg("「入れてもらっていい？」と聞かれたので、一本の傘に二人で入って歩いた。ちょっと濡れたけど楽しかった。",
                "'Can I share?' she asked, so we walked together under one umbrella. We got a bit wet but it was fun.",
                "问「能一起撑吗」，两人合撑一把伞走着。虽然淋了一点但很开心。", True),
            seg("駅で別れるとき、ユキが「今日楽しかったね。また遊ぼう」と言った。",
                "When we parted at the station, Yuki said 'Today was fun. Let's hang out again.'",
                "在车站分别时优纪说「今天好开心。下次再玩」。"),
            seg("家に帰ってから、買った小説を少し読んだ。知らない単語もあったけど、話が面白くてページが進んだ。",
                "After getting home, I read a bit of the novel I bought. There were some unknown words, but the story was interesting and the pages turned quickly.",
                "到家后看了会买的小说。有不认识的词，但故事有趣读得很快。"),
            seg("楽しい時間は早く過ぎるものだと思った。来週もどこかに行きたい。",
                "Fun times really do pass quickly. I want to go somewhere next week too.",
                "开心的时光果然过得快。下周也想去哪里逛逛。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 4. n3-decline-request-dialogue（配合已有 essay）
    # ═══════════════════════════════════════════
    {
        "id": "n3-decline-request-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "急な依頼を断る",
        "titleJp": "急な依頼を断る",
        "titleEn": "Declining an urgent request",
        "titleZh": "婉拒临时请求",
        "titleRuby": [],
        "sections": [
            section("依頼される", "Receiving the request", "被委托", "📋", [
                line("A", "ねえ、来週の企画書、私の分の資料まとめ手伝ってくれない？急に上から言われてさ。",
                     "Hey, can you help me put together materials for next week's proposal? I just got asked by management.",
                     "诶，下周的企划书，能帮我整理一下我那部分的资料吗？上面突然说的。"),
                line("B", "来週か……。今週どのくらい忙しいか見てみるね。",
                     "Next week... Let me check how busy I am this week.",
                     "下周啊……。我先看看这周多忙。"),
                line("A", "金曜までにできるとありがたいんだけど。",
                     "I'd appreciate it if you could do it by Friday.",
                     "周五之前搞定的话就太好了。"),
                line("B", "ごめん、今週はレビューと納品が三つ重なってて、ちょっと厳しい。",
                     "Sorry, this week I have three reviews and deliveries overlapping, so it's tough.",
                     "抱歉，这周评审和交付有三个撞在一起了，有点难。"),
                line("A", "そっか……。全部じゃなくても、一部だけでも助かるんだけど。",
                     "I see... Even just part of it would help.",
                     "这样啊……。不用全部，帮一部分也行的。"),
            ]),
            section("代案を出す", "Offering an alternative", "提出替代方案", "💡", [
                line("B", "テンプレだけなら今日中に共有できるよ。書式を揃えておけば、あとは自分のペースで埋められると思う。",
                     "I can share the template by today. If the format is set, you can fill in the rest at your own pace.",
                     "只是模板的话今天之内能共享。格式统一好了，剩下的按自己节奏填就行。"),
                line("A", "あ、それだけでも全然違う。助かる。",
                     "Oh, even just that makes a huge difference. That helps.",
                     "啊，光那样就完全不一样了。太好了。"),
                line("B", "あと、来週の火曜午後なら二時間くらい一緒に見られるよ。",
                     "Also, Tuesday afternoon next week I can spend about two hours looking at it with you.",
                     "另外下周二下午的话，能花两个小时一起看。"),
                line("A", "本当？じゃあ火曜にまとめてチェックしてもらおうかな。",
                     "Really? Then maybe I'll have you review it all together on Tuesday.",
                     "真的？那周二统一让你帮忙看看。"),
                line("B", "うん。無理に今週詰め込んで雑になるよりは、そっちの方がいいと思う。",
                     "Yeah. I think that's better than cramming it in this week and making it sloppy.",
                     "嗯。比硬塞到这周弄得粗糙要好。"),
                line("A", "ありがとう。上には「テンプレ協力あり」って伝えておくね。",
                     "Thanks. I'll tell management 'template assistance provided.'",
                     "谢谢。跟上面说「有模板协助」。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 5. n2-moving-dialogue（配合重写的 essay, 分3幕）
    # ═══════════════════════════════════════════
    {
        "id": "n2-moving-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "新居に遊びに来た友達",
        "titleJp": "新居に遊びに来た友達",
        "titleEn": "A friend visiting the new place",
        "titleZh": "朋友来新家玩",
        "titleRuby": [],
        "sections": [
            section("部屋に入る", "Entering the room", "进门", "🏠", [
                line("A", "おー、いい部屋じゃん。前より広いね。",
                     "Oh, nice place. It's bigger than before.",
                     "哦——挺好的房间嘛。比以前大。"),
                line("B", "でしょ？駅からは遠くなったけど、静かなのがいい。",
                     "Right? It's farther from the station, but the quiet is nice.",
                     "是吧？离车站远了，但安静这点好。"),
                line("A", "前のとこ、上の階うるさかったんだっけ。",
                     "The old place, the upstairs neighbor was noisy, right?",
                     "之前那边楼上很吵来着吧。"),
                line("B", "毎晩ドタドタしてさ。管理会社に言っても全然変わらなくて。",
                     "Stomping every night. I told the management company but nothing changed.",
                     "每晚咚咚咚的。跟管理公司说了也完全没用。"),
                line("A", "それは辛いわ。ここは静か？",
                     "That's rough. Is it quiet here?",
                     "那确实受不了。这边安静吗？"),
                line("B", "めちゃくちゃ静か。夜、虫の声しか聞こえない。",
                     "Super quiet. At night you can only hear insects.",
                     "安静得不行。晚上只听到虫子叫。"),
            ]),
            section("手続きの愚痴", "Complaining about paperwork", "吐槽办手续", "📄", [
                line("A", "引っ越しの手続き、大変だった？",
                     "Was the moving paperwork a hassle?",
                     "搬家手续麻烦吗？"),
                line("B", "転出届、転入届、マイナンバー、保険……。丸一日かかったよ。",
                     "Move-out notice, move-in notice, My Number, insurance... It took a whole day.",
                     "迁出、迁入、个人编号、保险……。花了整整一天。"),
                line("A", "全部窓口？オンラインでできないの？",
                     "All at the counter? Can't you do it online?",
                     "全在窗口？不能网上办吗？"),
                line("B", "それずっと思ってた。しかも平日しかやってないから仕事休んだ。",
                     "I've been thinking that the whole time. Plus it's only weekdays so I had to take off work.",
                     "我一直在想这个。而且只有工作日受理，请了假。"),
                line("A", "令和なのにねえ。",
                     "And this is the Reiwa era...",
                     "都令和了还这样……"),
                line("B", "ほんとそれ。",
                     "Seriously.",
                     "可不是嘛。"),
            ]),
            section("新生活の話", "Talking about the new life", "聊新生活", "🌳", [
                line("A", "近くに公園あるって言ってたよね。散歩してる？",
                     "You said there's a park nearby, right? Do you go for walks?",
                     "你说附近有公园来着吧。去散步吗？"),
                line("B", "うん、休みの日は必ず。この前ベンチでおばあさんと話し込んじゃって。",
                     "Yeah, every day off. The other day I ended up chatting with an old lady on a bench.",
                     "嗯，休息日一定去。前几天还在长椅上跟一个老奶奶聊了好久。"),
                line("A", "へえ、何の話？",
                     "Oh, what about?",
                     "诶，聊什么？"),
                line("B", "公園の桜が五十年前に植えられたとか。昔はこの辺全部田んぼだったらしい。",
                     "Like how the cherry trees were planted 50 years ago. Apparently this area used to be all rice paddies.",
                     "说公园的樱花树五十年前种的。说这一带以前全是稻田。"),
                line("A", "いい話。自炊はしてる？",
                     "Nice story. Are you cooking?",
                     "好故事。自己做饭吗？"),
                line("B", "この前初めて肉じゃが作ったんだけど、じゃがいも全部溶けた。",
                     "I tried making nikujaga for the first time, but all the potatoes dissolved.",
                     "前几天第一次做肉炖土豆，土豆全化了。"),
                line("A", "あはは。味は？",
                     "Haha. How did it taste?",
                     "哈哈哈。味道呢？"),
                line("B", "意外と悪くなかったよ。見た目は最悪だったけど。",
                     "Surprisingly not bad. It looked terrible though.",
                     "意外地还行。虽然卖相最差。"),
            ]),
        ],
    },
]


def main() -> None:
    path = ROOT / "public" / "data" / "ja_articles.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Remove articles that need replacing
    before = len(data["items"])
    data["items"] = [item for item in data["items"] if item["id"] not in REPLACE_IDS]
    removed = before - len(data["items"])
    print(f"Removed {removed} articles for replacement")

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

    print(f"\nDone: replaced {removed}, added {added}, total {len(data['items'])} articles")


if __name__ == "__main__":
    main()
