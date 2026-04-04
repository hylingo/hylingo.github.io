/**
 * 掌握测验候选队列：听、练里都可以把任意词加入测验。
 * 测验中 3 次不通过则打回（移出队列）。
 * 正式测验抽题必须只使用 getQuizQueueKeys()，不得从全量词表抽题。
 */
import { ref } from 'vue'
import { makeItemKey } from './itemKey'
import { useFirebase } from '@/composables/useFirebase'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useAppStore } from '@/stores/app'

const { syncToCloud } = useFirebase()

/** 列表「加入测验 / 可以测验了」行刷新用 */
export const quizQueueTick = ref(0)

function readStore(): Record<string, number> {
  try {
    const p = readSyncedJson(useAppStore().studyLang, 'quizQueue')
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {}
    const out: Record<string, number> = {}
    for (const k of Object.keys(p)) {
      const n = Number((p as Record<string, unknown>)[k])
      if (k && Number.isFinite(n)) out[k] = n
    }
    return out
  } catch {
    return {}
  }
}

/** 列表/练页筛选时一次性读取，避免对每个词条调用 isInQuizQueue 重复 parse */
export function getQuizQueueKeySet(): Set<string> {
  return new Set(Object.keys(readStore()))
}

function writeStore(r: Record<string, number>) {
  writeSyncedJson(useAppStore().studyLang, 'quizQueue', r)
  syncToCloud()
  quizQueueTick.value++
}

/** 任意词均可加入测验队列 */
export function canJoinQuizQueue(_cat: string, _id: number): boolean {
  return true
}

/** 按加入顺序（时间戳升序）返回 cat:id 列表，供测验模块唯一数据源 */
export function getQuizQueueKeys(): string[] {
  const r = readStore()
  return Object.entries(r)
    .sort((a, b) => a[1] - b[1])
    .map(([k]) => k)
}

export function isInQuizQueue(cat: string, id: number): boolean {
  return makeItemKey(cat, id) in readStore()
}

export function addToQuizQueue(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readStore()
  if (r[k] != null) return
  r[k] = Date.now()
  writeStore(r)
}

/** 移出队列（用户取消或测验结束后可调用） */
export function removeFromQuizQueue(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readStore()
  if (!(k in r)) return
  delete r[k]
  writeStore(r)
}

export function getQuizQueueSize(): number {
  return Object.keys(readStore()).length
}
