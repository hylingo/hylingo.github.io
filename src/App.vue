<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import { useFirebase } from '@/composables/useFirebase'
import { useQuiz } from '@/composables/useQuiz'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppNav from '@/components/layout/AppNav.vue'
import CategoryTabs from '@/components/common/CategoryTabs.vue'
import ListPanel from '@/components/list/ListPanel.vue'
import { defineAsyncComponent } from 'vue'
const PracticePanel = defineAsyncComponent(() => import('@/components/practice/PracticePanel.vue'))
const StatsPanel = defineAsyncComponent(() => import('@/components/stats/StatsPanel.vue'))
import LoopBar from '@/components/loop/LoopBar.vue'
import KanaGrid from '@/components/kana/KanaGrid.vue'
import ArticlesPanel from '@/components/articles/ArticlesPanel.vue'
import { useLoopPlayer } from '@/composables/useLoopPlayer'
import { stopLoop as stopPracticeAudioLoop } from '@/composables/useAudio'
import { useTheme } from '@/composables/useTheme'

const store = useAppStore()
const { loopPlaying, startListPlayback, stop: stopListPlayback } = useLoopPlayer()
const listPanelRef = ref<InstanceType<typeof ListPanel> | null>(null)

watch(loopPlaying, (val) => {
  if (!val) listPanelRef.value?.stopSpeaking()
})
const { userId, initFirebase, pullAndMerge } = useFirebase()
const { schedulePracticeStartQuiz } = useQuiz()
const { initTheme } = useTheme()

watch(
  () => [store.currentMode, store.currentCat, store.practiceArticleId] as const,
  () => {
    if (store.currentMode === 'practice') schedulePracticeStartQuiz()
  },
)

watch(
  () => store.currentMode,
  (mode, prev) => {
    // 离开「听」：停列表循环，避免与练争用全局 audioEl
    if (prev === 'list' && mode !== 'list') {
      stopListPlayback()
      listPanelRef.value?.stopSpeaking()
    }
    // 离开「练」：停单曲循环与保活
    if (prev === 'practice' && mode !== prev) {
      stopPracticeAudioLoop()
    }
  },
)

onMounted(async () => {
  initTheme()
  initFirebase()
  await store.loadData()

  // 如果初始就在 articles/dialogues 页，立即开始加载
  if (store.currentCat === 'articles' || store.currentCat === 'dialogues') {
    store.ensureArticles()
  }

  if (userId.value) {
    pullAndMerge().then((merged) => {
      if (merged) store.restorePracticeArticleFromLS()
    })
  }

})
</script>

<template>
  <AppHeader />
  <div class="flex min-h-[100svh]">
    <AppNav />
    <div
      class="flex-1 min-w-0 pb-20 md:ml-[200px] max-md:pb-[calc(5rem+env(safe-area-inset-bottom,0px))]"
    >
      <CategoryTabs />
      <div
        v-show="store.currentMode === 'list'"
        class="w-full min-w-0 md:max-w-[800px] md:mx-auto"
      >
        <KanaGrid v-if="store.currentCat === 'kana'" />
        <ArticlesPanel
          v-else-if="store.currentCat === 'articles' || store.currentCat === 'dialogues'"
          :key="store.currentCat"
          :filter-format="store.currentCat === 'dialogues' ? 'dialogue' : 'essay'"
        />
        <ListPanel
          v-else
          ref="listPanelRef"
          @speak="(items, from, to) => startListPlayback(items, from, to)"
          @stop="() => { stopListPlayback(); listPanelRef?.stopSpeaking() }"
        />
      </div>
      <div v-if="store.currentMode === 'practice'" class="px-4 pb-5 md:px-10 md:max-w-[800px] md:mx-auto">
        <PracticePanel />
      </div>
      <div v-if="store.currentMode === 'stats'" class="px-4 pb-5 md:px-10 md:max-w-[800px] md:mx-auto">
        <StatsPanel />
      </div>
    </div>
  </div>
  <LoopBar />
</template>
