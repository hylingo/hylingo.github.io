import type { VocabItem } from '@/types'

/** 口述比对：去空白与常见标点 */
export function normalizeJpSpeech(s: string): string {
  return s
    .trim()
    .replace(/[\s\u3000]+/g, '')
    .replace(/[。．、，,.]/g, '')
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
