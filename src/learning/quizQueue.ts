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

const MAX_FAILS = 3

const { debouncedSync } = useFirebase()

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

function writeStore(r: Record<string, number>) {
  writeSyncedJson(useAppStore().studyLang, 'quizQueue', r)
  debouncedSync()
  quizQueueTick.value++
}

// --- 失败计数 ---

function readFails(): Record<string, number> {
  try {
    const p = readSyncedJson(useAppStore().studyLang, 'quizFails')
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

function writeFails(r: Record<string, number>) {
  writeSyncedJson(useAppStore().studyLang, 'quizFails', r)
  debouncedSync()
}

/** 记录一次测验失败，达到 3 次自动移出队列并返回 true */
export function recordQuizFail(cat: string, id: number): boolean {
  const k = makeItemKey(cat, id)
  const f = readFails()
  f[k] = (f[k] || 0) + 1
  writeFails(f)
  if (f[k] >= MAX_FAILS) {
    removeFromQuizQueue(cat, id)
    clearQuizFails(cat, id)
    return true
  }
  return false
}

export function getQuizFailCount(cat: string, id: number): number {
  return readFails()[makeItemKey(cat, id)] || 0
}

export function clearQuizFails(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const f = readFails()
  if (k in f) {
    delete f[k]
    writeFails(f)
  }
}

// --- 第一步（读原文）通过记录 ---

function readPhase1(): Record<string, true> {
  try {
    const p = readSyncedJson(useAppStore().studyLang, 'quizPhase1')
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {}
    return p as Record<string, true>
  } catch {
    return {}
  }
}

function writePhase1(r: Record<string, true>) {
  writeSyncedJson(useAppStore().studyLang, 'quizPhase1', r)
  debouncedSync()
}

/** 标记第一步通过 */
export function markPhase1Passed(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readPhase1()
  r[k] = true
  writePhase1(r)
}

/** 是否已通过第一步 */
export function hasPhase1Passed(cat: string, id: number): boolean {
  return !!readPhase1()[makeItemKey(cat, id)]
}

/** 清除第一步记录（完全通过或被打回时） */
export function clearPhase1(cat: string, id: number): void {
  const k = makeItemKey(cat, id)
  const r = readPhase1()
  if (k in r) {
    delete r[k]
    writePhase1(r)
  }
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
