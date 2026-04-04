<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '../../stores/app'
import { getStats, statsVersion } from '../../composables/useStats'
import { useLang } from '@/i18n'
import { localMeaning } from '@/utils/helpers'
import { wrongWords as wrongWordsThresholds } from '@/config/thresholds'

const { t, currentLang } = useLang()

const store = useAppStore()

const wrongWords = computed(() => {
  statsVersion.value
  store.studyLang
  const stats = getStats()
  const wrongMap: Record<string, number> = {}
  for (const d of Object.values(stats)) {
    for (const [k, v] of Object.entries((d as any).wrong || {})) {
      wrongMap[k] = (wrongMap[k] || 0) + (v as number)
    }
  }
  return Object.entries(wrongMap)
    .filter(([, v]) => v >= wrongWordsThresholds.minMissCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, wrongWordsThresholds.topN)
    .map(([key, count]) => {
      const [cat, id] = key.split(':')
      const items = (store.data as any)[cat] as any[] | undefined
      const item = items?.find((it: any) => it.id === parseInt(id))
      return item
        ? {
            word: item.word,
            meaning: item.meaning,
            meaningEn: item.meaningEn,
            meaningEs: item.meaningEs,
            meaningJp: item.meaningJp,
            count,
          }
        : null
    })
    .filter(Boolean) as {
      word: string
      meaning: string
      meaningEn?: string
      meaningEs?: string
      meaningJp?: string
      count: number
    }[]
})

const wrongTitleText = computed(() =>
  t('wrongTitle', { n: wrongWordsThresholds.topN }),
)
</script>

<template>
  <div class="theme-card p-4 mt-4">
    <h3 class="text-base font-semibold theme-text mb-3">🔴 {{ wrongTitleText }}</h3>

    <div v-if="wrongWords.length === 0" class="theme-muted text-sm text-center py-5">
      {{ t('noData') }}
    </div>

    <div
      v-for="(item, idx) in wrongWords"
      :key="idx"
      class="flex items-center justify-between py-2 border-b border-[var(--border)] last:border-b-0"
    >
      <span class="font-semibold text-content-original">{{ item.word }}</span>
      <span class="text-sm text-content-translation mx-3 flex-1 truncate">{{ localMeaning(item, currentLang) }}</span>
      <span class="text-xs text-white bg-[#e74c3c] rounded-full px-2 py-0.5 shrink-0">
        ×{{ item.count }}
      </span>
    </div>
  </div>
</template>
