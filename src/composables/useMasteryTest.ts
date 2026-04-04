import { ref, computed } from 'vue'
import { useAppStore, type DataItem } from '../stores/app'
import {
  getQuizQueueKeys,
  removeFromQuizQueue,
  markMasteryQuizPassed,
  parseItemKey,
} from '@/learning'
import { speakWithExample, stopLoop } from './useAudio'

type QueueItem = DataItem & { _cat: string }

const items = ref<QueueItem[]>([])
const currentItem = ref<QueueItem | null>(null)
const isAnswered = ref(false)
const passedCount = ref(0)
const totalCount = ref(0)

function rebuildItems() {
  const store = useAppStore()
  if (!store.isDataLoaded) return
  const next: QueueItem[] = []
  for (const k of getQuizQueueKeys()) {
    const p = parseItemKey(k)
    if (!p) continue
    const list = store.data[p.cat as 'nouns' | 'verbs' | 'kana']
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
}

function markPassed() {
  stopLoop()
  passedCount.value++
  totalCount.value++
  isAnswered.value = true
  const it = currentItem.value
  if (!it) return
  markMasteryQuizPassed(it._cat, it.id)
  removeFromQuizQueue(it._cat, it.id)
  // rebuild to remove passed item from pool
  const store = useAppStore()
  if (!store.isDataLoaded) return
  const next: QueueItem[] = []
  for (const k of getQuizQueueKeys()) {
    const p = parseItemKey(k)
    if (!p) continue
    const list = store.data[p.cat as 'nouns' | 'verbs' | 'kana']
    if (!Array.isArray(list)) continue
    const found = list.find((x) => x.id === p.id)
    if (found) next.push({ ...found, _cat: p.cat })
  }
  items.value = next
}

/** 跳过：直接下一个 */
function skip() {
  stopLoop()
  totalCount.value++
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
    rebuildItems,
    pickRandom,
    markPassed,
    skip,
    nextAfterPass,
    returnToListenPractice,
    speakCurrent,
  }
}
