import { ref, computed } from 'vue'
import { useAppStore, type DataItem } from '../stores/app'
import {
  getQuizQueueKeys,
  removeFromQuizQueue,
  markMasteryQuizPassed,
  parseItemKey,
  recordQuizFail,
  clearQuizFails,
  markPhase1Passed,
  hasPhase1Passed,
  clearPhase1,
} from '@/learning'
import { speakWithExample, stopLoop } from './useAudio'

type QueueItem = DataItem & { _cat: string }

const items = ref<QueueItem[]>([])
const currentItem = ref<QueueItem | null>(null)
const isAnswered = ref(false)
const passedCount = ref(0)
const totalCount = ref(0)
/** 当前词的测验阶段，由持久化状态决定 */
const testPhase = ref<'read' | 'recall'>('read')

function rebuildItems() {
  const store = useAppStore()
  if (!store.isDataLoaded) return
  const next: QueueItem[] = []
  for (const k of getQuizQueueKeys()) {
    const p = parseItemKey(k)
    if (!p) continue
    const list = store.data[p.cat as 'nouns' | 'sentences' | 'kana']
    if (!Array.isArray(list)) continue
    const it = list.find((x) => x.id === p.id)
    if (it) next.push({ ...it, _cat: p.cat })
    else removeFromQuizQueue(p.cat, p.id)
  }
  items.value = next
  pickRandom()
}

function pickRandom() {
  const list = items.value
  if (list.length === 0) {
    currentItem.value = null
    return
  }
  if (list.length === 1) {
    currentItem.value = list[0]
  } else {
    let next: QueueItem
    do {
      next = list[Math.floor(Math.random() * list.length)]
    } while (next.id === currentItem.value?.id && next._cat === currentItem.value?._cat)
    currentItem.value = next
  }
  isAnswered.value = false
  // 根据持久化状态决定阶段
  const it = currentItem.value
  testPhase.value = it && hasPhase1Passed(it._cat, it.id) ? 'recall' : 'read'
}

/** 第一步通过：标记持久化，回到随机池 */
function passPhase1() {
  const it = currentItem.value
  if (!it) return
  markPhase1Passed(it._cat, it.id)
  pickRandom()
}

function markPassed() {
  stopLoop()
  passedCount.value++
  totalCount.value++
  isAnswered.value = true
  const it = currentItem.value
  if (!it) return
  clearQuizFails(it._cat, it.id)
  clearPhase1(it._cat, it.id)
  markMasteryQuizPassed(it._cat, it.id)
  removeFromQuizQueue(it._cat, it.id)
  // rebuild to remove passed item from pool
  const store = useAppStore()
  if (!store.isDataLoaded) return
  const next: QueueItem[] = []
  for (const k of getQuizQueueKeys()) {
    const p = parseItemKey(k)
    if (!p) continue
    const list = store.data[p.cat as 'nouns' | 'sentences' | 'kana']
    if (!Array.isArray(list)) continue
    const found = list.find((x) => x.id === p.id)
    if (found) next.push({ ...found, _cat: p.cat })
  }
  items.value = next
}

/** 跳过 = 不通过，累计 3 次打回（移出队列） */
function skip() {
  stopLoop()
  totalCount.value++
  const it = currentItem.value
  if (it) {
    const removed = recordQuizFail(it._cat, it.id)
    if (removed) {
      clearPhase1(it._cat, it.id)
      rebuildItems()
      return
    }
  }
  pickRandom()
}

function nextAfterPass() {
  pickRandom()
}

/** 从掌握测验队列移出，词条重新出现在「听」「练」 */
function returnToListenPractice() {
  const it = currentItem.value
  if (!it) return
  stopLoop()
  clearQuizFails(it._cat, it.id)
  clearPhase1(it._cat, it.id)
  removeFromQuizQueue(it._cat, it.id)
  rebuildItems()
}

function speakCurrent() {
  const it = currentItem.value
  if (!it) return
  speakWithExample(it.word, it.audio)
}

const hasItems = computed(() => items.value.length > 0)

export function useMasteryTest() {
  return {
    currentItem,
    isAnswered,
    passedCount,
    totalCount,
    hasItems,
    testPhase,
    rebuildItems,
    pickRandom,
    markPassed,
    passPhase1,
    skip,
    nextAfterPass,
    returnToListenPractice,
    speakCurrent,
  }
}
