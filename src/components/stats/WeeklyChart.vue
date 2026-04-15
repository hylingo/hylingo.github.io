<script setup lang="ts">
import { ref, computed } from 'vue'
import { getStats, statsVersion } from '../../composables/useStats'
import { formatListenTime } from '../../utils/helpers'
import { useLang } from '@/i18n'
import { weeklyChart } from '@/config/thresholds'
import { useAppStore } from '@/stores/app'

const { t } = useLang()
const store = useAppStore()

const showAll = ref(false)
const tappedDay = ref<string | null>(null)

const stats = computed(() => {
  statsVersion.value
  store.studyLang
  return getStats()
})

const recentDays = computed(() => {
  const result: string[] = []
  for (let i = weeklyChart.days - 1; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    result.push(d.toISOString().slice(0, 10))
  }
  return result
})

const allDays = computed(() => {
  const s = stats.value
  return Object.keys(s)
    .filter(k => /^\d{4}-\d{2}-\d{2}$/.test(k))
    .sort()
})

const days = computed(() => showAll.value ? allDays.value : recentDays.value)

const maxPractice = computed(() => {
  let m: number = weeklyChart.practiceScaleMin
  for (const d of days.value) {
    const dd = stats.value[d] || {}
    m = Math.max(m, (dd.studied || 0) + (dd.quizzed || 0))
  }
  return m
})

const maxTime = computed(() => {
  let m: number = weeklyChart.listenScaleMin
  for (const d of days.value) {
    const dd = stats.value[d] || {}
    m = Math.max(m, dd.listened || 0, dd.recorded || 0)
  }
  return m
})

function pct(val: number, max: number) {
  return max > 0 ? Math.max(val / max * 100, val > 0 ? 4 : 0) + '%' : '0%'
}

function dayHasData(day: string) {
  const dd = stats.value[day]
  if (!dd) return false
  return (dd.listened || 0) > 0 || (dd.recorded || 0) > 0 || (dd.studied || 0) + (dd.quizzed || 0) > 0
}

function barHeight(val: number, max: number, day: string) {
  if (val > 0) return pct(val, max)
  return dayHasData(day) ? '1px' : '0%'
}

function dayLabel(day: string) {
  const d = new Date(day + 'T00:00:00')
  const weekdays = ['日', '月', '火', '水', '木', '金', '土']
  return { date: day.slice(5), weekday: weekdays[d.getDay()] }
}

function onTapDay(day: string) {
  tappedDay.value = tappedDay.value === day ? null : day
}

function tipText(day: string) {
  const dd = stats.value[day] || {}
  const listen = dd.listened || 0
  const read = dd.recorded || 0
  const practice = (dd.studied || 0) + (dd.quizzed || 0)
  const parts: string[] = []
  if (listen > 0) parts.push(t('listenLabel') + ' ' + formatListenTime(listen, t))
  if (read > 0) parts.push(t('readLabel') + ' ' + read + t('timesUnit'))
  if (practice > 0) parts.push(t('practiceLabel') + ' ' + practice)
  return parts.length ? parts.join('  ') : '-'
}

const chartTitleText = computed(() => {
  if (showAll.value) {
    return t('chartTitleAll').replace('{n}', String(allDays.value.length))
  }
  return t('chartTitle').replace('{n}', String(weeklyChart.days))
})
</script>

