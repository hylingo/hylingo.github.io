import { ref } from 'vue'
import { useAppStore, type DataItem } from '../stores/app'
import { useFirebase } from './useFirebase'
import { todayKey } from './useStats'
import {
  readSyncedJson,
  writeSyncedJson,
  readListenedTodayRaw,
  writeListenedTodayRaw,
} from '@/learning/learnStorage'
import { coerceListenCount } from '@/utils/listenCount'
import { makeItemKey, getMasteryQuizPassedMap, getStarredMap } from '@/learning'

const { debouncedSync } = useFirebase()

/** 列表「练×」角标等依赖练习次数的 UI 刷新用 */
export const itemCountsTick = ref(0)

/** 听过次数变更时练页「加入测验」资格等刷新用 */
export const listenedCountsTick = ref(0)

function getItemCounts(): Record<string, number> {
  return readSyncedJson(useAppStore().studyLang, 'counts') as Record<string, number>
}

function saveItemCounts(c: Record<string, number>) {
  writeSyncedJson(useAppStore().studyLang, 'counts', c)
  debouncedSync()
}

/** 练习答题次数（仅统计，不用于「毕业/已掌握」） */
export function recordItemSeen(cat: string, id: number): number {
  const c = getItemCounts()
  const key = cat + ':' + id
  c[key] = (c[key] || 0) + 1
  saveItemCounts(c)
  itemCountsTick.value++
  return c[key]
}

/** 可练条目：该分类全部词条，仅排除未到期的「推迟复习」 */
export function getActiveItems(cat: string): (DataItem & { _cat?: string })[] {
  const store = useAppStore()
  const delays = getDelays()
  const today = new Date().toISOString().slice(0, 10)
  const mastery = getMasteryQuizPassedMap()

  if (cat === 'starred') {
    const starred = getStarredMap()
    const all: (DataItem & { _cat: string })[] = []
    for (const k of ['nouns', 'verbs'] as const) {
      store.data[k].forEach((it: DataItem) => {
        const key = makeItemKey(k, it.id)
        if (starred[key] && !(delays[key] > today) && !mastery[key]) {
          all.push({ ...it, _cat: k })
        }
      })
    }
    return all
  }

  if (cat === 'mix') {
    const all: (DataItem & { _cat: string })[] = []
    for (const k of ['nouns', 'verbs'] as const) {
      store.data[k].forEach((it: DataItem) => {
        const key = makeItemKey(k, it.id)
        if (!(delays[key] > today) && !mastery[key]) {
          all.push({ ...it, _cat: k })
        }
      })
    }
    for (let i = all.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[all[i], all[j]] = [all[j], all[i]]
    }
    return all
  }

  const items = store.data[cat as keyof typeof store.data]
  if (!Array.isArray(items)) return []
  return items.filter((it: DataItem) => {
    const key = makeItemKey(cat, it.id)
    return !(delays[key] > today) && !mastery[key]
  })
}

export function getItemCount(cat: string, id: number): number {
  const c = getItemCounts()
  return c[cat + ':' + id] || 0
}

/** 直接设置学习次数（用于"看答案/跳过"时的降档） */
export function setItemCount(cat: string, id: number, n: number): void {
  const c = getItemCounts()
  const key = cat + ':' + id
  if (n <= 0) delete c[key]
  else c[key] = n
  saveItemCounts(c)
  itemCountsTick.value++
}

/** 清除推迟复习标记，让该词立即可抽 */
export function clearDelay(cat: string, id: number): void {
  const d = getDelays()
  const key = cat + ':' + id
  if (!(key in d)) return
  delete d[key]
  saveDelays(d)
}

export function getDelays(): Record<string, string> {
  return readSyncedJson(useAppStore().studyLang, 'delays') as Record<string, string>
}

function saveDelays(d: Record<string, string>) {
  writeSyncedJson(useAppStore().studyLang, 'delays', d)
  debouncedSync()
}

export function delayItem(cat: string, id: number, days: number) {
  const d = getDelays()
  const until = new Date()
  until.setDate(until.getDate() + days)
  d[cat + ':' + id] = until.toISOString().slice(0, 10)
  saveDelays(d)
}

function getListenedItems(): Record<string, number> {
  return readSyncedJson(useAppStore().studyLang, 'listened') as Record<string, number>
}

function saveListenedItems(l: Record<string, number>) {
  writeSyncedJson(useAppStore().studyLang, 'listened', l)
  debouncedSync()
}

type ListenedTodayStore = { date: string; keys: Record<string, true> }

function loadListenedToday(): ListenedTodayStore {
  const d = todayKey()
  const lang = useAppStore().studyLang
  try {
    const raw = readListenedTodayRaw(lang)
    if (!raw) return { date: d, keys: {} }
    const p = JSON.parse(raw) as ListenedTodayStore
    if (!p || p.date !== d || !p.keys || typeof p.keys !== 'object') return { date: d, keys: {} }
    return { date: d, keys: p.keys }
  } catch {
    return { date: d, keys: {} }
  }
}

function saveListenedToday(p: ListenedTodayStore) {
  writeListenedTodayRaw(useAppStore().studyLang, JSON.stringify(p))
}

export function markListenedToday(cat: string, id: number) {
  const d = todayKey()
  let p = loadListenedToday()
  if (p.date !== d) p = { date: d, keys: {} }
  p.keys[cat + ':' + id] = true
  saveListenedToday(p)
}

export function isListenedToday(cat: string, id: number): boolean {
  return !!loadListenedToday().keys[cat + ':' + id]
}

/** 练页抽题、排序时一次性读取，避免对每个词条重复 JSON.parse */
export type QuizProgressSnapshot = {
  listened: Record<string, number>
  counts: Record<string, number>
  /** 仅当日 keys；与 listened 一致用于排序 */
  listenedTodayKeys: Record<string, true>
}

export function getQuizProgressSnapshot(): QuizProgressSnapshot {
  const today = loadListenedToday()
  const d = todayKey()
  return {
    listened: getListenedItems(),
    counts: getItemCounts(),
    listenedTodayKeys: today.date === d ? today.keys : {},
  }
}

function snapKey(cat: string, id: number) {
  return `${cat}:${id}`
}

export function snapListenCount(s: QuizProgressSnapshot, cat: string, id: number): number {
  return coerceListenCount(s.listened[snapKey(cat, id)])
}

export function snapItemCount(s: QuizProgressSnapshot, cat: string, id: number): number {
  return s.counts[snapKey(cat, id)] || 0
}

export function snapIsListenedToday(s: QuizProgressSnapshot, cat: string, id: number): boolean {
  return !!s.listenedTodayKeys[snapKey(cat, id)]
}

export function recordItemListened(cat: string, id: number) {
  const l = getListenedItems()
  const key = cat + ':' + id
  l[key] = coerceListenCount(l[key]) + 1
  saveListenedItems(l)
  markListenedToday(cat, id)
  listenedCountsTick.value++
}

export function getListenedCount(cat: string, id: number): number {
  const l = getListenedItems()
  return coerceListenCount(l[cat + ':' + id])
}

export function isDelayed(cat: string, id: number): boolean {
  const d = getDelays()
  const until = d[cat + ':' + id]
  if (!until) return false
  return until > new Date().toISOString().slice(0, 10)
}

export function useSpacedRepetition() {
  return {
    itemCountsTick,
    listenedCountsTick,
    recordItemSeen,
    getActiveItems,
    getItemCount,
    delayItem,
    getDelays,
    isDelayed,
    recordItemListened,
    getListenedCount,
    markListenedToday,
    isListenedToday,
  }
}
