import { ref, watch } from 'vue'
import { useAppStore } from '../stores/app'
import { recordQuiz } from './useStats'
import { readQuizScopeRaw, writeQuizScopeRaw, studyLangFromLocalStorage } from '@/learning/learnStorage'
import { makeItemKey } from '@/learning/itemKey'
import { quizQueueTick, getQuizQueueKeys, addToQuizQueue, removeFromQuizQueue, recordQuizFail, clearQuizFails } from '@/learning'
import { markPracticeAnswerKnown, markPracticeAnswerUnknown, milestoneStateTick, hasMasteryQuizPassed, markMasteryQuizPassed } from '@/learning/milestones'
import {
  getActiveItems,
  getQuizProgressSnapshot,
  snapIsListenedToday,
  snapListenCount,
  snapItemCount,
  type QuizProgressSnapshot,
} from './useSpacedRepetition'
import { quiz as quizThresholds } from '@/config/thresholds'

export type QuizMode = 'word' | 'audio' | 'meaning'
export type QuizScope = 'practice' | 'test'

const NEW_BATCH_SIZE = quizThresholds.newBatchSize

const quizItems = ref<any[]>([])
const quizIndex = ref(0)
const isAnswered = ref(false)
const quizLevels = ref<string[]>([])

function migrateQuizScope(): QuizScope {
  const s = readQuizScopeRaw(studyLangFromLocalStorage())
  if (s === 'practice' || s === 'test') return s
  return 'practice'
}

const quizScope = ref<QuizScope>(migrateQuizScope())

function filterByLevel(items: any[]): any[] {
  if (quizLevels.value.length === 0) return items
  return items.filter((it) => it.level && quizLevels.value.includes(it.level))
}

function isBrandNewItem(it: { _cat?: string; id: number }, cat: string, snap: QuizProgressSnapshot) {
  const c = it._cat || cat
  return snapListenCount(snap, c, it.id) === 0 && snapItemCount(snap, c, it.id) === 0
}

/** 练习池排序：优先今天听过 > 听过次数 > 练习次数 */
function sortPracticePool(items: any[], cat: string, snap: QuizProgressSnapshot) {
  const copy = [...items]
  copy.sort(() => Math.random() - 0.5)
  copy.sort((a, b) => {
    const ca = a._cat || cat
    const cb = b._cat || cat
    const ta = snapIsListenedToday(snap, ca, a.id) ? 1 : 0
    const tb = snapIsListenedToday(snap, cb, b.id) ? 1 : 0
    if (tb !== ta) return tb - ta
    const la = snapListenCount(snap, ca, a.id)
    const lb = snapListenCount(snap, cb, b.id)
    if (lb !== la) return lb - la
    return snapItemCount(snap, cb, b.id) - snapItemCount(snap, ca, a.id)
  })
  return copy
}

function startQuiz() {
  const store = useAppStore()
  const cat = store.currentCat
  const snap = getQuizProgressSnapshot()

  if (quizScope.value === 'practice') {
    // 练习：听过/练过的（排除已掌握），空了补全新的
    let items = filterByLevel([...getActiveItems(cat)])
      .filter((it) => !hasMasteryQuizPassed(it._cat || cat, it.id))

    // 先取已接触过的
    let studied = items.filter((it) => !isBrandNewItem(it, cat, snap))

    // 如果已接触的不够，补充全新的
    if (studied.length < NEW_BATCH_SIZE) {
      const brandNew = items.filter((it) => isBrandNewItem(it, cat, snap))
        .sort(() => Math.random() - 0.5)
        .slice(0, NEW_BATCH_SIZE - studied.length)
      studied = [...studied, ...brandNew]
    }

    quizItems.value = sortPracticePool(studied, cat, snap)
    quizIndex.value = 0
    isAnswered.value = false
    return
  }

  // 测试：从队列取（跨分类）
  const keys = getQuizQueueKeys()
  const allPool = new Map<string, any>()
  for (const c of ['nouns', 'sentences'] as const) {
    for (const it of (store.data[c] || [])) {
      allPool.set(makeItemKey(c, it.id), { ...it, _cat: c })
    }
  }
  const testItems = keys
    .map((k) => allPool.get(k))
    .filter(Boolean)
    .filter((it: any) => !hasMasteryQuizPassed(it._cat, it.id)) as any[]

  quizItems.value = testItems.sort(() => Math.random() - 0.5)
  quizIndex.value = 0
  isAnswered.value = false
}

function setQuizScope(scope: QuizScope) {
  if (quizScope.value === scope) return
  quizScope.value = scope
  writeQuizScopeRaw(useAppStore().studyLang, scope)
  startQuiz()
}

function showAnswer() {
  isAnswered.value = true
}

/** 练习模式：认识 → 加入测试队列 */
function submitCorrect() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  const cat = it._cat || store.currentCat
  markPracticeAnswerKnown(cat, it.id)
  addToQuizQueue(cat, it.id)
  recordQuiz(it, true, cat)
  advanceIndex()
}

/** 练习模式：不认识 */
function submitWrong() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  const cat = it._cat || store.currentCat
  markPracticeAnswerUnknown(cat, it.id)
  recordQuiz(it, false, cat)
  // 不 advance，等用户看完答案点下一个
}

/** 不认识看完答案后，下一个 */
function advanceAfterWrong() {
  advanceIndex()
}

/** 测试模式：掌握通过 */
function testPass() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  const cat = it._cat || store.currentCat
  markMasteryQuizPassed(cat, it.id)
  removeFromQuizQueue(cat, it.id)
  clearQuizFails(cat, it.id)
  advanceIndex()
}

/** 测试模式：失败一次，返回是否被打回 */
function testFail(): boolean {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return false
  const cat = it._cat || store.currentCat
  return recordQuizFail(cat, it.id)
}

/** 测试模式：失败3次被打回后，下一个 */
function testAdvance() {
  advanceIndex()
}

function advanceIndex() {
  quizIndex.value++
  isAnswered.value = false
  if (quizIndex.value >= quizItems.value.length) {
    quizIndex.value = 0
    startQuiz() // 重新加载池
  }
}

function setQuizLevels(levels: string[]) {
  quizLevels.value = levels
  startQuiz()
}

let quizWatchersBound = false

function bindQuizWatchersOnce() {
  if (quizWatchersBound) return
  quizWatchersBound = true

  watch(
    () => useAppStore().studyLang,
    () => {
      quizScope.value = migrateQuizScope()
      startQuiz()
    },
  )

  watch([milestoneStateTick, quizQueueTick], () => {
    const store = useAppStore()
    const cat = store.currentCat
    const before = quizItems.value.length
    quizItems.value = quizItems.value.filter((it) => {
      const c = it._cat || cat
      return !hasMasteryQuizPassed(c, it.id)
    })
    if (quizItems.value.length !== before && quizIndex.value >= quizItems.value.length) {
      quizIndex.value = Math.max(0, quizItems.value.length - 1)
    }
  })
}

export function useQuiz() {
  bindQuizWatchersOnce()
  return {
    quizItems,
    quizIndex,
    isAnswered,
    quizScope,
    quizLevels,
    startQuiz,
    setQuizLevels,
    showAnswer,
    submitCorrect,
    submitWrong,
    advanceAfterWrong,
    testPass,
    testFail,
    testAdvance,
    setQuizScope,
  }
}
