/**
 * 文章级统计：完整听次数 / 完整跟读次数，按 studyLang 分桶。
 */
import type { StudyLang } from '@/types'

function storageKey(lang: StudyLang): string {
  return `learn_${lang}_article_progress_v1`
}

export interface ArticleProgressEntry {
  listen: number
  shadow: number
}

function readMap(lang: StudyLang): Record<string, ArticleProgressEntry> {
  try {
    const raw = localStorage.getItem(storageKey(lang))
    if (!raw) return {}
    const m = JSON.parse(raw)
    return m && typeof m === 'object' ? m : {}
  } catch {
    return {}
  }
}

function writeMap(lang: StudyLang, m: Record<string, ArticleProgressEntry>) {
  localStorage.setItem(storageKey(lang), JSON.stringify(m))
}

export function getArticleProgress(lang: StudyLang, articleId: string): ArticleProgressEntry {
  const m = readMap(lang)
  return m[articleId] ?? { listen: 0, shadow: 0 }
}

export function getAllArticleProgress(lang: StudyLang): Record<string, ArticleProgressEntry> {
  return readMap(lang)
}

export function recordArticleListenComplete(lang: StudyLang, articleId: string) {
  const m = readMap(lang)
  if (!m[articleId]) m[articleId] = { listen: 0, shadow: 0 }
  m[articleId].listen++
  writeMap(lang, m)
}

export function recordArticleShadowComplete(lang: StudyLang, articleId: string) {
  const m = readMap(lang)
  if (!m[articleId]) m[articleId] = { listen: 0, shadow: 0 }
  m[articleId].shadow++
  writeMap(lang, m)
}
