#!/usr/bin/env python3
"""
batch11 → public/data/ja_articles.json

第1轮重写A: 6组医疗健康+运动场景 (12篇, essay 20-25句带分段, dialogue口语化)
- n4-clinic (诊所看病)
- n4-pharmacy (药店买药)
- n4-dental (洗牙)
- n4-eye-clinic (眼科)
- n4-child-fever (孩子发烧)
- n4-sports-pool (区民泳池)

运行: python3 scripts/append_ja_articles_batch11.py
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
    # 1. n4-clinic 诊所看病
    # ═══════════════════════════════════════════
    {
        "id": "n4-clinic-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "かかりつけの内科で診てもらう",
        "titleJp": "かかりつけの内科で診てもらう",
        "titleEn": "Getting examined at my regular clinic",
        "titleZh": "在常去的内科看病",
        "titleRuby": [],
        "segments": [
            seg("三日前から咳が止まらず、鼻水も出るようになった。市販の薬を飲んだが、あまり効かなかった。",
                "My cough hadn't stopped for three days, and I started getting a runny nose. Over-the-counter medicine didn't help much.",
                "三天前开始咳嗽不停，还流鼻涕了。吃了非处方药也没什么效果。", True),
            seg("四日目の朝、熱を測ると三十七度九分あった。これはもう病院に行くしかない。",
                "On the morning of the fourth day, my temperature was 37.9. I had no choice but to go to the hospital.",
                "第四天早上一量体温，三十七度九。这下只能去医院了。"),
            seg("会社に電話して「体調が悪いのでお休みをいただけますか」と伝えた。上司は「お大事に」と言ってくれた。",
                "I called the office and said 'I'm not feeling well, may I take the day off?' My boss said 'Take care.'",
                "打电话给公司说「身体不舒服能请假吗」。上司说了句「保重」。"),
            seg("駅前の内科クリニックは九時に開く。八時五十分に着いたが、もう五人並んでいた。",
                "The internal medicine clinic near the station opens at nine. I arrived at 8:50, but five people were already lined up.",
                "车站前的内科诊所九点开门。八点五十到了，已经排了五个人。", True),
            seg("受付で保険証を出して、問診票を書いた。「いつから症状がありますか」「三日前からです」と書く。",
                "At reception I showed my insurance card and filled out the questionnaire. 'When did symptoms start?' 'Three days ago.'",
                "在挂号处出示了保险证，填了问诊单。「什么时候开始有症状的」「三天前」。"),
            seg("体温計で測り直すと三十八度一分に上がっていた。待合室で名前を呼ばれるまで三十分ほど待った。",
                "When I remeasured with the thermometer, it had risen to 38.1. I waited about thirty minutes in the waiting room until my name was called.",
                "重新量了一下体温升到三十八度一了。在候诊室等了大约三十分钟才叫到名字。"),
            seg("診察室に入ると、医者が「どうしましたか」と聞いた。咳と鼻水と熱があることを伝えた。",
                "When I entered the examination room, the doctor asked 'What seems to be the problem?' I told him about the cough, runny nose, and fever.",
                "进了诊察室，医生问「怎么了」。我说了咳嗽、流鼻涕和发烧的情况。", True),
            seg("のどを見せて、と言われて口を大きく開けた。「少し赤いですね」と先生が言った。",
                "He told me to show my throat and I opened my mouth wide. 'It's a bit red,' the doctor said.",
                "让我看看喉咙，我张大了嘴。医生说「有点红呢」。"),
            seg("聴診器を胸と背中に当てられた。深く息を吸って、吐いてを繰り返す。",
                "He put the stethoscope on my chest and back. I breathed in deeply and out repeatedly.",
                "听诊器贴在胸口和后背。反复深吸气再呼气。"),
            seg("「風邪でしょう。インフルエンザの検査もしておきましょうか」と提案された。鼻に細い棒を入れる検査だ。少し痛かった。",
                "'It's probably a cold. Shall we test for flu too?' he suggested. It's a test where they put a thin stick in your nose. It hurt a little.",
                "「应该是感冒。也做个流感检查吧」他提议。就是往鼻子里插细棒的那种检查。有点痛。"),
            seg("十五分後、結果は陰性だった。「ただの風邪ですね。薬を三種類出します」と言われた。",
                "Fifteen minutes later, the result was negative. 'It's just a cold. I'll prescribe three types of medicine,' he said.",
                "十五分钟后结果是阴性。「只是感冒。给你开三种药」。", True),
            seg("処方箋を持って隣の薬局に行った。咳止めと、鼻水を抑える薬と、解熱剤をもらった。",
                "I took the prescription to the pharmacy next door. I got cough suppressant, medicine to reduce the runny nose, and fever reducer.",
                "拿着处方去了隔壁药房。拿到了止咳药、止鼻涕的药和退烧药。"),
            seg("薬剤師が「食後に飲んでください。眠くなることがあるので、車の運転は控えてください」と説明してくれた。",
                "The pharmacist explained, 'Take them after meals. They may cause drowsiness, so please refrain from driving.'",
                "药剂师说明「饭后服用。可能会犯困，请不要开车」。"),
            seg("家に帰って薬を飲み、布団に入った。汗をかいたのでパジャマを二回着替えた。",
                "I went home, took the medicine, and got into the futon. I sweated so much I changed pajamas twice.",
                "回家吃了药钻进被窝。出了好多汗，换了两次睡衣。", True),
            seg("夜になって少し楽になった。お粥を作って食べた。味はあまりしなかったが、温かくてほっとした。",
                "By night I felt a bit better. I made porridge and ate it. I couldn't taste much, but it was warm and comforting.",
                "到了晚上稍微轻松了。煮了粥吃。没什么味道，但热乎乎的很安心。"),
            seg("翌朝、熱は三十七度二分まで下がっていた。薬が効いたようだ。",
                "The next morning, my fever had dropped to 37.2. The medicine seemed to be working.",
                "第二天早上体温降到了三十七度二。药好像起效了。"),
            seg("三日間休んで、木曜日から会社に復帰した。マスクをして、同僚になるべく近づかないようにした。",
                "I rested for three days and returned to work on Thursday. I wore a mask and tried not to get too close to colleagues.",
                "休了三天，周四回去上班了。戴着口罩，尽量不靠近同事。"),
            seg("季節の変わり目は体調を崩しやすい。手洗い、うがい、睡眠。基本的なことが一番大切だと改めて思った。",
                "It's easy to get sick at the change of seasons. Hand washing, gargling, sleep. I was reminded that the basics matter most.",
                "换季容易生病。洗手、漱口、睡眠。重新认识到最基本的事情最重要。", True),
        ],
    },

    {
        "id": "n4-clinic-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "内科の受付と診察（患者と医師）",
        "titleJp": "内科の受付と診察（患者と医師）",
        "titleEn": "Reception and examination at the clinic (patient and doctor)",
        "titleZh": "内科挂号和看诊（患者和医生）",
        "titleRuby": [],
        "sections": [
            section("受付", "Reception", "挂号", "🏥", [
                line("A", "すみません、今日は予約してないんですけど、診てもらえますか？",
                     "Excuse me, I don't have an appointment today, but can I be seen?",
                     "不好意思，今天没预约，能看吗？"),
                line("B", "はい、大丈夫ですよ。保険証はお持ちですか？",
                     "Yes, that's fine. Do you have your insurance card?",
                     "可以的。带保险证了吗？"),
                line("A", "あ、はい。あと、問診票ってどこに書けばいいですか？",
                     "Oh, yes. Also, where do I fill out the questionnaire?",
                     "啊，带了。还有，问诊单在哪里填？"),
                line("B", "こちらです。症状と、いつから具合が悪いかを書いてくださいね。体温も測りますので、こちらの体温計をどうぞ。",
                     "Right here. Please write your symptoms and when you started feeling unwell. We'll also take your temperature, so please use this thermometer.",
                     "在这里。请写上症状和什么时候开始不舒服的。也要量体温，用这个体温计。"),
                line("A", "わかりました。……三十八度ある。やっぱり高いな。",
                     "Got it. ...It's 38. As expected, it's high.",
                     "好的。……三十八度。果然挺高的。"),
                line("B", "お名前をお呼びしますので、待合室でお待ちください。三十分くらいかかるかもしれません。",
                     "We'll call your name, so please wait in the waiting room. It might take about thirty minutes.",
                     "叫到名字会通知您，请在候诊室等一下。可能要等三十分钟左右。"),
            ]),
            section("診察室", "Examination room", "诊察室", "🩺", [
                line("B", "どうぞ、お入りください。今日はどうしましたか？",
                     "Please come in. What brings you in today?",
                     "请进。今天怎么了？"),
                line("A", "三日前から咳が止まらなくて、鼻水もひどいんです。昨日から熱も出てきて……。",
                     "I've had a cough that won't stop for three days, and a terrible runny nose. I started getting a fever yesterday too...",
                     "三天前开始咳嗽不停，鼻涕也很严重。从昨天开始还发烧了……"),
                line("B", "なるほど。じゃあ、まずのどを見せてください。はい、口を大きく開けて。……ちょっと赤いですね。",
                     "I see. Then first let me see your throat. Yes, open your mouth wide. ...It's a bit red.",
                     "原来如此。那先看一下喉咙。来，嘴巴张大。……有点红呢。"),
                line("A", "のどが痛いっていうか、イガイガするんですよね。",
                     "It's not so much pain, more like a scratchy feeling.",
                     "与其说喉咙痛，不如说有点刺刺的。"),
                line("B", "胸の音も聞かせてください。はい、大きく息を吸って、ゆっくり吐いて。……もう一回。",
                     "Let me listen to your chest too. Yes, breathe in deeply, breathe out slowly. ...One more time.",
                     "胸部也听一下。来，深吸气，慢慢呼气。……再来一次。"),
                line("A", "インフルエンザだったらどうしよう……。",
                     "What if it's the flu...",
                     "要是流感怎么办……"),
                line("B", "念のため検査しましょうか。鼻に棒を入れるやつなんですけど、ちょっと痛いかもしれません。",
                     "Shall we test just in case? It involves putting a stick in your nose, which might hurt a bit.",
                     "以防万一做个检查吧。就是往鼻子里插棒的那种，可能有点痛。"),
                line("A", "うっ……はい、お願いします。",
                     "Ugh... yes, please.",
                     "呜……好吧，拜托了。"),
            ]),
            section("結果と処方", "Results and prescription", "结果和开药", "💊", [
                line("B", "結果出ましたよ。インフルエンザは陰性です。ただの風邪でしょう。",
                     "The results are in. Flu is negative. It's probably just a cold.",
                     "结果出来了。流感是阴性。应该只是感冒。"),
                line("A", "よかった……。じゃあ薬で治りますかね？",
                     "Thank goodness... So will medicine fix it?",
                     "太好了……那吃药能好吧？"),
                line("B", "ええ。咳止めと鼻水の薬と解熱剤を出しますね。食後に飲んでください。",
                     "Yes. I'll prescribe cough suppressant, nose medicine, and fever reducer. Take them after meals.",
                     "嗯。给你开止咳药、鼻涕的药和退烧药。饭后吃。"),
                line("A", "眠くなったりしますか？仕事でパソコン使うので……。",
                     "Will they make me drowsy? I use a computer for work so...",
                     "会犯困吗？工作要用电脑所以……"),
                line("B", "鼻水の薬は少し眠くなるかもしれません。できれば二、三日は休んだ方がいいですよ。",
                     "The nose medicine might make you a little drowsy. If possible, it's better to rest for two or three days.",
                     "鼻涕的药可能会有点犯困。能的话最好休息两三天。"),
                line("A", "わかりました。水分もたくさん取った方がいいですよね？",
                     "Got it. I should drink lots of fluids too, right?",
                     "知道了。也要多喝水吧？"),
                line("B", "はい、水かスポーツドリンクをこまめに飲んでください。お風呂は熱が下がってからにしてくださいね。お大事に。",
                     "Yes, drink water or sports drinks frequently. Wait until your fever goes down before bathing. Take care.",
                     "是的，勤喝水或运动饮料。等退烧了再泡澡。请保重。"),
                line("A", "ありがとうございます。……あ、処方箋はどこに持っていけばいいですか？",
                     "Thank you. ...Oh, where do I take the prescription?",
                     "谢谢。……啊，处方拿到哪里？"),
                line("B", "隣に薬局がありますので、そちらでどうぞ。",
                     "There's a pharmacy next door, please go there.",
                     "隔壁有药房，去那里就好。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 2. n4-pharmacy 药店买药
    # ═══════════════════════════════════════════
    {
        "id": "n4-pharmacy-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "ドラッグストアで薬を選ぶ",
        "titleJp": "ドラッグストアで薬を選ぶ",
        "titleEn": "Choosing medicine at a drugstore",
        "titleZh": "在药妆店选药",
        "titleRuby": [],
        "segments": [
            seg("日曜日の朝、のどに違和感があった。唾を飲み込むと少し痛い。熱はないが、放っておくと悪くなりそうだ。",
                "Sunday morning, my throat felt off. It hurt a little when I swallowed. No fever, but I felt it would get worse if I left it.",
                "周日早上嗓子不太对劲。咽口水有点痛。虽然不发烧，但感觉不管的话会恶化。", True),
            seg("病院は日曜日で休みだから、近くのドラッグストアに行くことにした。",
                "The hospital was closed on Sunday, so I decided to go to the nearby drugstore.",
                "医院周日休息，就去了附近的药妆店。"),
            seg("店に入ると、棚にたくさんの薬が並んでいた。風邪薬だけで十種類以上ある。どれを選べばいいか分からない。",
                "When I entered the store, many medicines were lined up on the shelves. There were over ten kinds of cold medicine alone. I didn't know which to choose.",
                "进了店，架子上摆满了药。光感冒药就有十几种。不知道选哪个。", True),
            seg("パッケージを見ると、「のどの痛みに」「鼻水に」「咳に」「熱に」と書いてある。",
                "Looking at the packages, they read 'for sore throat,' 'for runny nose,' 'for cough,' 'for fever.'",
                "看包装上写着「缓解咽喉痛」「止鼻涕」「止咳」「退烧」。"),
            seg("のどが痛いだけなので、総合感冒薬ではなく、のど専用のトローチを探した。",
                "Since it was only a sore throat, I looked for throat-specific lozenges rather than a general cold medicine.",
                "只是嗓子痛，所以不找综合感冒药，而是找嗓子专用的含片。"),
            seg("迷っていると、白衣を着た薬剤師が「何かお探しですか」と声をかけてくれた。",
                "While I was hesitating, a pharmacist in a white coat asked 'Can I help you find something?'",
                "正犹豫的时候穿白大褂的药剂师问「在找什么吗」。", True),
            seg("症状を説明すると、「この薬がいいですよ。一日三回、食後に飲んでください」と勧めてくれた。",
                "When I explained my symptoms, she recommended, 'This medicine is good. Take it three times a day after meals.'",
                "说明了症状后推荐「这个药不错。一天三次饭后吃」。"),
            seg("「お酒と一緒に飲んでも大丈夫ですか」と聞いたら、「薬を飲んでいる間はお酒は控えてください」と言われた。",
                "When I asked 'Is it OK to take with alcohol?', she said 'Please refrain from alcohol while taking medicine.'",
                "问了「能和酒一起喝吗」，被告知「吃药期间请不要喝酒」。"),
            seg("薬のほかに、柔らかいティッシュとマスクとのど飴も買った。レジで千二百円。思ったより安かった。",
                "Besides medicine, I also bought soft tissues, masks, and throat drops. 1,200 yen at the register. Cheaper than I expected.",
                "除了药还买了软纸巾、口罩和润喉糖。收银台一千二百日元。比想象中便宜。", True),
            seg("家に帰って、説明書をよく読んでから薬を飲んだ。「副作用として眠気が出ることがあります」と書いてある。",
                "I went home, read the instructions carefully, and then took the medicine. It says 'drowsiness may occur as a side effect.'",
                "回家仔细看了说明书再吃药。上面写着「副作用可能出现嗜睡」。"),
            seg("温かいお湯にはちみつを入れて飲んだ。のどがじんわり楽になる。",
                "I drank hot water with honey. My throat gradually felt more comfortable.",
                "喝了加蜂蜜的热水。嗓子慢慢舒服了。"),
            seg("午後はずっと寝ていた。夕方起きると、のどの痛みが半分くらいに減っていた。",
                "I slept all afternoon. When I woke up in the evening, the throat pain had decreased by about half.",
                "下午一直在睡。傍晚醒来嗓子痛减了一半左右。"),
            seg("市販薬で治る程度なら、わざわざ病院に行かなくてもいい。ただ、二日経っても良くならなければ、必ず医者に行こうと決めた。",
                "If it's something over-the-counter medicine can fix, you don't have to bother going to the hospital. But I decided that if it doesn't improve in two days, I'll definitely see a doctor.",
                "如果非处方药能治好的程度就不用特意去医院。不过我决定如果两天还没好就一定去看医生。", True),
            seg("ドラッグストアは二十四時間やっている店もあるし、病院が閉まっている時間帯にはとても頼りになる存在だ。",
                "Some drugstores are open 24 hours, and they're very reliable during times when hospitals are closed.",
                "有些药妆店二十四小时营业，在医院关门的时段非常靠谱。"),
        ],
    },

    {
        "id": "n4-pharmacy-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "ドラッグストアで薬剤師に相談する",
        "titleJp": "ドラッグストアで薬剤師に相談する",
        "titleEn": "Consulting a pharmacist at the drugstore",
        "titleZh": "在药妆店咨询药剂师",
        "titleRuby": [],
        "sections": [
            section("症状を伝える", "Describing symptoms", "说明症状", "💊", [
                line("A", "すみません、風邪っぽいんですけど、薬を探してて……。",
                     "Excuse me, I think I have a cold, and I'm looking for medicine...",
                     "不好意思，好像感冒了，在找药……"),
                line("B", "どんな症状ですか？熱はありますか？",
                     "What are your symptoms? Do you have a fever?",
                     "什么症状？发烧了吗？"),
                line("A", "熱はなくて、のどが痛いのと、鼻水がちょっと。咳はまだ出てないです。",
                     "No fever, just a sore throat and a bit of a runny nose. No cough yet.",
                     "没发烧，就是嗓子痛、有点鼻涕。还没咳。"),
                line("B", "いつからですか？",
                     "Since when?",
                     "从什么时候开始的？"),
                line("A", "昨日の夜からですね。朝起きたらもっとひどくなってて。",
                     "Since last night. When I woke up this morning it was worse.",
                     "从昨天晚上。早上起来更厉害了。"),
                line("B", "なるほど。アレルギーはありますか？何か飲んでる薬とかは？",
                     "I see. Do you have any allergies? Are you taking any other medicine?",
                     "明白了。有过敏吗？在吃其他药吗？"),
                line("A", "アレルギーはないです。薬も飲んでないですね。",
                     "No allergies. Not taking any medicine either.",
                     "没有过敏。也没在吃别的药。"),
            ]),
            section("薬を選ぶ", "Choosing the medicine", "选药", "🔍", [
                line("B", "じゃあ、こちらがおすすめです。のどの炎症を抑える成分が入ってて、鼻水にも効きますよ。",
                     "Then I recommend this one. It contains an ingredient that reduces throat inflammation and also works for runny nose.",
                     "那推荐这个。里面有消炎成分，鼻涕也管用。"),
                line("A", "錠剤と液体タイプがあるんですね。どっちがいいですか？",
                     "There's a tablet and a liquid type. Which is better?",
                     "有药片和液体两种啊。哪个好？"),
                line("B", "効き目は同じです。液体の方が飲みやすいって言う方もいますけど、好みですね。",
                     "The effect is the same. Some people say the liquid is easier to take, but it's a matter of preference.",
                     "效果一样。有人觉得液体容易喝，不过看个人喜好。"),
                line("A", "じゃあ錠剤で。……あ、これ飲むと眠くなったりします？",
                     "Then I'll go with tablets. ...Oh, will this make me sleepy?",
                     "那要药片的。……对了，吃了会犯困吗？"),
                line("B", "鼻水を抑える成分で少し眠くなることがありますね。車の運転とかは気をつけてください。",
                     "The ingredient for the runny nose might make you a bit drowsy. Please be careful with things like driving.",
                     "止鼻涕的成分可能会有点犯困。开车什么的要注意。"),
                line("A", "あー、明日仕事なんだけどな……。眠くならないやつってありますか？",
                     "Ah, I have work tomorrow though... Is there a type that won't make me sleepy?",
                     "啊，明天还要上班呢……有不犯困的吗？"),
                line("B", "ありますよ。こっちは眠くなりにくいタイプです。ただ、少し値段が高めです。",
                     "Yes, there is. This one is a less-drowsy type. But it's a bit more expensive.",
                     "有的。这个是不太犯困的类型。不过价格稍微贵一点。"),
                line("A", "全然いいです、それにします。あとマスクものど飴も買っとこう。",
                     "That's totally fine, I'll take that. I should also grab masks and throat drops.",
                     "完全没问题，就那个了。再买点口罩和润喉糖吧。"),
            ]),
            section("レジで", "At the register", "收银台", "🧾", [
                line("B", "全部で千五百八十円になります。",
                     "The total is 1,580 yen.",
                     "一共一千五百八十日元。"),
                line("A", "カードで払えますか？",
                     "Can I pay by card?",
                     "能刷卡吗？"),
                line("B", "はい、大丈夫ですよ。……はい、お大事にしてくださいね。",
                     "Yes, that's fine. ...Here you go, please take care of yourself.",
                     "可以的。……好了，请保重。"),
                line("A", "ありがとうございます。早く治さないと。",
                     "Thank you. I need to get better quickly.",
                     "谢谢。得赶紧好起来。"),
            ]),
        ],
    },

    # ═══════════════════════════════════════════
    # 3. n4-dental 洗牙
    # ═══════════════════════════════════════════
    {
        "id": "n4-dental-essay",
        "level": "N4–N3",
        "format": "essay",
        "titleWord": "半年ぶりの歯医者",
        "titleJp": "半年ぶりの歯医者",
        "titleEn": "Going to the dentist for the first time in six months",
        "titleZh": "时隔半年去牙医",
        "titleRuby": [],
        "segments": [
            seg("「半年に一回は来てくださいね」と前回言われたのに、気づけば八ヶ月経っていた。",
                "'Please come once every six months,' they told me last time, but before I knew it, eight months had passed.",
                "上次说好「半年来一次」，一回头已经过了八个月。", True),
            seg("予約の電話をかけた。「来週の水曜日、十時からで大丈夫ですか」「はい、お願いします」。",
                "I called to make an appointment. 'Is next Wednesday at ten OK?' 'Yes, please.'",
                "打电话预约。「下周三十点可以吗」「好的，麻烦了」。"),
            seg("当日、歯科クリニックに着くと受付で名前を言い、待合室の椅子に座った。",
                "On the day, I arrived at the dental clinic, gave my name at reception, and sat in the waiting room chair.",
                "当天到了牙科诊所在挂号处报了名字，坐在候诊室的椅子上。"),
            seg("名前を呼ばれて診察台に横になった。口を開けて、と言われて大きく開ける。",
                "My name was called and I lay on the examination chair. 'Open your mouth,' they said, and I opened wide.",
                "叫到名字躺到诊疗台上。让我张嘴，张大。", True),
            seg("衛生士がミラーで歯を一本ずつ確認していく。「上の奥歯に少し歯石がありますね」と言われた。",
                "The hygienist checked each tooth with a mirror. 'There's a bit of tartar on your upper back teeth,' she said.",
                "卫生士用镜子一颗颗检查牙齿。「上面的后牙有点牙石」。"),
            seg("歯石を取る器具の音がキーンと響く。痛くはないが、振動が気になる。",
                "The sound of the tartar-removing instrument resonated with a high-pitched whine. It doesn't hurt but the vibration bothers me.",
                "去牙石的器具嗞嗞地响。不痛但振动有点难受。"),
            seg("「お水出しますね」と言われ、口をゆすぐ。ピンク色の水が出てきて少し驚いた。",
                "'I'll rinse now,' she said, and I rinsed my mouth. Pink water came out, which surprised me a little.",
                "说「冲一下水」让我漱口。吐出来的水是粉红色的，吓了一跳。"),
            seg("次に歯の表面を磨いてもらった。ミントの味がするペーストで、回転するブラシが当たるとくすぐったい。",
                "Next they polished my tooth surfaces. With a mint-flavored paste, the rotating brush tickled when it touched.",
                "然后磨了牙齿表面。薄荷味的膏体，旋转的刷头碰到牙齿痒痒的。", True),
            seg("最後にフッ素を塗ってもらった。「三十分は食べたり飲んだりしないでくださいね」と説明された。",
                "Finally they applied fluoride. 'Please don't eat or drink for thirty minutes,' they explained.",
                "最后涂了氟。嘱咐说「三十分钟内不要吃东西喝东西」。"),
            seg("先生が最後にチェックしに来た。「虫歯はないですね。でも左下の親知らずが少し気になりますね」。",
                "The dentist came for a final check. 'No cavities. But your lower-left wisdom tooth is a bit concerning.'",
                "医生最后来检查了一下。「没有蛀牙。不过左下的智齿有点让人在意」。"),
            seg("「痛くなったらまた来てください。それまでは様子を見ましょう」と言われ、少し安心した。",
                "'Come back if it starts to hurt. Until then let's monitor it,' he said, and I felt a bit relieved.",
                "「痛了再来。到那时候先观察」他说，稍微放心了一点。"),
            seg("受付で三千円を払い、次の予約を半年後に入れた。今度こそ忘れないようにスマホのカレンダーに入れた。",
                "I paid 3,000 yen at reception and booked my next appointment for six months later. This time I put it in my phone calendar so I won't forget.",
                "在挂号处付了三千日元，下次预约了半年后。这次为了不忘记写进了手机日历。", True),
            seg("歯医者は行くまでが面倒だが、終わると毎回「もっと早く来ればよかった」と思う。",
                "Getting to the dentist is the hassle, but after it's done I always think 'I should have come sooner.'",
                "去牙医之前总觉得麻烦，但每次结束都想「早该来的」。"),
            seg("ツルツルになった歯を舌で触る。この気持ちよさを忘れないうちに、次もちゃんと来よう。",
                "I run my tongue over my smooth teeth. While I still remember this nice feeling, I'll make sure to come next time too.",
                "用舌头舔舔变光滑的牙齿。趁还记得这种舒服感，下次也好好来。"),
        ],
    },

    {
        "id": "n4-dental-dialogue",
        "level": "N4–N3",
        "format": "dialogue",
        "titleWord": "歯のクリーニング（患者と衛生士）",
        "titleJp": "歯のクリーニング（患者と衛生士）",
        "titleEn": "Dental cleaning (patient and hygienist)",
        "titleZh": "洗牙（患者和卫生士）",
        "titleRuby": [],
        "sections": [
            section("確認", "Checking", "检查", "🦷", [
                line("B", "お久しぶりですね。前回から……八ヶ月くらい空いてますね。",
                     "It's been a while. Since last time... about eight months, right?",
                     "好久不见。距离上次……大概八个月了吧。"),
                line("A", "はい、すみません。忙しくて、つい……。",
                     "Yes, sorry. I was busy and just...",
                     "是的，不好意思。一忙就……"),
                line("B", "よくあることですよ。じゃあ、まず歯全体を見ますね。口を大きく開けてください。",
                     "It happens a lot. Well, let me check all your teeth first. Please open your mouth wide.",
                     "常有的事。那先看一下所有牙齿。请嘴巴张大。"),
                line("A", "あー。",
                     "Ahh.",
                     "啊——"),
                line("B", "上の奥歯に歯石がちょっと溜まってますね。あと、歯茎が少し腫れてるところがあります。",
                     "There's a bit of tartar buildup on your upper back teeth. Also, there's a spot where your gums are slightly swollen.",
                     "上面后牙有点牙石了。另外牙龈有个地方稍微肿了。"),
                line("A", "えっ、大丈夫ですか……？",
                     "Eh, is that OK...?",
                     "诶，没事吧……？"),
                line("B", "今日のクリーニングで良くなると思いますよ。歯磨きの仕方もあとで見直しましょうね。",
                     "I think it'll improve with today's cleaning. Let's also review your brushing technique afterwards.",
                     "今天洗完应该会好。之后再看看刷牙方法吧。"),
            ]),
            section("クリーニング中", "During cleaning", "洗牙过程中", "🪥", [
                line("B", "じゃあ歯石を取っていきますね。振動しますけど、痛かったら手を上げてください。",
                     "OK, I'll start removing the tartar. It'll vibrate, but raise your hand if it hurts.",
                     "那开始去牙石了。会有振动，痛的话举手告诉我。"),
                line("A", "（うなずく）",
                     "(nods)",
                     "（点头）"),
                line("B", "……はい、お水出しますね。ゆすいでください。",
                     "...OK, I'll rinse. Please spit.",
                     "……好，冲一下水。请漱口。"),
                line("A", "うわ、ピンクだ……。血が出てるんですか？",
                     "Whoa, it's pink... Am I bleeding?",
                     "哇，粉红色的……出血了吗？"),
                line("B", "歯茎が少し弱ってるところから出ちゃうんですよね。歯石を取ったら落ち着きますから、心配しないでくださいね。",
                     "It bleeds from where the gums are a bit weak. It'll settle down once the tartar is removed, so don't worry.",
                     "牙龈弱的地方会出一点。去了牙石就好了，别担心。"),
                line("A", "はい……。けっこう溜まってました？",
                     "OK... Was there a lot built up?",
                     "好……积了很多吗？"),
                line("B", "八ヶ月にしてはまあまあですね。半年に一回来てもらえると、もっと楽ですよ。",
                     "For eight months, it's about average. If you come every six months, it's much easier.",
                     "相对八个月来说还算一般。半年来一次的话会轻松很多。"),
            ]),
            section("仕上げとアドバイス", "Finishing and advice", "收尾和建议", "✨", [
                line("B", "最後にフッ素を塗りますね。ちょっと苦いかもしれないけど、我慢してくださいね。",
                     "I'll apply fluoride last. It might taste a bit bitter, but please bear with it.",
                     "最后涂氟。可能有点苦，忍一下哦。"),
                line("A", "んー……うん、大丈夫です。",
                     "Mmm... yeah, I'm OK.",
                     "嗯——……嗯没事。"),
                line("B", "はい、おつかれさまでした。三十分は飲食しないでくださいね。あと、奥歯の裏側、もうちょっと丁寧に磨いた方がいいですよ。",
                     "OK, great job. Please don't eat or drink for thirty minutes. Also, you should brush the back side of your rear teeth a bit more carefully.",
                     "好了辛苦了。三十分钟不要吃喝。还有后牙的内侧再刷仔细一点会更好。"),
                line("A", "やっぱりそこが弱いんですね……。電動歯ブラシとかの方がいいですかね？",
                     "I knew that was the weak spot... Would an electric toothbrush be better?",
                     "果然那里不行啊……用电动牙刷会不会好一些？"),
                line("B", "手で磨くのでも全然大丈夫ですよ。小さく動かすのがコツです。あとフロスもやってみてくださいね。",
                     "Manual brushing is totally fine. The trick is to move in small strokes. Also try using floss.",
                     "手动刷完全没问题的。诀窍是小幅度动。另外也用用牙线吧。"),
                line("A", "フロス、いっつも忘れちゃうんですよね……。今日から頑張ります。",
                     "I always forget to floss... I'll try from today.",
                     "牙线老是忘……从今天开始努力。"),
                line("B", "じゃあ、次は半年後ですね。忘れないでくださいね！",
                     "Then next time is in six months. Don't forget!",
                     "那下次半年后。别忘了！"),
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
