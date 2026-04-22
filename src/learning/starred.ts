/**
 * 收藏（星标）：用户主动标记的单词，跨分类。
 * 存储格式：Record<string, true>，key 为 cat:id。
 */
import { ref } from 'vue'
import { makeItemKey } from './itemKey'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useAppStore } from '@/stores/app'
import { useFirebase } from '@/composables/useFirebase'

const { debouncedSync } = useFirebase()

export const starredTick = ref(0)

function readMap(): Record<string, true> {
  try {
    const p = readSyncedJson(useAppStore().studyLang, 'starred')
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {}
    return p as Record<string, true>
  } catch {
    return {}
  }
}

function writeMap(r: Record<string, true>) {
  writeSyncedJson(useAppStore().studyLang, 'starred', r)
  debouncedSync()
  starredTick.value++
}

export function isStarred(cat: string, id: number): boolean {
  return !!readMap()[makeItemKey(cat, id)]
}

export function toggleStar(cat: string, id: number): boolean {
  const k = makeItemKey(cat, id)
  const r = readMap()
  if (r[k]) {
    delete r[k]
    writeMap(r)
    return false
  } else {
    r[k] = true
    writeMap(r)
    return true
  }
}

export function getStarredMap(): Record<string, true> {
  return readMap()
}

/** 仅统计当前词库中仍存在的收藏项，忽略因词条删除残留的幽灵键 */
export function getStarredCount(): number {
  const map = readMap()
  const store = useAppStore()
  const data = store.data as Record<string, { id: number }[]>
  let n = 0
  for (const c of ['nouns', 'verbs']) {
    const arr = data[c]
    if (!Array.isArray(arr)) continue
    for (const it of arr) {
      if (map[makeItemKey(c, it.id)]) n++
    }
  }
  return n
}
