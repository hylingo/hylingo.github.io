/**
 * 学习里程碑：听列表隐藏（遗留数据）、练习·认识、掌握测验。
 * 正式掌握测验的抽题范围以 `getQuizQueueKeys()`（`learning/quizQueue.ts`）为准，不得从全量词表抽题。
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

type TrueMapKey = 'practiceRecognized' | 'masteryQuizPassed'

function readTrueMapFor(ck: TrueMapKey): Record<string, true> {
  try {
    const lang = useAppStore().studyLang
    const p = readSyncedJson(lang, ck)
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {}
    return p as Record<string, true>
  } catch {
    return {}
  }
}

function writeTrueMapFor(ck: TrueMapKey, r: Record<string, true>) {
  writeSyncedJson(useAppStore().studyLang, ck, r)
  debouncedSync()
  milestoneStateTick.value++
}

// --- 练习：认识 / 不认识（次数仍走 recordItemSeen）---

/** 练习中点「✓ 认识」：计次 + 短期推迟 + 写入「曾认识」里程碑（供将来掌握条件） */
export function markPracticeAnswerKnown(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readTrueMapFor('practiceRecognized')
  r[k] = true
  writeTrueMapFor('practiceRecognized', r)
  recordItemSeen(cat, id)
  delayItem(cat, id, practiceThresholds.knownDelayDays)
}

/** 练习中点「✗ 不认识」：仅计练习次数 */
export function markPracticeAnswerUnknown(cat: string, id: number): void {
  recordItemSeen(cat, id)
}

/** 是否曾在练习中点过「认识」（持久标志，与当日 delay 无关） */
export function hasPracticeRecognized(cat: string, id: number): boolean {
  return !!readTrueMapFor('practiceRecognized')[makeItemKey(cat, id)]
}

// --- 掌握测验（预留：测验通过后调用 markMasteryQuizPassed）---

/** 练页抽题等批量筛选时一次性读取，避免对每个 id 重复 parse localStorage */
export function getMasteryQuizPassedMap(): Record<string, true> {
  return readTrueMapFor('masteryQuizPassed')
}

export function hasMasteryQuizPassed(cat: string, id: number): boolean {
  return !!readTrueMapFor('masteryQuizPassed')[makeItemKey(cat, id)]
}

/** 掌握测验通过时由测验模块调用；合并策略与「听清了」一致（多设备取并集） */
export function markMasteryQuizPassed(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readTrueMapFor('masteryQuizPassed')
  r[k] = true
  writeTrueMapFor('masteryQuizPassed', r)
}

/**
 * 已掌握：练习认识 + 测验通过（句子「听清」左滑已下线，不再作为条件）。
 */
export function isItemMastered(cat: string, id: number): boolean {
  return hasPracticeRecognized(cat, id) && hasMasteryQuizPassed(cat, id)
}
