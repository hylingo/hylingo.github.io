#!/usr/bin/env python3
"""
batch7 → public/data/ja_articles.json

3 组长文:
1 N3 日本の四季と暮らし
2 N2 おもてなし精神
3 N1 人口減少と地方再生

运行: python3 scripts/append_ja_articles_batch7.py
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

    # ===== 1. N3 日本の四季と暮らし =====
    {
        "id": "n3-four-seasons-essay",
        "level": "N3",
        "format": "essay",
        "titleWord": "日本の四季と暮らし",
        "titleJp": "日本の四季と暮らし",
        "titleEn": "Japan's four seasons and daily life",
        "titleZh": "日本的四季与生活",
        "titleRuby": [],
        "segments": [
            ("日本には春・夏・秋・冬の四つの季節がはっきりとある。",
             "Japan has four distinct seasons: spring, summer, autumn, and winter.",
             "日本有春、夏、秋、冬四个分明的季节。"),
            ("季節の変化は自然だけでなく、食べ物や行事、服装にも大きく影響している。",
             "Seasonal changes affect not only nature, but also food, events, and clothing.",
             "季节的变化不仅影响自然，也深刻影响着饮食、节庆和服装。"),
            ("春になると、桜が咲き始める。花見の季節で、公園には弁当を広げる人々の姿が見られる。",
             "When spring comes, the cherry blossoms begin to bloom. It's hanami season, and you can see people spreading out bento in the parks.",
             "到了春天，樱花开始绽放。赏花季节里，公园里可以看到铺开便当的人们。"),
            ("入学式や入社式など、新生活の始まりも春に多い。",
             "Entrance ceremonies for school and companies — many new beginnings happen in spring.",
             "入学典礼和入职仪式等，新生活的开始也多在春天。"),
            ("夏は蒸し暑く、エアコンなしでは過ごせない日が続く。",
             "Summer is hot and humid, with days when you can't get by without air conditioning.",
             "夏天闷热潮湿，没有空调的话日子没法过。"),
            ("花火大会やお盆など、夏ならではの行事も多い。",
             "There are many events unique to summer, like fireworks festivals and Obon.",
             "烟花大会和盂兰盆节等，夏天特有的活动也很多。"),
            ("浴衣を着て夏祭りに出かけるのは、日本の夏の風物詩だ。",
             "Wearing a yukata to summer festivals is a quintessential image of Japanese summer.",
             "穿浴衣去夏日祭，是日本夏天的风物诗。"),
            ("秋は過ごしやすい気候で、紅葉が美しい季節だ。",
             "Autumn has pleasant weather and is the season of beautiful autumn leaves.",
             "秋天气候宜人，是红叶美丽的季节。"),
            ("食欲の秋とも言われ、サンマや栗など旬の食べ物を楽しむ人が多い。",
             "It's also called the 'autumn of appetite,' and many people enjoy seasonal foods like sanma and chestnuts.",
             "也被称为食欲之秋，很多人享受秋刀鱼和栗子等当季美食。"),
            ("読書の秋、スポーツの秋など、秋にはさまざまな楽しみ方がある。",
             "Reading in autumn, sports in autumn — there are various ways to enjoy the season.",
             "读书之秋、运动之秋……秋天有各种各样的乐趣。"),
            ("冬になると、気温が下がり、日本海側では雪が多く降る。",
             "When winter comes, temperatures drop, and heavy snow falls on the Sea of Japan side.",
             "到了冬天，气温下降，日本海一侧降雪很多。"),
            ("お正月には家族が集まり、おせち料理を食べて新年を祝う。",
             "At New Year's, families gather together, eat osechi cuisine, and celebrate the new year.",
             "新年时全家团聚，吃御节料理庆祝新年。"),
            ("こたつでみかんを食べながらテレビを見るのが、冬の定番の過ごし方だ。",
             "Eating mandarin oranges under the kotatsu while watching TV is a classic way to spend winter.",
             "窝在暖桌里边吃橘子边看电视，是冬天的经典度过方式。"),
            ("四季があることで、日本人は季節の移り変わりを大切にしてきた。",
             "Because of the four seasons, Japanese people have long valued the changing of the seasons.",
             "正因为有四季，日本人一直珍视着季节的更替。"),
            ("俳句に季語があるように、言葉の中にも季節の感覚が深く根づいている。",
             "Just as haiku have seasonal words, a sense of the seasons is deeply rooted in the language.",
             "正如俳句中有季语一样，语言中也深深扎根着对季节的感受。"),
            ("旬のものを食べ、季節の行事を楽しむ。それが日本の暮らしの豊かさだと思う。",
             "Eating seasonal foods and enjoying seasonal events — that, I think, is the richness of life in Japan.",
             "吃当季的食物，享受季节的活动。我觉得这就是日本生活的丰富之处。"),
        ],
    },
    {
        "id": "n3-four-seasons-dialogue",
        "level": "N3",
        "format": "dialogue",
        "titleWord": "日本の四季の楽しみ方について話す",
        "titleJp": "日本の四季の楽しみ方について話す",
        "titleEn": "Talking about how to enjoy Japan's four seasons",
        "titleZh": "聊日本四季的乐趣",
        "titleRuby": [],
        "sections": [
            section("春と夏", "Spring and summer", "春与夏", "🌸", [
                ("A", "日本に来て一番感動したのは、春の桜かな。満開の桜並木は本当にきれいだった。",
                 "The thing that moved me most after coming to Japan was the spring cherry blossoms. The rows of trees in full bloom were truly beautiful.",
                 "来日本后最让我感动的大概是春天的樱花吧。盛开的樱花大道真的好漂亮。"),
                ("B", "花見は日本の文化だよね。友達とシートを広げて、お弁当を食べながら桜を見るのが最高。",
                 "Hanami is Japanese culture. Spreading a sheet with friends and eating bento while looking at the cherry blossoms is the best.",
                 "赏花是日本的文化呢。和朋友铺上垫子，一边吃便当一边看樱花，太棒了。"),
                ("A", "夏はとにかく暑いけど、花火大会が好き。浴衣を着て見に行くのが楽しい。",
                 "Summer is just so hot, but I love fireworks festivals. It's fun going in a yukata.",
                 "夏天热是真热，但我喜欢烟花大会。穿浴衣去看很开心。"),
                ("B", "かき氷を食べながら花火を見るのは、夏の最高の贅沢だと思う。",
                 "Watching fireworks while eating shaved ice is the ultimate summer luxury, I think.",
                 "我觉得一边吃刨冰一边看烟花，是夏天最奢侈的享受。"),
                ("A", "お盆の時期は電車が空くから、東京はちょっと静かになるよね。",
                 "During the Obon period the trains are less crowded, so Tokyo gets a little quiet.",
                 "盂兰盆节期间电车没那么挤，东京会安静一些呢。"),
            ]),
            section("秋と冬", "Autumn and winter", "秋与冬", "🍂", [
                ("A", "秋は一番好きな季節かもしれない。涼しくて、食べ物もおいしい。",
                 "Autumn might be my favorite season. It's cool and the food is delicious.",
                 "秋天可能是我最喜欢的季节。凉爽，食物也好吃。"),
                ("B", "紅葉を見に京都に行ったことある？あれは本当に感動するよ。",
                 "Have you been to Kyoto to see the autumn leaves? It's truly moving.",
                 "去过京都看红叶吗？那真的很感动。"),
                ("A", "まだ行ったことない。今年こそ行きたいな。",
                 "Not yet. I really want to go this year.",
                 "还没去过。今年一定要去。"),
                ("B", "冬はやっぱりこたつが恋しくなる。みかんを食べながらダラダラするのが最高。",
                 "In winter, I really miss the kotatsu. Lounging around eating mandarin oranges is the best.",
                 "冬天果然会想念暖桌。边吃橘子边懒洋洋的最棒了。"),
                ("A", "お正月のおせち料理も楽しみ。日本に来てから、季節ごとの楽しみが増えた気がする。",
                 "I look forward to New Year's osechi too. Since coming to Japan, I feel like I have more things to enjoy each season.",
                 "新年的御节料理也很期待。来日本之后，感觉每个季节的乐趣都增多了。"),
                ("B", "四季がはっきりしているのは、日本の一番いいところかもしれないね。",
                 "Having distinct four seasons might be the best thing about Japan.",
                 "四季分明或许是日本最好的地方呢。"),
            ]),
        ],
    },

    # ===== 2. N2 おもてなし =====
    {
        "id": "n2-omotenashi-essay",
        "level": "N2",
        "format": "essay",
        "titleWord": "日本の「おもてなし」精神とその裏側",
        "titleJp": "日本の「おもてなし」精神とその裏側",
        "titleEn": "Japan's spirit of 'omotenashi' and what lies behind it",
        "titleZh": "日本「待客之道」的精神与其背后",
        "titleRuby": [],
        "segments": [
            ("日本のサービスの質は世界的に高く評価されている。",
             "The quality of service in Japan is highly regarded worldwide.",
             "日本的服务质量在世界范围内得到了很高的评价。"),
            ("店員の丁寧な接客、ホテルの行き届いたサービス、公共交通の正確さ。いずれも「おもてなし」の精神が根底にある。",
             "Polite service from shop staff, attentive hotel service, the punctuality of public transport — all have the spirit of 'omotenashi' at their foundation.",
             "店员礼貌的接待、酒店周到的服务、公共交通的准时。这些背后都有「待客之道」的精神。"),
            ("おもてなしとは、相手が何を求めているかを察し、言われる前に行動することを指す。",
             "Omotenashi refers to sensing what the other person wants and acting before being asked.",
             "所谓待客之道，是指察觉对方的需求，在被告知之前就采取行动。"),
            ("たとえば、レストランで水がなくなりかけると、頼まなくても店員が注ぎに来る。",
             "For example, when your water glass is getting low at a restaurant, the staff will come to refill it without being asked.",
             "比如在餐厅，水快喝完的时候，不用叫服务员就会来倒水。"),
            ("こうした気配りは、外国人観光客を感動させることも多い。",
             "This kind of attentiveness often impresses foreign tourists.",
             "这样的细心体贴常常令外国游客感动。"),
            ("しかし、この高水準のサービスには代償がある。",
             "However, this high standard of service comes at a cost.",
             "然而，这种高水准的服务是有代价的。"),
            ("サービス業に従事する人々は、常に笑顔を求められ、理不尽なクレームにも耐えなければならない。",
             "People working in the service industry are constantly required to smile and must endure unreasonable complaints.",
             "从事服务行业的人被要求时刻保持微笑，还必须忍受不合理的投诉。"),
            ("「お客様は神様」という言葉があるが、それが行き過ぎると、従業員の精神的な負担は計り知れない。",
             "There's the expression 'the customer is God,' but when taken too far, the mental burden on employees is immeasurable.",
             "有句话叫「顾客就是上帝」，但走过头的话，对员工的精神负担是不可估量的。"),
            ("近年、カスタマーハラスメント、いわゆる「カスハラ」が社会問題となっている。",
             "In recent years, customer harassment — so-called 'kasuhara' — has become a social issue.",
             "近年来，顾客骚扰，即所谓的「顾客霸凌」已成为社会问题。"),
            ("暴言を吐いたり、土下座を強要したりする悪質な客に対して、企業が毅然とした対応を取る動きも出てきた。",
             "There's been a movement of companies taking a firm stance against malicious customers who hurl abuse or demand prostration apologies.",
             "对于口出恶言或强迫下跪道歉的恶劣顾客，也出现了企业采取坚决态度的动向。"),
            ("また、過剰サービスがコストを押し上げ、低価格競争の一因になっているとの指摘もある。",
             "There's also the point that excessive service drives up costs and contributes to price wars.",
             "也有人指出，过度服务推高了成本，成为低价竞争的原因之一。"),
            ("深夜のコンビニ営業や、送料無料の即日配送は、本当に必要なのかという声も上がっている。",
             "Voices are also being raised asking whether late-night convenience store operations and free same-day delivery are really necessary.",
             "也有人质疑，深夜便利店营业和免费当日配送真的有必要吗。"),
            ("おもてなしの精神そのものは美しい文化だが、それを支える人々が疲弊しては本末転倒だ。",
             "The spirit of omotenashi itself is a beautiful culture, but if the people supporting it are exhausted, it defeats the purpose.",
             "待客之道的精神本身是美好的文化，但如果支撑它的人都疲惫不堪就本末倒置了。"),
            ("提供する側も受け取る側も、互いに敬意を持つこと。それが真のおもてなしではないだろうか。",
             "Both the providers and receivers showing mutual respect — isn't that what true omotenashi is?",
             "提供方和接受方都相互尊重。这或许才是真正的待客之道吧。"),
            ("サービスの質を維持しながら、働く人の尊厳も守る。その両立が、これからの日本社会に求められている。",
             "Maintaining service quality while also protecting the dignity of workers — achieving both is what Japanese society needs going forward.",
             "在维持服务质量的同时也守护劳动者的尊严。兼顾两者正是今后日本社会所需要的。"),
        ],
    },
    {
        "id": "n2-omotenashi-dialogue",
        "level": "N2",
        "format": "dialogue",
        "titleWord": "日本のサービスと「カスハラ」について議論する",
        "titleJp": "日本のサービスと「カスハラ」について議論する",
        "titleEn": "Discussing Japanese service and 'customer harassment'",
        "titleZh": "讨论日本的服务与「顾客霸凌」",
        "titleRuby": [],
        "sections": [
            section("サービスの質", "Quality of service", "服务质量", "✨", [
                ("A", "日本のサービスって、本当に細かいところまで行き届いてるよね。",
                 "Japanese service really is attentive down to the smallest details.",
                 "日本的服务真的是连细节都照顾到了。"),
                ("B", "この前、デパートで商品を買ったら、店員さんがエレベーターまで見送ってくれて驚いた。",
                 "The other day, when I bought something at a department store, the clerk walked me all the way to the elevator — I was surprised.",
                 "前几天在百货公司买了东西，店员送我到电梯那里，吓了一跳。"),
                ("A", "海外じゃ考えられないよね。でも、それを当たり前にしている店員さんは大変だろうなと思う。",
                 "It's unthinkable overseas. But I imagine it must be tough for the staff who make it routine.",
                 "在国外简直不可想象。但我觉得把这当成理所当然的店员一定很辛苦。"),
                ("B", "確かに。常に笑顔で丁寧にっていうのは、相当なストレスだと思う。",
                 "True. Always smiling and being polite must be incredibly stressful.",
                 "确实。一直保持微笑、礼貌待客，压力应该相当大。"),
            ]),
            section("カスハラ問題", "Customer harassment", "顾客霸凌问题", "⚠️", [
                ("A", "最近、カスハラのニュースが増えてるけど、実際に見たことある？",
                 "Recently there's been more news about customer harassment — have you actually seen it?",
                 "最近顾客霸凌的新闻越来越多，你实际见过吗？"),
                ("B", "コンビニでバイトしてたとき、理不尽に怒鳴られたことは何度かある。",
                 "When I was working part-time at a convenience store, I was yelled at unreasonably several times.",
                 "在便利店打工的时候，被无理取闹地吼过好几次。"),
                ("A", "それはひどいね。最近は企業がマニュアルを作って、毅然と対応するところも増えてきたらしい。",
                 "That's terrible. Recently it seems more companies are creating manuals and responding firmly.",
                 "那太过分了。最近好像越来越多的企业制定了应对手册，采取坚决态度。"),
                ("B", "「お客様は神様」っていう意識が変わらないと、根本的な解決にはならないと思う。",
                 "I think unless the mindset of 'the customer is God' changes, there won't be a fundamental solution.",
                 "我觉得如果「顾客就是上帝」的观念不改变，就不会有根本的解决。"),
                ("A", "サービスを受ける側にも、感謝の気持ちと最低限の礼儀は必要だよね。",
                 "Those receiving service also need gratitude and basic courtesy.",
                 "接受服务的一方也需要有感恩的心和起码的礼貌呢。"),
                ("B", "おもてなしって、双方向のものであるべきだと思う。一方的に尽くすだけじゃ、長続きしないよ。",
                 "I think omotenashi should be bidirectional. If it's just one side giving, it won't last.",
                 "我觉得待客之道应该是双向的。只是单方面付出的话，是持续不下去的。"),
            ]),
        ],
    },

    # ===== 3. N1 人口減少と地方再生 =====
    {
        "id": "n1-depopulation-essay",
        "level": "N1",
        "format": "essay",
        "titleWord": "人口減少社会における地方再生の模索",
        "titleJp": "人口減少社会における地方再生の模索",
        "titleEn": "The search for regional revitalization in a depopulating society",
        "titleZh": "人口减少社会中地方振兴的探索",
        "titleRuby": [],
        "segments": [
            ("日本の総人口は二〇〇八年をピークに減少に転じ、以来、その傾向に歯止めがかかる気配はない。",
             "Japan's total population peaked in 2008 and turned to decline, and since then there has been no sign of this trend stopping.",
             "日本的总人口在2008年达到顶峰后转为减少，此后这一趋势毫无停止的迹象。"),
            ("とりわけ深刻なのは地方部であり、若年層の大都市圏への流出が、地域社会の存続そのものを脅かしている。",
             "The situation is especially serious in rural areas, where the outflow of young people to metropolitan areas threatens the very survival of local communities.",
             "尤为严重的是地方地区，年轻人向大城市圈的流出正在威胁着地域社会的存亡。"),
            ("総務省の調査によれば、全国の自治体のうち約半数が、二〇四〇年までに「消滅可能性都市」に該当するとされている。",
             "According to a Ministry of Internal Affairs survey, approximately half of all municipalities in the country are classified as 'cities at risk of disappearing' by 2040.",
             "据总务省调查，全国约半数自治体到2040年将被归为「可能消失的城市」。"),
            ("空き家問題はその象徴的な事例である。全国の空き家率は過去最高を記録し、管理が行き届かない物件が防災・防犯上のリスクとなっている。",
             "The vacant house problem is a symbolic example. The national vacancy rate has hit a record high, and poorly maintained properties pose disaster prevention and public safety risks.",
             "空置房问题是其标志性案例。全国空置率创历史新高，管理不到位的房屋在防灾防盗方面构成风险。"),
            ("こうした状況に対し、国は「地方創生」を掲げ、移住支援や起業支援など様々な施策を講じてきた。",
             "In response to this situation, the national government has championed 'regional revitalization,' implementing various measures including migration and entrepreneurship support.",
             "面对这种状况，国家提出了「地方创生」的口号，采取了移居支援和创业支援等各种政策。"),
            ("中でも「地域おこし協力隊」制度は注目を集めている。都市部の若者が地方に移住し、農業振興や観光開発に携わるこの仕組みは、年間六千人以上が参加するまでに拡大した。",
             "Among these, the 'Regional Revitalization Cooperation Corps' system has attracted attention. This scheme, in which young urban residents move to rural areas to engage in agricultural promotion and tourism development, has expanded to over 6,000 participants annually.",
             "其中「地域振兴协力队」制度备受关注。城市年轻人移居地方从事农业振兴和旅游开发，该制度已扩大到每年六千人以上参与。"),
            ("任期終了後も約六割が定住しているというデータは、一定の成果を示すものだろう。",
             "Data showing that about 60% remain settled after their term ends likely indicates a certain degree of success.",
             "任期结束后约六成人留下定居的数据，大概显示了一定的成果。"),
            ("ただし、成功事例ばかりではない。受け入れ側の自治体との意思疎通がうまくいかず、途中で離脱するケースも報告されている。",
             "However, it's not all success stories. Cases where communication with the host municipality breaks down and participants drop out partway have also been reported.",
             "不过并非全是成功案例。也有报道称与接收方自治体沟通不畅、中途退出的情况。"),
            ("近年は「関係人口」という概念が提唱されている。完全な移住ではなく、ふるさと納税やボランティア、週末だけの滞在など、多様な形で地域と関わる人々を指す。",
             "In recent years, the concept of 'related population' has been proposed. It refers to people who engage with a region in diverse ways — not full migration, but through hometown tax donations, volunteering, or weekend stays.",
             "近年来「关系人口」这一概念被提出。不是完全移居，而是通过故乡纳税、志愿活动、仅周末停留等多种形式与地区产生联系的人群。"),
            ("定住人口の増加が困難であるならば、地域に関心を持つ人々の裾野を広げるという発想は、現実的な打開策と言えよう。",
             "If increasing the settled population is difficult, then the idea of broadening the base of people interested in the region can be called a realistic breakthrough strategy.",
             "如果增加定居人口困难的话，那么拓宽对地区感兴趣的人群基础这一思路，可以说是现实的突破口。"),
            ("テクノロジーの活用も鍵を握る。高速インターネットの整備により、地方でも都市部と同等の仕事環境を構築できるようになりつつある。",
             "The utilization of technology also holds the key. With the development of high-speed internet, it is becoming possible to build work environments in rural areas equivalent to those in urban areas.",
             "技术的运用也是关键。随着高速互联网的完善，地方也逐渐能构建与城市同等的工作环境。"),
            ("遠隔医療やオンライン教育の普及は、地方の生活利便性を飛躍的に向上させる可能性を秘めている。",
             "The spread of telemedicine and online education holds the potential to dramatically improve the convenience of rural living.",
             "远程医疗和在线教育的普及蕴含着大幅提升地方生活便利性的可能。"),
            ("しかしながら、地方再生に特効薬はない。地域ごとに歴史や資源が異なる以上、画一的な処方箋は通用しない。",
             "However, there is no silver bullet for regional revitalization. Since each region has different history and resources, a one-size-fits-all prescription won't work.",
             "然而，地方振兴并没有特效药。既然每个地区的历史和资源各不相同，千篇一律的方案就行不通。"),
            ("重要なのは、その土地に暮らす人々が主体的に未来を描き、外部の力を柔軟に取り入れることではないだろうか。",
             "What matters is perhaps for the people living in those regions to proactively envision their future and flexibly incorporate outside resources.",
             "重要的或许是当地居民主动描绘未来，并灵活引入外部力量。"),
            ("人口が減ること自体を止められなくとも、地域の魅力を再発見し、持続可能な形で次世代へつないでいく。",
             "Even if the population decline itself cannot be stopped, rediscovering regional charm and passing it on to the next generation in a sustainable form.",
             "即使无法阻止人口减少本身，也要重新发现地区的魅力，以可持续的方式传承给下一代。"),
            ("その営みこそが、人口減少社会における地方再生の本質であると、私は考える。",
             "I believe that such endeavors are the essence of regional revitalization in a depopulating society.",
             "我认为，这样的努力才是人口减少社会中地方振兴的本质。"),
        ],
    },
    {
        "id": "n1-depopulation-dialogue",
        "level": "N1",
        "format": "dialogue",
        "titleWord": "地方の過疎化と再生の取り組みについて議論する",
        "titleJp": "地方の過疎化と再生の取り組みについて議論する",
        "titleEn": "Discussing rural depopulation and revitalization efforts",
        "titleZh": "讨论地方过疏化与振兴的举措",
        "titleRuby": [],
        "sections": [
            section("現状認識", "Understanding the current situation", "现状认识", "📊", [
                ("A", "先日、地元に帰省したら、商店街がほとんどシャッター通りになっていて衝撃を受けた。",
                 "When I went back to my hometown the other day, I was shocked to find the shopping street had become almost entirely shuttered.",
                 "前几天回了趟老家，发现商店街几乎全变成了关门街，很震惊。"),
                ("B", "人口減少の影響は、地方の商業にもっとも顕著に表れるからね。客がいなければ、店を続けようがない。",
                 "The impact of population decline shows most prominently in local commerce. If there are no customers, there's no way to keep a shop running.",
                 "人口减少的影响在地方商业中表现得最为明显。没有顾客的话，店就开不下去。"),
                ("A", "空き家も目立つようになった。子どもの頃に遊んだ公園も、雑草だらけで荒れていた。",
                 "Vacant houses have become conspicuous too. The park where I played as a child was overgrown with weeds and neglected.",
                 "空置房也越来越醒目了。小时候玩耍的公园也杂草丛生、荒废了。"),
                ("B", "そういった光景を見ると、このままでは本当に町が消えてしまうんじゃないかと危機感を覚えるよ。",
                 "Seeing such scenes, I feel a genuine sense of crisis that the town might really disappear at this rate.",
                 "看到这种景象，真的会产生危机感，觉得这样下去小镇恐怕真的会消失。"),
            ]),
            section("再生への取り組み", "Revitalization efforts", "振兴的举措", "🌱", [
                ("A", "地域おこし協力隊について聞いたことある？都市部から若者が移住して、地域活性化に取り組む制度なんだけど。",
                 "Have you heard of the Regional Revitalization Cooperation Corps? It's a system where young people move from urban areas and work on regional vitalization.",
                 "你听说过地域振兴协力队吗？是城市年轻人移居到地方、致力于地区振兴的制度。"),
                ("B", "知ってる。六割が任期後も定住するらしいから、単なるお試しではなくて、本気で根を下ろす人も多いんだよね。",
                 "I know. Apparently 60% stay even after their term, so it's not just a trial — many seriously put down roots.",
                 "知道。据说六成人任期后也留下了，不只是尝试，真正扎根的人也不少。"),
                ("A", "ただ、受け入れ側との溝が埋まらずに途中で辞めてしまうケースもあるらしい。やはり外から来た人と地元の人との価値観の違いは簡単には埋められない。",
                 "But apparently there are also cases where the gap with the host community can't be bridged and people quit midway. The difference in values between outsiders and locals can't be easily reconciled.",
                 "不过好像也有与接收方之间的隔阂无法弥合、中途退出的案例。果然外来者和当地人之间价值观的差异不是轻易能消除的。"),
                ("B", "「関係人口」という考え方も面白いと思う。完全に住まなくても、ふるさと納税やボランティアで関わり続けるという形もあり得る。",
                 "I think the concept of 'related population' is interesting too. Even without fully relocating, continued involvement through hometown tax or volunteering is also possible.",
                 "我觉得「关系人口」这个概念也很有意思。即使不完全住下来，通过故乡纳税或志愿活动持续参与也是一种形式。"),
                ("A", "テクノロジーの力も大きいよね。リモートワークが普及すれば、地方にいても都市部の仕事ができる。",
                 "Technology plays a big role too. If remote work spreads, you can do urban jobs while living in the countryside.",
                 "技术的力量也很大呢。如果远程办公普及的话，在地方也能做城市的工作。"),
                ("B", "結局のところ、その土地に暮らす人たちが当事者意識を持って動かないと、外部の支援だけでは限界があるんだろうね。",
                 "In the end, unless the people living there take ownership and act, there are limits to what outside support alone can achieve.",
                 "归根结底，如果当地居民不带着主人翁意识行动起来，光靠外部支援是有局限性的吧。"),
                ("A", "人口が減っても、地域の文化や自然は残せるはず。縮小しながらも、豊かさを維持する道を探るしかないのかもしれない。",
                 "Even if the population decreases, regional culture and nature should be preservable. Perhaps the only path is to search for ways to maintain richness even while shrinking.",
                 "即使人口减少，地区的文化和自然应该是可以保留的。或许只能在缩小的同时，探索维持丰富性的道路。"),
            ]),
        ],
    },
]


def main():
    path = ROOT / "public" / "data" / "ja_articles.json"
    data = json.loads(path.read_text("utf-8"))
    existing_ids = {it["id"] for it in data["items"]}

    added = 0
    for item in NEW_ITEMS:
        if item["id"] in existing_ids:
            print(f"  skip (exists): {item['id']}")
            continue

        if item["format"] == "essay":
            raw = item["segments"]
            item["segments"] = [enrich_segment(w, e, z) for w, e, z in raw]

        item["titleRuby"] = gr.make_ruby(item["titleWord"])

        data["items"].append(item)
        added += 1
        print(f"  added: {item['id']} — {item['titleWord']}")

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"\n合計 {added} 件追加しました。")


if __name__ == "__main__":
    main()
