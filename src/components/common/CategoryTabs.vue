<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'

const store = useAppStore()
const { t } = useLang()

const isWordsCat = computed(
  () => store.currentCat === 'nouns' || store.currentCat === 'verbs',
)

const wordCount = computed(() => store.data.nouns.length + store.data.verbs.length)

const essayCount = computed(() => store.articles.filter((a) => a.format === 'essay').length)
const dialogueCount = computed(() => store.articles.filter((a) => a.format === 'dialogue').length)

const showWordSubTabs = computed(
  () => store.studyLang === 'ja' && store.data.verbs.length > 0,
)

const categories = computed(() => {
  const base = [
    { key: 'articles', labelKey: 'catArticles', count: String(essayCount.value) },
    { key: 'dialogues', labelKey: 'catDialogues', count: String(dialogueCount.value) },
    {
      key: 'words',
      labelKey: 'catWords',
      count: String(wordCount.value),
    },
  ] as const
  if (store.studyLang === 'ja') {
    return [...base, { key: 'kana' as const, labelKey: 'catKana' as const, count: '' }]
  }
  return [...base]
})

function onMainTabClick(key: string) {
  if (key === 'words') {
    if (!isWordsCat.value) store.switchCat('nouns')
    return
  }
  store.switchCat(key)
}

function mainTabSelected(key: string): boolean {
  if (key === 'words') return isWordsCat.value
  return store.currentCat === key
}
</script>

<template>
  <div
    v-if="store.currentMode !== 'stats' && store.currentMode !== 'test'"
    class="w-full min-w-0 px-4 pt-2 pb-2 md:px-10 md:max-w-[800px] md:mx-auto md:pb-3"
  >
    <div
      role="tablist"
      class="category-tab-rail flex w-full max-w-full flex-wrap items-stretch gap-0.5 rounded-2xl p-1 sm:flex-nowrap"
    >
      <button
        v-for="cat in categories"
        :key="cat.key"
        type="button"
        role="tab"
        :aria-selected="mainTabSelected(cat.key)"
        class="category-tab-btn min-h-[40px] min-w-0 flex-1 rounded-[11px] px-2 py-2 text-center transition-all duration-200 outline-none cursor-pointer focus-visible:ring-2 focus-visible:ring-[var(--primary)]/35 focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--bg)] sm:px-4"
        :class="
          mainTabSelected(cat.key)
            ? 'category-tab-btn--active'
            : 'category-tab-btn--inactive'
        "
        @click="onMainTabClick(cat.key)"
      >
        <span class="flex items-baseline justify-center gap-1.5 whitespace-nowrap sm:gap-2">
          <span class="text-[13px] font-semibold tracking-wide">{{ t(cat.labelKey) }}</span>
          <span
            v-if="cat.count"
            class="category-tab-count text-[11px] font-medium tabular-nums"
          >{{ cat.count }}</span>
        </span>
      </button>
    </div>

    <!-- 单词：名词 / 动词（仅日语且有动词数据时） -->
    <div
      v-if="showWordSubTabs && isWordsCat"
      class="mt-2 flex w-full max-w-full flex-wrap gap-1.5 rounded-2xl border border-[var(--border)] bg-[var(--card)]/60 p-1.5 sm:flex-nowrap"
      role="tablist"
      :aria-label="t('catWords')"
    >
      <button
        type="button"
        role="tab"
        :aria-selected="store.currentCat === 'nouns'"
        class="min-h-[36px] min-w-0 flex-1 rounded-[10px] px-3 py-1.5 text-center text-[12px] font-semibold transition-all outline-none cursor-pointer focus-visible:ring-2 focus-visible:ring-[var(--primary)]/35"
        :class="
          store.currentCat === 'nouns'
            ? 'category-tab-btn--active'
            : 'category-tab-btn--inactive opacity-85'
        "
        @click="store.switchCat('nouns')"
      >
        <span class="inline-flex items-baseline justify-center gap-1.5">
          {{ t('catNouns') }}
          <span class="category-tab-count text-[11px] font-medium tabular-nums">{{
            store.data.nouns.length
          }}</span>
        </span>
      </button>
      <button
        type="button"
        role="tab"
        :aria-selected="store.currentCat === 'verbs'"
        class="min-h-[36px] min-w-0 flex-1 rounded-[10px] px-3 py-1.5 text-center text-[12px] font-semibold transition-all outline-none cursor-pointer focus-visible:ring-2 focus-visible:ring-[var(--primary)]/35"
        :class="
          store.currentCat === 'verbs'
            ? 'category-tab-btn--active'
            : 'category-tab-btn--inactive opacity-85'
        "
        @click="store.switchCat('verbs')"
      >
        <span class="inline-flex items-baseline justify-center gap-1.5">
          {{ t('catVerbs') }}
          <span class="category-tab-count text-[11px] font-medium tabular-nums">{{
            store.data.verbs.length
          }}</span>
        </span>
      </button>
    </div>
  </div>
</template>
