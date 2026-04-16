<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '../../stores/app'
import type { VocabItemWithCat } from '../../types'
import {
  getMasteryQuizPassedMap,
  milestoneStateTick,
  starredTick,
  getStarredMap,
} from '@/learning'
import { useQuiz } from '@/composables/useQuiz'
import ListToolbar, { type ListReviewFilter } from './ListToolbar.vue'
import ListContainer from './ListContainer.vue'
import PaginationBar from '../common/PaginationBar.vue'
import { getDelays, getQuizProgressSnapshot } from '@/composables/useSpacedRepetition'
import { list as listThresholds } from '@/config/thresholds'

const store = useAppStore()
const router = useRouter()
const route = useRoute()
const { setQuizLevels } = useQuiz()

const PAGE_SIZE = listThresholds.pageSize

// ---- URL query 派生状态：可分享、可后退、刷新不丢 ----
function qStr(key: string): string {
  const v = route.query[key]
  return typeof v === 'string' ? v : ''
}
function qNum(key: string, def: number): number {
  const n = parseInt(qStr(key) || '', 10)
  return Number.isFinite(n) && n > 0 ? n : def
}
function qList(key: string): string[] {
  const v = qStr(key)
  return v ? v.split(',').filter(Boolean) : []
}

const searchQuery = computed(() => qStr('q'))
const currentPage = computed(() => qNum('page', 1))
const selectedTopic = computed(() => qStr('topic'))
const selectedLevels = computed(() => qList('lv'))

/** 写入 query；undefined 表示从 URL 删掉这个 key。用 replace 避免每次输入都污染 history */
function setQuery(patch: Record<string, string | number | string[] | undefined>) {
  const next: Record<string, string | undefined> = { ...(route.query as Record<string, string | undefined>) }
  for (const [k, v] of Object.entries(patch)) {
    if (v === undefined || v === '' || (Array.isArray(v) && v.length === 0)) {
      delete next[k]
    } else if (Array.isArray(v)) {
      next[k] = v.join(',')
    } else {
      next[k] = String(v)
    }
  }
  router.replace({ query: next })
}

// 仅 UI 临时态
const isSpeaking = ref(false)
// 听模式新筛选：三段 + ⭐收藏
const reviewFilter = ref<ListReviewFilter>('all')
const showStarredOnly = ref(false)

// 同步级别筛选到练习模式（URL `?lv=` 仍然生效，保留以免误伤练习）
watch(selectedLevels, (v) => setQuizLevels(v), { immediate: true })

const emit = defineEmits<{
  speak: [items: VocabItemWithCat[], from: number, to: number]
  stop: []
}>()

// 听模式：永远合并名词 + 动词，不再按 currentCat 分；收藏交给 ⭐ 按钮
const allItems = computed<VocabItemWithCat[]>(() => {
  const all: VocabItemWithCat[] = [
    ...store.data.nouns.map(it => ({ ...it, _cat: 'nouns' as const })),
    ...store.data.verbs.map(it => ({ ...it, _cat: 'verbs' as const })),
  ]
  if (showStarredOnly.value) {
    starredTick.value
    const map = getStarredMap()
    return all.filter(it => !!map[it._cat + ':' + it.id])
  }
  return all
})

const filteredItems = computed<VocabItemWithCat[]>(() => {
  milestoneStateTick.value // 触发重计算
  let items = allItems.value

  // URL 级别过滤仍保留（方便练习模式通过 URL 携带）
  if (selectedLevels.value.length > 0) {
    items = items.filter(it => it.level && selectedLevels.value.includes(it.level))
  }

  const q = searchQuery.value.toLowerCase()
  if (q) {
    items = items.filter(it =>
      it.word.toLowerCase().includes(q) ||
      it.reading.includes(q) ||
      it.meaning.includes(q) ||
      (it.meaningEn && it.meaningEn.toLowerCase().includes(q)) ||
      (it.meaningEs && it.meaningEs.toLowerCase().includes(q)) ||
      (it.meaningJp && it.meaningJp.toLowerCase().includes(q)) ||
      (it.example && it.example.includes(q))
    )
  }

  // 三段筛选：复习（count>0 且今日到期）/ 未学过（count===0）/ 全部
  if (reviewFilter.value !== 'all') {
    const today = new Date().toISOString().slice(0, 10)
    const counts = getQuizProgressSnapshot().counts
    const delays = reviewFilter.value === 'review' ? getDelays() : null
    items = items.filter(it => {
      const k = `${it._cat}:${it.id}`
      const c = counts[k] || 0
      if (reviewFilter.value === 'new') return c === 0
      // review
      if (c <= 0) return false
      const due = delays![k]
      return !due || due <= today
    })
  }

  // 搜索时显示已掌握的词（当词典用）；非搜索时过滤掉
  if (!q) {
    milestoneStateTick.value
    const masteryMap = getMasteryQuizPassedMap()
    items = items.filter(it => !masteryMap[`${it._cat}:${it.id}`])
  }
  return items
})

const canUseRange = computed(() =>
  selectedTopic.value === '' &&
  selectedLevels.value.length === 0 &&
  reviewFilter.value === 'all' &&
  !showStarredOnly.value,
)

const totalPages = computed(() => Math.ceil(filteredItems.value.length / PAGE_SIZE))

const pagedItems = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredItems.value.slice(start, start + PAGE_SIZE)
})

function onSearch(q: string) {
  setQuery({ q, page: undefined })
}

function onPageChange(dir: number) {
  const next = Math.max(1, Math.min(totalPages.value, currentPage.value + dir))
  setQuery({ page: next === 1 ? undefined : next })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onPageGoto(page: number) {
  const next = Math.max(1, Math.min(totalPages.value, page))
  setQuery({ page: next === 1 ? undefined : next })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onSpeak(from: number, to: number) {
  isSpeaking.value = true
  emit('speak', filteredItems.value, from, to)
}

/** 卡片上「播放」：从当前条播放到筛选列表末尾（与工具栏列表播放同一套连播） */
function onPlayListFrom(rowNumber: number) {
  const total = filteredItems.value.length
  if (total < 1 || rowNumber < 1 || rowNumber > total) return
  isSpeaking.value = true
  emit('speak', filteredItems.value, rowNumber, total)
}

function onStop() {
  isSpeaking.value = false
  emit('stop')
}

defineExpose({ stopSpeaking: () => { isSpeaking.value = false } })
</script>

<template>
  <div>
    <div class="mb-2 px-4 md:mb-3 md:px-10">
      <div class="list-controls-panel pb-3 md:pb-4">
        <div>
          <ListToolbar
            :total-items="filteredItems.length"
            :is-speaking="isSpeaking"
            :can-use-range="canUseRange"
            :query="searchQuery"
            :review-filter="reviewFilter"
            :show-starred-only="showStarredOnly"
            @search="onSearch"
            @speak="onSpeak"
            @stop="onStop"
            @update:review-filter="(v) => (reviewFilter = v)"
            @update:show-starred-only="(v) => (showStarredOnly = v)"
          />
        </div>
      </div>
    </div>
    <ListContainer
      :items="pagedItems"
      :row-offset="(currentPage - 1) * PAGE_SIZE"
      @play-list-from="onPlayListFrom"
    />
    <PaginationBar
      v-if="totalPages > 1"
      :current-page="currentPage"
      :total-pages="totalPages"
      :total-items="filteredItems.length"
      @page-change="onPageChange"
      @page-goto="onPageGoto"
    />
  </div>
</template>