<template>
  <div class="theme-card p-4 mt-4">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-base font-semibold theme-text">{{ chartTitleText }}</h3>
      <button
        type="button"
        class="h-7 px-2.5 rounded-full flex items-center justify-center cursor-pointer transition-colors border-0 text-xs font-bold tabular-nums"
        :class="showAll ? 'bg-primary/15 text-primary-dark' : 'theme-soft theme-muted'"
        @click="showAll = !showAll; tappedDay = null"
      >{{ showAll ? '全' : '7' }}</button>
    </div>

    <!-- 柱状图 -->
    <div class="overflow-x-auto -mx-1 px-1">
      <div
        class="flex items-end"
        :style="{ height: '140px', minWidth: days.length > 10 ? days.length * 36 + 'px' : undefined }"
      >
        <div
          v-for="(day, idx) in days"
          :key="day"
          class="flex-1 flex flex-col items-center h-full cursor-pointer"
          :style="{ minWidth: days.length > 10 ? '32px' : undefined }"
          @click="onTapDay(day)"
        >
          <!-- 柱子组 -->
          <div
            class="flex items-end justify-center gap-[2px] flex-1 w-full px-[2px] rounded-t-md transition-colors"
            :class="[
              tappedDay === day ? 'bg-primary/8' : '',
              idx % 2 === 0 ? 'day-even' : 'day-odd'
            ]"
          >
            <div class="flex-1 flex items-end justify-center h-full max-w-[14px]">
              <div
                class="w-full rounded-t chart-bar-listen transition-all duration-300"
                :style="{ height: barHeight(stats[day]?.listened || 0, maxTime, day) }"
              />
            </div>
            <div class="flex-1 flex items-end justify-center h-full max-w-[14px]">
              <div
                class="w-full rounded-t chart-bar-read transition-all duration-300"
                :style="{ height: barHeight(stats[day]?.recorded || 0, maxTime, day) }"
              />
            </div>
            <div class="flex-1 flex items-end justify-center h-full max-w-[14px]">
              <div
                class="w-full rounded-t chart-bar-practice transition-all duration-300"
                :style="{ height: barHeight((stats[day]?.studied || 0) + (stats[day]?.quizzed || 0), maxPractice, day) }"
              />
            </div>
          </div>

          <!-- 日期 -->
          <div class="text-center pt-1 w-full border-t" style="border-color: color-mix(in srgb, var(--text) 10%, transparent);">
            <div class="text-[10px] font-medium theme-text tabular-nums leading-tight">{{ dayLabel(day).date }}</div>
            <div class="text-[8px] theme-muted leading-tight">{{ dayLabel(day).weekday }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 点击提示 -->
    <div
      v-if="tappedDay"
      class="mt-2 px-3 py-1.5 rounded-lg text-xs text-center theme-text transition-all"
      style="background: color-mix(in srgb, var(--text) 6%, transparent);"
    >
      <span class="font-medium">{{ tappedDay.slice(5) }}</span>
      <span class="mx-1.5 opacity-40">|</span>
      <span class="tabular-nums">{{ tipText(tappedDay) }}</span>
    </div>

    <!-- 图例 -->
    <div class="flex justify-center gap-4 text-[11px] theme-muted mt-3">
      <span class="flex items-center gap-1"><span class="inline-block w-2.5 h-2.5 rounded-sm chart-bar-listen"></span>{{ t('listenLabel') }}</span>
      <span class="flex items-center gap-1"><span class="inline-block w-2.5 h-2.5 rounded-sm chart-bar-read"></span>{{ t('readLabel') }}</span>
      <span class="flex items-center gap-1"><span class="inline-block w-2.5 h-2.5 rounded-sm chart-bar-practice"></span>{{ t('practiceLabel') }}</span>
    </div>
  </div>
</template>

<style scoped>
.chart-bar-listen { background: #d96a53; }
.chart-bar-read { background: #5a7ab0; }
.chart-bar-practice { background: #4f8a6f; }

.day-even { background: transparent; }
.day-odd { background: color-mix(in srgb, var(--text) 3%, transparent); }

:global(:root:not(.theme-watercolor)) .chart-bar-listen { background: #c4705c; }
:global(:root:not(.theme-watercolor)) .chart-bar-read { background: #7aa0d2; }
:global(:root:not(.theme-watercolor)) .chart-bar-practice { background: #6da585; }
:global(:root:not(.theme-watercolor)) .day-odd { background: color-mix(in srgb, #ffffff 4%, transparent); }
</style>
