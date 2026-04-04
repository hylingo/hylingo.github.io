import { ref } from 'vue'
import { makeItemKey } from '@/learning/itemKey'
import { useFirebase } from './useFirebase'
import { readSyncedJson, writeSyncedJson } from '@/learning/learnStorage'
import { useAppStore } from '@/stores/app'

const { debouncedSync } = useFirebase()

/** 列表重渲染用 */
export const listenDismissTick = ref(0)

function readDismissed(): Record<string, true> {
  try {
    const p = readSyncedJson(useAppStore().studyLang, 'listenDismissed')
    if (!p || typeof p !== 'object' || Array.isArray(p)) return {}
    return p as Record<string, true>
  } catch {
    return {}
  }
}

function writeDismissed(r: Record<string, true>) {
  writeSyncedJson(useAppStore().studyLang, 'listenDismissed', r)
  debouncedSync()
}

export function isListenDismissed(cat: string, id: number): boolean {
  return !!readDismissed()[makeItemKey(cat, id)]
}

/** 听清了：从听列表隐藏（不改动练习/听过计数）；左滑入口已下线，保留供数据/同步兼容 */
export function listenDismissClear(cat: string, id: number) {
  const r = readDismissed()
  r[makeItemKey(cat, id)] = true
  writeDismissed(r)
  listenDismissTick.value++
}

/**
 * 用户进入「测验」模式时调用：清空听列表隐藏标记，
 * 使先前因「听清了」从听/练列表隐藏的句子重新出现。
 */
export function restoreListenListHiddenOnTestMode() {
  const r = readDismissed()
  if (Object.keys(r).length === 0) return
  writeDismissed({})
  listenDismissTick.value++
  debouncedSync()
}
