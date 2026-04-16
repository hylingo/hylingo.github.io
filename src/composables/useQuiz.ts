import { ref, watch } from 'vue'
import { useAppStore, type DataItem } from '../stores/app'
import { recordQuiz } from './useStats'
import {
  recordStudy,
  recordSkip,
  markMastered,
  milestoneStateTick,
  hasMasteryQuizPassed,
  getMasteryQuizPassedMap,
} from '@/learning/milestones'
import { markArticlePracticeDone } from '@/learning/articlePracticeDone'
import { recordArticleShadowComplete } from '@/learning/articleProgress'
import { articleToPracticeQuizItems } from '@/utils/articleQuiz'
import { currentLang } from '@/i18n'
import {
  getDelays,
  getQuizProgressSnapshot,
} from './useSpacedRepetition'
import { makeItemKey, getStarredMap } from '@/learning'
import { useFirebase } from '@/composables/useFirebase'

export type QuizMode = 'word' | 'audio' | 'meaning'

const quizItems = ref<DataItem[]>([])
const quizIndex = ref(0)
const isAnswered = ref(false)
const quizLevels = ref<string[]>([])

/** 本篇逐句练习刚跑完，供练页展示完成态 */
export const articleBlockJustCompleted = ref<{ title: string; sentenceCount: number } | null>(null)

function isArticleQuizItem(it: unknown): it is { _quizSource: 'article'; _articleId: string } {
  return !!it && typeof it === 'object' && (it as { _quizSource?: string })._quizSource === 'article'
}


/**
 * 宽松 SRS 抽题：根据状态分桶 + 加权随机。
 *
 * 桶               权重     说明
 * ─────────────────────────────────────────────
 * 到期               100    counts>0 且 delays 已过期
 * 未学过              70    counts=0
 * 学习中未到期        30    counts>0 且 delays 未到
 * 已掌握               0    masteryQuizPassed=true，永不抽
 *
 * 加权随机用 reservoir-style：每条 key = -log(rand) / weight，按 key 升序取前 N。
 * 这等价于经典的 weighted random sampling without replacement。
 */

const POOL_SIZE = 30 // 一次抽多少条进入练习队列

const W_DUE = 100
const W_NEW = 70
const W_NOT_DUE = 30

/** 新词按难度加权：没选级别筛选时，简单的权重更高，让新词优先从 N5 起步 */
// 强偏置：N5 新词权重 ~= N4 的 6 倍，N3 的 20 倍。
// 效果：新词几乎只抽 N5，偶尔冒一个 N4，N5 抽完后才大量过渡到 N4/N3。
const LEVEL_EASY_BIAS: Record<string, number> = {
  N5: 5.0, N4: 0.8, N3: 0.25, N2: 0.08, N1: 0.03,
}
function newWeightByLevel(level?: string): number {
  if (!level) return W_NEW
  const mult = LEVEL_EASY_BIAS[level] ?? 1.0
  return W_NEW * mult
}

type PoolEntry = { it: DataItem & { _cat?: string }; weight: number }

function collectPool(cat: string, applyEasyBias: boolean): PoolEntry[] {
  const store = useAppStore()
  const delays = getDelays()
  const today = new Date().toISOString().slice(0, 10)
  const mastery = getMasteryQuizPassedMap()
  const snap = getQuizProgressSnapshot()
  const counts = snap.counts

  const pickCats: string[] =
    cat === 'mix'
      ? (['nouns', 'verbs'] as string[])
      : cat === 'starred'
        ? (['nouns', 'verbs'] as string[])
        : [cat]

  const starred = cat === 'starred' ? getStarredMap() : null
  const out: PoolEntry[] = []

  for (const c of pickCats) {
    const arr = (store.data as Record<string, DataItem[]>)[c]
    if (!Array.isArray(arr)) continue
    for (const it of arr) {
      const k = makeItemKey(c, it.id)
      if (mastery[k]) continue
      if (starred && !starred[k]) continue
      const cnt = counts[`${c}:${it.id}`] || 0
      let weight: number
      if (cnt === 0) {
        weight = applyEasyBias ? newWeightByLevel(it.level) : W_NEW
      } else {
        const due = delays[k]
        weight = !due || due <= today ? W_DUE : W_NOT_DUE
      }
      out.push({ it: { ...it, _cat: c }, weight })
    }
  }
  return out
}

/** 加权随机抽 N 条（无放回），key = -log(U) / w */
function weightedSample(pool: PoolEntry[], n: number): (DataItem & { _cat?: string })[] {
  if (pool.length === 0) return []
  const keyed = pool.map((e) => {
    const u = Math.random() || 1e-9
    return { it: e.it, k: -Math.log(u) / e.weight }
  })
  keyed.sort((a, b) => a.k - b.k)
  return keyed.slice(0, n).map((x) => x.it)
}

function startQuiz() {
  const store = useAppStore()
  const cat = store.currentCat

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

  // 宽松 SRS：分桶加权随机。没选级别筛选时，新词按 N5→N1 降权，优先抽简单的。
  const noLevelFilter = quizLevels.value.length === 0
  const pool = collectPool(cat, noLevelFilter).filter((e) => {
    if (noLevelFilter) return true
    return !!e.it.level && quizLevels.value.includes(e.it.level)
  })
  quizItems.value = weightedSample(pool, POOL_SIZE)
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

function hideAnswer() {
  isAnswered.value = false
}

/** 完成一次学习（录音/听写）：记次 + 推迟到 SRS 间隔 */
function submitStudy() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  if (isArticleQuizItem(it)) return
  const cat = it._cat || store.currentCat
  recordStudy(cat, it.id)
  recordQuiz(it, true, cat)
}

/** 主动看答案 / 跳过：算作"没记住"，counts 回退 + 临近重排 */
function submitSkip() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  if (isArticleQuizItem(it)) return
  const cat = it._cat || store.currentCat
  recordSkip(cat, it.id)
  recordQuiz(it, false, cat)
}

/** 用户点「掌握了」：标记掌握并进入下一题 */
function submitMastered() {
  const store = useAppStore()
  const it = quizItems.value[quizIndex.value]
  if (!it) return
  if (isArticleQuizItem(it)) {
    advanceIndex()
    return
  }
  const cat = it._cat || store.currentCat
  markMastered(cat, it.id)
  advanceIndex()
}

/** 跳到下一题（不改变学习状态，例如「看答案」后用户选择跳过） */
function nextQuestion() {
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
      recordArticleShadowComplete(store.studyLang, cur._articleId)
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
    hideAnswer,
    submitStudy,
    submitSkip,
    submitMastered,
    nextQuestion,
    dismissArticleBlockComplete,
  }
}
