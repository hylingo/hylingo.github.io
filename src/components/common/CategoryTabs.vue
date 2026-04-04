<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'

const store = useAppStore()
const { t } = useLang()

const categories = computed(() => {
  const base = [
    { key: 'articles', labelKey: 'catArticles', count: String(store.articles.length) },
    { key: 'sentences', labelKey: 'catSent', count: String(store.data.sentences.length) },
    { key: 'nouns', labelKey: 'catNouns', count: String(store.data.nouns.length) },
  ] as const
  if (store.studyLang === 'ja') {
    return [...base, { key: 'kana' as const, labelKey: 'catKana' as const, count: '' }]
  }
  return [...base]
})
</script>

<template>
  <div
    v-if="store.currentMode !== 'stats' && store.currentMode !== 'test'"
    class="w-full min-w-0 px-4 pt-2 pb-4 md:px-10 md:max-w-[800px] md:mx-auto"
  >
    <div
      role="tablist"
      class="category-tab-rail inline-flex max-w-full flex-wrap items-center gap-0.5 rounded-2xl p-1"
    >
      <button
        v-for="cat in categories"
        :key="cat.key"
        type="button"
        role="tab"
        :aria-selected="store.currentCat === cat.key"
        class="category-tab-btn min-h-[40px] rounded-[11px] px-4 py-2 text-left transition-all duration-200 outline-none cursor-pointer focus-visible:ring-2 focus-visible:ring-[var(--primary)]/35 focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--bg)]"
        :class="
          store.currentCat === cat.key
            ? 'category-tab-btn--active'
            : 'category-tab-btn--inactive'
        "
        @click="store.switchCat(cat.key)"
      >
        <span class="flex items-baseline gap-2 whitespace-nowrap">
          <span class="text-[13px] font-semibold tracking-wide">{{ t(cat.labelKey) }}</span>
          <span
            v-if="cat.count"
            class="category-tab-count text-[11px] font-medium tabular-nums"
          >{{ cat.count }}</span>
        </span>
      </button>
    </div>
  </div>
</template>
