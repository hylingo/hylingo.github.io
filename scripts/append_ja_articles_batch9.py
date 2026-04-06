#!/usr/bin/env python3
"""
batch9 → public/data/ja_articles.json

P1: 6篇家庭/人际关系主题 (3 essay + 3 dialogue, 口语化对话)

运行: python3 scripts/append_ja_articles_batch9.py
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

    # ===== 1. 介绍家人 (essay, N5-N4) =====
    {
        "id": "n5-family-intro-essay",
        "level": "N5–N4",
        "format": "essay",
        "titleWord": "うちの家族はこんな人たち",
        "titleJp": "うちの家族はこんな人たち",
        "titleEn": "What my family is like",
        "titleZh": "我家人是这样的",
        "titleRuby": [],
        "segments": [
            ("うちは六人家族だ。父親、母親、兄、姉、弟、そしてわたし。",
             "We're a family of six. Father, mother, older brother, older sister, younger brother, and me.",
             "我家六口人。爸爸、妈妈、哥哥、姐姐、弟弟、还有我。"),
            ("父親は五十三歳で、銀行に勤めている。毎朝ネクタイをして出かける。背が高くて、男の人の中では目立つ。",
             "My father is 53 and works at a bank. He goes out in a tie every morning. He's tall and stands out among men.",
             "爸爸五十三岁，在银行上班。每天早上系着领带出门。个子高，在男性里很显眼。"),
            ("母親は料理が上手で、毎日の晩ご飯がいつもおいしい。奥さんとしても、お母さんとしても、すごい人だと思う。",
             "My mother is a great cook, and dinner every day is always delicious. I think she's amazing both as a wife and as a mother.",
             "妈妈做菜很好，每天的晚饭都好吃。不管是作为妻子还是妈妈，我觉得她都很厉害。"),
            ("兄は二十五歳で、もう結婚している。お嫁さんは優しい人だ。",
             "My brother is 25 and already married. His wife is a kind person.",
             "哥哥二十五岁，已经结婚了。嫂子人很温柔。"),
            ("姉は大学生で、姉妹のように仲がいい友達がたくさんいる。",
             "My sister is a college student and has many friends she's close with, like sisters.",
             "姐姐是大学生，有很多像姐妹一样要好的朋友。"),
            ("弟は中学生だ。毎日うるさいけど、兄弟の中で一番おもしろい。",
             "My younger brother is a middle school student. He's noisy every day, but the funniest among the siblings.",
             "弟弟是初中生。每天吵吵闹闹的，但兄弟姐妹里他最有意思。"),
            ("祖父と祖母は田舎に住んでいる。おじいさんは八十歳だが、畑仕事をしていて元気だ。",
             "My grandparents live in the countryside. My grandfather is 80 but stays active working in the fields.",
             "爷爷奶奶住在乡下。爷爷八十岁了，但干着农活很精神。"),
            ("お正月やお盆になると、親戚が大勢集まる。おじさんやおばさん、従兄弟も来る。",
             "At New Year's and Obon, a lot of relatives gather. Uncles, aunts, and cousins come too.",
             "新年和盂兰盆节，亲戚们一大群聚在一起。叔叔阿姨、堂兄弟都来。"),
            ("大勢で食べるご飯はにぎやかで楽しい。これからもずっとこんな家族でいたい。",
             "Eating together with many people is lively and fun. I want us to always stay a family like this.",
             "一大家子吃饭又热闹又开心。希望以后也一直是这样的一家人。"),
        ],
    },

    # ===== 2. 新年亲戚聚会 (dialogue, N5-N3, 口語化) =====
    {
        "id": "n4-new-year-relatives-dialogue",
        "level": "N5–N3",
        "format": "dialogue",
        "titleWord": "お正月に親戚が集まる（従兄弟同士）",
        "titleJp": "お正月に親戚が集まる（従兄弟同士）",
        "titleEn": "Relatives gathering at New Year's (between cousins)",
        "titleZh": "新年亲戚聚会（堂兄弟之间）",
        "titleRuby": [],
        "sections": [
            section("久しぶりの再会", "Reunion after a long time", "久别重逢", "🎍", [
                ("A", "あっ、久しぶり！いつ来たの？",
                 "Oh, long time no see! When did you get here?",
                 "啊，好久不见！什么时候来的？"),
                ("B", "一昨日の夜。お父さんの車で来たんだけど、渋滞がすごくてさ。",
                 "The night before yesterday. We came in Dad's car, but the traffic was terrible.",
                 "前天晚上。坐爸爸的车来的，堵车堵得要命。"),
                ("A", "あー、年末はどこも混んでるよね。おじさんとおばさんは元気？",
                 "Ah, everywhere is crowded at year-end, right? How are your dad and mom?",
                 "啊——年底哪里都堵。叔叔阿姨还好吧？"),
                ("B", "うん、元気。叔母さんがおせち作ってくれてるよ。台所にいる。",
                 "Yeah, they're fine. Auntie is making osechi. She's in the kitchen.",
                 "嗯，挺好的。阿姨在做御节料理呢。在厨房。"),
                ("A", "おばあちゃん、今年も元気そうでよかった。おじいちゃんは？",
                 "Grandma looks well this year too, that's good. How about Grandpa?",
                 "奶奶今年也精神挺好的。爷爷呢？"),
                ("B", "おじいさん、さっきまで庭にいたよ。なんか花の手入れしてた。",
                 "Grandpa was in the garden just now. He was tending to the flowers or something.",
                 "爷爷刚才在院子里。好像在打理花。"),
            ]),
            section("子どもたちとお年玉", "Kids and New Year's money", "孩子们和压岁钱", "🧧", [
                ("A", "うわ、赤ん坊！あれ誰の子？",
                 "Whoa, a baby! Whose kid is that?",
                 "哇，有小婴儿！那是谁家的？"),
                ("B", "お兄ちゃんとこの。去年生まれたんだって。男の子。",
                 "My brother's. Born last year, apparently. A boy.",
                 "我哥那边的。说是去年出生的。男孩。"),
                ("A", "へえ、かわいい。あ、あそこで遊んでる女の子は？",
                 "Wow, cute. Oh, who's the girl playing over there?",
                 "哇好可爱。啊，那边在玩的女孩是谁？"),
                ("B", "従姉妹のさくらちゃん。五歳になったらしい。双子の妹もいるんだけど、今日は熱で来れなかったって。",
                 "Cousin Sakura. Apparently she just turned five. She has a twin sister too, but she couldn't come today because of a fever.",
                 "是表妹小樱。好像满五岁了。她还有个双胞胎妹妹，不过今天发烧没来。"),
                ("A", "そっか、残念。あ、お年玉もう配った？",
                 "I see, that's too bad. Oh, have they handed out the New Year's money yet?",
                 "这样啊，可惜。哦对，压岁钱发了吗？"),
                ("B", "まだ。おじさんが「ご飯の後でね」って言ってた。末っ子のたくやが待ちきれなくてうろうろしてるよ。",
                 "Not yet. Uncle said 'after dinner.' The youngest, Takuya, can't wait and is wandering around.",
                 "还没。叔叔说「吃完饭再发」。最小的拓也等不及了在那转来转去。"),
                ("A", "あはは、子どもはみんなそうだよね。…ねえ、僕らもまだもらえるかな？",
                 "Haha, kids are all like that. ...Hey, do you think we still get some?",
                 "哈哈，小孩都那样。……诶，我们还能拿到吗？"),
                ("B", "二十歳超えてるんだから、もう無理でしょ。",
                 "We're over 20, so probably not.",
                 "都过了二十岁了，不可能了吧。"),
            ]),
        ],
    },

    # ===== 3. 夫妻聊孩子成长 (dialogue, N4-N3, 口語化) =====
    {
        "id": "n4-couple-talk-child-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "子どもの成長を話す夫婦",
        "titleJp": "子どもの成長を話す夫婦",
        "titleEn": "A couple talking about their child's growth",
        "titleZh": "夫妻聊孩子的成长",
        "titleRuby": [],
        "sections": [
            section("寝る前の会話", "Bedtime conversation", "睡前对话", "🌙", [
                ("A", "ねえ、今日たけし、初めて一人でトイレに行けたんだよ。",
                 "Hey, today Takeshi went to the toilet by himself for the first time.",
                 "诶，小刚今天第一次自己去厕所了。"),
                ("B", "えっ、ほんとに？すごいじゃん。もう三歳だもんね。",
                 "Eh, really? That's amazing. He is three already after all.",
                 "诶，真的假的？好厉害啊。毕竟已经三岁了嘛。"),
                ("A", "うん。でもね、帰りに迷子になりかけて焦った。",
                 "Yeah. But on the way back he almost got lost and I panicked.",
                 "嗯。不过回来的时候差点走丢，我急死了。"),
                ("B", "あー、お子さん連れだと目が離せないよね。",
                 "Ah, when you have a kid with you, you can't take your eyes off them.",
                 "啊——带孩子真是一刻都不能松懈。"),
                ("A", "保育園の保護者会で聞いたんだけど、三歳くらいが一番手がかかるんだって。",
                 "I heard at the nursery parents' meeting that around age three is the most demanding.",
                 "在保育园家长会上听说，三岁左右是最累人的时候。"),
                ("B", "まあ、大変だけど、かわいい時期でもあるよね。",
                 "Well, it's tough, but it's also the cutest stage.",
                 "嗯，虽然辛苦，但也是最可爱的时候嘛。"),
            ]),
            section("これからのこと", "About the future", "关于将来", "👶", [
                ("A", "ねえ、二人目どうする？家内の母に「そろそろ」って言われてるんだけど。",
                 "Hey, what do you think about a second child? My wife's mother keeps saying 'it's about time.'",
                 "诶，要不要第二个？我妈一直说「差不多了吧」。"),
                ("B", "んー、産むのは私なんだけどね。…まあ、息子に弟か妹がいたら楽しいかなとは思う。",
                 "Hmm, I'm the one giving birth though. ...Well, I do think it'd be fun if our son had a sibling.",
                 "嗯——生的人是我啊。……不过，觉得儿子有个弟弟妹妹的话会更热闹。"),
                ("A", "男の子がいいな。いや、女の子もかわいいか。",
                 "I'd like a boy. No wait, a girl would be cute too.",
                 "想要个男孩。不，女孩也可爱。"),
                ("B", "どっちでもいいよ。元気に生まれてくれたら。",
                 "Either is fine. As long as the baby is born healthy.",
                 "哪个都好啦。只要健健康康就行。"),
                ("A", "そうだね。……あ、ご主人って呼ばれるの、まだ慣れないな。",
                 "Right. ...Oh, I'm still not used to being called 'your husband.'",
                 "说得也是。……啊，被叫「您先生」，我还是不太习惯。"),
                ("B", "あはは、夫婦になってもう四年なのに。",
                 "Haha, and it's been four years since we became a couple.",
                 "哈哈哈，都结婚四年了还不习惯。"),
            ]),
        ],
    },

    # ===== 4. 在爷爷家过暑假 (essay, N5-N3) =====
    {
        "id": "n4-summer-at-grandpas-essay",
        "level": "N5–N3",
        "format": "essay",
        "titleWord": "おじいちゃんの家での夏休み",
        "titleJp": "おじいちゃんの家での夏休み",
        "titleEn": "Summer vacation at Grandpa's house",
        "titleZh": "在爷爷家过暑假",
        "titleRuby": [],
        "segments": [
            ("子どもの頃、毎年夏休みになると祖父の家に行った。",
             "When I was a child, every summer vacation I would go to my grandfather's house.",
             "小时候每年暑假都去爷爷家。"),
            ("祖母はいつも門の前で待っていてくれた。「大きくなったね」と言いながら頭を撫でてくれる。",
             "My grandmother would always be waiting in front of the gate. She'd pat my head saying 'You've gotten bigger.'",
             "奶奶总是在门口等我。一边说「长高了呢」一边摸摸我的头。"),
            ("お兄さんとお姉さんも一緒に来ることが多かった。弟と妹はまだ小さかったので、母親と家にいた。",
             "My older brother and sister often came together. My younger brother and sister were still small, so they stayed home with Mother.",
             "哥哥姐姐也常一起来。弟弟妹妹还小，和妈妈留在家里。"),
            ("祖父は毎朝早く起きて、畑で野菜を作っていた。わたしも手伝った。",
             "Grandfather woke up early every morning and grew vegetables in the field. I helped too.",
             "爷爷每天一大早起来在田里种菜。我也帮忙了。"),
            ("昼は川で泳いだ。年寄りの近所の人が「気をつけてな」と声をかけてくれた。",
             "At noon we swam in the river. An elderly neighbor called out 'Be careful!'",
             "中午在河里游泳。上了年纪的邻居叮嘱说「小心点啊」。"),
            ("夜は花火をした。孫が来ると祖父はいつもうれしそうだった。",
             "At night we set off fireworks. Grandfather always looked happy when his grandchildren came.",
             "晚上放烟花。孙子来的时候爷爷总是很高兴的样子。"),
            ("押入れの中から古い人形やおもちゃを見つけた。お母さんが子どもの頃に遊んでいたものだという。",
             "I found old dolls and toys in the closet. They said Mom used to play with them as a child.",
             "从壁橱里翻出了旧人偶和玩具。说是妈妈小时候玩的。"),
            ("お盆には親戚が集まって、先祖のお墓参りに行った。子孫が元気でいることを報告した。",
             "At Obon, relatives gathered and we visited our ancestors' graves. We reported that the descendants are doing well.",
             "盂兰盆节亲戚们聚在一起去扫墓。告诉先祖子孙们都很好。"),
            ("あの頃の夏は、毎日が長くて、毎日が楽しかった。今でも時々、あの田舎の匂いを思い出す。",
             "The summers back then — every day was long and every day was fun. Even now I sometimes recall the smell of that countryside.",
             "那时候的夏天，每一天都很长，每一天都很快乐。直到现在偶尔还会想起那乡下的味道。"),
        ],
    },

    # ===== 5. 和朋友吵架后和好 (essay, N3-N2) =====
    {
        "id": "n3-fight-and-makeup-essay",
        "level": "N3–N2",
        "format": "essay",
        "titleWord": "親友と喧嘩した日",
        "titleJp": "親友と喧嘩した日",
        "titleEn": "The day I fought with my best friend",
        "titleZh": "和好朋友吵架的那天",
        "titleRuby": [],
        "segments": [
            ("大学の親友と初めて喧嘩した。原因は些細なことだった。",
             "I had my first fight with my best friend from college. The cause was trivial.",
             "和大学最好的朋友第一次吵架。起因是件小事。"),
            ("グループの飲み会で、わたしのことを他人の前で冗談にした。みんなは笑ったけど、わたしは笑えなかった。",
             "At a group drinking party, he made a joke about me in front of others. Everyone laughed, but I couldn't.",
             "在聚会上，他当着别人的面拿我开玩笑。大家都笑了，我笑不出来。"),
            ("帰り道、「あれはひどくない？」と聞いたら、「冗談じゃん」と返された。",
             "On the way home, I asked 'Wasn't that harsh?' and he replied 'It was just a joke.'",
             "回去的路上问他「那不过分吗？」，他回了一句「开玩笑而已嘛」。"),
            ("悪口ではないと言うけど、言われた側はそう思えなかった。",
             "He said it wasn't badmouthing, but the one on the receiving end didn't feel that way.",
             "他说不是说坏话，但被说的人没法那么想。"),
            ("それから一週間、連絡しなかった。仲間が心配して「どうしたの？」とメッセージをくれた。",
             "After that, we didn't contact each other for a week. Our friends were worried and messaged me asking what happened.",
             "之后一周没联系。伙伴们担心地发消息问「怎么了？」。"),
            ("友情って、近すぎると傷つけ合うことがある。でも、他人に戻りたくはなかった。",
             "Friendship — when you're too close, you can hurt each other. But I didn't want us to become strangers.",
             "友情这东西，太近了有时会互相伤害。但我不想变回陌生人。"),
            ("結局、向こうから「悪かった」とメッセージが来た。わたしも「こっちも言い方がきつかった」と返した。",
             "In the end, he sent me a message saying 'I'm sorry.' I replied 'My way of saying it was harsh too.'",
             "最终对方发来「是我不好」。我也回了「我说话也太冲了」。"),
            ("週末、二人でカフェに行って、ゆっくり話した。仲直りした。",
             "On the weekend, we went to a café together and talked at length. We made up.",
             "周末两个人去了咖啡馆，慢慢聊了一下。和好了。"),
            ("失恋の話も、仕事の悩みも、一番に話すのはやっぱりあいつだ。恋よりも長く続く友好がある。",
             "Whether it's heartbreak or work troubles, the first person I talk to is still him. There are friendships that last longer than love.",
             "不管是失恋还是工作烦恼，第一个倾诉的还是他。有些友谊比恋爱更长久。"),
        ],
    },

    # ===== 6. 把男/女朋友介绍给父母 (dialogue, N4-N3, 口語化) =====
    {
        "id": "n4-meet-parents-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "恋人を親に紹介する日（カップル）",
        "titleJp": "恋人を親に紹介する日（カップル）",
        "titleEn": "The day of introducing your partner to your parents (couple)",
        "titleZh": "把恋人介绍给父母（情侣对话）",
        "titleRuby": [],
        "sections": [
            section("家に着く前", "Before arriving", "到家之前", "💑", [
                ("A", "ねえ、緊張してる？",
                 "Hey, are you nervous?",
                 "诶，你紧张吗？"),
                ("B", "めちゃくちゃ緊張してる。お父さん怖くない？",
                 "I'm super nervous. Is your dad scary?",
                 "紧张死了。你爸凶不凶？"),
                ("A", "大丈夫、優しい人だよ。ただ、最初はちょっと無口かも。",
                 "It's fine, he's a kind person. Just, he might be a bit quiet at first.",
                 "没事的，人很好。不过一开始可能话不多。"),
                ("B", "お母さんは？",
                 "And your mom?",
                 "妈妈呢？"),
                ("A", "お母さんはすぐ話しかけてくるから心配しないで。……あ、「おばさん」じゃなくて「お母さん」って呼んでね。喜ぶから。",
                 "Mom will start talking to you right away so don't worry. ...Oh, call her 'Mom' not 'Auntie.' She'll be happy.",
                 "妈妈会马上跟你搭话的别担心。……对了，别叫「阿姨」叫「妈妈」哦。她会高兴的。"),
                ("B", "えっ、いきなり？まだ結婚もしてないのに。",
                 "Eh, just like that? We're not even married yet.",
                 "诶，这就叫了？还没结婚呢。"),
                ("A", "うちはそういう家なの。気楽にね。",
                 "That's just how my family is. Relax.",
                 "我家就是这样的。放轻松。"),
            ]),
            section("食事の席で", "At the dinner table", "吃饭的时候", "🍽️", [
                ("B", "あの、初めまして。リンと申します。いつもお世話になっております。",
                 "Um, nice to meet you. My name is Rin. Thank you for always taking care of...",
                 "那个，初次见面。我叫琳。一直承蒙……"),
                ("A", "あはは、硬すぎ。彼女、ちょっと緊張してて。",
                 "Haha, too formal. She's a bit nervous.",
                 "哈哈哈，太正式了。她有点紧张。"),
                ("B", "……うん、すみません。えーと、お料理、すごくおいしいです。",
                 "...Yeah, sorry. Um, the food is really delicious.",
                 "……嗯，不好意思。嗯，菜非常好吃。"),
                ("A", "お母さんの得意料理なんだよ。ね、お父さんも何か言ってよ。",
                 "It's Mom's specialty. Come on Dad, say something too.",
                 "这是妈妈的拿手菜。爸你也说句话呗。"),
                ("B", "あ、両親に挨拶……ちゃんとできてるかな。夫人って呼ぶべき？奥さん？",
                 "Oh, the greeting to the parents... am I doing it right? Should I say 'ma'am'? 'Mrs.'?",
                 "啊，跟父母打招呼……我做对了吗？该叫夫人？还是太太？"),
                ("A", "いいよいいよ、そんな堅い言葉使わなくて。普通でいいから。",
                 "It's fine, you don't need to use such formal words. Just be natural.",
                 "没事没事，别用那么生硬的词。自然就好。"),
                ("B", "はあ……帰ったら絶対倒れる。",
                 "Sigh... I'm definitely going to collapse when we get home.",
                 "唉……回去了我肯定要瘫倒。"),
                ("A", "でもさ、お母さん、すごくうれしそうだったよ。花嫁候補が来たって思ってるかも。",
                 "But you know, Mom looked really happy. She might be thinking a potential bride has arrived.",
                 "不过你看，妈妈特别高兴。说不定觉得未来儿媳来了。"),
                ("B", "えっ、そこまで！？",
                 "Eh, that far!?",
                 "诶，想那么远了！？"),
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
