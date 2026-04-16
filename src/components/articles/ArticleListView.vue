<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'
import type { ArticleItem, ArticleEssay, ArticleDialogue } from '@/types'
import AppIcon from '@/components/common/AppIcon.vue'
import ArticleCover from '@/components/common/ArticleCover.vue'
import { getAllArticleProgress, type ArticleProgressEntry } from '@/learning/articleProgress'
import { isArticleFullyPerfect, getPerfectSentencesOf, articlePerfectTick } from '@/learning/articlePerfect'
import { flatArticleSegments } from '@/utils/articleQuiz'

const props = defineProps<{ filterFormat: 'essay' | 'dialogue' }>()
const emit = defineEmits<{ select: [id: string] }>()

const store = useAppStore()
const { t, currentLang } = useLang()

const articleSearch = ref('')

// 文章级进度（完整听 / 跟读次数）
const progressMap = ref<Record<string, ArticleProgressEntry>>({})
function refreshProgressMap() {
  progressMap.value = getAllArticleProgress(store.studyLang)
}
onMounted(refreshProgressMap)
watch(() => store.studyLang, refreshProgressMap)
// 父组件回到列表时也刷新一次（通过暴露的方法）
defineExpose({ refreshProgressMap })

/** 每篇文章的满分句数 / 总句数 */
function sentenceProgress(articleId: string): { perfected: number; total: number } {
  articlePerfectTick.value
  const art = store.articles.find((a) => a.id === articleId)
  if (!art) return { perfected: 0, total: 0 }
  const total = flatArticleSegments(art).length
  const set = getPerfectSentencesOf(articleId)
  let perfected = 0
  for (let i = 0; i < total; i++) {
    if (set[String(i)]) perfected++
  }
  return { perfected, total }
}

const levelOrder: Record<string, number> = { N5: 0, N4: 1, N3: 2, N2: 3, N1: 4 }
function levelSortKey(level: string): number {
  const m = level.match(/N[1-5]/g)
  if (!m) return 9
  return Math.min(...m.map((l) => levelOrder[l] ?? 9))
}

const list = computed(() =>
  store.articles
    .filter((a) => a.format === props.filterFormat && !(a as { hidden?: boolean }).hidden)
    .slice()
    .sort((a, b) => levelSortKey(a.level) - levelSortKey(b.level)),
)

/** 跨 essay+dialogue 全文搜索；返回 null 表示未输入查询词 */
const searchResults = computed<{ article: ArticleItem; matches: string[] }[] | null>(() => {
  const q = articleSearch.value.trim().toLowerCase()
  if (!q) return null
  const results: { article: ArticleItem; matches: string[] }[] = []
  for (const a of store.articles) {
    if ((a as { hidden?: boolean }).hidden) continue
    const hits: string[] = []
    if (a.format === 'essay') {
      for (const s of (a as ArticleEssay).segments ?? []) {
        if (
          s.word.toLowerCase().includes(q) ||
          s.zh?.toLowerCase().includes(q) ||
          s.en?.toLowerCase().includes(q)
        ) {
          hits.push(s.word)
        }
      }
    } else {
      for (const sec of (a as ArticleDialogue).sections ?? []) {
        for (const l of sec.lines ?? []) {
          if (
            l.word.toLowerCase().includes(q) ||
            l.zh?.toLowerCase().includes(q) ||
            l.en?.toLowerCase().includes(q)
          ) {
            hits.push(`${l.speaker}: ${l.word}`)
          }
        }
      }
    }
    if (
      a.titleWord?.toLowerCase().includes(q) ||
      a.titleZh?.toLowerCase().includes(q) ||
      a.titleEn?.toLowerCase().includes(q)
    ) {
      if (!hits.length) hits.push(a.titleWord)
    }
    if (hits.length) results.push({ article: a, matches: hits.slice(0, 3) })
  }
  return results
})

function isFullyPerfect(it: ArticleItem): boolean {
  articlePerfectTick.value
  const total = flatArticleSegments(it).length
  return isArticleFullyPerfect(it.id, total)
}

function formatLabel(it: ArticleItem) {
  const kind = it.format === 'essay' ? t('articleKindEssay') : t('articleKindDialogue')
  return `${it.level} · ${kind}`
}

function openItem(id: string) {
  articleSearch.value = ''
  emit('select', id)
}
</script>

