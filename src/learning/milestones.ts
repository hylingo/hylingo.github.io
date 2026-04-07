/**
 * 学习里程碑：宽松 SRS 复习 + 手动「掌握了」。
 *
 * 核心规则：
 * - 任意完成一次学习（录音 / 听写）→ recordStudy(cat, id)
 *   - counts +1（既有 recordItemSeen）
 *   - 按 counts 查间隔表，写入 delays 作为下次复习时间
 * - 用户主动点「掌握了」→ markMastered(cat, id)
 * - 「我的-掌握列表」可取消 → unmarkMastered(cat, id)
 *
 * 旧 API（markPracticeAnswerKnown / markPracticeAnswerUnknown / 自动连续答对掌握）
 * 已废弃但保留 no-op 避免破坏外部引用，新代码不要使用。
 */
import { makeItemKey } from './itemKey'
import { milestoneStateTick } from './milestoneTick'
import { recordItemSeen, delayItem, getItemCount } from '@/composables/useSpacedRepetition'
import { useFirebase } from '@/composables/useFirebase'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useAppStore } from '@/stores/app'

const { debouncedSync } = useFirebase()

export { milestoneStateTick }

/**
 * SRS 间隔表（按学习次数 → 复习间隔天数）。
 * 索引 = 学习次数（已完成的次数）；首次学完 (count=1) 用 SRS_INTERVALS[1] = 1 天。
 * 超出表长用最后一个值（封顶 240 天）。
 */
const SRS_INTERVALS = [0, 1, 2, 4, 7, 14, 30, 60, 120, 240]

/** 按已完成的学习次数算下次到期的天数 */
export function srsIntervalDays(studyCount: number): number {
  if (studyCount <= 0) return 0
  if (studyCount >= SRS_INTERVALS.length) return SRS_INTERVALS[SRS_INTERVALS.length - 1]
  return SRS_INTERVALS[studyCount]
}

type SyncedMapKey = 'practiceRecognized' | 'masteryQuizPassed' | 'practiceStreak'

// 内存缓存：避免每次调用都 JSON.parse localStorage
const _cache = new Map<string, { data: unknown }>()

function _cacheKey(ck: SyncedMapKey): string {
  return `${useAppStore().studyLang}:${ck}`
}

function readJsonMap<T = Record<string, unknown>>(ck: SyncedMapKey): T {
  const key = _cacheKey(ck)
  const cached = _cache.get(key)
  if (cached) return cached.data as T
  try {
    const lang = useAppStore().studyLang
    const p = readSyncedJson(lang, ck)
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {} as T
    _cache.set(key, { data: p })
    return p as T
  } catch {
    return {} as T
  }
}

function writeJsonMap(ck: SyncedMapKey, r: unknown) {
  _cache.set(_cacheKey(ck), { data: r })
  writeSyncedJson(useAppStore().studyLang, ck, r)
  debouncedSync()
  milestoneStateTick.value++
}

/** 清除缓存（语言切换时调用） */
export function clearMilestoneCache() {
  _cache.clear()
}

// --- 学习一次（录音 / 听写完成）---

/** 完成一次练习：counts++，并按新次数推迟到 SRS 间隔表对应的天数 */
export function recordStudy(cat: string, id: number): void {
  recordItemSeen(cat, id)
  const next = getItemCount(cat, id) // recordItemSeen 内部已 +1，这里读到的是新值
  const days = srsIntervalDays(next)
  if (days > 0) delayItem(cat, id, days)
}

// --- 掌握 ---

export function getMasteryQuizPassedMap(): Record<string, true> {
  return readJsonMap<Record<string, true>>('masteryQuizPassed')
}

export function hasMasteryQuizPassed(cat: string, id: number): boolean {
  return !!readJsonMap<Record<string, true>>('masteryQuizPassed')[makeItemKey(cat, id)]
}

/** 用户主动点「掌握了」 */
export function markMastered(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readJsonMap<Record<string, true>>('masteryQuizPassed')
  if (r[k]) return
  r[k] = true
  writeJsonMap('masteryQuizPassed', r)
}

/** 取消掌握（从掌握列表里移除，回到学习中状态） */
export function unmarkMastered(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readJsonMap<Record<string, true>>('masteryQuizPassed')
  if (!r[k]) return
  delete r[k]
  writeJsonMap('masteryQuizPassed', r)
}

/** 已掌握 */
export function isItemMastered(cat: string, id: number): boolean {
  return !!readJsonMap<Record<string, true>>('masteryQuizPassed')[makeItemKey(cat, id)]
}

// --- 旧 API 兼容 shim（已废弃，新代码请用 recordStudy / markMastered） ---

/** @deprecated 使用 recordStudy 代替 */
export function markPracticeAnswerKnown(cat: string, id: number): void {
  recordStudy(cat, id)
}

/** @deprecated 不再有「不认识」语义，调用等价于一次普通学习 */
export function markPracticeAnswerUnknown(cat: string, id: number): void {
  recordStudy(cat, id)
}

/** @deprecated 不再使用 */
export function hasPracticeRecognized(_cat: string, _id: number): boolean {
  return false
}
