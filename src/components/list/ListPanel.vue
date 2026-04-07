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
import ListToolbar from './ListToolbar.vue'
import ListContainer from './ListContainer.vue'
import PaginationBar from '../common/PaginationBar.vue'
import TopicChips from './TopicChips.vue'
import { list as listThresholds } from '@/config/thresholds'

const store = useAppStore()
const router = useRouter()
const route = useRoute()
const { setQuizLevels } = useQuiz()
const isWordsCat = computed(() => store.currentCat === 'nouns' || store.currentCat === 'verbs')

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

// 同步级别筛选到练习模式
watch(selectedLevels, (v) => setQuizLevels(v), { immediate: true })

const emit = defineEmits<{
  speak: [items: VocabItemWithCat[], from: number, to: number]
  stop: []
}>()

const allItems = computed<VocabItemWithCat[]>(() => {
  if (store.currentCat === 'mix' || store.currentCat === 'starred') {
    const all = [
      ...store.data.nouns.map(it => ({ ...it, _cat: 'nouns' as const })),
      ...store.data.verbs.map(it => ({ ...it, _cat: 'verbs' as const })),
    ]
    if (store.currentCat === 'starred') {
      starredTick.value
      const map = getStarredMap()
      return all.filter(it => !!map[it._cat + ':' + it.id])
    }
    return all
  }
  const cat = store.currentCat as 'nouns' | 'verbs'
  return (store.data[cat] || []).map(it => ({ ...it, _cat: cat }))
})

const topics = computed(() => {
  const counts: Record<string, number> = {}
  for (const it of allItems.value) {
    if (it.topic) counts[it.topic] = (counts[it.topic] || 0) + 1
  }
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .map(([topic, count]) => ({ topic, count }))
})

const levels = computed(() => {
  const set = new Set<string>()
  for (const it of allItems.value) {
    if (it.level) set.add(it.level)
  }
  return [...set].sort((a, b) => {
    const na = parseInt(a.replace(/\D/g, '')) || 0
    const nb = parseInt(b.replace(/\D/g, '')) || 0
    return nb - na // N5 first
  })
})

const filteredItems = computed<VocabItemWithCat[]>(() => {
  milestoneStateTick.value // 触发重计算
  let items = allItems.value

  if (selectedTopic.value) {
    items = items.filter(it => it.topic === selectedTopic.value)
  }

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

  milestoneStateTick.value
  const masteryMap = getMasteryQuizPassedMap()
  return items.filter(it => !masteryMap[`${it._cat}:${it.id}`])
})

const canUseRange = computed(() => selectedTopic.value === '' && selectedLevels.value.length === 0)

const totalPages = computed(() => Math.ceil(filteredItems.value.length / PAGE_SIZE))

const pagedItems = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredItems.value.slice(start, start + PAGE_SIZE)
})

function onSearch(q: string) {
  setQuery({ q, page: undefined })
}

function onTopicSelect(topic: string) {
  setQuery({ topic, page: undefined })
}

function onLevelToggle(level: string) {
  const cur = selectedLevels.value
  const next = cur.includes(level) ? cur.filter((l) => l !== level) : [...cur, level]
  setQuery({ lv: next, page: undefined })
}

function onLevelClear() {
  setQuery({ lv: undefined, page: undefined })
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
    <!-- 筛选按钮 Teleport 到 CategoryTabs 子 tab 行（仅单词分类有子 tab 行） -->
    <Teleport v-if="isWordsCat" to="#sub-tab-right-slot">
      <TopicChips
        v-if="topics.length > 0 || levels.length > 0"
        :topics="topics"
        :selected="selectedTopic"
        :levels="levels"
        :selected-levels="selectedLevels"
        @select="onTopicSelect"
        @toggle-level="onLevelToggle"
        @clear-levels="onLevelClear"
      />
    </Teleport>
    <div class="mb-2 px-4 md:mb-3 md:px-10">
      <div class="list-controls-panel pb-3 md:pb-4">
        <div>
          <ListToolbar
            :total-items="filteredItems.length"
            :is-speaking="isSpeaking"
            :can-use-range="canUseRange"
            :query="searchQuery"
            @search="onSearch"
            @speak="onSpeak"
            @stop="onStop"
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
