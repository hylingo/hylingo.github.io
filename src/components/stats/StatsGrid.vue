<script setup lang="ts">
import { computed } from 'vue'
import { getStats, todayKey, statsVersion } from '../../composables/useStats'
import { formatListenTime } from '../../utils/helpers'
import { useLang } from '@/i18n'
import { milestoneStateTick } from '@/learning'
import { useAppStore } from '@/stores/app'
import { readSyncedJson } from '@/learning/learnStorage'

const { t } = useLang()
const emit = defineEmits<{ mastered: [] }>()
const store = useAppStore()

const stats = computed(() => {
  statsVersion.value
  store.studyLang
  return getStats()
})
const today = computed(() => todayKey())
const todayData = computed(() => stats.value[today.value] || { studied: 0, quizzed: 0, correct: 0, wrong: {}, listened: 0, recorded: 0 })

/** 已掌握词数 */
const masteredCount = computed(() => {
  milestoneStateTick.value
  store.studyLang
  try {
    const m = readSyncedJson(store.studyLang, 'masteryQuizPassed') as Record<string, unknown>
    return Object.keys(m).length
  } catch { return 0 }
})

</script>

<template>
  <div class="grid grid-cols-3 gap-3 mt-4">
    <!-- 听 -->
    <div class="rounded-xl p-4 text-center text-white stat-card stat-card--listen">
      <div class="flex items-center justify-center gap-1.5 mb-1.5">
        <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
        <span class="text-xs font-medium opacity-90">{{ t('todayListen') }}</span>
      </div>
      <div class="text-xl font-bold tabular-nums">{{ formatListenTime(todayData.listened || 0, t) }}</div>
    </div>

    <!-- 读 -->
    <div class="rounded-xl p-4 text-center text-white stat-card stat-card--read">
      <div class="flex items-center justify-center gap-1.5 mb-1.5">
        <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
        <span class="text-xs font-medium opacity-90">{{ t('todayRead') }}</span>
      </div>
      <div class="text-xl font-bold tabular-nums">{{ (todayData.recorded || 0) + t('timesUnit') }}</div>
    </div>

    <!-- 练 -->
    <div class="rounded-xl p-4 text-center text-white stat-card stat-card--practice">
      <div class="flex items-center justify-center gap-1.5 mb-1.5">
        <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        <span class="text-xs font-medium opacity-90">{{ t('todayPractice') }}</span>
      </div>
      <div class="text-xl font-bold tabular-nums">{{ todayData.studied + todayData.quizzed }}</div>
    </div>
  </div>

  <!-- 已掌握 -->
  <div
    class="mt-3 rounded-xl p-3 text-center text-white stat-card stat-card--mastered cursor-pointer active:scale-[0.97] transition-transform"
    @click="emit('mastered')"
  >
    <div class="flex items-center justify-center gap-2">
      <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      <span class="text-xs font-medium opacity-90">{{ t('masteredStats') }}</span>
      <span class="text-lg font-bold tabular-nums">{{ masteredCount }}</span>
    </div>
  </div>
</template>
