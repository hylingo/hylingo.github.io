#!/usr/bin/env python3
"""
batch17 → public/data/ja_articles.json

补全缺 essay 的 7 个主题:
N4–N3: asking-directions, clinic-friend, couple-talk-child, meet-parents
N5–N3: new-year-relatives
N3–N2: office-senpai
N2:    appliance-repair

运行: python3 scripts/append_ja_articles_batch17.py
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


NEW_ITEMS: list[dict] = [

    # ═══════════════════════════════════════════
    # 1. n4-asking-directions 问路
    # ═══════════════════════════════════════════
    {
        "id": "n4-asking-directions-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "道に迷った午後",
        "titleJp": "道に迷った午後",
        "titleEn": "An afternoon of being lost",
        "titleZh": "迷路的下午",
        "titleRuby": [],
        "segments": [
            seg("郵便局に行きたかったのに、道に迷ってしまった。スマホの地図を見ても、自分がどこにいるか分からない。",
                "I wanted to go to the post office but got lost. Even looking at the map on my phone, I couldn't tell where I was.",
                "明明想去邮局，却迷路了。看手机地图也搞不清自己在哪。", True),
            seg("交差点に立って周りを見た。コンビニと花屋と、知らないビルがあるだけだった。",
                "I stood at an intersection and looked around. There was just a convenience store, a flower shop, and unfamiliar buildings.",
                "站在十字路口环顾四周。只有便利店、花店和不认识的大楼。"),
            seg("仕方なく、通りかかった人に声をかけた。「すみません、この辺に郵便局はありますか」。",
                "With no choice, I called out to a passerby. 'Excuse me, is there a post office around here?'",
                "没办法，叫住了路过的人。「不好意思，这附近有邮局吗」。"),
            seg("その人は少し考えてから、「この道をまっすぐ行って、二つ目の信号を右に曲がってください」と教えてくれた。",
                "After thinking for a moment, they told me, 'Go straight down this road and turn right at the second light.'",
                "那个人想了一下，告诉我「沿这条路直走，第二个红绿灯右转」。", True),
            seg("「橋は渡らないでください。橋の手前で右です」とも言われた。交番の隣にあるらしい。",
                "'Don't cross the bridge. Turn right before it,' they added. Apparently it's next to the police box.",
                "还说了「不要过桥。桥前面右转」。好像在派出所旁边。"),
            seg("お礼を言って歩き出した。信号を一つ過ぎ、二つ目の信号で右に曲がった。",
                "I thanked them and started walking. I passed one light and turned right at the second.",
                "道了谢开始走。过了一个红绿灯，在第二个路口右转了。"),
            seg("すると、小さな橋が見えた。その手前に交番があり、隣に赤い看板の郵便局があった。",
                "Then I could see a small bridge. Before it was the police box, and next to it was the post office with a red sign.",
                "然后看到一座小桥。桥前面有派出所，旁边就是挂着红色招牌的邮局。", True),
            seg("封筒と切手を買って、手紙を出した。用事を済ませてほっとした。",
                "I bought envelopes and stamps and mailed my letter. I felt relieved to get it done.",
                "买了信封和邮票，寄了信。办完事松了口气。"),
            seg("帰り道はもう迷わなかった。一度通った道は覚えるものだ。",
                "I didn't get lost on the way back. Once you've walked a road, you remember it.",
                "回去的路上没再迷路。走过一次的路就记住了。"),
            seg("でも、もし声をかけなかったら、今でもあの交差点に立っていたかもしれない。聞くのは恥ずかしくない。",
                "But if I hadn't asked, I might still be standing at that intersection. There's no shame in asking.",
                "不过要是当时没开口问，说不定现在还站在那个路口。开口问路不丢人。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n4-clinic-friend 给不舒服的朋友打电话
    # ═══════════════════════════════════════════
    {
        "id": "n4-clinic-friend-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "友達のお見舞い",
        "titleJp": "友達のお見舞い",
        "titleEn": "Visiting a sick friend",
        "titleZh": "探望生病的朋友",
        "titleRuby": [],
        "segments": [
            seg("今日、ミキが学校に来なかった。LINEを送っても既読にならない。心配になって電話した。",
                "Today Miki didn't come to school. My LINE messages weren't read. I got worried and called.",
                "今天美希没来学校。发LINE也不显示已读。担心起来就打了电话。", True),
            seg("電話に出たミキの声はいつもより低かった。「朝から頭が痛くて、鼻水も止まらない」と言う。",
                "Miki's voice on the phone was lower than usual. 'My head has been hurting since morning and my nose won't stop running,' she said.",
                "接电话的美希声音比平时低。说「从早上开始头疼，鼻涕也止不住」。"),
            seg("「熱は？」と聞いたら、三十八度あったので午前中に病院に行ったそうだ。風邪と言われて薬をもらったらしい。",
                "'Do you have a fever?' I asked. She had 38 degrees, so she went to the hospital in the morning. They said it was a cold and gave her medicine.",
                "问「发烧了吗」，说三十八度，上午去了医院。说是感冒，开了药。"),
            seg("「ご飯は食べた？」と聞くと、食欲がなくて何も食べていないと言う。それは心配だ。",
                "'Did you eat?' I asked. She said she had no appetite and hadn't eaten anything. That worried me.",
                "问「吃饭了吗」，说没胃口什么都没吃。这让人担心。", True),
            seg("「何か買ってこうか？」と言ったら、「みかんとゼリーがあると嬉しい」と小さな声で答えた。",
                "'Want me to bring something?' I said. 'Tangerines and jelly would be nice,' she answered in a small voice.",
                "说了句「要不我给你带点什么」，她小声回答「有橘子和果冻就好」。"),
            seg("コンビニでみかんとゼリーとポカリを買った。柔らかいティッシュも買った。鼻のかみすぎで痛いだろうから。",
                "I bought tangerines, jelly, and Pocari at the convenience store. I also got soft tissues, since her nose must hurt from blowing it so much.",
                "在便利店买了橘子、果冻和宝矿力。还买了柔软纸巾。擤鼻涕擤多了肯定疼。"),
            seg("ミキの部屋に着くと、パジャマ姿で布団に包まっていた。顔が赤くて、目が腫れている。",
                "When I arrived at Miki's room, she was wrapped in a futon in pajamas. Her face was red and her eyes were swollen.",
                "到了美希房间，她穿着睡衣裹在被子里。脸红红的，眼睛也肿了。", True),
            seg("「来てくれてありがとう。一人だと心細かったから」とミキが言った。",
                "'Thank you for coming. I was feeling lonely being alone,' Miki said.",
                "美希说「谢谢你来。一个人的时候好没安全感」。"),
            seg("みかんの皮をむいて渡した。ミキは少し食べて、「おいしい」と笑った。",
                "I peeled a tangerine and handed it to her. Miki ate a little and smiled, saying 'delicious.'",
                "剥了橘子皮递给她。美希吃了一点，笑着说「好吃」。"),
            seg("帰り道、「友達がいてよかった」とLINEが来た。こっちこそ、と思った。",
                "On my way home, I got a LINE message: 'I'm glad I have a friend like you.' I thought: me too.",
                "回去的路上收到LINE「有朋友真好」。我想，我也是。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-couple-talk-child 夫妻聊孩子
    # ═══════════════════════════════════════════
    {
        "id": "n4-couple-talk-child-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "子どもの成長を見守る日々",
        "titleJp": "子どもの成長を見守る日々",
        "titleEn": "Days of watching our child grow",
        "titleZh": "陪伴孩子成长的日子",
        "titleRuby": [],
        "segments": [
            seg("息子のたけしが三歳になった。最近、いろんなことができるようになってきた。",
                "Our son Takeshi turned three. Lately he's been learning to do all sorts of things.",
                "儿子小刚满三岁了。最近学会了各种各样的事。", True),
            seg("今日、初めて一人でトイレに行けた。妻が興奮して教えてくれた。「すごいでしょ？」と目を輝かせていた。",
                "Today he went to the toilet by himself for the first time. My wife excitedly told me. 'Isn't that amazing?' she said, her eyes sparkling.",
                "今天第一次自己去了厕所。妻子兴奋地告诉我。「厉害吧？」眼睛亮亮的。"),
            seg("でも帰り道に迷子になりかけて、妻はかなり焦ったらしい。目が離せない年頃だ。",
                "But on the way back he almost got lost, and apparently my wife panicked quite a bit. He's at that age where you can't take your eyes off him.",
                "不过回来的路上差点走丢，妻子急坏了。是不能放松警惕的年纪。"),
            seg("保育園の保護者会で、三歳が一番手がかかる時期だと聞いた。確かに、毎日が体力勝負だ。",
                "At the nursery parents' meeting, I heard that age three is the most demanding. Indeed, every day is a physical battle.",
                "在保育园家长会上听说三岁是最累人的时候。确实，每天都是体力活。", True),
            seg("でも、かわいい時期でもある。「パパ、見て！」と何度も呼ばれる。",
                "But it's also the cutest stage. He calls out 'Daddy, look!' over and over.",
                "不过也是最可爱的时候。总是喊「爸爸你看！」。"),
            seg("先日、積み木で高い塔を作って見せてくれた。倒れた瞬間、大笑いしていた。",
                "The other day he built a tall tower with blocks to show me. When it fell, he burst out laughing.",
                "前几天用积木搭了高塔给我看。倒的瞬间笑得不行。"),
            seg("夜、妻と二人目のことを話した。妻の母に「そろそろ」と言われているらしい。",
                "At night, my wife and I talked about having a second child. Apparently her mother has been saying 'it's about time.'",
                "晚上和妻子聊了要不要第二个。听说岳母一直说「差不多了吧」。", True),
            seg("「産むのは私なんだけどね」と妻は笑った。男の子でも女の子でも、元気に生まれてくれたらいい。",
                "'I'm the one giving birth though,' my wife laughed. Boy or girl, as long as the baby is born healthy.",
                "「生的人是我」妻子笑着说。不管男孩女孩，健康就好。"),
            seg("たけしに弟か妹がいたら、きっと楽しいだろう。にぎやかな食卓が目に浮かぶ。",
                "If Takeshi had a little brother or sister, it would surely be fun. I can picture a lively dinner table.",
                "小刚要是有弟弟妹妹，一定很热闹。眼前浮现出欢闹的餐桌。"),
            seg("「ご主人」と呼ばれるのにはまだ慣れないが、この家族を守っていきたいと思う。",
                "I'm still not used to being called 'husband,' but I want to protect this family.",
                "被叫「您先生」还是不习惯，但我想守护这个家。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 4. n4-meet-parents 见父母
    # ═══════════════════════════════════════════
    {
        "id": "n4-meet-parents-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "恋人を親に紹介した日",
        "titleJp": "恋人を親に紹介した日",
        "titleEn": "The day I introduced my partner to my parents",
        "titleZh": "把恋人介绍给父母的那天",
        "titleRuby": [],
        "segments": [
            seg("今日は恋人のリンを実家に連れていく日だ。朝から緊張している。私より、リンの方がもっと緊張しているだろう。",
                "Today is the day I bring my girlfriend Rin to my parents' house. I've been nervous since morning. Rin is probably even more nervous than me.",
                "今天是带恋人琳回老家的日子。从早上就紧张。比起我，琳肯定更紧张。", True),
            seg("家に向かう電車の中で、リンが聞いた。「お父さん、怖くない？」。「優しい人だよ。ただ、最初はちょっと無口かも」と答えた。",
                "On the train to my parents' house, Rin asked, 'Is your dad scary?' 'He's a kind person. Just, he might be a bit quiet at first,' I answered.",
                "去家里的电车上，琳问「你爸凶不凶」。我说「人很好。不过一开始可能话不多」。"),
            seg("母は話好きだから心配していない。「おばさん」ではなく「お母さん」と呼んでね、と伝えた。喜ぶから。",
                "I'm not worried about Mom since she loves to chat. I told Rin to call her 'Mom' instead of 'Auntie.' She'll be happy.",
                "妈妈爱说话所以不担心。让琳别叫「阿姨」叫「妈妈」。她会高兴的。"),
            seg("家に着いた。玄関で靴を脱いで、居間に通された。テーブルの上に母の料理がたくさん並んでいた。",
                "We arrived at the house. We took off our shoes at the entrance and were shown to the living room. Mom's dishes were lined up all over the table.",
                "到了家。在玄关脱了鞋，被领到客厅。桌上摆满了妈妈做的菜。", True),
            seg("リンは「初めまして。リンと申します」と丁寧に挨拶した。声が少し震えていた。",
                "Rin politely greeted them: 'Nice to meet you. My name is Rin.' Her voice trembled a little.",
                "琳礼貌地打了招呼「初次见面。我叫琳」。声音有点发抖。"),
            seg("母はすぐに「まあ、かわいい人ね。どうぞどうぞ」と言った。父は黙って頷いただけだった。",
                "Mom immediately said, 'Oh, what a lovely person. Please, come in.' Dad just nodded silently.",
                "妈妈马上说「哎呀，好漂亮的人啊。快请快请」。爸爸只是沉默地点了点头。"),
            seg("食事が始まると、リンは「おいしいです」と何度も言った。母は嬉しそうに「もっと食べて」と料理を勧めた。",
                "Once the meal started, Rin kept saying 'It's delicious.' Mom happily urged her to eat more.",
                "开始吃饭后，琳不停地说「好好吃」。妈妈高兴地劝她「多吃点」。", True),
            seg("父も少しずつ話し始めた。「どこの大学？」「仕事は何をしているの？」。硬い質問だが、興味がある証拠だ。",
                "Dad gradually started talking too. 'Which university?' 'What do you do for work?' Stiff questions, but proof he's interested.",
                "爸爸也渐渐开口了。「哪个大学的？」「做什么工作？」。虽然问得生硬，但说明感兴趣。"),
            seg("帰り道、リンは「疲れた……でも、お母さん優しかった」と笑った。",
                "On the way home, Rin smiled and said, 'I'm exhausted... but your mom was so kind.'",
                "回去的路上琳笑着说「累死了……不过妈妈好温柔」。"),
            seg("「お父さんも気に入ってたと思うよ」と言ったら、リンは「本当？」と目を丸くした。うまくいったと思う。",
                "'I think Dad liked you too,' I said, and Rin's eyes went wide. 'Really?' I think it went well.",
                "我说「爸爸应该也喜欢你」，琳瞪大了眼睛「真的？」。应该挺成功的。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 5. n4-new-year-relatives 新年亲戚聚会
    # ═══════════════════════════════════════════
    {
        "id": "n4-new-year-relatives-essay",
        "level": "N5–N3",
        "format": "essay",
        "titleWord": "お正月に親戚が集まる",
        "titleJp": "お正月に親戚が集まる",
        "titleEn": "Relatives gathering at New Year's",
        "titleZh": "新年亲戚聚会",
        "titleRuby": [],
        "segments": [
            seg("お正月になると、祖父母の家に親戚が集まる。今年も従兄弟のゆうきが来ていた。",
                "At New Year's, relatives gather at our grandparents' house. This year my cousin Yuuki was there too.",
                "过年的时候亲戚们会聚在爷爷奶奶家。今年堂兄悠希也来了。", True),
            seg("ゆうきとは一年ぶりだ。「久しぶり！いつ来たの？」と聞いたら、一昨日の夜に車で来たらしい。渋滞がひどかったそうだ。",
                "I hadn't seen Yuuki in a year. 'Long time no see! When did you arrive?' I asked. He came by car the night before last. The traffic was terrible, he said.",
                "和悠希一年没见了。问「好久不见！什么时候来的」，说前天晚上开车来的。堵车堵得很厉害。"),
            seg("おばあちゃんは元気そうだった。おじいちゃんは庭で花の手入れをしていた。毎年変わらない光景だ。",
                "Grandma looked well. Grandpa was tending flowers in the garden. The same scene every year.",
                "奶奶看起来精神不错。爷爷在院子里打理花。每年都一样的景象。"),
            seg("台所ではおばさんがおせち料理を作っていた。黒豆と数の子と伊達巻。甘い匂いがする。",
                "In the kitchen, Auntie was making osechi. Black beans, herring roe, and datemaki. It smelled sweet.",
                "厨房里阿姨在做御节料理。黑豆、鲱鱼子和伊达卷。甜甜的味道。", True),
            seg("お兄ちゃんの赤ちゃんがいた。去年生まれた男の子だ。みんなで「かわいい」と騒いだ。",
                "My older brother's baby was there. A boy born last year. Everyone fussed over how cute he was.",
                "哥哥家的小宝宝也在。去年出生的男孩。大家围着说「好可爱」。"),
            seg("従姉妹のさくらちゃんは五歳になったらしい。双子の妹は熱で来られなかった。残念だ。",
                "Cousin Sakura apparently turned five. Her twin sister couldn't come because of a fever. Too bad.",
                "表妹小樱好像满五岁了。双胞胎妹妹发烧没来。真可惜。"),
            seg("子どもたちはお年玉を楽しみにしている。末っ子のたくやが待ちきれずにうろうろしていた。",
                "The kids were looking forward to their New Year's money. The youngest, Takuya, was wandering around impatiently.",
                "孩子们都盼着压岁钱。最小的拓也等不及了转来转去。", True),
            seg("おじさんが「ご飯の後でね」と言ったが、子どもたちには長い待ち時間だろう。",
                "Uncle said 'After dinner,' but for the kids it must feel like a long wait.",
                "叔叔说「吃完饭再发」，但对孩子们来说一定等得很漫长。"),
            seg("ゆうきと「僕らもまだもらえるかな」と冗談を言った。「二十歳超えてるから無理でしょ」と笑われた。",
                "Yuuki and I joked, 'Think we can still get some?' 'We're over twenty, so probably not,' he laughed.",
                "和悠希开玩笑说「我们还能拿到吗」。被笑着说「都过了二十岁了，不可能」。"),
            seg("お正月はみんなが集まれる貴重な日だ。来年もこうして会えたらいいと思った。",
                "New Year's is a precious day when everyone can gather. I hope we can meet like this again next year.",
                "新年是大家能聚在一起的珍贵日子。希望明年也能这样见面。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 6. n3-office-senpai 向前辈请教
    # ═══════════════════════════════════════════
    {
        "id": "n3-office-senpai-essay",
        "level": "N3–N2",
        "format": "essay",
        "titleWord": "先輩に助けられた話",
        "titleJp": "先輩に助けられた話",
        "titleEn": "The story of being helped by a senior",
        "titleZh": "被前辈帮助的故事",
        "titleRuby": [],
        "segments": [
            seg("入社して半年、初めてお客さんに提案をすることになった。資料を作り、リハーサルもした。準備は万全のつもりだった。",
                "Six months after joining the company, I was to make my first proposal to a client. I prepared materials and rehearsed. I thought I was fully prepared.",
                "入职半年，第一次要向客户提方案。做了资料，也排练了。自以为准备万全。", True),
            seg("しかし、結果は散々だった。お客さんの反応は薄く、質問にもうまく答えられなかった。",
                "But the result was terrible. The client's response was lukewarm, and I couldn't answer their questions well.",
                "然而结果惨不忍睹。客户反应冷淡，提问也答不好。"),
            seg("帰り道、課長に「もう少し工夫しろ」と言われた。工夫って何だろう。どうすればいいか分からなかった。",
                "On the way back, my section chief told me to 'put more thought into it.' What does that even mean? I didn't know what to do.",
                "回去的路上课长说「再下点功夫」。下什么功夫呢？完全不知道该怎么办。"),
            seg("自分の席で落ち込んでいると、先輩の木村さんが声をかけてくれた。「ちょっといいか？」。",
                "While I was sulking at my desk, my senior Kimura-san called out to me. 'Got a minute?'",
                "在座位上垂头丧气的时候，前辈木村先生叫了我。「方便吗？」。", True),
            seg("「最初はそんなもんだよ」と先輩は言った。自分も新人のとき、部長にひどく怒られたそうだ。",
                "'That's how it is at first,' senpai said. He told me he was chewed out badly by the department head when he was new too.",
                "「一开始都那样」前辈说。他新人时期也被部长狠狠骂过。"),
            seg("「工夫っていうのは、相手の立場で考えることだよ。お客さんが何に困ってるかを、もっと聞くんだ」。",
                "'Putting thought into it means thinking from the other person's perspective. Listen more to what the client is struggling with.'",
                "「所谓下功夫，就是站在对方立场想。多听客户到底在烦什么」。"),
            seg("なるほどと思った。自分は言いたいことを並べただけで、相手が何を求めているか考えていなかった。",
                "That made sense. I had just listed what I wanted to say, without thinking about what the other person needed.",
                "恍然大悟。我只是把自己想说的罗列出来，没有考虑对方需要什么。", True),
            seg("「同期と比べるな。人によって伸びるタイミングは違う。三年後に笑ってればいいんだ」と先輩は続けた。",
                "'Don't compare yourself to your cohort. Everyone grows at different times. If you're laughing three years from now, that's what matters,' senpai continued.",
                "「别跟同期比。每个人成长的节奏不一样。三年后笑着就好了」前辈继续说。"),
            seg("その言葉で気持ちが楽になった。完璧でなくていい。一歩ずつ進めばいい。",
                "Those words eased my mind. I don't need to be perfect. I just need to take it one step at a time.",
                "这句话让心情轻松了。不需要完美。一步一步来就好。"),
            seg("「よし、飯行こう。俺がおごる」と先輩は笑った。その日のラーメンは、いつもより温かく感じた。",
                "'Alright, let's go eat. My treat,' senpai smiled. The ramen that day felt warmer than usual.",
                "「走，吃饭。我请」前辈笑着说。那天的拉面感觉比平时更暖和。", True),
        ],
    },

    # ═══════════════════════════════════════════
    # 7. n2-appliance-repair 洗衣机坏了
    # ═══════════════════════════════════════════
    {
        "id": "n2-appliance-repair-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "家電が一気に壊れる法則",
        "titleJp": "家電が一気に壊れる法則",
        "titleEn": "The law of appliances breaking all at once",
        "titleZh": "家电一起坏的定律",
        "titleRuby": [],
        "segments": [
            seg("洗濯機から変な音がする。ガタガタと振動して、蛇口のあたりから水が漏れている。",
                "The washing machine is making a strange noise. It vibrates with a rattling sound, and water is leaking from around the faucet.",
                "洗衣机发出怪声。咔哒咔哒地震动，水龙头附近在漏水。", True),
            seg("妻に「昨日からだよ」と言われた。なぜもっと早く言わないのか。とりあえずコンセントを抜いた。",
                "My wife said 'Since yesterday.' Why didn't she tell me sooner? I unplugged it for now.",
                "妻子说「从昨天就开始了」。怎么不早说。先把插头拔了。"),
            seg("もう七年使っている。修理か買い替えか、悩むところだ。",
                "We've been using it for seven years. Whether to repair or replace it — that's the question.",
                "已经用了七年。修还是换，让人纠结。"),
            seg("ネットで調べたら、洗濯機の寿命は七年から十年らしい。ちょうどそのころだ。",
                "I looked it up online: the lifespan of a washing machine is apparently 7 to 10 years. Right on schedule.",
                "网上查了一下，洗衣机寿命大概七到十年。刚好到时候了。", True),
            seg("修理の見積もりを取ったら三万円。新品は八万円から。修理しても他の部品がまた壊れるかもしれない。",
                "I got a repair estimate: 30,000 yen. A new one starts at 80,000. Even after repair, other parts might break again.",
                "问了修理报价三万日元。新的八万起。修了别的零件可能又坏。"),
            seg("「家電って一気に壊れるよね」と妻が言う。確かに、先週は蛍光灯が切れた。掃除機の吸引力も弱くなっている。",
                "'Appliances all break at once, don't they,' my wife said. Indeed, the fluorescent light died last week. The vacuum's suction is getting weaker too.",
                "妻子说「家电就是一起坏的」。确实，上周荧光灯坏了。吸尘器吸力也变弱了。"),
            seg("とりあえず洗濯物はクリーニング屋に持っていくことにした。出費が痛い。",
                "For now we decided to take the laundry to the dry cleaner. The expense hurts.",
                "暂时先把衣服送干洗店。花销心疼。", True),
            seg("休みの日に家電量販店に行った。最新の洗濯機は乾燥機能付きで十五万円。目が飛び出そうだ。",
                "On my day off I went to the electronics store. The latest washing machines with dryer function cost 150,000 yen. My eyes nearly popped out.",
                "休息日去了电器店。最新的带烘干功能的洗衣机十五万日元。眼珠子差点掉出来。"),
            seg("結局、型落ちモデルを九万円で買った。機能は十分だし、配送と設置もしてくれる。",
                "In the end, I bought a previous model for 90,000 yen. The features are sufficient, and they deliver and install it.",
                "最终买了上一代型号九万日元。功能够用，还送货上门安装。"),
            seg("新しい洗濯機が来た日、回した一回目の洗濯はとても静かだった。やっぱり買い替えてよかった。",
                "The day the new washing machine arrived, the first load was incredibly quiet. Replacing it was definitely the right call.",
                "新洗衣机到的那天，转的第一桶衣服特别安静。果然该换的。", True),
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
