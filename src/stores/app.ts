import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import type { ArticleItem, GrammarPoint, StudyLang } from '@/types'
import { clearMilestoneCache } from '@/learning/milestones'
import { safeSet } from '@/storage/safeLS'
import { LS } from '@/storage/keys'
import { showError } from '@/composables/useToasts'
import { t as i18nT } from '@/i18n'
import { readPracticeSlot } from '@/storage/practiceSlot'
import { KANA_DATA } from '@/data/kana'
import { fetchVocabBundle, fetchArticleBundle } from '@/data/dataLoader'
import { usePracticeArticle, catToFormat } from '@/composables/usePracticeArticle'

export interface DataItem {
  id: number
  word: string
  reading: string
  meaning: string
  meaningEn?: string
  meaningJp?: string
  example?: string
  exampleCn?: string
  audio?: string
  audioExample?: string
  topic?: string
  level?: string
  ruby?: { t: string; r?: string }[]
  _cat?: string
  _audioFn?: string
  _articleId?: string
  /** 标记为本篇精读练习的题目（来自 articleToPracticeQuizItems） */
  _quizSource?: 'article'
}

export interface AppData {
  nouns: DataItem[]
  verbs: DataItem[]
  kana: DataItem[]
}

export const useAppStore = defineStore('app', () => {
  const router = useRouter()
  const route = router.currentRoute

  // ---- 路由派生状态：URL 是真相源 ----
  const studyLang = computed<StudyLang>(
    () => ((route.value.params.lang as StudyLang) || 'ja'),
  )
  const currentCat = computed<string>(
    () => (route.value.params.cat as string) || 'articles',
  )
  const currentMode = computed<string>(() => {
    const n = route.value.name
    if (n === 'practice' || n === 'practice-article') return 'practice'
    if (n === 'stats') return 'stats'
    return 'list'
  })

  // ---- 远端数据 in-memory 缓存 ----
  const data = ref<AppData>({ nouns: [], verbs: [], kana: KANA_DATA })
  /** 精读文章（短文 / 对话）：日语 ja_articles.json，英语 en_articles.json */
  const articles = ref<ArticleItem[]>([])
  /** 语法点（按 id 索引） */
  const grammarMap = ref<Record<string, GrammarPoint>>({})
  const isDataLoaded = ref(false)
  const isArticlesLoaded = ref(false)
  let _articlesLoadPromise: Promise<void> | null = null

  // 文章详情是否打开（仅 UI 状态：决定是否隐藏全局分类 tab）
  const articleDetailOpen = ref(false)

  // ---- 本篇精读练习状态机：抽到 composable ----
  const {
    practiceArticleId,
    practiceArticleTitle,
    practiceArticleIndex,
    startArticlePractice,
    clearArticlePractice,
    savePracticeArticleIndex,
    restorePracticeArticleFromLS,
  } = usePracticeArticle({ articles, studyLang, currentCat })

  // ---- 数据加载 ----

  async function loadData() {
    try {
      const bundle = await fetchVocabBundle(studyLang.value)
      data.value.nouns = bundle.nouns
      data.value.verbs = bundle.verbs
      isDataLoaded.value = true
      // 切换语言后 articles 也要重新加载
      _articlesLoadPromise = null
      isArticlesLoaded.value = false
    } catch (e) {
      console.error('Failed to load data', e)
      throw e
    }
  }

  /** 按需加载 articles + grammar（首次调用触发 fetch，后续复用 in-flight promise） */
  async function ensureArticles(): Promise<void> {
    if (isArticlesLoaded.value) return
    if (_articlesLoadPromise) return _articlesLoadPromise
    _articlesLoadPromise = _loadArticles()
    return _articlesLoadPromise
  }

  async function _loadArticles(): Promise<void> {
    try {
      const bundle = await fetchArticleBundle(studyLang.value)
      articles.value = bundle.articles
      grammarMap.value = bundle.grammarMap
      isArticlesLoaded.value = true

      // 若 URL 上的 articleId 在最新数据里找不到，清掉并退回 practice 列表
      if (practiceArticleId.value) {
        const art = articles.value.find((a) => a.id === practiceArticleId.value)
        if (!art) {
          clearArticlePractice()
        } else {
          // 触发 watcher 重新填 title/index
          restorePracticeArticleFromLS()
        }
      }
    } catch (e) {
      console.error('Failed to load articles', e)
      _articlesLoadPromise = null
      showError(i18nT('toastArticlesLoadFailed') || '文章数据加载失败', {
        actionLabel: i18nT('retry') || '重试',
        onAction: () => { void ensureArticles() },
      })
    }
  }

  // ---- 语言切换 ----

  // 持久化 study_lang，供 / 重定向使用
  watch(
    studyLang,
    (lang) => { safeSet(LS.STUDY_LANG, lang) },
    { immediate: true },
  )

  // lang 变化：清缓存 + 重新拉数据（watch 仅在值真正变化时触发，无需手动 guard）
  watch(studyLang, async () => {
    clearMilestoneCache()
    try {
      await loadData()
    } catch {
      showError(i18nT('toastDataLoadFailed') || '数据加载失败', {
        actionLabel: i18nT('retry') || '重试',
        onAction: () => { void loadData().catch(() => {}) },
      })
      return
    }
    // loadData 重置了 isArticlesLoaded；若当前页/练习需要 articles，重新触发加载
    if (
      currentCat.value === 'articles' ||
      currentCat.value === 'dialogues' ||
      practiceArticleId.value
    ) {
      ensureArticles()
    }
  })

  async function switchStudyLang(lang: StudyLang) {
    if (studyLang.value === lang) return
    // 切语言时落到一个安全的 cat
    let cat = currentCat.value
    if (lang === 'en' && cat === 'kana') cat = 'articles'
    if (lang === 'en' && cat === 'verbs') cat = 'nouns'
    await router.push({ name: 'list', params: { lang, cat } })
  }

  // ---- 模式 / 分类切换 ----

  function switchMode(mode: string) {
    const lang = studyLang.value
    if (mode === 'stats') {
      router.push({ name: 'stats', params: { lang } })
      return
    }
    if (mode === 'practice') {
      // 文章/对话分类下：尝试恢复 LS 槽位 → 直接进 article practice；
      // 否则回退到 nouns 词练习（保留原行为）
      const fmt = catToFormat(currentCat.value)
      const slot = fmt ? readPracticeSlot(fmt) : null
      if (slot) {
        ensureArticles()
        router.push({
          name: 'practice-article',
          params: { lang, cat: currentCat.value, articleId: slot.id },
        })
      } else {
        const cat =
          currentCat.value === 'articles' || currentCat.value === 'dialogues'
            ? 'nouns'
            : currentCat.value
        router.push({ name: 'practice', params: { lang, cat } })
      }
      return
    }
    // list
    router.push({ name: 'list', params: { lang, cat: currentCat.value } })
  }

  function switchCat(cat: string) {
    const lang = studyLang.value
    if (cat === 'articles' || cat === 'dialogues') ensureArticles()
    // 在练习模式下切 cat：保持 practice 路由，并尝试恢复对应 cat 的文章槽位
    if (currentMode.value === 'practice') {
      const fmt = cat === 'articles' ? 'essay' : cat === 'dialogues' ? 'dialogue' : null
      const slot = fmt ? readPracticeSlot(fmt) : null
      if (slot) {
        router.push({
          name: 'practice-article',
          params: { lang, cat, articleId: slot.id },
        })
      } else {
        router.push({ name: 'practice', params: { lang, cat } })
      }
      return
    }
    router.push({ name: 'list', params: { lang, cat } })
  }

  return {
    // 路由派生状态
    studyLang,
    currentMode,
    currentCat,
    // UI 状态
    articleDetailOpen,
    // 远端数据
    data,
    articles,
    grammarMap,
    isDataLoaded,
    isArticlesLoaded,
    loadData,
    ensureArticles,
    // 本篇练习
    practiceArticleId,
    practiceArticleTitle,
    practiceArticleIndex,
    startArticlePractice,
    clearArticlePractice,
    savePracticeArticleIndex,
    restorePracticeArticleFromLS,
    // 切换动作
    switchStudyLang,
    switchMode,
    switchCat,
  }
})
