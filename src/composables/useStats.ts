import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useFirebase } from './useFirebase'
import type { StatsMap } from '@/types'

const { debouncedSync } = useFirebase()

/** Bump this to trigger reactive re-reads of stats */
export const statsVersion = ref(0)

export function todayKey(): string {
  return new Date().toISOString().slice(0, 10)
}

export function getStats(): StatsMap {
  const lang = useAppStore().studyLang
  return (readSyncedJson(lang, 'stats') as StatsMap) || {}
}

export function saveStats(s: StatsMap) {
  const lang = useAppStore().studyLang
  writeSyncedJson(lang, 'stats', s)
  statsVersion.value++
  debouncedSync()
}

export function recordStudy() {
  const s = getStats()
  const d = todayKey()
  if (!s[d]) s[d] = { studied: 0, quizzed: 0, correct: 0, wrong: {} }
  s[d].studied++
  saveStats(s)
}

export function recordQuiz(item: { id: number }, correct: boolean, cat: string) {
  const s = getStats()
  const d = todayKey()
  if (!s[d]) s[d] = { studied: 0, quizzed: 0, correct: 0, wrong: {} }
  s[d].quizzed++
  if (correct) {
    s[d].correct++
  } else {
    const key = cat + ':' + item.id
    s[d].wrong[key] = (s[d].wrong[key] || 0) + 1
  }
  saveStats(s)
}

export function recordListenTime(seconds: number) {
  if (!seconds || !isFinite(seconds)) return
  const s = getStats()
  const d = todayKey()
  if (!s[d]) s[d] = { studied: 0, quizzed: 0, correct: 0, wrong: {} }
  s[d].listened = Math.round(((s[d].listened || 0) + seconds) * 10) / 10
  saveStats(s)
}

export function recordReadTime(seconds: number) {
  if (!seconds || !isFinite(seconds)) return
  const s = getStats()
  const d = todayKey()
  if (!s[d]) s[d] = { studied: 0, quizzed: 0, correct: 0, wrong: {} }
  s[d].recorded = Math.round(((s[d].recorded || 0) + seconds) * 10) / 10
  saveStats(s)
}

export function recordFollowComplete(itemCount: number) {
  const s = getStats()
  const d = todayKey()
  if (!s[d]) s[d] = { studied: 0, quizzed: 0, correct: 0, wrong: {} }
  s[d].followCompleted = (s[d].followCompleted || 0) + 1
  s[d].followSentences = (s[d].followSentences || 0) + itemCount
  saveStats(s)
}

export function useStats() {
  return {
    recordStudy,
    recordQuiz,
    recordListenTime,
    recordReadTime,
    getStats,
    saveStats,
    todayKey,
  }
}
