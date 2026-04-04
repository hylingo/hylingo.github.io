import { ref, watch } from 'vue'
import { useAppStore } from '../stores/app'
import { recordQuiz } from './useStats'
import {
  markPracticeAnswerKnown,
  markPracticeAnswerUnknown,
  milestoneStateTick,
  hasMasteryQuizPassed,
} from '@/learning/milestones'
import { markArticlePracticeDone } from '@/learning/articlePracticeDone'
import { articleToPracticeQuizItems } from '@/utils/articleQuiz'
import { currentLang } from '@/i18n'
import {
  getActiveItems,
  getQuizProgressSnapshot,
  snapIsListenedToday,
  snapListenCount,
  snapItemCount,
  type QuizProgressSnapshot,
} from './useSpacedRepetition'
import { quiz as quizThresholds } from '@/config/thresholds'
import { useFirebase } from '@/composables/useFirebase'

export type QuizMode = 'word' | 'audio' | 'meaning'

const NEW_BATCH_SIZE = quizThresholds.newBatchSize

const quizItems = ref<any[]>([])
const quizIndex = ref(0)
const isAnswered = ref(false)
const quizLevels = ref<string[]>([])

/** 本篇逐句练习刚跑完，供练页展示完成态 */
export const articleBlockJustCompleted = ref<{ title: string; sentenceCount: number } | null>(null)

function isArticleQuizItem(it: unknown): it is { _quizSource: 'article'; _articleId: string } {
  return !!it && typeof it === 'object' && (it as { _quizSource?: string })._quizSource === 'article'
}


function filterByLevel(items: any[]): any[] {
  if (quizLevels.value.length === 0) return items
  return items.filter((it) => it.level && quizLevels.value.includes(it.level))
}

function isBrandNewItem(it: { _cat?: string; id: number }, cat: string, snap: QuizProgressSnapshot) {
  const c = it._cat || cat
  return snapListenCount(snap, c, it.id) === 0 && snapItemCount(snap, c, it.id) === 0
}

/** 练习池排序：优先今天听过 > 听过次数 > 练习次数（先算好键再 sort，避免比较器里重复读 snapshot） */
function sortPracticePool(items: any[], cat: string, snap: QuizProgressSnapshot) {
  const decorated = items.map((it) => {
    const c = it._cat || cat
    return {
      it,
      r: Math.random(),
      t: snapIsListenedToday(snap, c, it.id) ? 1 : 0,
      l: snapListenCount(snap, c, it.id),
      ic: snapItemCount(snap, c, it.id),
    }
  })
  decorated.sort((a, b) => {
    if (b.t !== a.t) return b.t - a.t
    if (b.l !== a.l) return b.l - a.l
    if (b.ic !== a.ic) return b.ic - a.ic
    return a.r - b.r
  })
  return decorated.map((d) => d.it)
}

function startQuiz() {
  const store = useAppStore()
  const cat = store.currentCat
  const snap = getQuizProgressSnapshot()

  articleBlockJustCompleted.value = null

  if (store.practiceArticleId && (cat === 'articles' || cat === 'dialogues')) {
    const art = store.articles.find((a) => a.id === store.practiceArticleId)
    const formatMatch = art && ((cat === 'articles' && art.format === 'essay') || (cat === 'dialogues' && art.format === 'dialogue'))
    if (!art) {
      store.clearArticlePractice()
    } else if (formatMatch) {
      const items = articleToPracticeQuizItems(art, currentLang.value)
      quizItems.value = items
      const saved = store.practiceArticleIndex
      quizIndex.value = saved > 0 && saved < items.length ? saved : 0
      isAnswered.value = false
      return
    }
  }

  // 练习：听过/练过的（排除已掌握），空了补全新的
  let items = filterByLevel([...getActiveItems(cat)])

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
}

/** 同一事件环内多次触发（如同时改 practiceArticleId + mode）合并为一次抽题 */
let practiceStartQuizCoalesce = false
export function schedulePracticeStartQuiz() {
  if (practiceStartQuizCoalesce) return
  practiceStartQuizCoalesce = true
  queueMicrotask(() => {
    practiceStartQuizCoalesce = false
    if (useAppStore().currentMode === 'practice') startQuiz()
  })
}


function showAnswer() {
  isAnswered.value = true
}

/** 练习模式：认识 */
function submitCorrect() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  if (isArticleQuizItem(it)) {
    advanceIndex()
    return
  }
  const cat = it._cat || store.currentCat
  markPracticeAnswerKnown(cat, it.id)
  recordQuiz(it, true, cat)
  advanceIndex()
}

/** 练习模式：不认识（若 UI 调用；当前练页主要由 showAnswer + advanceAfterWrong 驱动） */
function submitWrong() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  if (isArticleQuizItem(it)) return
  const cat = it._cat || store.currentCat
  markPracticeAnswerUnknown(cat, it.id)
  recordQuiz(it, false, cat)
}

/** 不认识看完答案后，下一个 */
function advanceAfterWrong() {
  advanceIndex()
}


function advanceIndex() {
  const store = useAppStore()
  const cur = quizItems.value[quizIndex.value]
  const inArticleBlock =
    quizItems.value.length > 0 && isArticleQuizItem(quizItems.value[0])

  quizIndex.value++
  isAnswered.value = false

  // 本篇练习：保存进度
  if (inArticleBlock) {
    store.savePracticeArticleIndex(quizIndex.value)
    useFirebase().debouncedSync()
  }

  if (quizIndex.value >= quizItems.value.length) {
    if (inArticleBlock && cur && isArticleQuizItem(cur)) {
      const n = quizItems.value.length
      const title = store.practiceArticleTitle || store.articles.find((a) => a.id === cur._articleId)?.titleWord || ''
      markArticlePracticeDone(store.studyLang, cur._articleId)
      articleBlockJustCompleted.value = { title, sentenceCount: n }
      store.clearArticlePractice()
      useFirebase().debouncedSync()
      quizItems.value = []
      quizIndex.value = 0
      return
    }
    quizIndex.value = 0
    startQuiz() // 重新加载池
  }
}

export function dismissArticleBlockComplete() {
  articleBlockJustCompleted.value = null
  startQuiz()
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
      startQuiz()
    },
  )

  watch(milestoneStateTick, () => {
    const store = useAppStore()
    if (quizItems.value.length && isArticleQuizItem(quizItems.value[0])) return
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
    quizLevels,
    articleBlockJustCompleted,
    schedulePracticeStartQuiz,
    startQuiz,
    setQuizLevels,
    showAnswer,
    submitCorrect,
    submitWrong,
    advanceAfterWrong,
    dismissArticleBlockComplete,
  }
}
