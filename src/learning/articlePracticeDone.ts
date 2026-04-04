/**
 * 精读篇目「逐句练习」全部完成标记（仅本地，不参与 Firebase 同步）
 */
import type { StudyLang } from '@/types'

function storageKey(lang: StudyLang): string {
  return `learn_${lang}_article_practice_done_v1`
}

export function markArticlePracticeDone(lang: StudyLang, articleId: string): void {
  try {
    const k = storageKey(lang)
    const raw = localStorage.getItem(k)
    const map: Record<string, true> = raw ? (JSON.parse(raw) as Record<string, true>) : {}
    map[articleId] = true
    localStorage.setItem(k, JSON.stringify(map))
  } catch {
    /* ignore */
  }
}

export function hasArticlePracticeDone(lang: StudyLang, articleId: string): boolean {
  try {
    const raw = localStorage.getItem(storageKey(lang))
    if (!raw) return false
    const map = JSON.parse(raw) as Record<string, true>
    return !!map[articleId]
  } catch {
    return false
  }
}
