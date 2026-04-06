#!/usr/bin/env python3
"""
batch12 → public/data/ja_articles.json

第1轮重写B: 3组场景 (6篇, essay 20-25句带分段, dialogue口语化)
- n4-eye-clinic (眼科)
- n4-child-fever (孩子发烧)
- n4-sports-pool (区民泳池)

运行: python3 scripts/append_ja_articles_batch12.py
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
    # 1. n4-eye-clinic 眼科
    # ═══════════════════════════════════════════
    {
        "id": "n4-eye-clinic-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "目がかすんで眼科に行く",
        "titleJp": "目がかすんで眼科に行く",
        "titleEn": "Going to the eye doctor for blurry vision",
        "titleZh": "眼睛模糊去了眼科",
        "titleRuby": [],
        "segments": [
            seg("最近、パソコンの画面を見ていると目がかすむようになった。文字がぼやけて、ピントが合わない。",
                "Recently my eyes have been getting blurry when I look at the computer screen. The text is fuzzy and I can't focus.",
                "最近看电脑屏幕时眼睛开始模糊了。字看不清，对不上焦。", True),
            seg("コンタクトレンズの度が合わなくなったのかもしれない。買い替えるにしても、まず検査が必要だ。",
                "Maybe my contact lens prescription no longer fits. Even if I want to replace them, I need an exam first.",
                "可能是隐形眼镜的度数不对了。就算要换，也得先做检查。"),
            seg("同僚に相談したら、「駅前に評判のいい眼科があるよ」と教えてくれた。",
                "When I asked a colleague, they told me 'There's a well-reviewed eye clinic near the station.'",
                "跟同事说了一下，对方告诉我「车站前有家口碑不错的眼科」。"),
            seg("仕事帰りに駅前の眼科クリニックに寄った。予約なしでも受け付けてくれた。",
                "On the way home from work I stopped by the eye clinic near the station. They accepted me without an appointment.",
                "下班路上去了车站前的眼科。没预约也给看了。"),
            seg("受付で「目がかすみます」と伝えると、問診票を渡された。いつから症状があるか、コンタクトは使っているかなどの質問に答えた。",
                "At reception I said 'my eyes are blurry' and was given a questionnaire. I answered questions about when symptoms started and whether I use contacts.",
                "在挂号处说了「眼睛模糊」，拿到了问诊单。回答了什么时候开始有症状、有没有戴隐形眼镜之类的问题。", True),
            seg("待合室にはお年寄りが多かった。テレビで健康番組が流れていて、みんな静かに見ていた。",
                "The waiting room was mostly elderly people. A health program was playing on the TV, and everyone was quietly watching.",
                "候诊室里老年人居多。电视放着健康节目，大家安静地看着。"),
            seg("まず視力検査をした。片目ずつ隠して、Cの字の開いている方向を答える。",
                "First I did a vision test. Covering one eye at a time, I answered which direction the C-shape was open.",
                "先做了视力检查。一只一只眼睛遮住，回答C字缺口朝哪边。"),
            seg("右が〇・五、左が〇・四。去年より下がっている。やっぱり度が変わったようだ。",
                "Right was 0.5, left was 0.4. Lower than last year. My prescription really has changed.",
                "右眼零点五，左眼零点四。比去年又降了。果然度数变了。"),
            seg("次に機械で目に風を当てる検査をした。眼圧を測るためだそうだ。風が来る瞬間、思わず目をつぶってしまう。",
                "Next they tested by blowing air into my eyes with a machine. It's to measure eye pressure, they said. I couldn't help closing my eyes the moment the air came.",
                "接着用机器往眼睛里吹气做检查。说是测眼压的。吹气那一瞬间忍不住闭了眼。", True),
            seg("「もう一回お願いします。目を大きく開けていてくださいね」と看護師に言われた。二回目はなんとか成功した。",
                "The nurse said 'One more time please. Keep your eyes wide open.' I managed it on the second try.",
                "护士说「再来一次。请睁大眼睛」。第二次总算成功了。"),
            seg("暗い部屋に移動して、先生が特殊なライトで目の中を覗いた。「ちょっとまぶしいですけど、動かないでくださいね」。",
                "I moved to a dark room and the doctor looked inside my eyes with a special light. 'It'll be a bit bright, but please don't move.'",
                "转到暗室，医生用特殊的灯看眼睛里面。「会有点刺眼，请不要动」。"),
            seg("ライトが当たると涙が出そうになったが、じっと我慢した。検査は一分ほどで終わった。",
                "When the light hit my eyes I almost teared up, but I held still. The exam took about one minute.",
                "灯照过来差点流泪，但使劲忍住了。检查大概一分钟就结束了。"),
            seg("検査の結果、目の病気ではなく、ただの近視の進行だと分かった。少しほっとした。",
                "The exam showed it wasn't an eye disease, just progressing nearsightedness. I felt a bit relieved.",
                "检查结果不是眼病，只是近视加深了。稍微松了口气。", True),
            seg("先生に「一日八時間以上画面を見ていますか」と聞かれた。正直に「十時間くらいです」と答えた。",
                "The doctor asked 'Do you look at screens more than eight hours a day?' I honestly answered 'about ten hours.'",
                "医生问「一天看屏幕超过八小时吗」。老实回答说「十小时左右」。"),
            seg("「それは多いですね」と言われた。パソコンとスマホを合わせたら、起きている時間のほとんどが画面だ。",
                "'That's a lot,' the doctor said. Combining computer and phone, almost all my waking hours are screen time.",
                "「那太多了」医生说。电脑加手机，醒着的大部分时间都在看屏幕。"),
            seg("「一時間に一回は目を休めてください。遠くの景色を見るだけでも違いますよ」とアドバイスされた。",
                "He advised, 'Rest your eyes once every hour. Even just looking at distant scenery makes a difference.'",
                "「每小时休息一次眼睛。哪怕只是看看远处的风景也不一样」。"),
            seg("目薬も処方してもらった。ドライアイ気味だと言われて、一日四回さすように言われた。",
                "I also got eye drops prescribed. He said I had a tendency toward dry eyes and told me to use them four times a day.",
                "也开了眼药水。说我有点干眼倾向，让我每天滴四次。", True),
            seg("新しい度数でコンタクトの処方箋を書いてもらった。隣のメガネ屋でも使えるそうだ。",
                "I got a prescription for contacts with the new prescription. Apparently it works at the glasses shop next door too.",
                "开了新度数的隐形眼镜处方。说隔壁眼镜店也能用。"),
            seg("会計は保険が使えて千五百円ほどだった。コンタクト代は別だが、検査だけなら思ったより安い。",
                "The bill was about 1,500 yen with insurance. Contact costs are separate, but just the exam was cheaper than I thought.",
                "费用用了保险大概一千五百日元。隐形眼镜另算，但光检查比想象的便宜。"),
            seg("隣のコンタクト屋に処方箋を持っていくと、新しいレンズは三日後に届くと言われた。",
                "When I took the prescription to the contact shop next door, they said the new lenses would arrive in three days.",
                "拿着处方去了隔壁隐形眼镜店，说新镜片三天后到。"),
            seg("帰り道、遠くのビルの看板をぼんやり眺めた。新しいレンズが届いたら、またはっきり見えるようになるだろう。",
                "On the way home I gazed at signs on distant buildings. Once the new lenses arrive, I'll be able to see clearly again.",
                "回去的路上望了望远处楼上的招牌。等新镜片到了，应该又能看清了。", True),
            seg("家に帰って、さっそく目薬をさした。冷たくて気持ちいい。目の疲れが少し和らいだ気がする。",
                "I got home and used the eye drops right away. They were cool and felt nice. My eye fatigue seemed to ease a little.",
                "到家后马上滴了眼药水。凉凉的很舒服。感觉眼睛疲劳减轻了一点。"),
            seg("しばらくはスマホを見る時間も減らそうと思った。目は一生使うものだから、大事にしなければ。",
                "I thought I'd reduce my phone screen time for a while. Your eyes last a lifetime, so you have to take care of them.",
                "打算暂时少看手机。眼睛要用一辈子的，得好好爱护。"),
        ],
    },

    {
        "id": "n4-eye-clinic-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "眼科の待合室で",
        "titleJp": "眼科の待合室で",
        "titleEn": "In the eye clinic waiting room",
        "titleZh": "在眼科候诊室",
        "titleRuby": [],
        "sections": [
            section("受付と問診", "Reception and intake", "挂号和问诊", "🏥", [
                line("A", "すみません、予約してないんですけど、今日診てもらえますか？",
                     "Excuse me, I don't have an appointment, but can I be seen today?",
                     "不好意思，没有预约，今天能看吗？"),
                line("B", "大丈夫ですよ。ただ、予約の方が先になりますので、三十分ほどお待ちいただくかもしれません。",
                     "That's fine. However, patients with appointments go first, so you may have to wait about thirty minutes.",
                     "可以的。不过预约的优先，可能要等三十分钟左右。"),
                line("A", "全然大丈夫です。あの、保険証ってこれでいいですか？マイナンバーカードなんですけど。",
                     "That's totally fine. Um, is this OK for insurance? It's my My Number card.",
                     "完全没问题。那个，保险证用这个行吗？是个人编号卡。"),
                line("B", "はい、マイナンバーカードで大丈夫です。こちらの問診票にご記入お願いします。",
                     "Yes, a My Number card is fine. Please fill out this questionnaire.",
                     "可以的，个人编号卡就行。请填一下这张问诊单。"),
                line("A", "えーと……「現在の症状」は……目がかすむのと、なんか目が疲れやすいんですよね。",
                     "Um... 'current symptoms'... my eyes are blurry and, like, they get tired easily.",
                     "嗯……「现在的症状」……就是眼睛模糊，而且总觉得容易疲劳。"),
                line("B", "コンタクトはお使いですか？",
                     "Do you use contacts?",
                     "有戴隐形眼镜吗？"),
                line("A", "はい、毎日使ってます。ワンデーのやつです。",
                     "Yes, I use them every day. The daily disposable kind.",
                     "有，每天都戴。日抛的那种。"),
            ]),
            section("診察室にて", "In the exam room", "在诊察室", "👁", [
                line("C", "はい、じゃあ視力から測りましょうか。右目から行きますね。この輪っか、どっちが開いてる？",
                     "OK, let's start with your vision. Right eye first. Which way is this ring open?",
                     "好，先测视力吧。从右眼开始。这个环缺口朝哪边？"),
                line("A", "えっと……右……いや、上？ごめんなさい、よく見えなくて。",
                     "Um... right... no, up? Sorry, I can't see it well.",
                     "呃……右……不，上？对不起，看不太清。"),
                line("C", "大丈夫ですよ。じゃあ次、眼圧の検査しますね。ここに顎を乗せて、目を大きく開けてください。",
                     "It's OK. Next, we'll check your eye pressure. Rest your chin here and open your eyes wide.",
                     "没关系。接下来测眼压。把下巴放这里，眼睛睁大。"),
                line("A", "うわっ、風が来るやつですよね……苦手なんですよ、これ。",
                     "Whoa, it's the one that blows air, right... I'm bad with this one.",
                     "哇，是吹气那个吧……我最怕这个了。"),
                line("C", "はい、みんなそう言います。ちょっとだけ我慢してくださいね。……はい、上手。",
                     "Yes, everyone says that. Just bear with it for a moment. ...There, nicely done.",
                     "是啊，大家都这么说。稍微忍一下哦。……好，做得很好。"),
                line("A", "あ、意外と平気だった。",
                     "Oh, that was easier than I thought.",
                     "啊，意外地没事。"),
            ]),
            section("結果と処方", "Results and prescription", "结果和处方", "📋", [
                line("C", "検査の結果なんですけど、近視がちょっと進んでますね。病気じゃないんで安心してください。",
                     "About the results — your nearsightedness has progressed a little. It's not a disease, so don't worry.",
                     "检查结果呢，近视稍微加深了。不是病，请放心。"),
                line("A", "ああ、よかった……。パソコンのせいですかね？毎日十時間くらい見てるんですけど。",
                     "Ah, that's good... Is it because of the computer? I look at it about ten hours a day.",
                     "啊，太好了……是电脑的原因吗？每天看十小时左右。"),
                line("C", "それは多いですね。一時間ごとに休憩を入れてください。あと、寝る前のスマホもできれば控えて。",
                     "That's a lot. Take breaks every hour. Also try to avoid your phone before bed if possible.",
                     "那确实多。每小时休息一下。另外睡前尽量少看手机。"),
                line("A", "寝る前のスマホ、やめられる気がしないんですけど……。",
                     "I don't think I can give up my phone before bed though...",
                     "睡前不看手机，感觉做不到啊……"),
                line("C", "まあ、せめて画面を暗くするとか、ナイトモードにするとかしてみてください。",
                     "Well, at least try dimming the screen or using night mode.",
                     "那至少把屏幕调暗，或者用夜间模式试试。"),
                line("A", "分かりました。コンタクトの処方箋もお願いできますか？",
                     "Got it. Can I also get a contact lens prescription?",
                     "明白了。隐形眼镜的处方也能开吗？"),
                line("C", "もちろん。新しい度数で出しますね。隣のコンタクト屋さんに持って行ってください。",
                     "Of course. I'll write it with the new prescription. Take it to the contact shop next door.",
                     "当然。按新度数开。拿去隔壁的隐形眼镜店就行。"),
                line("A", "ありがとうございます。次はいつ来ればいいですか？",
                     "Thank you. When should I come next?",
                     "谢谢。下次什么时候来？"),
                line("C", "半年後くらいにまた来てください。気になることがあればいつでもどうぞ。",
                     "Come again in about half a year. If anything concerns you, come anytime.",
                     "大概半年后再来。有什么在意的随时来。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n4-child-fever 孩子发烧
    # ═══════════════════════════════════════════
    {
        "id": "n4-child-fever-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "子どもが夜中に熱を出した",
        "titleJp": "子どもが夜中に熱を出した",
        "titleEn": "My child got a fever in the middle of the night",
        "titleZh": "孩子半夜发烧了",
        "titleRuby": [],
        "segments": [
            seg("夜中の二時ごろ、隣で寝ている四歳の息子が急に泣き出した。体を触ると、すごく熱い。",
                "Around 2 AM, my four-year-old son sleeping next to me suddenly started crying. When I touched his body, he was very hot.",
                "凌晨两点左右，睡在旁边的四岁儿子突然哭了起来。一摸身体，烫得不行。", True),
            seg("慌てて体温計で測ると、三十八度七分あった。昼間は元気だったのに、急に高い熱が出た。",
                "I hurriedly measured with a thermometer — 38.7 degrees. He was fine during the day, but suddenly got a high fever.",
                "赶紧量了体温，三十八度七。白天还好好的，突然就烧了。"),
            seg("妻を起こして相談した。「どうする？救急に行く？」「まず様子を見よう。水分を取らせて、冷やそう」。",
                "I woke my wife to discuss. 'What do we do? Go to the ER?' 'Let's wait and see first. Give him fluids and cool him down.'",
                "叫醒妻子商量。「怎么办？去急诊吗？」「先观察一下。让他喝水，降降温」。"),
            seg("冷蔵庫から冷却シートを出して、おでこに貼った。息子は嫌がって剥がそうとする。",
                "I took a cooling sheet from the fridge and put it on his forehead. He didn't like it and tried to peel it off.",
                "从冰箱拿出退热贴贴在额头上。儿子嫌难受想撕掉。", True),
            seg("「ゆうくん、これ気持ちいいよ。ちょっとだけ我慢してね」となだめた。",
                "I soothed him saying 'Yuu-kun, this feels nice. Just bear with it a little.'",
                "「小悠，这个很舒服的。稍微忍一下哦」哄着他。"),
            seg("子ども用の解熱剤を飲ませようとしたが、「にがい！いやだ！」と口から出してしまった。",
                "I tried to give him children's fever reducer, but he spat it out saying 'Bitter! I don't want it!'",
                "想给他吃儿童退烧药，结果「苦！不要！」吐出来了。"),
            seg("りんごジュースに混ぜてもう一度飲ませた。今度はなんとか飲んでくれた。",
                "I mixed it with apple juice and had him drink it again. This time he managed to swallow it.",
                "混在苹果汁里再让他喝。这次总算喝下去了。"),
            seg("三十分ほどで薬が効いてきたのか、泣き止んで寝てくれた。でも私と妻はなかなか寝られなかった。",
                "In about thirty minutes the medicine seemed to kick in — he stopped crying and fell asleep. But my wife and I couldn't get back to sleep easily.",
                "过了三十分钟药好像起效了，不哭了也睡着了。但我和妻子怎么也睡不着。", True),
            seg("一時間おきに息子のおでこに手を当てて、熱が上がっていないか確認した。",
                "Every hour I placed my hand on his forehead to check if his fever had risen.",
                "每隔一小时摸摸儿子的额头，确认有没有再烧上去。"),
            seg("朝になって熱を測ると、三十七度五分に下がっていた。食欲はないが、少しお粥を食べてくれた。",
                "In the morning his temperature had dropped to 37.5. He had no appetite, but ate a little porridge.",
                "到了早上量了体温，降到三十七度五了。没胃口，但吃了点粥。"),
            seg("念のため小児科に連れて行くことにした。妻は仕事があるので、私が会社を休んだ。",
                "To be safe, we decided to take him to the pediatrician. My wife had work, so I took the day off.",
                "为了保险起见决定带他去儿科。妻子要上班，所以我请了假。"),
            seg("上司にメールで「子どもが熱を出したので休みます」と送った。すぐに「お大事に」と返事が来た。",
                "I emailed my boss saying 'My child has a fever so I'll take the day off.' He quickly replied 'Take care.'",
                "发邮件跟上司说「孩子发烧了请个假」。很快回了「保重」。", True),
            seg("病院は朝から混んでいた。待合室には同じくらいの年の子どもが何人もいた。",
                "The hospital was crowded from the morning. In the waiting room were several children around the same age.",
                "医院从早上就人很多。候诊室里有好几个差不多大的小孩。"),
            seg("息子は待っている間、ぐったりして私の膝の上で寝てしまった。",
                "While waiting, my son became listless and fell asleep on my lap.",
                "等的时候儿子蔫蔫地趴在我腿上睡着了。"),
            seg("先生に診てもらうと、「のどが赤いですね。おそらく風邪でしょう」と言われた。",
                "When the doctor examined him, he said 'His throat is red. It's probably a cold.'",
                "医生看了看说「嗓子红了。应该是感冒吧」。", True),
            seg("「保育園で流行っていますか」と聞かれた。確かに先週、同じクラスの子が何人か休んでいた。",
                "'Is it going around at daycare?' the doctor asked. Indeed, several classmates were absent last week.",
                "「保育园在流行吗」被问到。确实上周同班好几个孩子请了假。"),
            seg("「もし明日も三十八度以上あったら、もう一度来てください」と言われた。抗生物質ではなく、風邪薬を処方された。",
                "He said 'If his fever is still above 38 tomorrow, come again.' He prescribed cold medicine, not antibiotics.",
                "「如果明天还在三十八度以上就再来一趟」。开了感冒药，不是抗生素。"),
            seg("薬局でシロップの薬をもらった。甘いイチゴ味で、息子は喜んで飲んだ。",
                "At the pharmacy I got syrup medicine. It was sweet strawberry flavor, and my son happily drank it.",
                "在药房拿了糖浆。甜甜的草莓味，儿子很高兴地喝了。", True),
            seg("帰り道にコンビニでゼリーとりんごジュースを買った。熱があるときは食べやすいものがいい。",
                "On the way home I bought jelly and apple juice at the convenience store. Easy-to-eat food is best when you have a fever.",
                "回去路上在便利店买了果冻和苹果汁。发烧的时候吃容易入口的东西比较好。"),
            seg("昼過ぎには熱が三十七度まで下がり、少し元気が出てきた。おもちゃで遊び始めたので、少し安心した。",
                "By the afternoon his fever dropped to 37 and he got a bit more energetic. He started playing with toys, so I felt relieved.",
                "过了中午烧退到三十七度，精神好了点。开始玩玩具了，稍微放心了。"),
            seg("子どもの急な発熱は何度経験しても慌てる。でも冷静に対応することが大切だと改めて思った。",
                "No matter how many times you experience a child's sudden fever, you panic. But I realized again how important it is to stay calm.",
                "不管经历多少次孩子突然发烧都会慌。不过再次体会到冷静应对很重要。"),
            seg("夜、妻が帰ってきて息子の顔を見て「よかった」と言った。家族が元気でいることが一番だ。",
                "At night my wife came home, looked at our son's face and said 'Thank goodness.' Having a healthy family is what matters most.",
                "晚上妻子回来看了看儿子的脸说「太好了」。家人健康是最重要的。"),
        ],
    },

    {
        "id": "n4-child-fever-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "子どもが熱を出して小児科へ",
        "titleJp": "子どもが熱を出して小児科へ",
        "titleEn": "Taking a feverish child to the pediatrician",
        "titleZh": "孩子发烧去儿科",
        "titleRuby": [],
        "sections": [
            section("夜中の相談", "Late-night discussion", "半夜商量", "🌙", [
                line("A", "ねえ、起きて。ゆうくん、すごい熱いんだけど。",
                     "Hey, wake up. Yuu-kun is really hot.",
                     "喂，醒醒。小悠好烫啊。"),
                line("B", "え、マジ？……三十八度七？高いな。昼は元気だったのに。",
                     "Huh, really? ...38.7? That's high. He was fine this afternoon.",
                     "嗯？真的？……三十八度七？好高。白天还好好的呢。"),
                line("A", "救急行った方がいいかな？ぐったりしてるわけじゃないけど……。",
                     "Should we go to the ER? He's not listless but...",
                     "要不要去急诊？虽然还没蔫……"),
                line("B", "うーん、意識もあるし、とりあえず冷やして様子見よう。冷却シートある？",
                     "Hmm, he's conscious, so let's cool him down and see for now. Do we have cooling sheets?",
                     "嗯，意识也清楚，先降温观察吧。有退热贴吗？"),
                line("A", "冷蔵庫にあるはず。あと解熱剤飲ませたいんだけど、前も吐き出しちゃったんだよね。",
                     "Should be in the fridge. Also I want to give him fever reducer but he spat it out last time too.",
                     "冰箱里应该有。还有退烧药想给他吃，但上次也吐出来了。"),
                line("B", "ジュースに混ぜてみたら？りんごジュースなら味ごまかせるかも。",
                     "Try mixing it with juice? Apple juice might mask the taste.",
                     "混到果汁里试试？苹果汁的话也许能盖住味道。"),
                line("A", "そうだね、やってみる。……あ、飲んだ。よかった。",
                     "Right, I'll try that. ...Oh, he drank it. Good.",
                     "也是，试试看。……啊，喝了。太好了。"),
            ]),
            section("小児科の受付", "Pediatric clinic reception", "儿科挂号", "🏥", [
                line("A", "おはようございます。四歳の息子なんですけど、昨日の夜から熱が出てて。",
                     "Good morning. My four-year-old son has had a fever since last night.",
                     "早上好。四岁的儿子，从昨晚开始发烧。"),
                line("C", "おはようございます。今朝のお熱はどのくらいですか？",
                     "Good morning. What was his temperature this morning?",
                     "早上好。今天早上体温多少？"),
                line("A", "三十七度五分です。夜中は三十八度七分ありました。",
                     "37.5. It was 38.7 in the middle of the night.",
                     "三十七度五。半夜的时候三十八度七。"),
                line("C", "咳や鼻水はありますか？",
                     "Does he have a cough or runny nose?",
                     "有咳嗽或流鼻涕吗？"),
                line("A", "鼻水は少し出てます。咳はあんまりないかな。",
                     "A little runny nose. Not much of a cough, I think.",
                     "鼻涕有一点。咳嗽倒不怎么有。"),
                line("C", "分かりました。では、こちらでお待ちください。順番にお呼びしますね。",
                     "Understood. Please wait here. We'll call you in order.",
                     "知道了。在这边等一下。会按顺序叫号的。"),
            ]),
            section("診察と処方", "Examination and prescription", "诊察和开药", "💊", [
                line("D", "ゆうくん、お口開けてくれるかな？……うん、のどが赤いですね。",
                     "Yuu-kun, can you open your mouth? ...Yep, his throat is red.",
                     "小悠，能张开嘴吗？……嗯，嗓子红了。"),
                line("A", "やっぱり風邪ですかね？保育園で流行ってるみたいで。",
                     "Is it a cold after all? It seems to be going around at daycare.",
                     "果然是感冒吗？保育园好像在流行。"),
                line("D", "そうですね、おそらく風邪でしょう。お薬出しますけど、シロップと粉どっちがいいですか？",
                     "Yes, it's probably a cold. I'll prescribe medicine — would you prefer syrup or powder?",
                     "是的，应该是感冒。开药的话，糖浆和粉剂哪个好？"),
                line("A", "シロップの方が飲んでくれるので、シロップでお願いします。",
                     "He takes syrup better, so syrup please.",
                     "糖浆他比较肯喝，麻烦开糖浆。"),
                line("D", "分かりました。もし明日もまだ三十八度超えてたら、もう一度来てくださいね。",
                     "Got it. If his fever is still over 38 tomorrow, please come again.",
                     "好的。如果明天还超过三十八度的话就再来一趟。"),
                line("A", "保育園はいつから行かせていいですか？",
                     "When can he go back to daycare?",
                     "保育园什么时候可以去？"),
                line("D", "丸一日熱がなければ大丈夫ですよ。焦らず休ませてあげてください。",
                     "If he's had no fever for a full day, he'll be fine. Don't rush it — let him rest.",
                     "整整一天不发烧就没事。别着急，让他好好休息。"),
                line("A", "分かりました。ありがとうございます。",
                     "Understood. Thank you.",
                     "知道了。谢谢。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-sports-pool 区民泳池
    # ═══════════════════════════════════════════
    {
        "id": "n4-sports-pool-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "区民プールで泳ぐ",
        "titleJp": "区民プールで泳ぐ",
        "titleEn": "Swimming at the community pool",
        "titleZh": "在社区游泳池游泳",
        "titleRuby": [],
        "segments": [
            seg("運動不足を感じて、近所の区民プールに行くことにした。学生のとき以来だから、十年ぶりくらいだ。",
                "Feeling a lack of exercise, I decided to go to the local community pool. It's been about ten years since I was a student.",
                "觉得运动不足，决定去附近的社区泳池。上次还是学生时候，大概十年了。", True),
            seg("最近、体重が三キロ増えた。お腹の肉がズボンの上に乗っている。さすがにまずい。",
                "Recently I gained three kilos. My belly fat sits on top of my pants. This is bad.",
                "最近胖了三公斤。肚子上的肉压在裤子上面。这可不行。"),
            seg("ホームページで調べると、一回五百円で、水着と帽子とゴーグルが必要だと書いてあった。",
                "I checked the website and it said it's 500 yen per visit, and you need a swimsuit, cap, and goggles.",
                "查了网页，一次五百日元，需要泳衣、泳帽和泳镜。"),
            seg("水着は昔のがまだあったが、ゴーグルが見つからない。スポーツ用品店で千円のゴーグルを買った。",
                "I still had an old swimsuit, but couldn't find my goggles. I bought 1,000-yen goggles at a sports store.",
                "泳衣还有以前的，但泳镜找不到了。在体育用品店买了一副一千日元的。"),
            seg("日曜日の朝十時に着いた。券売機でチケットを買って、受付に出す。ロッカーの鍵を渡された。",
                "I arrived Sunday morning at ten. Bought a ticket from the machine, handed it to reception, and was given a locker key.",
                "周日早上十点到了。在售票机买了票交给前台。拿到了储物柜的钥匙。", True),
            seg("更衣室で着替えて、シャワーを浴びてからプールに向かった。入る前にシャワーを浴びるのがルールだ。",
                "I changed in the locker room, took a shower, and headed to the pool. Showering before entering is the rule.",
                "在更衣室换好衣服冲了个澡，然后去泳池。入水前冲澡是规定。"),
            seg("プールは二十五メートルが六コースあった。「自由遊泳」と「往復コース」に分かれている。",
                "The pool had six lanes of 25 meters. They were divided into 'free swimming' and 'lap lanes.'",
                "泳池是二十五米六条泳道。分成「自由游泳」和「来回泳道」。"),
            seg("壁に注意事項が貼ってあった。「飛び込み禁止」「走らないでください」と書いてある。",
                "Rules were posted on the wall. 'No diving' and 'Please don't run' were written on them.",
                "墙上贴着注意事项。写着「禁止跳水」「请勿奔跑」。"),
            seg("まず端のコースでゆっくり歩いた。水に入った瞬間は冷たかったが、すぐ慣れた。",
                "First I walked slowly in the end lane. The water was cold the moment I entered, but I got used to it quickly.",
                "先在边上的泳道慢慢走了走。入水那一刻很凉，但很快就习惯了。", True),
            seg("クロールで泳いでみたが、二十五メートルで息が上がった。体力が落ちているのを実感した。",
                "I tried swimming freestyle, but was out of breath after 25 meters. I really felt how much my stamina had dropped.",
                "试着自由泳了一下，二十五米就喘了。切实感到体力下降了。"),
            seg("壁につかまって息を整えた。学生の頃は五百メートルくらい平気で泳げたのに。",
                "I held onto the wall to catch my breath. Back in school I could easily swim 500 meters.",
                "扶着墙喘气。上学那会儿五百米都轻轻松松。"),
            seg("隣のコースではおばあさんが平泳ぎできれいに泳いでいた。自分より全然上手で、ちょっと恥ずかしかった。",
                "In the next lane, an elderly woman was swimming a beautiful breaststroke. She was way better than me, which was a bit embarrassing.",
                "旁边泳道一位奶奶蛙泳游得很漂亮。比我强太多了，有点不好意思。"),
            seg("休み休み、合計で五百メートルほど泳いだ。たった五百メートルなのに全身がだるい。",
                "Taking breaks, I swam about 500 meters total. Despite it being only 500 meters, my whole body felt heavy.",
                "休息着游，总共游了大概五百米。才五百米全身就酸了。", True),
            seg("途中で監視員のお兄さんに「大丈夫ですか」と声をかけられた。そんなに辛そうに見えたのか。",
                "Midway, a lifeguard called out 'Are you OK?' Did I really look that worn out?",
                "中途救生员小哥问了句「没事吧」。看起来那么难受吗。"),
            seg("プールから上がって、シャワーを浴びた。水の中では分からなかったが、かなり汗をかいていたようだ。",
                "I got out of the pool and took a shower. I hadn't noticed in the water, but apparently I had sweated quite a lot.",
                "上岸冲了个澡。在水里没感觉到，其实出了不少汗。"),
            seg("自動販売機でスポーツドリンクを買って、ロビーで飲んだ。運動の後の一杯は最高にうまい。",
                "I bought a sports drink from the vending machine and drank it in the lobby. A drink after exercise tastes absolutely great.",
                "在自动售货机买了瓶运动饮料，在大厅喝了。运动后的一杯真是最棒。", True),
            seg("ロビーの掲示板に水泳教室の案内があった。毎週水曜日の夜、初心者向けのクラスがあるらしい。",
                "On the lobby bulletin board there was information about swimming classes. Apparently there's a beginner class every Wednesday night.",
                "大厅公告栏上有游泳教室的通知。每周三晚上好像有初学者班。"),
            seg("帰り道、体が軽く感じた。疲れているのに気分はいい。水泳は全身運動だから効率がいい。",
                "On the way home, my body felt light. Tired but in a good mood. Swimming works the whole body so it's efficient.",
                "回去的路上身体感觉轻了。虽然累但心情很好。游泳是全身运动，效率很高。"),
            seg("来週も来ようと思った。毎週通えば、半年で一キロくらい泳げるようになるかもしれない。",
                "I thought I'd come again next week. If I come every week, maybe I can swim a kilometer in half a year.",
                "想着下周也来。每周来的话，半年也许能游一公里了。", True),
            seg("月に四回で二千円。ジムに比べたら安い。しかも区民プールは夜九時まで開いているから、仕事の後でも行ける。",
                "Four times a month is 2,000 yen. Cheaper than a gym. Plus the community pool is open until 9 PM, so I can go after work.",
                "一个月四次两千日元。比健身房便宜。而且社区泳池开到晚上九点，下班后也能去。"),
            seg("久しぶりの運動は大変だったが、始めてよかった。少しずつ続けていこう。",
                "Exercising for the first time in ages was tough, but I'm glad I started. I'll keep it up little by little.",
                "久违的运动虽然辛苦，但开始了就好。慢慢坚持下去吧。"),
        ],
    },

    {
        "id": "n4-sports-pool-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "区民プールに行こうよ",
        "titleJp": "区民プールに行こうよ",
        "titleEn": "Let's go to the community pool",
        "titleZh": "一起去社区泳池吧",
        "titleRuby": [],
        "sections": [
            section("友達を誘う", "Inviting a friend", "约朋友", "📱", [
                line("A", "ねえ、最近運動してる？俺、全然動いてなくてさ。",
                     "Hey, have you been exercising lately? I haven't moved at all.",
                     "诶，你最近运动了吗？我完全没动。"),
                line("B", "してないしてない。テレワークで一日中座ってるよ。やばいよね。",
                     "Nope. I'm sitting all day with remote work. It's bad, right.",
                     "没有没有。远程办公坐一整天。太糟了。"),
                line("A", "実はさ、うちの近くに区民プールがあるんだけど、一回五百円なんだよ。一緒に行かない？",
                     "Actually, there's a community pool near my place, and it's only 500 yen per visit. Wanna go together?",
                     "其实我家附近有个社区泳池，一次五百日元。一起去呗？"),
                line("B", "えー、泳ぐの？中学以来泳いでないんだけど。",
                     "Huh, swimming? I haven't swum since middle school.",
                     "诶，游泳？从初中就没游过了。"),
                line("A", "俺もだよ。でも歩くだけのコースもあるみたいだし、無理しなくていいじゃん。",
                     "Me neither. But there seems to be a walking lane too, so no need to push it.",
                     "我也是。不过好像也有只走路的泳道，不用勉强嘛。"),
                line("B", "それなら行ってみようかな。水着、入るかな……。",
                     "Then maybe I'll try going. I wonder if my swimsuit still fits...",
                     "那倒是可以去看看。泳衣还穿得下吗……"),
                line("A", "入らなかったらユニクロで買えばいいよ。日曜の朝、十時に駅で待ち合わせでどう？",
                     "If it doesn't fit just buy one at Uniqlo. How about meeting at the station at ten on Sunday?",
                     "穿不下去优衣库买一条就好了。周日早上十点车站碰头怎么样？"),
            ]),
            section("プールにて", "At the pool", "在泳池", "🏊", [
                line("B", "うわ、思ったよりちゃんとしたプールだね。六コースもある。",
                     "Wow, it's a more proper pool than I expected. Six lanes.",
                     "哇，比想象中正规啊。有六条泳道。"),
                line("A", "だろ？これで五百円だよ。あっちが自由遊泳で、こっちが往復コース。",
                     "Right? And it's only 500 yen. That side is free swimming, this side is lap lanes.",
                     "吧？这才五百日元。那边是自由游泳，这边是来回泳道。"),
                line("B", "まず歩くところから始めていい？いきなり泳ぐのは怖いんだよね。",
                     "Can I start with walking? I'm scared of jumping straight into swimming.",
                     "先从走路开始行吗？突然游有点怕。"),
                line("A", "いいよ。俺は一本泳いでみる。……はあはあ、二十五メートルでもう無理。",
                     "Sure. I'll try swimming a lap. ...Huff huff, I can't do it after just 25 meters.",
                     "行啊。我先游一趟看看。……呼呼，二十五米就不行了。"),
                line("B", "あはは、俺と変わんないじゃん。あ、隣のおばあちゃん、めっちゃきれいなフォームで泳いでるよ。",
                     "Haha, you're no different from me. Oh, the grandma in the next lane is swimming with incredible form.",
                     "哈哈，跟我没两样嘛。啊，旁边那奶奶泳姿好漂亮。"),
                line("A", "うわ、ほんとだ。完全に負けてる。",
                     "Whoa, you're right. We're totally outclassed.",
                     "哇，真的。完全比不上。"),
            ]),
            section("帰り道", "On the way home", "回去的路上", "🚶", [
                line("B", "いやー、疲れたけど気持ちよかったね。五百メートルも泳いでないのに全身筋肉痛になりそう。",
                     "Man, I'm tired but it felt great. I didn't even swim 500 meters but I'm gonna be sore all over.",
                     "哎，累是累但很舒服。连五百米都没游，全身要肌肉酸痛了。"),
                line("A", "明日の朝、起きられないかもね。でもなんか気分いいよな。",
                     "We might not be able to get up tomorrow morning. But it feels nice, huh.",
                     "明天早上可能起不来。但心情确实很好。"),
                line("B", "うん。来週も行く？毎週通ったらちょっとは体力つくかな。",
                     "Yeah. Going next week too? If we go every week, think we'll get fitter?",
                     "嗯。下周也去？每周去的话能恢复点体力吧。"),
                line("A", "絶対つくよ。月四回で二千円だし、ジムよりコスパいいじゃん。",
                     "Definitely. It's 2,000 yen for four times a month — better value than a gym.",
                     "肯定能。一个月四次两千日元，比健身房划算。"),
                line("B", "よし、じゃあ来週も日曜朝ね。あ、その前にスポーツドリンク買っていい？めちゃくちゃ喉乾いた。",
                     "OK, then next Sunday morning too. Oh, can we buy sports drinks first? I'm super thirsty.",
                     "好，那下周也周日早上。啊，先买瓶运动饮料行吗？渴死了。"),
                line("A", "いいよ。あそこに自販機あるじゃん。俺も買う。",
                     "Sure. There's a vending machine right there. I'll buy one too.",
                     "好啊。那边不是有自动售货机嘛。我也买。"),
                line("B", "運動の後の一杯ってなんでこんなにうまいんだろうね。",
                     "Why does a drink after exercise taste so damn good?",
                     "运动后的一杯为什么这么好喝呢。"),
                line("A", "ほんとそれ。じゃ、また来週。",
                     "So true. See you next week then.",
                     "真的。那下周见。"),
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
