/**
 * 本篇精读练习槽位的 LS 读写。
 * 单一真相源 —— store 和 useFirebase 都从这里访问，避免 key 命名漂移。
 */

import { safeGet, safeSet, safeRemove } from './safeLS'
import { practiceSlotKey } from './keys'

export type PracticeSlot = { id: string; title: string; index: number }

export function readPracticeSlot(format: string): PracticeSlot | null {
  const id = safeGet(practiceSlotKey.id(format))
  if (!id) return null
  return {
    id,
    title: safeGet(practiceSlotKey.title(format)) || '',
    index: Number(safeGet(practiceSlotKey.index(format)) || '0'),
  }
}

export function writePracticeSlot(format: string, slot: PracticeSlot | null): void {
  if (slot && slot.id) {
    safeSet(practiceSlotKey.id(format), slot.id)
    safeSet(practiceSlotKey.title(format), slot.title || '')
    safeSet(practiceSlotKey.index(format), String(slot.index || 0))
  } else {
    safeRemove(practiceSlotKey.id(format))
    safeRemove(practiceSlotKey.title(format))
    safeRemove(practiceSlotKey.index(format))
  }
}

/** 仅更新 index，不动 id/title（用于练习过程中保存进度） */
export function writePracticeSlotIndex(format: string, index: number): void {
  safeSet(practiceSlotKey.index(format), String(index))
}
