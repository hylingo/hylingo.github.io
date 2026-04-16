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

function singleMatch(t: string, w: string, r: string): boolean {
  if (t.length < 1) return false
  if (t === w || t === r) return true
  if (w.length >= 2 && t.includes(w)) return true
  if (r.length >= 2 && t.includes(r)) return true
  if (w.length === 1 && t === w) return true
  if (r.length === 1 && t === r) return true
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