<template>
  <div class="space-y-3 pt-1">
    <!-- 搜索框 -->
    <div class="relative">
      <input
        v-model="articleSearch"
        type="text"
        :placeholder="t('search')"
        class="w-full rounded-xl border border-[var(--border)] bg-transparent py-2 pr-3 pl-9 text-sm theme-text outline-none transition-[border-color,box-shadow] focus:border-[var(--primary)] focus:shadow-[0_0_0_3px_color-mix(in_srgb,var(--primary)_18%,transparent)]"
      />
      <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 theme-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
      </svg>
    </div>

    <!-- 搜索结果 -->
    <template v-if="searchResults">
      <p class="text-xs theme-muted">{{ searchResults.length }} 篇文章匹配</p>
      <button
        v-for="r in searchResults"
        :key="r.article.id"
        type="button"
        class="w-full text-left rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-4 pl-5 transition hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] active:scale-[0.99] cursor-pointer border-0 border-l-[3px] border-l-[var(--primary)]/40"
        @click="openItem(r.article.id)"
      >
        <div class="flex items-start gap-3">
          <ArticleCover
            v-if="false"
            :article-id="r.article.id"
            variant="thumb"
            :icon="r.article.format === 'dialogue' ? 'chat' : 'book'"
            :alt="r.article.titleWord"
          />
          <div class="min-w-0 flex-1">
            <div class="text-[11px] font-medium theme-muted mb-1.5 tracking-wide">
              <AppIcon :name="r.article.format === 'dialogue' ? 'chat' : 'book'" :size="14" />
              {{ formatLabel(r.article) }}
            </div>
            <div class="text-base font-bold text-content-original leading-snug">{{ r.article.titleWord }}</div>
            <div class="mt-1.5 space-y-0.5">
              <p v-for="(m, i) in r.matches" :key="i" class="text-xs theme-muted truncate">…{{ m }}…</p>
            </div>
          </div>
        </div>
      </button>
      <p v-if="!searchResults.length" class="text-sm theme-muted py-8 text-center">未找到匹配内容</p>
    </template>

    <!-- 正常列表 -->
    <template v-else>
      <p class="text-sm theme-muted mb-3">
        {{ props.filterFormat === 'dialogue' ? t('dialogueIntro') : t('articleIntro') }}
      </p>
      <button
        v-for="it in list"
        :key="it.id"
        type="button"
        class="relative w-full text-left rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-4 pl-5 transition hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] active:scale-[0.99] cursor-pointer border-0 border-l-[3px] border-l-[var(--primary)]/40"
        @click="openItem(it.id)"
      >
        <span
          class="absolute top-2.5 right-3 flex items-center gap-1.5 text-[10px] tabular-nums theme-muted"
          :class="sentenceProgress(it.id).perfected > 0 ? 'opacity-70' : 'opacity-35'"
        >
          <span>{{ sentenceProgress(it.id).perfected }}/{{ sentenceProgress(it.id).total }}</span>
          <span v-if="isArticleFullyPerfect(it.id, sentenceProgress(it.id).total)" style="color: var(--primary)">✓</span>
        </span>
        <div class="flex items-start gap-3">
          <ArticleCover
            v-if="false"
            :article-id="it.id"
            variant="thumb"
            :icon="it.format === 'dialogue' ? 'chat' : 'book'"
            :alt="it.titleWord"
          />
          <div class="min-w-0 flex-1">
            <div class="text-[11px] font-medium theme-muted mb-1.5 tracking-wide">{{ formatLabel(it) }}</div>
            <div class="text-base font-bold text-content-original leading-snug">
              <span v-if="isFullyPerfect(it)" class="mr-1 align-middle" title="全篇已满分" aria-label="全篇已满分">👑</span>
              {{ it.titleWord }}
            </div>
            <div v-if="currentLang === 'zh'" class="text-sm mt-1 text-content-translation">{{ it.titleZh }}</div>
            <div v-else-if="currentLang === 'en'" class="text-sm mt-1 text-content-translation opacity-90">{{ it.titleEn }}</div>
            <div v-else class="text-sm mt-1 text-content-translation opacity-90">{{ it.titleJp ?? it.titleZh }}</div>
          </div>
        </div>
      </button>
      <p v-if="!list.length" class="text-sm theme-muted py-8 text-center">{{ t('articleEmpty') }}</p>
    </template>
  </div>
</template>
