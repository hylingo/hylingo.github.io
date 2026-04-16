<script setup lang="ts">
import { computed } from 'vue'
import { getStats, todayKey, statsVersion } from '../../composables/useStats'
import { formatListenTime } from '../../utils/helpers'
import { useLang } from '@/i18n'
import { milestoneStateTick } from '@/learning'
import { useAppStore } from '@/stores/app'
import { readSyncedJson } from '@/learning/learnStorage'
import { isArticleFullyPerfect, articlePerfectTick } from '@/learning/articlePerfect'
import { flatArticleSegments } from '@/utils/articleQuiz'

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

/** 所有天累计 */
const totalData = computed(() => {
  let listened = 0, recorded = 0, studied = 0, quizzed = 0
  for (const d of Object.values(stats.value)) {
    listened += d.listened || 0
    recorded += d.recorded || 0
    studied += d.studied || 0
    quizzed += d.quizzed || 0
  }
  return { listened, recorded, studied, quizzed }
})

/** 有效学习天数：读>=30 or 练>=30 */
const effectiveDays = computed(() => {
  let count = 0
  for (const d of Object.values(stats.value)) {
    const practiced = (d.studied || 0) + (d.quizzed || 0)
    if (practiced >= 30 || (d.recorded || 0) >= 30) count++
  }
  return count
})

/** 累计学习天数：读 10~29 or 练 10~29（不含已算入有效天数的） */
const totalStudyDays = computed(() => {
  let count = 0
  for (const d of Object.values(stats.value)) {
    const practiced = (d.studied || 0) + (d.quizzed || 0)
    const recorded = d.recorded || 0
    const isEffective = practiced >= 30 || recorded >= 30
    if (isEffective) continue
    if ((practiced >= 10 && practiced < 30) || (recorded >= 10 && recorded < 30)) count++
  }
  return count
})

/** 已掌握单词数 */
const masteredWordCount = computed(() => {
  milestoneStateTick.value
  store.studyLang
  try {
    const m = readSyncedJson(store.studyLang, 'masteryQuizPassed') as Record<string, unknown>
    return Object.keys(m).length
  } catch { return 0 }
})

/** 已掌握文章数（整篇满分 👑） */
const masteredArticleCount = computed(() => {
  articlePerfectTick.value
  let count = 0
  for (const art of store.articles) {
    const total = flatArticleSegments(art).length
    if (total > 0 && isArticleFullyPerfect(art.id, total)) count++
  }
  return count
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
      <div class="text-xl font-bold tabular-nums leading-tight">{{ formatListenTime(todayData.listened || 0, t) }}</div>
      <div class="text-[10px] opacity-60 tabular-nums mt-0.5">{{ t('totalPrefix') }} {{ formatListenTime(totalData.listened, t) }}</div>
    </div>

    <!-- 读 -->
    <div class="rounded-xl p-4 text-center text-white stat-card stat-card--read">
      <div class="flex items-center justify-center gap-1.5 mb-1.5">
        <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
        <span class="text-xs font-medium opacity-90">{{ t('todayRead') }}</span>
      </div>
      <div class="text-xl font-bold tabular-nums leading-tight">{{ (todayData.recorded || 0) + t('timesUnit') }}</div>
      <div class="text-[10px] opacity-60 tabular-nums mt-0.5">{{ t('totalPrefix') }} {{ totalData.recorded + t('timesUnit') }}</div>
    </div>

    <!-- 练 -->
    <div class="rounded-xl p-4 text-center text-white stat-card stat-card--practice">
      <div class="flex items-center justify-center gap-1.5 mb-1.5">
        <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        <span class="text-xs font-medium opacity-90">{{ t('todayPractice') }}</span>
      </div>
      <div class="text-xl font-bold tabular-nums leading-tight">{{ todayData.studied + todayData.quizzed }}</div>
      <div class="text-[10px] opacity-60 tabular-nums mt-0.5">{{ t('totalPrefix') }} {{ totalData.studied + totalData.quizzed }}</div>
    </div>
  </div>

  <!-- 有效学习天数 -->
  <div class="mt-3">
    <div class="rounded-xl p-3 text-center text-white stat-card stat-card--mastered">
      <div class="flex items-center justify-center gap-1.5 mb-1">
        <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        <span class="text-xs font-medium opacity-90">{{ t('effectiveDays') }}</span>
        <span class="text-lg font-bold tabular-nums">{{ effectiveDays }}</span>
      </div>
      <div v-if="totalStudyDays > 0" class="text-[10px] opacity-60 tabular-nums">{{ t('totalStudyDays') }} {{ totalStudyDays }}</div>
    </div>
  </div>

  <!-- 已掌握：单词 + 文章 -->
  <div
    class="mt-3 rounded-xl p-3 text-white stat-card stat-card--mastered cursor-pointer active:scale-[0.97] transition-transform"
    @click="emit('mastered')"
  >
    <div class="flex items-center justify-center gap-2 mb-2">
      <svg class="w-4 h-4 opacity-80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      <span class="text-xs font-medium opacity-90">{{ t('masteredLabel') }}</span>
    </div>
    <div class="grid grid-cols-2 gap-2">
      <div class="text-center">
        <div class="text-xl font-bold tabular-nums leading-tight">{{ masteredWordCount }}</div>
        <div class="text-[10px] font-medium opacity-60 mt-0.5">{{ t('masteredStats') }}</div>
      </div>
      <div class="text-center">
        <div class="text-xl font-bold tabular-nums leading-tight">{{ masteredArticleCount }}</div>
        <div class="text-[10px] font-medium opacity-60 mt-0.5">{{ t('masteredArticles') }}</div>
      </div>
    </div>
  </div>
</template>
