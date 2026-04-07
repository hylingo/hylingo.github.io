/**
 * 学习进度按 studyLang 分桶；本地仅使用 learn_{ja|en}_*。
 */
import { useAppStore } from '@/stores/app'
import type { StudyLang } from '@/types'
import { safeGet, safeSet, safeRemove } from '@/storage/safeLS'
import { LS } from '@/storage/keys'

export const STUDY_LANGS: StudyLang[] = ['ja', 'en']

/**
 * 与 app store 中 study_lang 同源（localStorage），可在 Pinia 尚未 app.use 时安全调用。
 */
export function studyLangFromLocalStorage(): StudyLang {
  const s = safeGet(LS.STUDY_LANG)
  if (s === 'en' || s === 'ja') return s
  return 'ja'
}

export const SYNCED_CLOUD_KEYS = [
  'stats',
  'counts',
  'delays',
  'listened',
  'practiceRecognized',
  'masteryQuizPassed',
  'quizQueue',
  'starred',
  'practiceStreak',
] as const

export type SyncedCloudKey = (typeof SYNCED_CLOUD_KEYS)[number]

const CLOUD_TO_LOCAL_SUFFIX: Record<SyncedCloudKey, string> = {
  stats: 'stats',
  counts: 'item_counts',
  delays: 'delays',
  listened: 'listened',
  practiceRecognized: 'practice_recognized',
  masteryQuizPassed: 'mastery_quiz_passed',
  quizQueue: 'quiz_queue',
  starred: 'starred',
  practiceStreak: 'practice_streak',
}

const LEARN_ARTICLE_SUFFIX = {
  mode: 'article_mode',
  show_zh: 'article_show_zh',
  show_reading: 'article_show_reading',
  voice: 'article_tts_voice',
} as const

export function learnLocalStorageKey(lang: StudyLang, cloudKey: SyncedCloudKey): string {
  return `learn_${lang}_${CLOUD_TO_LOCAL_SUFFIX[cloudKey]}`
}

export function currentLearnStorageKey(cloudKey: SyncedCloudKey): string {
  return learnLocalStorageKey(useAppStore().studyLang, cloudKey)
}

export function listenedTodayKey(lang: StudyLang): string {
  return `learn_${lang}_listened_today`
}

export function quizScopeKey(lang: StudyLang): string {
  return `learn_${lang}_quiz_scope`
}

export function articlePrefKey(lang: StudyLang, id: keyof typeof LEARN_ARTICLE_SUFFIX): string {
  return `learn_${lang}_${LEARN_ARTICLE_SUFFIX[id]}`
}

export function readSyncedRaw(lang: StudyLang, cloudKey: SyncedCloudKey): string | null {
  return safeGet(learnLocalStorageKey(lang, cloudKey))
}

export function readSyncedJson(lang: StudyLang, cloudKey: SyncedCloudKey): unknown {
  try {
    const raw = readSyncedRaw(lang, cloudKey)
    if (raw == null || raw === '') return {}
    const p = JSON.parse(raw)
    return p && typeof p === 'object' && !Array.isArray(p) ? p : {}
  } catch {
    return {}
  }
}

export function writeSyncedJson(lang: StudyLang, cloudKey: SyncedCloudKey, value: unknown) {
  safeSet(learnLocalStorageKey(lang, cloudKey), JSON.stringify(value ?? {}))
}

export type LangBundle = Record<SyncedCloudKey, unknown>

export function readLangBundle(lang: StudyLang): LangBundle {
  const b = {} as LangBundle
  for (const ck of SYNCED_CLOUD_KEYS) {
    b[ck] = readSyncedJson(lang, ck)
  }
  return b
}

export function writeLangBundle(lang: StudyLang, bundle: Partial<LangBundle>) {
  for (const ck of SYNCED_CLOUD_KEYS) {
    const v = bundle[ck]
    if (v !== undefined) {
      writeSyncedJson(lang, ck, v)
    }
  }
}

export function writeLangBundleFull(lang: StudyLang, bundle: LangBundle) {
  for (const ck of SYNCED_CLOUD_KEYS) {
    writeSyncedJson(lang, ck, bundle[ck] ?? {})
  }
}

export function readListenedTodayRaw(lang: StudyLang): string | null {
  return safeGet(listenedTodayKey(lang))
}

export function writeListenedTodayRaw(lang: StudyLang, raw: string) {
  safeSet(listenedTodayKey(lang), raw)
}

export function readQuizScopeRaw(lang: StudyLang): string | null {
  return safeGet(quizScopeKey(lang))
}

export function writeQuizScopeRaw(lang: StudyLang, scope: string) {
  safeSet(quizScopeKey(lang), scope)
}

export function readArticlePrefRaw(lang: StudyLang, id: keyof typeof LEARN_ARTICLE_SUFFIX): string | null {
  return safeGet(articlePrefKey(lang, id))
}

export function writeArticlePrefRaw(lang: StudyLang, id: keyof typeof LEARN_ARTICLE_SUFFIX, value: string) {
  safeSet(articlePrefKey(lang, id), value)
}

/** 清除 learn_* 学习数据（不含 jp_user_id / jp_lang / 主题等） */
export function clearAllLearnProgressLocal() {
  for (const lang of STUDY_LANGS) {
    for (const ck of SYNCED_CLOUD_KEYS) {
      safeRemove(learnLocalStorageKey(lang, ck))
    }
    safeRemove(listenedTodayKey(lang))
    safeRemove(quizScopeKey(lang))
    for (const id of Object.keys(LEARN_ARTICLE_SUFFIX) as (keyof typeof LEARN_ARTICLE_SUFFIX)[]) {
      safeRemove(articlePrefKey(lang, id))
    }
  }
}
