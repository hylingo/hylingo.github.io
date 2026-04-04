<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAppStore } from '../../stores/app'
import type { VocabItemWithCat } from '../../types'
import {
  hasMasteryQuizPassed,
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
const { setQuizLevels } = useQuiz()
const isWordsCat = computed(() => store.currentCat === 'nouns' || store.currentCat === 'verbs')

const PAGE_SIZE = listThresholds.pageSize
const searchQuery = ref('')
const currentPage = ref(1)
const isSpeaking = ref(false)
const selectedTopic = ref('')
const selectedLevels = ref<string[]>([])

// 同步级别筛选到练习模式
watch(selectedLevels, (v) => setQuizLevels(v))

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
  return items.filter(it => {
    if (hasMasteryQuizPassed(it._cat, it.id)) return false
    return true
  })
})

const canUseRange = computed(() => selectedTopic.value === '' && selectedLevels.value.length === 0)

const totalPages = computed(() => Math.ceil(filteredItems.value.length / PAGE_SIZE))

const pagedItems = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredItems.value.slice(start, start + PAGE_SIZE)
})

function onSearch(q: string) {
  searchQuery.value = q
  currentPage.value = 1
}

function onTopicSelect(topic: string) {
  selectedTopic.value = topic
  currentPage.value = 1
}

function onLevelToggle(level: string) {
  const idx = selectedLevels.value.indexOf(level)
  if (idx >= 0) {
    selectedLevels.value = selectedLevels.value.filter(l => l !== level)
  } else {
    selectedLevels.value = [...selectedLevels.value, level]
  }
  currentPage.value = 1
}

function onLevelClear() {
  selectedLevels.value = []
  currentPage.value = 1
}

function onPageChange(dir: number) {
  currentPage.value = Math.max(1, Math.min(totalPages.value, currentPage.value + dir))
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onPageGoto(page: number) {
  currentPage.value = Math.max(1, Math.min(totalPages.value, page))
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
