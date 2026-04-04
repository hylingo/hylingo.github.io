/**
 * 学习里程碑：练习·认识、连续答对自动掌握。
 * 单词掌握条件：连续答对 N 次（MASTERY_STREAK）自动标记。
 * 文章/对话掌握：由 articlePracticeDone 按篇管理，不走本模块。
 */
import { makeItemKey } from './itemKey'
import { milestoneStateTick } from './milestoneTick'
import { recordItemSeen, delayItem } from '@/composables/useSpacedRepetition'
import { useFirebase } from '@/composables/useFirebase'
import { practice as practiceThresholds } from '@/config/thresholds'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useAppStore } from '@/stores/app'

const { debouncedSync } = useFirebase()

export { milestoneStateTick }

/** 连续答对几次自动掌握 */
const MASTERY_STREAK = 3

type SyncedMapKey = 'practiceRecognized' | 'masteryQuizPassed' | 'practiceStreak'

function readJsonMap<T = Record<string, unknown>>(ck: SyncedMapKey): T {
  try {
    const lang = useAppStore().studyLang
    const p = readSyncedJson(lang, ck)
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {} as T
    return p as T
  } catch {
    return {} as T
  }
}

function writeJsonMap(ck: SyncedMapKey, r: unknown) {
  writeSyncedJson(useAppStore().studyLang, ck, r)
  debouncedSync()
  milestoneStateTick.value++
}

// --- 连续答对计数 ---

function readStreakMap(): Record<string, number> {
  return readJsonMap<Record<string, number>>('practiceStreak')
}

function writeStreakMap(r: Record<string, number>) {
  writeJsonMap('practiceStreak', r)
}

// --- 练习：认识 / 不认识 ---

/** 练习中点「✓ 认识」：计次 + 短期推迟 + 连续答对计数（达标自动掌握） */
export function markPracticeAnswerKnown(cat: string, id: number): void {
  const k = makeItemKey(cat, id)

  // 写入「曾认识」
  const r = readJsonMap<Record<string, true>>('practiceRecognized')
  r[k] = true
  writeJsonMap('practiceRecognized', r)

  // 连续答对 +1，达标自动掌握
  const streaks = readStreakMap()
  const next = (streaks[k] || 0) + 1
  streaks[k] = next
  writeStreakMap(streaks)

  if (next >= MASTERY_STREAK) {
    markMasteryPassed(cat, id)
  }

  recordItemSeen(cat, id)
  delayItem(cat, id, practiceThresholds.knownDelayDays)
}

/** 练习中点「✗ 不认识」：重置连续答对计数 + 计练习次数 */
export function markPracticeAnswerUnknown(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const streaks = readStreakMap()
  if (streaks[k]) {
    streaks[k] = 0
    writeStreakMap(streaks)
  }
  recordItemSeen(cat, id)
}

/** 是否曾在练习中点过「认识」 */
export function hasPracticeRecognized(cat: string, id: number): boolean {
  return !!readJsonMap<Record<string, true>>('practiceRecognized')[makeItemKey(cat, id)]
}

// --- 掌握 ---

export function getMasteryQuizPassedMap(): Record<string, true> {
  return readJsonMap<Record<string, true>>('masteryQuizPassed')
}

export function hasMasteryQuizPassed(cat: string, id: number): boolean {
  return !!readJsonMap<Record<string, true>>('masteryQuizPassed')[makeItemKey(cat, id)]
}

/** 标记单词掌握（连续答对达标时自动调用） */
function markMasteryPassed(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readJsonMap<Record<string, true>>('masteryQuizPassed')
  r[k] = true
  writeJsonMap('masteryQuizPassed', r)
}

/** 已掌握：连续答对 N 次自动标记 */
export function isItemMastered(cat: string, id: number): boolean {
  return !!readJsonMap<Record<string, true>>('masteryQuizPassed')[makeItemKey(cat, id)]
}
