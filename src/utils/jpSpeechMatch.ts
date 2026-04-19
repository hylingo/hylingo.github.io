import type { VocabItem } from '@/types'

/** 汉数字 → 阿拉伯数字（支持 十/百/千/万，覆盖常见年龄/年份等） */
const CN_DIGIT: Record<string, number> = {
  〇: 0, 零: 0, 一: 1, 二: 2, 両: 2, 三: 3, 四: 4, 五: 5,
  六: 6, 七: 7, 八: 8, 九: 9, 壱: 1, 弐: 2, 参: 3,
}
const CN_UNIT: Record<string, number> = { 十: 10, 拾: 10, 百: 100, 千: 1000, 万: 10000 }

function cnNumToInt(s: string): number {
  let total = 0, section = 0, num = 0
  for (const ch of s) {
    if (ch in CN_DIGIT) {
      num = CN_DIGIT[ch]
    } else if (ch in CN_UNIT) {
      const unit = CN_UNIT[ch]
      if (unit === 10000) {
        section = (section + (num || 0)) * unit
        total += section
        section = 0
      } else {
        section += (num || 1) * unit
      }
      num = 0
    }
  }
  return total + section + num
}

/** 把字符串里的汉数字串替换成阿拉伯数字；纯数字读法（二〇二六）和带单位（二十）都支持 */
export function normalizeNumbers(s: string): string {
  // 带单位的汉数字串：一至九 可带 十/百/千/万
  s = s.replace(/[〇零一二三四五六七八九壱弐参両十拾百千万]+/g, (m) => {
    // 纯"〇/零 + 个位"序列（如 二〇二六）：按位拼
    if (/^[〇零一二三四五六七八九]+$/.test(m) && m.length >= 2) {
      return [...m].map((c) => String(CN_DIGIT[c])).join('')
    }
    const n = cnNumToInt(m)
    return Number.isFinite(n) && n > 0 ? String(n) : m
  })
  return s
}

/** 片假名 → 平假名（U+30A1..U+30F6 → 对应平假名），其他保留。用于对比时归一 */
export function toHiragana(s: string): string {
  let out = ''
  for (let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i)
    if (c >= 0x30a1 && c <= 0x30f6) out += String.fromCharCode(c - 0x60)
    else out += s[i]
  }
  return out
}

/**
 * STT 同音误识别映射：同じ読みで STT が別の漢字を返すケース。
 * key=STT が返す表記, value=正解側の表記
 */
const KANJI_SYNONYMS: [string, string][] = [
  ['引け', '弾け'], ['引き', '弾き'], ['引く', '弾く'],
  ['聞け', '弾け'],
  ['退け', '弾け'],
  ['装置', 'そっち'],
  ['印象', '一緒'],
  ['携帯で', '着て'],
  ['御飯', 'ご飯'],
  ['美味しい', 'おいしい'],
  ['美味しく', 'おいしく'],
  ['美味しかっ', 'おいしかっ'],
]

function applySynonyms(s: string): string {
  for (const [from, to] of KANJI_SYNONYMS) {
    if (s.includes(from)) s = s.replaceAll(from, to)
  }
  return s
}

/** 口述比对：去空白、标点、汉数字归一、片假名 → 平假名、同音漢字归一 */
export function normalizeJpSpeech(s: string): string {
  return toHiragana(
    applySynonyms(
      normalizeNumbers(
        s
          .trim()
          .replace(/[\s\u3000]+/g, '')
          .replace(/[。．、，,.]/g, ''),
      ),
    ),
  )
}

/**
 * STT 同音兜底：当目标读音命中 key 时，transcript 出现任一 alias 就补一个等同于 key 的候选。
 * 例：きゃく 常被 Google STT 听成 ひゃく 并转成 "100"。
 * 注意 alias 已是经过 normalizeJpSpeech 后的形态。
 */
const READING_ALIASES: Record<string, string[]> = {
  きゃく: ['ひゃく', '100'],
}

/** 针对目标读音/表记生成 transcript 同音兜底候选（已 normalize 过的字符串） */
export function homophoneAliases(normalizedTranscript: string, normalizedReading: string): string[] {
  const aliases = READING_ALIASES[normalizedReading]
  if (!aliases) return []
  return aliases.some((a) => normalizedTranscript === a || normalizedTranscript.includes(a))
    ? [normalizedReading]
    : []
}

function singleMatch(t: string, w: string, r: string): boolean {
  if (t.length < 1) return false
  if (t === w || t === r) return true
  if (w.length >= 2 && t.includes(w)) return true
  if (r.length >= 2 && t.includes(r)) return true
  if (w.length === 1 && t === w) return true
  if (r.length === 1 && t === r) return true
  if (homophoneAliases(t, r).length > 0) return true
  return false
}

/** 识别结果是否与词条的「表记」或「读音」匹配（允许多说，不允许明显少说） */
export function speechMatchesVocab(
  transcript: string,
  item: Pick<VocabItem, 'word' | 'reading'>,
  alternatives?: string[],
): boolean {
  const w = normalizeJpSpeech(item.word)
  const r = normalizeJpSpeech(item.reading)
  if (singleMatch(normalizeJpSpeech(transcript), w, r)) return true
  if (alternatives) {
    for (const alt of alternatives) {
      if (singleMatch(normalizeJpSpeech(alt), w, r)) return true
    }
  }
  return false
}
