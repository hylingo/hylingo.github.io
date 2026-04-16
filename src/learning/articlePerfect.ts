/**
 * 文章满分激励：每句跟读得 100 分落盘；整篇"全部满分"时文章列表 / 详情页打印记。
 * 粒度：Record<articleId, Record<sentenceIndex, true>>，只存正向事件，不退化。
 */
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useFirebase } from '@/composables/useFirebase'

/** UI 响应式 tick：有任一满分写入就递增，让卡片/列表重算 */
export const articlePerfectTick = ref(0)

export type ArticlePerfectMap = Record<string, Record<string, true>>

function read(): ArticlePerfectMap {
  const raw = readSyncedJson(useAppStore().studyLang, 'articlePerfect')
  return (raw && typeof raw === 'object' ? (raw as ArticlePerfectMap) : {}) || {}
}

function write(m: ArticlePerfectMap) {
  writeSyncedJson(useAppStore().studyLang, 'articlePerfect', m)
  articlePerfectTick.value++
  useFirebase().debouncedSync()
}

/** 标记一句话已满分（幂等） */
export function markSentencePerfect(articleId: string, sentenceIndex: number): void {
  const m = read()
  const key = String(sentenceIndex)
  if (m[articleId]?.[key]) return
  if (!m[articleId]) m[articleId] = {}
  m[articleId][key] = true
  write(m)
}

/** 某句是否已满分 */
export function isSentencePerfect(articleId: string, sentenceIndex: number): boolean {
  const m = read()
  return !!m[articleId]?.[String(sentenceIndex)]
}

/** 某篇已满分过的句索引集合 */
export function getPerfectSentencesOf(articleId: string): Record<string, true> {
  return read()[articleId] ?? {}
}

/** 全部句子都满分过（需传入实际句数）*/
export function isArticleFullyPerfect(articleId: string, totalSentences: number): boolean {
  if (totalSentences <= 0) return false
  const set = read()[articleId] ?? {}
  for (let i = 0; i < totalSentences; i++) {
    if (!set[String(i)]) return false
  }
  return true
}
