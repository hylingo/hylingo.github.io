#!/usr/bin/env python3
"""
N2语法覆盖文章 → public/data/ja_articles.json
共18篇文章覆盖N2核心语法点约180个

运行: python3 scripts/append_ja_articles_n2_grammar.py
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
    # 1. essay - 旅行が教えてくれたこと
    # 語法: ～にとって、～として、～に関して、～をもとに、～にわたって、～を通じて、～をきっかけに、～次第、～たびに、～際に、～うちに
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-travel-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "旅行が教えてくれたこと",
        "titleJp": "旅行が教えてくれたこと",
        "titleEn": "What travel taught me",
        "titleZh": "旅行教会我的事",
        "titleRuby": [],
        "segments": [
            seg("私にとって、旅行は単なる娯楽ではなく、人生の教科書のようなものだ。",
                "For me, travel is not just entertainment but something like a textbook of life.",
                "对我来说，旅行不仅仅是娱乐，而是像人生的教科书一样的存在。",
                True),
            seg("学生として初めて一人旅をしたのは、二十歳の夏だった。異文化に関して何も知らなかった私は、現地の人々を通じて多くのことを学んだ。",
                "My first solo trip as a student was in the summer when I was twenty. Knowing nothing about different cultures, I learned many things through the local people.",
                "作为学生第一次独自旅行是在二十岁的夏天。对异国文化一无所知的我，通过当地人学到了很多东西。"),
            seg("その旅をきっかけに、私は毎年必ず海外へ行くようになった。旅行のたびに新しい発見があり、三週間にわたって南米を回ったこともある。",
                "That trip led me to start going abroad every year without fail. Each trip brought new discoveries, and I even spent three weeks traveling around South America.",
                "以那次旅行为契机，我每年都一定会去国外。每次旅行都有新发现，我还曾花三周时间环游南美。"),
            seg("旅先での体験をもとに、ブログを書き始めた。出発の際には必ず現地の歴史を調べるようにしている。",
                "Based on my travel experiences, I started writing a blog. When departing, I always make sure to research the local history.",
                "以旅途中的经历为基础，我开始写博客。出发之际，我总会提前调查当地的历史。"),
            seg("準備次第で旅の楽しさは大きく変わる。知らないうちに、旅行は私の生き方そのものを変えていた。",
                "The enjoyment of a trip changes greatly depending on the preparation. Before I knew it, travel had changed my very way of living.",
                "旅行的乐趣会因准备工作的不同而大不相同。不知不觉间，旅行已经改变了我的生活方式本身。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. dialogue - 旅行計画を立てる
    # 語法: ～に対して、～について、～に沿って
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-travel-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "旅行計画を立てる",
        "titleJp": "旅行計画を立てる",
        "titleEn": "Making travel plans",
        "titleZh": "制定旅行计划",
        "titleRuby": [],
        "sections": [
            section("行き先を決める", "Deciding the destination", "决定目的地", "🗺️", [
                line("A", "夏休みの旅行について、そろそろ決めない？",
                     "Shouldn't we decide about the summer vacation trip soon?",
                     "暑假旅行的事，差不多该决定了吧？"),
                line("B", "うん、私は自然が多いところがいいな。都会に対して田舎のほうが落ち着くし。",
                     "Yeah, I'd like a place with lots of nature. The countryside is more relaxing compared to the city.",
                     "嗯，我想去自然多的地方。相比城市，乡下更让人放松。"),
                line("A", "じゃあ、海沿いの町はどう？海岸線に沿ってドライブするのも楽しそうだよ。",
                     "Then how about a seaside town? It'd be fun to drive along the coastline.",
                     "那海边的小镇怎么样？沿着海岸线兜风也很有趣吧。"),
            ]),
            section("日程を組む", "Setting the schedule", "安排日程", "📅", [
                line("B", "何泊にする？私は三泊四日がちょうどいいと思うけど。",
                     "How many nights? I think three nights and four days would be just right.",
                     "住几晚？我觉得三晚四天刚刚好。"),
                line("A", "賛成。初日は移動日にして、二日目から観光に集中しよう。",
                     "Agreed. Let's make the first day a travel day and focus on sightseeing from the second day.",
                     "赞成。第一天当移动日，从第二天开始集中观光。"),
                line("B", "ガイドブックに沿って回るのもいいけど、自由時間も入れたいね。",
                     "It's fine to follow the guidebook, but I'd like to include some free time too.",
                     "按导游书来玩也行，但也想留点自由时间。"),
            ]),
            section("予算を決める", "Setting the budget", "确定预算", "💰", [
                line("A", "予算についてなんだけど、一人五万円くらいでどうかな。",
                     "About the budget, how about around fifty thousand yen per person?",
                     "关于预算，一个人大概五万日元怎么样？"),
                line("B", "それくらいなら大丈夫。宿泊費に対して食事代は抑えめにしよう。",
                     "That should be fine. Let's keep the food costs low relative to the accommodation costs.",
                     "那个程度没问题。相对于住宿费，餐费就省着点吧。"),
                line("A", "了解。じゃあ、今週中に宿を予約するね。",
                     "Got it. Then I'll book the hotel within this week.",
                     "了解。那这周内我来预订住宿。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. essay - 転職を考える理由
    # 語法: ～上で、～において、～にかけて、～を中心に、～に基づいて、～にしたがって、～につれて
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-work-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "転職を考える理由",
        "titleJp": "転職を考える理由",
        "titleEn": "Reasons for considering a career change",
        "titleZh": "考虑换工作的理由",
        "titleRuby": [],
        "segments": [
            seg("仕事を選ぶ上で、給料だけでなくやりがいも大切だと思う。",
                "When choosing a job, I think not only salary but also fulfillment is important.",
                "在选择工作的时候，我认为不仅是薪水，成就感也很重要。",
                True),
            seg("現在の職場において、私は営業部を中心に五年間働いてきた。しかし、年齢を重ねるにつれて、自分の本当にやりたいことが見えてきた。",
                "At my current workplace, I've worked for five years mainly in the sales department. However, as I've gotten older, I've started to see what I truly want to do.",
                "在目前的职场，我以营业部为中心工作了五年。但是，随着年龄增长，我逐渐看清了自己真正想做的事。"),
            seg("特に去年の秋から冬にかけて、将来のキャリアについて真剣に考えた。自分の経験に基づいて判断すると、IT業界のほうが向いていると感じた。",
                "Especially from fall to winter last year, I seriously thought about my future career. Judging based on my own experience, I felt the IT industry suited me better.",
                "尤其是去年秋天到冬天期间，我认真思考了未来的职业。基于自己的经验判断，我觉得IT行业更适合我。"),
            seg("上司の指示にしたがって動くだけの仕事では、成長に限界がある。転職活動は不安も多いが、新しい一歩を踏み出す価値はあるはずだ。",
                "In a job where I just follow my boss's instructions, there are limits to growth. Job hunting comes with a lot of anxiety, but it should be worth taking a new step.",
                "只是按照上司的指示行动的工作，成长是有限的。换工作虽然有很多不安，但迈出新一步应该是有价值的。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 4. dialogue - 新入社員の相談
    # 語法: ～に伴って、～とともに、～一方で、～反面、～に比べて、～割に、～わりには
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-work-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "新入社員の相談",
        "titleJp": "新入社員の相談",
        "titleEn": "A new employee's consultation",
        "titleZh": "新员工的咨询",
        "titleRuby": [],
        "sections": [
            section("悩みを打ち明ける", "Sharing concerns", "倾诉烦恼", "😟", [
                line("A", "先輩、ちょっと相談してもいいですか。仕事が増えるに伴って、残業も多くなってきて。",
                     "Senpai, may I consult you about something? As work has increased, overtime has also gotten more frequent.",
                     "前辈，能跟您商量点事吗？随着工作增加，加班也变多了。"),
                line("B", "分かるよ。経験とともに任される仕事も増えるからね。でも、慣れる一方で、新しいプレッシャーも出てくるものだよ。",
                     "I understand. As you gain experience, you get entrusted with more work. But while you get used to it, new pressures also come up.",
                     "我理解。随着经验增长，被委托的工作也会增多。不过在习惯的同时，新的压力也会出现的。"),
            ]),
            section("アドバイス", "Advice", "建议", "💡", [
                line("A", "この会社はやりがいがある反面、ワークライフバランスが難しいですよね。",
                     "This company is rewarding, but on the flip side, work-life balance is difficult, isn't it?",
                     "这家公司虽然有成就感，但另一方面工作生活平衡很难呢。"),
                line("B", "前の部署に比べて今のほうが忙しいけど、給料の割にはいい経験ができてると思うよ。",
                     "It's busier now compared to the previous department, but I think you're getting good experience relative to the salary.",
                     "虽然和之前的部门比现在更忙，但我觉得相对于薪水来说，你获得了很好的经验。"),
                line("A", "そう考えると、もう少し頑張れそうです。ありがとうございます。",
                     "Thinking about it that way, I feel I can keep going a bit longer. Thank you.",
                     "这样想的话，我觉得还能再加油一下。谢谢您。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 5. essay - 大人になってからの勉強
    # 語法: ～おかげで、～せいで、～ばかりに、～以上は、～からには、～限り、～ものなら
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-study-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "大人になってからの勉強",
        "titleJp": "大人になってからの勉強",
        "titleEn": "Studying as an adult",
        "titleZh": "成年后的学习",
        "titleRuby": [],
        "segments": [
            seg("学生時代に怠けたせいで、社会人になってから苦労することが多い。",
                "Because I slacked off during my student days, I've struggled a lot since becoming a working adult.",
                "因为学生时代偷了懒，成为社会人后吃了很多苦。",
                True),
            seg("英語が話せないばかりに、海外出張のチャンスを逃したことがある。あの経験のおかげで、勉強し直す決意ができた。",
                "Just because I couldn't speak English, I once missed a chance for an overseas business trip. Thanks to that experience, I was able to resolve to study again.",
                "仅仅因为不会说英语，就错过了海外出差的机会。多亏了那次经历，我下定决心重新学习。"),
            seg("やると決めた以上は、途中で諦めたくない。資格を取ると決めたからには、毎日最低一時間は勉強するようにしている。",
                "Once I've decided to do it, I don't want to give up halfway. Since I've decided to get a qualification, I make sure to study at least one hour every day.",
                "既然决定了要做，就不想中途放弃。既然决定要考证，我每天至少学习一个小时。"),
            seg("できる限り効率よく勉強したいが、戻れるものなら学生時代に戻ってもっと真剣にやりたかった。",
                "I want to study as efficiently as possible, but if I could go back, I'd want to return to my student days and be more serious about it.",
                "我想尽可能高效地学习，但如果能回去的话，真想回到学生时代更认真地对待。"),
            seg("それでも、大人になってからの勉強は目的が明確な分、集中しやすいとも感じている。",
                "Even so, I also feel that studying as an adult is easier to focus on because the purpose is clearer.",
                "尽管如此，我也觉得成年后的学习因为目的明确，反而更容易集中精力。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 6. dialogue - 留学について話す
    # 語法: ～としたら、～にしても、～たところで、～ようがない、～わけがない、～はずがない、～ことはない
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-study-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "留学について話す",
        "titleJp": "留学について話す",
        "titleEn": "Talking about studying abroad",
        "titleZh": "聊留学",
        "titleRuby": [],
        "sections": [
            section("留学の不安", "Worries about studying abroad", "留学的不安", "🌍", [
                line("A", "来年留学しようと思ってるんだけど、うまくいくか不安で。",
                     "I'm thinking about studying abroad next year, but I'm worried whether it'll go well.",
                     "我想明年去留学，但不安能不能顺利。"),
                line("B", "仮にうまくいかなかったとしたら、どうするつもり？",
                     "If hypothetically it doesn't go well, what would you plan to do?",
                     "假如不顺利的话，你打算怎么办？"),
                line("A", "正直、考えようがないよ。でも、挑戦しないで後悔するのは嫌だな。",
                     "Honestly, there's no way to think about it. But I don't want to regret not trying.",
                     "说实话，我也没法想。但是不挑战就后悔的话我不愿意。"),
            ]),
            section("背中を押す", "Encouragement", "鼓励", "💪", [
                line("B", "にしても、一年くらい海外で暮らすのは貴重な経験だよ。心配したところで、行ってみないと分からないし。",
                     "Even so, living abroad for about a year is a valuable experience. No matter how much you worry, you won't know until you try.",
                     "话虽如此，在国外生活一年左右是很宝贵的经验。就算担心也没用，不去试试是不会知道的。"),
                line("A", "言葉ができないと友達なんかできるわけがないって思ってたけど、そうでもないのかな。",
                     "I thought there's no way I could make friends if I can't speak the language, but maybe that's not the case.",
                     "我以为不会语言的话不可能交到朋友，但也许并非如此。"),
                line("B", "そんなはずがないよ。言葉が完璧じゃなくても、仲良くなれる人は必ずいるから。そんなに心配することはないよ。",
                     "That can't be true. Even if your language isn't perfect, there will definitely be people you can become close with. There's no need to worry that much.",
                     "不可能是那样的。就算语言不完美，也一定有能成为好朋友的人。没必要那么担心。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 7. essay - 高齢化社会の課題
    # 語法: ～べき、～ものだ、～ことだ、～ざるを得ない、～ないわけにはいかない、～てはいられない、～かねない
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-society-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "高齢化社会の課題",
        "titleJp": "高齢化社会の課題",
        "titleEn": "Challenges of an aging society",
        "titleZh": "老龄化社会的课题",
        "titleRuby": [],
        "segments": [
            seg("日本は今、高齢化社会の問題に真剣に向き合うべき時期に来ている。",
                "Japan has now come to a time when it must seriously face the problems of an aging society.",
                "日本现在已经到了必须认真面对老龄化社会问题的时期。",
                True),
            seg("年を取ったら誰でも体が弱くなるものだ。大切なことは、高齢者が安心して暮らせる環境を整えることだ。",
                "It's natural that everyone's body weakens with age. The important thing is to create an environment where the elderly can live with peace of mind.",
                "上了年纪身体变弱是很自然的事。重要的是建设让老年人能安心生活的环境。"),
            seg("介護の人手が足りない現状を見ると、このままでは制度が崩壊しかねない。社会全体で支えないわけにはいかないだろう。",
                "Looking at the current situation where there aren't enough caregiving workers, the system could collapse if things continue like this. Society as a whole has no choice but to provide support.",
                "看到护理人手不足的现状，如果继续这样，制度有可能崩溃。整个社会不得不共同支撑。"),
            seg("若い世代も、この問題を他人事だと思ってはいられない。将来は自分たちの問題になるのだから、今から準備せざるを得ないのだ。",
                "The younger generation also cannot afford to think of this problem as someone else's business. Since it will become their own problem in the future, they have no choice but to prepare now.",
                "年轻一代也不能再把这个问题当成别人的事了。因为将来会变成自己的问题，所以不得不从现在开始准备。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 8. dialogue - ニュースについて議論する
    # 語法: ～恐れがある、～つつある、～一方だ、～ばかりだ、～がちだ、～気味だ、～っぽい
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-society-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "ニュースについて議論する",
        "titleJp": "ニュースについて議論する",
        "titleEn": "Discussing the news",
        "titleZh": "讨论新闻",
        "titleRuby": [],
        "sections": [
            section("少子化のニュース", "News about declining birthrate", "少子化新闻", "📰", [
                line("A", "最近、出生率が下がる一方だってニュースで見たよ。人口減少が加速しつつあるらしい。",
                     "I saw on the news recently that the birth rate just keeps declining. Apparently, the population decline is accelerating.",
                     "最近在新闻上看到出生率一直在下降。人口减少好像正在加速。"),
                line("B", "子育ての費用が増えるばかりだから、若い人が子どもを持つのをためらいがちなんだよね。",
                     "Since childcare costs just keep increasing, young people tend to hesitate about having children.",
                     "因为育儿费用不断增加，年轻人往往对生孩子犹豫不决。"),
            ]),
            section("対策を考える", "Thinking about solutions", "思考对策", "🤔", [
                line("A", "このままだと、年金制度が破綻する恐れがあるよね。",
                     "If things continue like this, there's a risk that the pension system could collapse.",
                     "这样下去的话，养老金制度有崩溃的风险吧。"),
                line("B", "うん。最近ちょっと疲れ気味で、将来のことまで考えると暗くなっちゃうけど。",
                     "Yeah. I've been a bit tired lately, and it gets depressing when I think about the future.",
                     "嗯。最近有点疲劳的感觉，一想到未来的事就很沮丧。"),
                line("A", "確かに。でも、政治家の発言って怒りっぽい反応ばかり呼ぶけど、冷静に議論すべきだよね。",
                     "True. But politicians' statements just provoke angry reactions. We should discuss things calmly.",
                     "确实。但是政治家的发言总是只引起愤怒的反应，应该冷静讨论才对。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 9. essay - AIと人間の未来
    # 語法: ～にすぎない、～に過ぎない、～に限らず、～のみならず、～はもちろん、～はもとより、～ぬきで、～抜きにして
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-tech-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "AIと人間の未来",
        "titleJp": "AIと人間の未来",
        "titleEn": "The future of AI and humans",
        "titleZh": "AI与人类的未来",
        "titleRuby": [],
        "segments": [
            seg("AIは便利な道具にすぎないという人もいるが、その影響は計り知れない。",
                "Some say AI is nothing more than a convenient tool, but its impact is immeasurable.",
                "有人说AI不过是方便的工具，但它的影响是无法估量的。",
                True),
            seg("AIの進歩はIT業界に限らず、医療はもちろん、教育や農業のみならず、芸術の分野にまで及んでいる。",
                "The progress of AI extends not only to the IT industry, but naturally to medicine, and not only education and agriculture, but even to the field of arts.",
                "AI的进步不限于IT行业，医疗自不必说，不仅是教育和农业，甚至已经延伸到艺术领域。"),
            seg("効率はもとより、創造性の面でもAIの能力は人間に迫りつつある。感情論抜きにして冷静に考えれば、人間にしかできないことは確かに存在する。",
                "Not only in efficiency but also in creativity, AI's capabilities are approaching human levels. Setting emotions aside and thinking calmly, there are certainly things only humans can do.",
                "不仅是效率，在创造性方面AI的能力也在逼近人类。抛开感情论冷静思考的话，确实存在只有人类才能做到的事。"),
            seg("しかし、技術の進歩を楽観論ぬきで見つめることも必要だ。AIと共存する未来を、今から真剣に考えなければならない。",
                "However, it's also necessary to look at technological progress without optimism. We must seriously think about a future of coexisting with AI starting now.",
                "但是，不带乐观论地审视技术进步也是必要的。从现在起就必须认真思考与AI共存的未来。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 10. dialogue - スマホ依存について
    # 語法: ～をはじめ、～だけでなく、～ばかりでなく、～どころか、～くせに、～にもかかわらず
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-tech-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "スマホ依存について",
        "titleJp": "スマホ依存について",
        "titleEn": "About smartphone addiction",
        "titleZh": "关于手机依赖",
        "titleRuby": [],
        "sections": [
            section("スマホの使いすぎ", "Overusing smartphones", "过度使用手机", "📱", [
                line("A", "最近、SNSをはじめ、動画アプリやゲームに時間を取られすぎてるんだよね。",
                     "Lately, starting with social media, I've been spending too much time on video apps and games.",
                     "最近，从SNS开始，在视频app和游戏上花的时间太多了。"),
                line("B", "分かる。スマホは便利なだけでなく、依存性も高いからね。",
                     "I understand. Smartphones are not only convenient, they're also highly addictive.",
                     "我懂。智能手机不仅方便，依赖性也很高。"),
                line("A", "やめようと思ってるくせに、気がつくとまた触ってる。",
                     "Even though I'm thinking of quitting, before I know it I'm touching it again.",
                     "明明想着要戒，回过神来又在玩了。"),
            ]),
            section("対策を話し合う", "Discussing countermeasures", "商讨对策", "🛡️", [
                line("B", "使用時間を制限するアプリを入れたにもかかわらず、結局解除しちゃうんだよね。",
                     "Despite installing an app to limit usage time, I end up disabling it.",
                     "虽然装了限制使用时间的app，结果还是解除了。"),
                line("A", "時間を減らすどころか、逆に増えてる気がする。スマホばかりでなく、タブレットも見ちゃうし。",
                     "Far from reducing time, I feel it's actually increasing. And it's not just the smartphone—I watch the tablet too.",
                     "别说减少时间了，反而觉得在增加。不仅是手机，平板也在看。"),
                line("B", "週末だけでもデジタルデトックスしてみない？",
                     "How about trying a digital detox just on weekends?",
                     "要不要试试周末进行数字排毒？"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 11. essay - 健康的な生活を目指して
    # 語法: ～がたい、～かねる、～得る/得ない、～っこない、～ようにする、～ことにする、～ことになる
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-health-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "健康的な生活を目指して",
        "titleJp": "健康的な生活を目指して",
        "titleEn": "Aiming for a healthy lifestyle",
        "titleZh": "追求健康生活",
        "titleRuby": [],
        "segments": [
            seg("健康診断の結果を見て、信じがたい数値が並んでいた。このままでは病気になりかねないと医師に言われた。",
                "Looking at the health checkup results, there were unbelievable numbers lined up. The doctor told me I could get sick if things continued like this.",
                "看到体检结果，排列着难以置信的数值。医生说如果继续这样下去可能会生病。",
                True),
            seg("忙しいからといって、運動しなくていいということにはなり得ない。そこで、毎日三十分歩くことにした。",
                "Just because you're busy doesn't mean it's acceptable not to exercise. So I decided to walk thirty minutes every day.",
                "不能因为忙就说不运动也行。于是我决定每天走路三十分钟。"),
            seg("最初は続けられっこないと思ったが、なるべく階段を使うようにするなど、小さな工夫を重ねた。",
                "At first I thought there was no way I could keep it up, but I accumulated small efforts like trying to use the stairs as much as possible.",
                "最初觉得根本坚持不了，但通过尽量走楼梯等小小的努力积累了起来。"),
            seg("三か月後、体重が減り、体調もよくなった。医師も改善を認めかねるどころか、大いに褒めてくれた。",
                "Three months later, I lost weight and felt better. Far from being reluctant to acknowledge the improvement, the doctor greatly praised me.",
                "三个月后，体重减了，身体状况也变好了。医生非但没有犹豫承认改善，还大力表扬了我。"),
            seg("健康は一日にしてならず。毎日の積み重ねこそが、将来の自分を守ることになるのだ。",
                "Health is not built in a day. It is the daily accumulation that will end up protecting your future self.",
                "健康不是一天就能得到的。每天的积累，最终会保护将来的自己。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 12. dialogue - ダイエットの話
    # 語法: ～ようになる、～てくる、～ていく、～てしまう、～ておく、～てみる、～たがる
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-health-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "ダイエットの話",
        "titleJp": "ダイエットの話",
        "titleEn": "Talking about dieting",
        "titleZh": "聊减肥",
        "titleRuby": [],
        "sections": [
            section("ダイエット開始", "Starting a diet", "开始减肥", "🏃", [
                line("A", "最近、野菜を食べるようになったんだけど、なかなか痩せなくて。",
                     "I've started eating vegetables recently, but I'm not losing weight easily.",
                     "最近开始吃蔬菜了，但怎么也瘦不下来。"),
                line("B", "私もダイエットを始めてから、だんだん体重が落ちてきたよ。最初は変化がなかったけど。",
                     "Since I started my diet, my weight has been gradually dropping too. At first there was no change though.",
                     "我也开始减肥后体重慢慢降下来了。虽然一开始没有变化。"),
                line("A", "つい甘いものを食べてしまうんだよね。先に低カロリーのお菓子を買っておくべきかな。",
                     "I end up eating sweets unintentionally. Maybe I should buy low-calorie snacks in advance.",
                     "总是忍不住吃甜食。应该提前买好低卡零食吗？"),
            ]),
            section("コツを共有する", "Sharing tips", "分享技巧", "📝", [
                line("B", "ジムに通ってみたら？体を動かすと気分もよくなっていくし。",
                     "How about trying going to the gym? Moving your body makes you feel better over time.",
                     "试试去健身房怎么样？运动的话心情也会慢慢变好的。"),
                line("A", "うちの弟もジムに行きたがるんだけど、結局続かないんだよね。",
                     "My younger brother also keeps wanting to go to the gym, but he never keeps it up.",
                     "我弟弟也总想去健身房，但最后都坚持不下来。"),
                line("B", "最初から無理すると続かないよ。少しずつ習慣にしていくのが大事だと思う。",
                     "If you push too hard from the start, you won't keep it up. I think it's important to gradually make it a habit.",
                     "一开始太勉强的话坚持不了的。我觉得慢慢养成习惯比较重要。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 13. essay - 環境問題を考える
    # 語法: ～だらけ、～まみれ、～ぎみ、～向き、～向け、～かけ、～っぱなし、～きり
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-environment-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "環境問題を考える",
        "titleJp": "環境問題を考える",
        "titleEn": "Thinking about environmental issues",
        "titleZh": "思考环境问题",
        "titleRuby": [],
        "segments": [
            seg("海岸を歩くと、ゴミだらけの砂浜が目に入る。油まみれの海鳥を見ると、胸が痛む。",
                "Walking along the coast, the sandy beach covered in trash catches your eye. Seeing seabirds covered in oil makes my heart ache.",
                "走在海岸上，满是垃圾的沙滩映入眼帘。看到浑身沾满油的海鸟，心里很难受。",
                True),
            seg("環境保護は遅れぎみだと言われているが、最近は子ども向けの環境教育プログラムが増えてきた。初心者向きの活動も多い。",
                "Environmental protection is said to be lagging behind, but recently educational programs for children have been increasing. There are also many activities suited for beginners.",
                "虽然说环境保护有些滞后，但最近面向儿童的环境教育项目增多了。适合初学者的活动也很多。"),
            seg("しかし、まだ問題は山積みだ。エアコンをつけっぱなしにしたり、水を出しっぱなしにしたり、日常の無駄は多い。",
                "However, problems are still piling up. Leaving the air conditioner on, leaving the water running—there is a lot of daily waste.",
                "但是问题仍然堆积如山。开着空调不关、水开着不停，日常浪费很多。"),
            seg("読みかけの環境レポートを最後まで読んだ。それきり何もしないのではなく、小さなことから始めるべきだと感じた。",
                "I finished reading an environmental report I had started. I felt that rather than doing nothing after that, I should start with small things.",
                "把读了一半的环境报告读完了。我觉得不应该就此不了了之，而应该从小事做起。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 14. dialogue - ゴミの分別について
    # 語法: ～ずくめ、～まい、～ものか、～ことか、～ではないか、～のではないだろうか
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-environment-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "ゴミの分別について",
        "titleJp": "ゴミの分別について",
        "titleEn": "About garbage sorting",
        "titleZh": "关于垃圾分类",
        "titleRuby": [],
        "sections": [
            section("分別のルール", "Sorting rules", "分类规则", "♻️", [
                line("A", "この町のゴミの分別ルール、規則ずくめで大変だよね。",
                     "The garbage sorting rules in this town are full of regulations and tough, right?",
                     "这个町的垃圾分类规则，全是规定，真够累的。"),
                line("B", "本当に。でも、もう二度とルールを無視するまいと思ってるよ。前に注意されたことか。",
                     "Really. But I've decided I'll never ignore the rules again. How many times I was warned...",
                     "真的。不过我决定再也不无视规则了。被提醒过多少次啊。"),
                line("A", "環境のためだと思えば、文句なんか言うものか。みんなで協力すべきではないか。",
                     "If you think it's for the environment, how could you complain? Shouldn't everyone cooperate?",
                     "想到是为了环境，怎么能抱怨呢。大家不是应该合作吗？"),
            ]),
            section("改善の提案", "Suggestions for improvement", "改善建议", "💡", [
                line("B", "でも、もっと分かりやすくできるのではないだろうか。外国人には特に難しいと思う。",
                     "But couldn't it be made easier to understand? I think it's especially difficult for foreigners.",
                     "不过，是不是能做得更易懂一些呢？我觉得对外国人来说尤其难。"),
                line("A", "確かに。多言語の説明があれば助かるよね。どれほど便利になることか。",
                     "True. It would help if there were multilingual explanations. How convenient that would be.",
                     "确实。如果有多语言说明就好了。那会方便多少啊。"),
                line("B", "市役所に提案してみようよ。きっと前向きに検討してくれると思うよ。",
                     "Let's try suggesting it to the city hall. I'm sure they'll consider it positively.",
                     "向市政府提议试试吧。我觉得他们一定会积极考虑的。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 15. essay - 日本の祭りの魅力
    # 語法: ～をこめて、～を問わず、～によらず、～にかかわらず、～もかまわず、～つつ、～ながらも
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-culture-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "日本の祭りの魅力",
        "titleJp": "日本の祭りの魅力",
        "titleEn": "The charm of Japanese festivals",
        "titleZh": "日本祭典的魅力",
        "titleRuby": [],
        "segments": [
            seg("日本各地では、季節を問わず様々な祭りが行われている。",
                "Throughout Japan, various festivals are held regardless of the season.",
                "在日本各地，不论季节都会举办各种各样的祭典。",
                True),
            seg("祭りの参加者は、年齢や性別にかかわらず、心をこめて準備をする。国籍によらず、誰でも参加できるのも魅力の一つだ。",
                "Festival participants prepare with great care regardless of age or gender. The fact that anyone can participate regardless of nationality is also one of its charms.",
                "祭典的参加者不分年龄和性别，都会用心准备。不论国籍谁都能参加，这也是魅力之一。"),
            seg("雨もかまわず踊り続ける人々の姿は、見ている側の心も動かす。伝統を守りつつ、新しい要素も取り入れている祭りが増えている。",
                "The sight of people continuing to dance despite the rain moves the hearts of those watching. Festivals that incorporate new elements while preserving tradition are increasing.",
                "不顾雨水继续跳舞的人们的身影，也打动了旁观者的心。在守护传统的同时融入新元素的祭典越来越多。"),
            seg("小さな町ながらも、地域の祭りを何百年も続けているところがある。その情熱には、本当に感動させられる。",
                "Even though they are small towns, some places have continued their local festivals for hundreds of years. Their passion truly moves you.",
                "虽然是小镇，却有些地方将地方祭典延续了数百年。那份热情真的令人感动。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 16. dialogue - 着物を着てみたい
    # 語法: ～ものの、～とはいえ、～にしては、～わりに、～くらい/ぐらい、～ほど、～さえ～ば
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-culture-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "着物を着てみたい",
        "titleJp": "着物を着てみたい",
        "titleEn": "I want to try wearing kimono",
        "titleZh": "想试穿和服",
        "titleRuby": [],
        "sections": [
            section("着物への興味", "Interest in kimono", "对和服的兴趣", "👘", [
                line("A", "前から着物を着てみたいと思ってたものの、なかなか機会がなくて。",
                     "I've been wanting to try wearing kimono, but I haven't had the chance.",
                     "虽然之前一直想试穿和服，但一直没有机会。"),
                line("B", "外国人とはいえ、着物体験は気軽にできるよ。レンタルの店も多いし。",
                     "Even though you're a foreigner, you can easily try kimono experiences. There are many rental shops.",
                     "虽说是外国人，但和服体验可以很轻松地参加。出租店也很多。"),
                line("A", "初心者にしては、結構上手に着れたって言われたことがあるんだ。嬉しかったな。",
                     "I was once told I wore it quite well for a beginner. I was happy about that.",
                     "有人说过我作为初学者穿得挺好的。当时很开心。"),
            ]),
            section("着付けの話", "About dressing", "关于穿着", "🎀", [
                line("B", "着物は見た目のわりに動きやすいものもあるよ。浴衣ぐらいなら一人でも着られるし。",
                     "Some kimono are easier to move in than they look. If it's just a yukata, you can wear it by yourself.",
                     "和服有些看起来不方便但其实好活动的。浴衣的程度的话一个人也能穿。"),
                line("A", "帯の結び方が難しいほど、着た時の達成感があるよね。",
                     "The harder the obi knot is to tie, the more sense of achievement you get when wearing it.",
                     "腰带的系法越难，穿上时的成就感越大呢。"),
                line("B", "やる気さえあれば、すぐ上手になるよ。今度一緒に体験に行こう。",
                     "As long as you have motivation, you'll get good quickly. Let's go to an experience together next time.",
                     "只要有干劲，很快就能变熟练的。下次一起去体验吧。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 17. essay - 人との距離感
    # 語法: ～かと思うと、～か～ないかのうちに、～そばから、～て以来、～を契機に、～あげく、～末に
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-relationship-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "人との距離感",
        "titleJp": "人との距離感",
        "titleEn": "The sense of distance with others",
        "titleZh": "与人的距离感",
        "titleRuby": [],
        "segments": [
            seg("仲良くなったかと思うと急に冷たくなる人がいる。連絡先を交換するか しないかのうちに、もう距離を置かれていることもある。",
                "There are people who suddenly become cold just when you think you've become close. Sometimes even before you've finished exchanging contact info, they've already distanced themselves.",
                "有些人，刚觉得关系变好了，就突然变冷淡了。有时候刚交换完联系方式，就已经被疏远了。",
                True),
            seg("大学に入って以来、人間関係に悩むことが増えた。注意したそばから同じ失敗を繰り返す自分にも腹が立つ。",
                "Since entering university, I've had more worries about relationships. I'm also frustrated with myself for repeating the same mistakes right after being careful.",
                "进入大学以来，为人际关系烦恼的事情增多了。刚注意完就又重复同样的错误，对自己也很生气。"),
            seg("ある友人との大喧嘩を契機に、自分のコミュニケーションの問題に気づいた。",
                "A big fight with a certain friend made me realize my communication problems.",
                "以与某个朋友的一次大吵为契机，我意识到了自己沟通上的问题。"),
            seg("悩んだあげく、カウンセリングに通うことにした。長い葛藤の末に、少しずつ人との距離感がつかめるようになった。",
                "After much worrying, I decided to go to counseling. After a long struggle, I gradually became able to grasp the right distance with others.",
                "烦恼了很久之后，决定去做心理咨询。经过长时间的纠结，渐渐能把握与人的距离感了。"),
            seg("完璧な人間関係などないが、相手を理解しようとする姿勢が大切だと、今は思えるようになった。",
                "There is no such thing as a perfect relationship, but I've come to feel that the attitude of trying to understand the other person is important.",
                "虽然不存在完美的人际关系，但我现在已经能觉得试图理解对方的态度很重要了。"),
        ],
    },

    # ═══════════════════════════════════════════
    # 18. dialogue - 友達との誤解
    # 語法: ～結果、～ことから、～ところから、～ばこそ、～てこそ、～からこそ、～さえ
    # ═══════════════════════════════════════════
    {
        "id": "n2-grammar-relationship-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "友達との誤解",
        "titleJp": "友達との誤解",
        "titleEn": "Misunderstanding with a friend",
        "titleZh": "与朋友的误解",
        "titleRuby": [],
        "sections": [
            section("誤解の原因", "Cause of misunderstanding", "误解的原因", "😔", [
                line("A", "ゆみちゃんと気まずくなっちゃった。LINEの返事が遅いことから、怒ってると思われたみたい。",
                     "Things got awkward with Yumi. It seems she thought I was angry because my LINE replies were slow.",
                     "和由美关系变尴尬了。好像因为LINE回复慢，被以为在生气。"),
                line("B", "それだけのところから誤解が生まれたの？話し合った結果、どうなったの？",
                     "A misunderstanding arose just from that? What happened as a result of talking it over?",
                     "仅仅因为那个就产生了误解？谈了之后结果怎样？"),
                line("A", "まだ話せてないんだ。連絡する勇気さえなくて。",
                     "I haven't been able to talk to her yet. I don't even have the courage to contact her.",
                     "还没谈呢。连联系的勇气都没有。"),
            ]),
            section("仲直りへ", "Toward reconciliation", "走向和好", "🤝", [
                line("B", "友達を大切に思えばこそ、ちゃんと向き合うべきだよ。話し合ってこそ、本当の関係が築けるんだから。",
                     "It's precisely because you care about your friend that you should face this properly. It's only by talking that you can build a real relationship.",
                     "正因为珍惜朋友，才应该好好面对。只有通过沟通，才能建立真正的关系。"),
                line("A", "そうだよね。からこそ、勇気を出して連絡してみるよ。",
                     "You're right. That's exactly why I'll muster up the courage and reach out.",
                     "说得对。正因如此，我鼓起勇气联系看看。"),
                line("B", "きっと分かってくれるよ。素直に気持ちを伝えれば大丈夫。",
                     "She'll surely understand. If you honestly convey your feelings, it'll be fine.",
                     "她一定会理解的。坦率地传达心情就没问题。"),
            ]),
        ],
    },

]


def main():
    fp = ROOT / "public" / "data" / "ja_articles.json"
    data = json.loads(fp.read_text("utf-8"))
    exist = {it["id"] for it in data["items"]}
    added = 0
    for it in NEW_ITEMS:
        if it["id"] not in exist:
            data["items"].append(it)
            added += 1
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"✅ Done – added {added}, total {len(data['items'])}")


if __name__ == "__main__":
    main()
