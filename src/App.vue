<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useFirebase } from '@/composables/useFirebase'
import { useQuiz } from '@/composables/useQuiz'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppNav from '@/components/layout/AppNav.vue'
import CategoryTabs from '@/components/common/CategoryTabs.vue'
import ListPanel from '@/components/list/ListPanel.vue'
import { defineAsyncComponent } from 'vue'
import SkeletonPanel from '@/components/common/SkeletonPanel.vue'
import SkeletonVocabList from '@/components/common/SkeletonVocabList.vue'
const PracticePanel = defineAsyncComponent({
  loader: () => import('@/components/practice/PracticePanel.vue'),
  loadingComponent: SkeletonPanel,
  delay: 120,
})
const StatsPanel = defineAsyncComponent({
  loader: () => import('@/components/stats/StatsPanel.vue'),
  loadingComponent: SkeletonPanel,
  delay: 120,
})
import LoopBar from '@/components/loop/LoopBar.vue'
import KanaGrid from '@/components/kana/KanaGrid.vue'
import ArticlesPanel from '@/components/articles/ArticlesPanel.vue'
import ToastStack from '@/components/common/ToastStack.vue'
import { showError } from '@/composables/useToasts'
import { t as i18nT } from '@/i18n'
import { useLoopPlayer } from '@/composables/useLoopPlayer'
import { stopLoop as stopPracticeAudioLoop } from '@/composables/useAudio'
import { useTheme } from '@/composables/useTheme'

const store = useAppStore()
const route = useRoute()

// 根据当前路由，给 <html> 打上 mode-* class，供 CSS 切换水彩背景位置
const MODE_CLASSES = ['mode-list', 'mode-practice', 'mode-stats'] as const
function routeToMode(name: unknown): typeof MODE_CLASSES[number] {
  if (name === 'practice' || name === 'practice-article') return 'mode-practice'
  if (name === 'stats') return 'mode-stats'
  return 'mode-list'
}
watch(
  () => route.name,
  (name) => {
    const root = document.documentElement
    MODE_CLASSES.forEach(c => root.classList.remove(c))
    root.classList.add(routeToMode(name))
  },
  { immediate: true },
)
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

async function loadInitialDataWithRetry() {
  try {
    await store.loadData()
  } catch {
    showError(i18nT('toastDataLoadFailed') || '数据加载失败', {
      actionLabel: i18nT('retry') || '重试',
      onAction: () => { void loadInitialDataWithRetry() },
    })
    return
  }
  // 如果初始就在 articles/dialogues 页，或冷启动直接落到本篇练习 URL，立即加载 articles
  const needsArticles =
    store.currentCat === 'articles' ||
    store.currentCat === 'dialogues' ||
    !!store.practiceArticleId
  if (needsArticles) {
    await store.ensureArticles()
  }
  // 冷启动落在 practice 路由时，watch 不会触发（mode 没"变化"），手动抽一次题
  if (store.currentMode === 'practice') {
    schedulePracticeStartQuiz()
  }
}

onMounted(async () => {
  initTheme()
  // Firebase Auth 状态恢复是异步的，先等它确定再判断 userId
  await initFirebase()
  await loadInitialDataWithRetry()

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
        <template v-else>
          <SkeletonVocabList v-if="!store.isDataLoaded" />
          <ListPanel
            v-else
            ref="listPanelRef"
            @speak="(items, from, to) => startListPlayback(items, from, to)"
            @stop="() => { stopListPlayback(); listPanelRef?.stopSpeaking() }"
          />
        </template>
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
  <ToastStack />
</template>
