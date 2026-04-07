<script setup lang="ts">
import { computed, ref, nextTick, onMounted, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'
import { starredTick, getStarredCount } from '@/learning'

const store = useAppStore()
const { t } = useLang()

const isWordsCat = computed(
  () => store.currentCat === 'nouns' || store.currentCat === 'verbs' || store.currentCat === 'starred',
)

const starredCount = computed(() => {
  starredTick.value
  return getStarredCount()
})

const wordCount = computed(() => store.data.nouns.length + store.data.verbs.length)

const essayCount = computed(() => store.articles.filter((a) => a.format === 'essay').length)
const dialogueCount = computed(() => store.articles.filter((a) => a.format === 'dialogue').length)


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

// 滑动指示器
const tabBtnRefs = ref<HTMLButtonElement[]>([])
const indicatorStyle = ref<{ left: string; width: string; opacity: number }>({ left: '0px', width: '0px', opacity: 0 })

function setBtnRef(el: unknown, idx: number) {
  if (el instanceof HTMLButtonElement) tabBtnRefs.value[idx] = el
}

async function updateIndicator() {
  await nextTick()
  const idx = categories.value.findIndex((c) => mainTabSelected(c.key))
  const btn = idx >= 0 ? tabBtnRefs.value[idx] : null
  if (!btn) {
    indicatorStyle.value = { ...indicatorStyle.value, opacity: 0 }
    return
  }
  indicatorStyle.value = {
    left: btn.offsetLeft + 'px',
    width: btn.offsetWidth + 'px',
    opacity: 1,
  }
}

onMounted(() => {
  updateIndicator()
  window.addEventListener('resize', updateIndicator)
})
watch(() => [store.currentCat, categories.value.length] as const, updateIndicator)

const wordSubTabs = computed(() => {
  const tabs: { key: string; label: string; count: number }[] = [
    { key: 'nouns', label: t('catNouns'), count: store.data.nouns.length },
  ]
  if (store.studyLang === 'ja' && store.data.verbs.length > 0) {
    tabs.push({ key: 'verbs', label: t('catVerbs'), count: store.data.verbs.length })
  }
  if (starredCount.value > 0) {
    tabs.push({ key: 'starred', label: t('catStarred'), count: starredCount.value })
  }
  return tabs
})
</script>

<template>
  <div
    v-if="store.currentMode !== 'stats'"
    class="w-full min-w-0 px-4 pt-2 pb-2 md:px-10 md:max-w-[800px] md:mx-auto md:pb-3"
  >
    <div
      role="tablist"
      class="category-tab-rail relative flex w-full max-w-full flex-wrap items-stretch gap-0.5 rounded-2xl p-1 sm:flex-nowrap"
    >
      <div class="category-tab-indicator" :style="indicatorStyle" aria-hidden="true" />
      <button
        v-for="(cat, i) in categories"
        :key="cat.key"
        :ref="(el) => setBtnRef(el, i)"
        type="button"
        role="tab"
        :aria-selected="mainTabSelected(cat.key)"
        class="category-tab-btn relative z-[1] min-h-[40px] min-w-0 flex-1 rounded-[11px] px-2 py-2 text-center transition-colors duration-200 outline-none cursor-pointer focus-visible:ring-2 focus-visible:ring-[var(--primary)]/35 focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--bg)] sm:px-4"
        :class="
          mainTabSelected(cat.key)
            ? 'category-tab-btn--active-text'
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

    <!-- 单词子 tab：名词 / 动词 / 收藏 + 筛选 -->
    <div
      v-show="isWordsCat"
      class="mt-1.5 flex items-center gap-1"
      role="tablist"
      :aria-label="t('catWords')"
    >
      <template v-if="isWordsCat">
        <button
          v-for="sub in wordSubTabs"
          :key="sub.key"
          type="button"
          role="tab"
          :aria-selected="store.currentCat === sub.key"
          class="category-sub-tab min-h-[32px] rounded-[9px] px-3 py-1.5 text-[12px] font-semibold cursor-pointer transition-all duration-200 outline-none border-none"
          :class="store.currentCat === sub.key ? 'category-tab-btn--active' : 'category-tab-btn--inactive'"
          @click="store.switchCat(sub.key)"
        >
          <span class="flex items-baseline justify-center gap-1 whitespace-nowrap">
            <span>{{ sub.label }}</span>
            <span class="category-tab-count text-[10px] font-medium tabular-nums">{{ sub.count }}</span>
          </span>
        </button>
      </template>
      <div class="flex-1" />
      <!-- 听页面的筛选按钮通过 Teleport 注入到这里 -->
      <div id="sub-tab-right-slot" class="flex items-center gap-1" />
    </div>
  </div>
</template>
