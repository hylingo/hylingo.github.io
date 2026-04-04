#!/usr/bin/env python3
"""为 sentences.json 中每条句子自动标注语法点。

用法：python scripts/add_grammar.py
输出：直接覆写 public/data/sentences.json（加 grammar 字段）
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "data" / "sentences.json"

# ── 语法库 ─────────────────────────────────────────────
# (pattern_regex, display_pattern, level, note_zh, note_en)
# 按优先级排列，长模式优先匹配

GRAMMAR: list[tuple[str, str, str, str, str]] = [
    # ── N1 ──
    (r"ともなると", "〜ともなると", "N1", "一旦到了…的程度/立场", "when it comes to; once you reach the level of"),
    (r"ともなれば", "〜ともなれば", "N1", "一旦到了…的程度/立场", "when it comes to; once you reach the level of"),
    (r"をものともせず", "〜をものともせず", "N1", "不把…当回事，不顾", "without being deterred by"),
    (r"であれ[、]?であれ", "〜であれ〜であれ", "N1", "无论…还是…", "whether … or …"),
    (r"であれ", "〜であれ", "N1", "即使是…", "even if it is"),
    (r"たりとも", "〜たりとも", "N1", "即使一…也（不）", "not even one …"),
    (r"にたえる", "〜に堪える", "N1", "值得…；经得起…", "worthy of; can withstand"),
    (r"にたえない", "〜に堪えない", "N1", "不值得…；无法忍受", "not worthy of; cannot bear"),
    (r"に堪える", "〜に堪える", "N1", "值得…；经得起…", "worthy of; can withstand"),
    (r"に堪えない", "〜に堪えない", "N1", "不值得…；无法忍受", "not worthy of; cannot bear"),
    (r"をよそに", "〜をよそに", "N1", "不顾…", "ignoring; despite"),
    (r"を皮切りに", "〜を皮切りに", "N1", "以…为开端", "starting with"),
    (r"を禁じ得ない", "〜を禁じ得ない", "N1", "禁不住…；不由得…", "cannot help but"),
    (r"極まりない", "〜極まりない", "N1", "极其…；…到了极点", "extremely"),
    (r"きわまりない", "〜極まりない", "N1", "极其…；…到了极点", "extremely"),
    (r"ずにはおかない", "〜ずにはおかない", "N1", "不…不行；必定会…", "cannot help but; inevitably"),
    (r"ないではおかない", "〜ないではおかない", "N1", "不…不行；必定会…", "cannot help but; inevitably"),
    (r"までもない", "〜までもない", "N1", "用不着…；不必…", "there is no need to"),
    (r"まじき", "〜まじき", "N1", "不应该…的", "should not; unbecoming of"),
    (r"べからず", "〜べからず", "N1", "不可…；禁止…", "must not; shall not"),
    (r"べからざる", "〜べからざる", "N1", "不可缺少的；不可…的", "indispensable; must not"),
    (r"んがため", "〜んがため", "N1", "为了…", "in order to (literary)"),
    (r"んばかり", "〜んばかり", "N1", "几乎要…的样子", "as if about to"),
    (r"といったらありはしない", "〜といったらありはしない", "N1", "…得不得了", "incredibly; extremely"),
    (r"といったらない", "〜といったらない", "N1", "…得不得了", "incredibly; extremely"),
    (r"とあれば", "〜とあれば", "N1", "如果是…的话（就）", "if it is the case that"),
    (r"ようが[、]?ようが", "〜ようが〜ようが", "N1", "无论…还是…", "whether … or …"),
    (r"ようが", "〜ようが", "N1", "无论怎么…也", "no matter how"),
    (r"ようと", "〜ようと", "N1", "无论怎么…也", "no matter how"),
    (r"がてら", "〜がてら", "N1", "顺便…", "while; on the occasion of"),
    (r"かたがた", "〜かたがた", "N1", "顺便…", "while; on the occasion of"),
    (r"が最後", "〜が最後", "N1", "一旦…就（不可挽回）", "once … there's no going back"),
    (r"たが最後", "〜たが最後", "N1", "一旦…就（不可挽回）", "once … there's no going back"),
    (r"からある", "〜からある", "N1", "多达…；足有…", "as much/many as"),
    (r"(?<!いき)(?<!つま)(?<!な)なり[^ま]", "〜なり", "N1", "一…就…", "as soon as"),
    (r"ただ[^い].*のみ", "ただ〜のみ", "N1", "只有…；仅仅…", "only; merely"),

    # ── N2 ──
    (r"ことなしに", "〜ことなしに", "N2", "不…就…", "without doing"),
    (r"にほかならない", "〜にほかならない", "N2", "正是…；无非是…", "nothing but; precisely"),
    (r"に他ならない", "〜に他ならない", "N2", "正是…；无非是…", "nothing but; precisely"),
    (r"ずにはいられない", "〜ずにはいられない", "N2", "不由得…；忍不住…", "cannot help but"),
    (r"ないではいられない", "〜ないではいられない", "N2", "不由得…；忍不住…", "cannot help but"),
    (r"わけにはいかない", "〜わけにはいかない", "N2", "不能…；不可以…", "cannot; must not"),
    (r"わけがない", "〜わけがない", "N2", "不可能…", "there is no way that"),
    (r"というものではない", "〜というものではない", "N2", "并非…", "it's not that; not necessarily"),
    (r"というものだ", "〜というものだ", "N2", "这才叫…；就是这么回事", "that's what … is"),
    (r"ということだ", "〜ということだ", "N2", "据说…；也就是说…", "it means that; I heard that"),
    (r"というわけではない", "〜というわけではない", "N2", "并不是说…", "it doesn't mean that"),
    (r"といっても", "〜といっても", "N2", "虽说…但其实…", "although I say …, actually"),
    (r"とは限らない", "〜とは限らない", "N2", "未必…；不一定…", "not necessarily"),
    (r"に限らず", "〜に限らず", "N2", "不限于…；不仅…", "not limited to"),
    (r"に限って", "〜に限って", "N2", "偏偏…", "it's always …; when it comes to"),
    (r"にかけては", "〜にかけては", "N2", "在…方面（很擅长）", "when it comes to (strong at)"),
    (r"にわたって", "〜にわたって", "N2", "历经…；遍及…", "over; spanning"),
    (r"にわたり", "〜にわたり", "N2", "历经…；遍及…", "over; spanning"),
    (r"にかかわらず", "〜にかかわらず", "N2", "不管…；无论…", "regardless of"),
    (r"にかかわる", "〜にかかわる", "N2", "关系到…；涉及…", "relating to; concerning"),
    (r"に関わらず", "〜に関わらず", "N2", "不管…；无论…", "regardless of"),
    (r"を問わず", "〜を問わず", "N2", "不论…；不管…", "regardless of"),
    (r"にしたがって", "〜にしたがって", "N2", "随着…", "as; in accordance with"),
    (r"に従って", "〜に従って", "N2", "随着…", "as; in accordance with"),
    (r"につれて", "〜につれて", "N2", "随着…", "as … changes"),
    (r"に伴って", "〜に伴って", "N2", "伴随着…", "along with; as"),
    (r"にともなって", "〜に伴って", "N2", "伴随着…", "along with; as"),
    (r"に基づいて", "〜に基づいて", "N2", "基于…；根据…", "based on"),
    (r"にもとづいて", "〜に基づいて", "N2", "基于…；根据…", "based on"),
    (r"に応じて", "〜に応じて", "N2", "根据…；按照…", "according to; depending on"),
    (r"において", "〜において", "N2", "在…（场所/场合）", "in; at (formal)"),
    (r"における", "〜における", "N2", "在…的（场所/场合）", "in; at (formal, attributive)"),
    (r"にとって", "〜にとって", "N2", "对…来说", "for; to (someone)"),
    (r"に対して", "〜に対して", "N2", "对…；针对…", "toward; against; in contrast to"),
    (r"にたいして", "〜に対して", "N2", "对…；针对…", "toward; against; in contrast to"),
    (r"に関して", "〜に関して", "N2", "关于…", "regarding; concerning"),
    (r"にかんして", "〜に関して", "N2", "关于…", "regarding; concerning"),
    (r"に沿って", "〜に沿って", "N2", "沿着…；按照…", "along; in line with"),
    (r"にそって", "〜に沿って", "N2", "沿着…；按照…", "along; in line with"),
    (r"に先立って", "〜に先立って", "N2", "在…之前", "prior to; before"),
    (r"に先立ち", "〜に先立ち", "N2", "在…之前", "prior to; before"),
    (r"をはじめ", "〜をはじめ", "N2", "以…为首；…等", "starting with; including"),
    (r"をきっかけに", "〜をきっかけに", "N2", "以…为契机", "triggered by; prompted by"),
    (r"を通じて", "〜を通じて", "N2", "通过…；贯穿…", "through; throughout"),
    (r"を通して", "〜を通して", "N2", "通过…；贯穿…", "through; throughout"),
    (r"をもとに", "〜をもとに", "N2", "以…为基础", "based on"),
    (r"を元に", "〜を元に", "N2", "以…为基础", "based on"),
    (r"を中心に", "〜を中心に", "N2", "以…为中心", "centered on"),
    (r"上で", "〜上で", "N2", "在…之后；在…方面", "after; in terms of"),
    (r"一方で", "〜一方で", "N2", "另一方面", "on the other hand; while"),
    (r"一方だ", "〜一方だ", "N2", "一直…；越来越…", "keeps …-ing"),
    (r"おかげで", "〜おかげで", "N2", "多亏了…", "thanks to"),
    (r"おかげさまで", "おかげさまで", "N2", "托您的福", "thanks to you"),
    (r"せいで", "〜せいで", "N2", "因为…（负面原因）", "because of (negative)"),
    (r"せいか", "〜せいか", "N2", "也许是因为…", "perhaps because of"),
    (r"からこそ", "〜からこそ", "N2", "正因为…才…", "precisely because"),
    (r"からといって", "〜からといって", "N2", "虽说…但不能因此…", "just because … doesn't mean"),
    (r"からには", "〜からには", "N2", "既然…就…", "since; now that"),
    (r"以上は", "〜以上は", "N2", "既然…就…", "since; now that"),
    (r"以上[、]", "〜以上（は）", "N2", "既然…就…", "since; now that"),
    (r"次第で", "〜次第で", "N2", "取决于…", "depending on"),
    (r"次第だ", "〜次第だ", "N2", "取决于…", "depending on"),
    (r"しだいで", "〜次第で", "N2", "取决于…", "depending on"),
    (r"たところ", "〜たところ", "N2", "…之后（发现）", "upon doing; when I did"),
    (r"たとたん", "〜たとたん", "N2", "刚一…就…", "the moment; as soon as"),
    (r"た途端", "〜たとたん", "N2", "刚一…就…", "the moment; as soon as"),
    (r"ばかりに", "〜ばかりに", "N2", "就因为…（才导致坏结果）", "just because (with bad result)"),
    (r"ばかりか", "〜ばかりか", "N2", "不仅…而且…", "not only … but also"),
    (r"ばかりでなく", "〜ばかりでなく", "N2", "不仅…而且…", "not only … but also"),
    (r"どころか", "〜どころか", "N2", "别说…；岂止…", "far from; let alone"),
    (r"どころではない", "〜どころではない", "N2", "哪有心思…；不是…的时候", "this is no time for"),
    (r"ものなら", "〜ものなら", "N2", "如果能…的话；要是…", "if one could; if you dare"),
    (r"ものだから", "〜ものだから", "N2", "因为…（辩解语气）", "because (excuse/reason)"),
    (r"もんだから", "〜もんだから", "N2", "因为…（辩解，口语）", "because (excuse, casual)"),
    (r"ものの", "〜ものの", "N2", "虽然…但是…", "although; even though"),
    (r"ものがある", "〜ものがある", "N2", "确实有…之处", "there is indeed something"),
    (r"ものだ", "〜ものだ", "N2", "就应该…；真是…啊", "should; how …; used to"),
    (r"もので", "〜もので", "N2", "因为…", "because"),
    (r"こそ", "〜こそ", "N2", "正是…；才是…", "precisely; it is … that"),
    (r"さえ.*ば", "〜さえ〜ば", "N2", "只要…就…", "as long as; if only"),
    (r"さえ", "〜さえ", "N2", "甚至…；连…都…", "even"),
    (r"すら", "〜すら", "N2", "甚至…；连…都…", "even (literary)"),
    (r"っぽい", "〜っぽい", "N2", "有…的倾向；像…似的", "-ish; tending to"),
    (r"がち", "〜がち", "N2", "容易…；往往…", "tend to; apt to"),
    (r"気味", "〜気味", "N2", "有点…；略微…", "slightly; a touch of"),
    (r"ぎみ", "〜気味", "N2", "有点…；略微…", "slightly; a touch of"),
    (r"向け", "〜向け", "N2", "面向…的；给…用的", "aimed at; for"),
    (r"最中", "〜最中", "N2", "正在…的时候", "in the middle of"),
    (r"さいちゅう", "〜最中", "N2", "正在…的时候", "in the middle of"),
    (r"反面", "〜反面", "N2", "另一方面", "on the other hand"),
    (r"はんめん", "〜反面", "N2", "另一方面", "on the other hand"),
    (r"とともに", "〜とともに", "N2", "和…一起；随着…", "together with; as"),
    (r"にしても", "〜にしても", "N2", "即使…也…", "even if; even though"),
    (r"にしろ", "〜にしろ", "N2", "即使…也…", "even if"),
    (r"にせよ", "〜にせよ", "N2", "即使…也…", "even if"),
    (r"としたら", "〜としたら", "N2", "如果…的话", "if; supposing"),
    (r"とすれば", "〜とすれば", "N2", "如果…的话", "if; supposing"),
    (r"としては", "〜としては", "N2", "作为…来说", "as; for"),
    (r"として", "〜として", "N2", "作为…", "as; in the capacity of"),
    (r"くせに", "〜くせに", "N2", "明明…却…", "even though; despite"),
    (r"つつある", "〜つつある", "N2", "正在…（逐渐变化中）", "in the process of; -ing"),
    (r"つつ[もは、]", "〜つつも", "N2", "虽然…却…", "while; although"),
    (r"得る", "〜得る", "N2", "能…；可能…", "can; possible to"),
    (r"うる", "〜得る", "N2", "能…；可能…", "can; possible to"),
    (r"かねる", "〜かねる", "N2", "难以…；不便…", "hard to; unable to"),
    (r"かねない", "〜かねない", "N2", "有可能…（负面）", "might; could (negative)"),

    # ── N3 ──
    (r"ようにする", "〜ようにする", "N3", "尽量做到…", "try to; make sure to"),
    (r"ようになる", "〜ようになる", "N3", "变得能…了", "come to; become able to"),
    (r"ようにしている", "〜ようにしている", "N3", "一直注意做…", "make it a habit to"),
    (r"ことにする", "〜ことにする", "N3", "决定…", "decide to"),
    (r"ことになる", "〜ことになる", "N3", "结果变成…", "it turns out that; it's been decided"),
    (r"ことにしている", "〜ことにしている", "N3", "习惯…；一直坚持…", "make it a rule to"),
    (r"ことがある", "〜ことがある", "N3", "有时会…", "sometimes; there are times when"),
    (r"ことができる", "〜ことができる", "N3", "能…；可以…", "can; be able to"),
    (r"ことはない", "〜ことはない", "N3", "不必…；没必要…", "there is no need to"),
    (r"ということ", "〜ということ", "N3", "就是说…", "that; the fact that"),
    (r"ように言[わっ]", "〜ように言う", "N3", "让…做…", "tell someone to"),
    (r"ために", "〜ために", "N3", "为了…；因为…", "in order to; because of"),
    (r"ないで", "〜ないで", "N3", "不做…就…", "without doing"),
    (r"ずに", "〜ずに", "N3", "不做…就…", "without doing"),
    (r"てしまう", "〜てしまう", "N3", "完成…；不小心…了", "end up doing; completely"),
    (r"ちゃった", "〜てしまった", "N3", "不小心…了（口语）", "ended up doing (casual)"),
    (r"ちゃう", "〜てしまう", "N3", "（口语）完成/不小心…", "end up doing (casual)"),
    (r"じゃった", "〜でしまった", "N3", "不小心…了（口语）", "ended up doing (casual)"),
    (r"じゃう", "〜でしまう", "N3", "（口语）完成/不小心…", "end up doing (casual)"),
    (r"はずだ", "〜はずだ", "N3", "应该…；理应…", "should be; is expected to"),
    (r"はず[がで]", "〜はずだ", "N3", "应该…；理应…", "should be; is expected to"),
    (r"わけだ", "〜わけだ", "N3", "当然…；怪不得…", "no wonder; that's why"),
    (r"わけではない", "〜わけではない", "N3", "并不是…", "it doesn't mean that"),
    (r"てほしい", "〜てほしい", "N3", "希望（别人）做…", "want someone to"),
    (r"てもらう", "〜てもらう", "N3", "请（别人）做…", "have someone do"),
    (r"てくれる", "〜てくれる", "N3", "（别人）为我做…", "someone does … for me"),
    (r"てあげる", "〜てあげる", "N3", "为（别人）做…", "do … for someone"),
    (r"てみる", "〜てみる", "N3", "试着做…", "try doing"),
    (r"ておく", "〜ておく", "N3", "事先做好…", "do in advance"),
    (r"とく[よね。]", "〜とく", "N3", "事先做好…（口语）", "do in advance (casual)"),
    (r"ていく", "〜ていく", "N3", "…下去（持续变化）", "continue to; go on"),
    (r"てくる", "〜てくる", "N3", "…起来；变得…", "come to; start to"),
    (r"てある", "〜てある", "N3", "（已经）…好了", "has been done (resulting state)"),
    (r"てばかり", "〜てばかり", "N3", "总是…；光…", "always doing; nothing but"),
    (r"ばかり", "〜ばかり", "N3", "净…；光…", "nothing but; only"),
    (r"ところだ", "〜ところだ", "N3", "正要…/正在…/刚刚…", "about to / in the middle of / just did"),
    (r"ところだった", "〜ところだった", "N3", "差点就…了", "almost; nearly"),
    (r"ようとする", "〜ようとする", "N3", "想要…；正要…", "try to; be about to"),
    (r"ようとしない", "〜ようとしない", "N3", "怎么也不肯…", "refuse to; won't try to"),
    (r"ようがない", "〜ようがない", "N3", "没办法…", "there's no way to"),
    (r"ようもない", "〜ようもない", "N3", "没办法…", "there's no way to"),
    (r"らしい", "〜らしい", "N3", "好像…；像…样的", "seems; -like"),
    (r"みたい", "〜みたい", "N3", "好像…；像…", "looks like; seems"),
    (r"っけ", "〜っけ", "N3", "…来着？（回忆确认）", "wasn't it…? (trying to recall)"),
    (r"て(い|)る間に", "〜ている間に", "N3", "在…的期间", "while"),
    (r"間に", "〜間に", "N3", "在…期间（做了某事）", "while; during"),
    (r"うちに", "〜うちに", "N3", "趁着…", "while; before it's too late"),
    (r"たびに", "〜たびに", "N3", "每次…都…", "every time"),
    (r"度に", "〜たびに", "N3", "每次…都…", "every time"),
    (r"かどうか", "〜かどうか", "N3", "是否…", "whether or not"),
    (r"って[いゆ]う", "〜という", "N3", "叫做…；所谓…", "called; so-called"),
    (r"という", "〜という", "N3", "叫做…；所谓…", "called; so-called"),
    (r"ように", "〜ように", "N3", "为了…；像…一样", "so that; like"),
    (r"ような", "〜ような", "N3", "像…一样的", "like; such as"),
    (r"べきだ", "〜べきだ", "N3", "应该…", "should"),
    (r"べき", "〜べき", "N3", "应该…的", "should"),
    (r"(?<!ほど)(?<!なる)ほど(?!ほど)", "〜ほど", "N3", "…的程度；越…越…", "to the extent; the more … the more"),
    (r"だけでなく", "〜だけでなく", "N3", "不仅…而且…", "not only … but also"),
    (r"だけではなく", "〜だけではなく", "N3", "不仅…而且…", "not only … but also"),
    (r"代わりに", "〜代わりに", "N3", "代替…；作为交换", "instead of; in exchange for"),
    (r"かわりに", "〜代わりに", "N3", "代替…；作为交换", "instead of; in exchange for"),
    (r"とおり", "〜とおり", "N3", "按照…那样", "as; just as"),
    (r"通り", "〜通り", "N3", "按照…那样", "as; just as"),
    (r"っぱなし", "〜っぱなし", "N3", "一直…着（没处理）", "leaving … as is"),
    (r"がる", "〜がる", "N3", "表现出…；显得…", "show signs of; appear to"),

    # ── N4 ──
    (r"てもいい", "〜てもいい", "N4", "可以…", "may; it's okay to"),
    (r"てもいいです", "〜てもいいですか", "N4", "可以…吗？", "may I …?"),
    (r"てはいけない", "〜てはいけない", "N4", "不可以…", "must not"),
    (r"てはだめ", "〜てはだめ", "N4", "不可以…", "must not"),
    (r"ちゃだめ", "〜ちゃだめ", "N4", "不可以…（口语）", "must not (casual)"),
    (r"なければならない", "〜なければならない", "N4", "必须…", "must; have to"),
    (r"なければなりません", "〜なければなりません", "N4", "必须…", "must; have to"),
    (r"なきゃ", "〜なきゃ", "N4", "必须…（口语）", "have to (casual)"),
    (r"なくてはいけない", "〜なくてはいけない", "N4", "必须…", "must; have to"),
    (r"ないといけない", "〜ないといけない", "N4", "必须…", "must; have to"),
    (r"なくてもいい", "〜なくてもいい", "N4", "不…也可以", "don't have to"),
    (r"[たて]ことがある", "〜たことがある", "N4", "曾经…过", "have done before"),
    (r"たことがない", "〜たことがない", "N4", "没…过", "have never done"),
    (r"たり.*たり", "〜たり〜たり", "N4", "又…又…；一会儿…一会儿…", "doing things like … and …"),
    (r"ながら", "〜ながら", "N4", "一边…一边…", "while doing"),
    (r"すぎる", "〜すぎる", "N4", "过于…；太…了", "too much; overly"),
    (r"すぎ", "〜すぎ", "N4", "过于…；太…了", "too much; overly"),
    (r"やすい", "〜やすい", "N4", "容易…", "easy to"),
    (r"にくい", "〜にくい", "N4", "难以…", "hard to; difficult to"),
    (r"づらい", "〜づらい", "N4", "难以…（身心感受）", "hard to (emotional/physical)"),
    (r"かた[がを、。]", "〜方", "N4", "…的方法", "way of; how to"),
    (r"方が", "〜方がいい", "N4", "最好…；…比较好", "had better; it's better to"),
    (r"(?<!と)ても", "〜ても", "N4", "即使…也…", "even if; even though"),
    (r"でも", "〜でも", "N4", "即使…也…", "even if"),
    (r"たら", "〜たら", "N4", "如果…的话；…之后", "if; when; after"),
    (r"なら", "〜なら", "N4", "如果…的话", "if; in that case"),
    (r"ば[、]", "〜ば", "N4", "如果…的话", "if (conditional)"),
    (r"れば", "〜ば", "N4", "如果…的话", "if (conditional)"),
    (r"そうだ", "〜そうだ", "N4", "看起来…；据说…", "looks like; I heard"),
    (r"そうです", "〜そうです", "N4", "看起来…；据说…", "looks like; I heard"),
    (r"てくださ", "〜てください", "N4", "请…", "please do"),
    (r"ている", "〜ている", "N4", "正在…；处于…状态", "is doing; state of"),
    (r"てる[。、よね]", "〜てる", "N4", "正在…（口语）", "is doing (casual)"),
    (r"のに[、。]", "〜のに", "N4", "明明…却…；尽管…", "although; despite"),
    (r"はずがない", "〜はずがない", "N4", "不可能…", "there's no way"),
    (r"かもしれない", "〜かもしれない", "N4", "也许…", "might; maybe"),
    (r"かもしれません", "〜かもしれません", "N4", "也许…", "might; maybe"),
    (r"つもり", "〜つもり", "N4", "打算…", "intend to; plan to"),
    (r"予定", "〜予定", "N4", "计划…；预定…", "scheduled to; plan to"),
    (r"始める", "〜始める", "N4", "开始…", "start to"),
    (r"続ける", "〜続ける", "N4", "持续…", "continue to"),
    (r"終わる", "〜終わる", "N4", "做完…", "finish doing"),
    (r"出す", "〜出す", "N4", "突然开始…", "suddenly start to"),
    (r"させる", "〜させる", "N4", "让…做…（使役）", "make/let someone do"),
    (r"される", "〜される", "N4", "被…（被动）", "is done (passive)"),
    (r"られる", "〜られる", "N4", "被…；能…（被动/可能）", "passive / potential"),
    (r"と思う", "〜と思う", "N4", "我觉得…", "I think that"),
    (r"と思います", "〜と思います", "N4", "我觉得…", "I think that"),

    # ── N5 ──
    (r"たい[で。、]", "〜たい", "N5", "想…", "want to"),
    (r"たいです", "〜たいです", "N5", "想…", "want to"),
    (r"てから", "〜てから", "N5", "做完…之后", "after doing"),
    (r"ましょう", "〜ましょう", "N5", "一起…吧", "let's"),
    (r"ませんか", "〜ませんか", "N5", "要不要…？", "would you like to?"),
    (r"ないでください", "〜ないでください", "N5", "请不要…", "please don't"),
    (r"がほしい", "〜がほしい", "N5", "想要…", "want (something)"),
    (r"が欲しい", "〜が欲しい", "N5", "想要…", "want (something)"),
]

# 编译正则
COMPILED = [(re.compile(pat), disp, lv, zh, en) for pat, disp, lv, zh, en in GRAMMAR]


def annotate(sentence: str) -> list[dict]:
    """返回匹配到的语法点列表（去重，长模式抑制短模式）。"""
    seen: set[str] = set()
    results: list[dict] = []
    # 收集所有匹配的 display pattern
    matched: list[tuple[str, str, str, str]] = []
    for regex, disp, lv, zh, en in COMPILED:
        if disp in seen:
            continue
        if regex.search(sentence):
            seen.add(disp)
            matched.append((disp, lv, zh, en))

    # 如果一个长模式包含短模式的核心部分，跳过短模式
    # 例如 〜てもいい 包含 〜ても，〜ないでください 包含 〜ないで
    SUPPRESS = {
        "〜ても": {"〜てもいい", "〜てもいいですか", "〜にしても"},
        "〜でも": {"〜てもいい", "〜てもいいですか"},
        "〜ないで": {"〜ないでください"},
        "〜たい": {"〜たいです"},
        "〜そうだ": {"〜そうです"},
        "〜と思う": {"〜と思います"},
        "〜かもしれない": {"〜かもしれません"},
        "〜てもいい": {"〜てもいいですか"},
        "〜はずだ": {"〜はずがない"},
        "〜ば": set(),
        "〜ように": {"〜ようにする", "〜ようになる", "〜ようにしている", "〜ように言う"},
        "〜ようと": {"〜ようとする", "〜ようとしない"},
        "〜こそ": {"〜からこそ"},
        "〜ことがある": {"〜たことがある", "〜たことがない"},
    }

    matched_set = {disp for disp, _, _, _ in matched}
    for disp, lv, zh, en in matched:
        suppressors = SUPPRESS.get(disp)
        if suppressors and suppressors & matched_set:
            continue
        results.append({"pattern": disp, "level": lv, "note": zh, "noteEn": en})
    return results


def main():
    data = json.loads(SRC.read_text("utf-8"))
    total = len(data)
    annotated = 0
    for item in data:
        grams = annotate(item["word"])
        if grams:
            item["grammar"] = grams
            annotated += 1
        elif "grammar" in item:
            del item["grammar"]

    SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(f"Done: {annotated}/{total} sentences annotated with grammar points.")

    # 统计
    from collections import Counter
    c = Counter()
    for item in data:
        for g in item.get("grammar", []):
            c[g["pattern"]] += 1
    print(f"\nTop 20 grammar points:")
    for pat, cnt in c.most_common(20):
        print(f"  {pat}: {cnt}")


if __name__ == "__main__":
    main()
