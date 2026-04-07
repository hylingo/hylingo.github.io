/**
 * 本篇精读练习状态机：
 *  - articleId 是 URL 真相源（route.params.articleId），computed 派生
 *  - title / index 是 in-memory 元数据，从 articles[] 或 LS 槽位回填
 *  - 用 LS 槽位（按 essay/dialogue 分别存）持久化"上一次在练哪篇"
 *
 * 抽出于原 src/stores/app.ts，store 现在通过 import 此 composable 组装。
 *
 * 依赖：调用方（store）必须传入：
 *  - articles ref（用于通过 id 反查 format/title）
 *  - studyLang / currentCat computed（决定写哪个 LS 槽位、navigate 时的 params）
 */
import { computed, ref, watch, type ComputedRef, type Ref } from 'vue'
import type { ArticleItem, StudyLang } from '@/types'
import { useRouter } from 'vue-router'
import {
  readPracticeSlot,
  writePracticeSlot,
  writePracticeSlotIndex,
  type PracticeSlot,
} from '@/storage/practiceSlot'

/** essay / dialogue / null（其他分类没有本篇练习概念） */
export function catToFormat(cat: string): 'essay' | 'dialogue' | null {
  if (cat === 'articles') return 'essay'
  if (cat === 'dialogues') return 'dialogue'
  return null
}

interface PracticeArticleDeps {
  articles: Ref<ArticleItem[]>
  studyLang: ComputedRef<StudyLang>
  currentCat: ComputedRef<string>
}

export function usePracticeArticle(deps: PracticeArticleDeps) {
  const { articles, studyLang, currentCat } = deps
  const router = useRouter()
  const route = router.currentRoute

  // articleId 直接从 URL 派生
  const practiceArticleId = computed<string | null>(
    () => (route.value.params.articleId as string) || null,
  )
  const practiceArticleTitle = ref('')
  const practiceArticleIndex = ref(0)

  /** 用当前 articleId 从 articles[]/LS 重新填 title 和 index。 */
  function reloadTitleAndIndex(id: string | null) {
    if (!id) {
      practiceArticleTitle.value = ''
      practiceArticleIndex.value = 0
      return
    }
    const art = articles.value.find((a) => a.id === id)
    const fmt = art?.format || catToFormat(currentCat.value)
    const slot = fmt ? readPracticeSlot(fmt) : null
    if (slot && slot.id === id) {
      practiceArticleTitle.value = slot.title || art?.titleWord || ''
      practiceArticleIndex.value = slot.index
    } else {
      practiceArticleTitle.value = art?.titleWord || ''
      practiceArticleIndex.value = 0
    }
  }

  // articleId 变化时自动同步 title/index
  watch(practiceArticleId, (id) => reloadTitleAndIndex(id), { immediate: true })

  /** 启动一篇文章的练习：写 LS 槽位 + push 路由到 /:lang/:cat/practice/:articleId */
  function startArticlePractice(articleId: string) {
    const art = articles.value.find((a) => a.id === articleId)
    if (!art) return
    const fmt = art.format // 'essay' | 'dialogue'
    const targetCat = fmt === 'dialogue' ? 'dialogues' : 'articles'
    const slot: PracticeSlot = { id: articleId, title: art.titleWord ?? '', index: 0 }
    writePracticeSlot(fmt, slot)
    practiceArticleTitle.value = slot.title
    practiceArticleIndex.value = 0
    router.push({
      name: 'practice-article',
      params: { lang: studyLang.value, cat: targetCat, articleId },
    })
  }

  /** 清除当前篇练习：擦 LS 槽位 + 若 URL 还在 article practice 路由就 replace 出去 */
  function clearArticlePractice() {
    const fmt = catToFormat(currentCat.value)
    if (fmt) writePracticeSlot(fmt, null)
    practiceArticleTitle.value = ''
    practiceArticleIndex.value = 0
    if (route.value.name === 'practice-article') {
      router.replace({
        name: 'practice',
        params: { lang: studyLang.value, cat: currentCat.value },
      })
    }
  }

  /** 用户答完一题后保存进度（仅写 index 槽位） */
  function savePracticeArticleIndex(index: number) {
    practiceArticleIndex.value = index
    const art = articles.value.find((a) => a.id === practiceArticleId.value)
    const fmt = art?.format || catToFormat(currentCat.value)
    if (fmt) writePracticeSlotIndex(fmt, index)
  }

  /** 云端 pull 之后调一次：用 URL 的 articleId 重读 LS（slot 可能被云端覆盖了） */
  function restorePracticeArticleFromLS() {
    reloadTitleAndIndex(practiceArticleId.value)
  }

  return {
    practiceArticleId,
    practiceArticleTitle,
    practiceArticleIndex,
    startArticlePractice,
    clearArticlePractice,
    savePracticeArticleIndex,
    restorePracticeArticleFromLS,
  }
}
