/**
 * 精读篇目「逐句练习」全部完成标记（仅本地，不参与 Firebase 同步）
 */
import type { StudyLang } from '@/types'
import { safeGetJSON, safeSetJSON } from '@/storage/safeLS'

function storageKey(lang: StudyLang): string {
  return `learn_${lang}_article_practice_done_v1`
}

export function markArticlePracticeDone(lang: StudyLang, articleId: string): void {
  const map = safeGetJSON<Record<string, true>>(storageKey(lang), {})
  map[articleId] = true
  safeSetJSON(storageKey(lang), map)
}

export function hasArticlePracticeDone(lang: StudyLang, articleId: string): boolean {
  const map = safeGetJSON<Record<string, true>>(storageKey(lang), {})
  return !!map[articleId]
}
