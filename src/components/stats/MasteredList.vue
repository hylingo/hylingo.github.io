<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore, type DataItem } from '../../stores/app'
import { hasMasteryQuizPassed, milestoneStateTick, unmarkMastered } from '@/learning'
import { speakWithExample } from '../../composables/useAudio'
import { useLang } from '@/i18n'
import { localMeaning, localExampleCn } from '@/utils/helpers'
import RubyText from '@/components/common/RubyText.vue'
import AppIcon from '@/components/common/AppIcon.vue'

const { t, currentLang } = useLang()
const store = useAppStore()
const emit = defineEmits<{ back: [] }>()

type MasteredItem = DataItem & { _cat: string }

const masteredItems = computed<MasteredItem[]>(() => {
  milestoneStateTick.value
  store.studyLang
  const result: MasteredItem[] = []
  const categories =
    store.studyLang === 'en'
      ? (['nouns'] as const)
      : (['nouns', 'verbs', 'kana'] as const)
  for (const cat of categories) {
    for (const it of store.data[cat]) {
      if (hasMasteryQuizPassed(cat, it.id)) {
        result.push({ ...it, _cat: cat })
      }
    }
  }
  return result
})

function onSpeak(item: MasteredItem) {
  speakWithExample(item.word, item.audio)
}

function onUnmaster(item: MasteredItem) {
  unmarkMastered(item._cat, item.id)
}
</script>

<template>
  <div class="px-4 pb-8 md:px-10 md:max-w-[800px] md:mx-auto">
    <div class="flex items-center gap-3 py-4">
      <button
        type="button"
        class="shrink-0 w-8 h-8 flex items-center justify-center rounded-full theme-soft cursor-pointer"
        @click="emit('back')"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <h2 class="text-lg font-bold theme-text">{{ t('masteredListTitle') }}</h2>
      <span class="text-sm theme-muted">{{ masteredItems.length }}</span>
    </div>

    <div v-if="masteredItems.length === 0" class="text-sm theme-muted text-center py-12">
      {{ t('masteredListEmpty') }}
    </div>

    <div class="flex flex-col gap-3">
      <div
        v-for="item in masteredItems"
        :key="item._cat + ':' + item.id"
        class="flex items-center theme-surface rounded-2xl shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-4 cursor-pointer transition-all hover:shadow-[0_8px_32px_rgba(0,0,0,0.10)] active:scale-[0.98] animate-fadeUp"
        @click="onSpeak(item)"
      >
        <div class="w-9 h-9 rounded-full theme-soft text-[#5b8a72] flex items-center justify-center text-xs font-bold shrink-0 mr-3">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-base font-bold text-content-original">
            <RubyText v-if="item.ruby" :tokens="item.ruby" />
            <template v-else>{{ item.word }}</template>
          </div>
          <div class="text-sm mt-0.5 text-content-translation">{{ localMeaning(item, currentLang) }}</div>
          <div v-if="item.example" class="text-content-example mt-1 text-xs leading-relaxed">
            {{ item.example }}
            <br v-if="localExampleCn(item, currentLang)" />
            <span v-if="localExampleCn(item, currentLang)">{{ localExampleCn(item, currentLang) }}</span>
          </div>
        </div>
        <button
          type="button"
          class="text-xl ml-2 shrink-0 bg-transparent border-none cursor-pointer"
          @click.stop="onSpeak(item)"
        >
          <AppIcon name="volume" :size="16" />
        </button>
        <button
          type="button"
          class="ml-2 shrink-0 px-2.5 py-1 rounded-md text-[11px] font-medium cursor-pointer border theme-muted bg-transparent"
          style="border-color: var(--border)"
          @click.stop="onUnmaster(item)"
        >{{ t('practiceUnmaster') }}</button>
      </div>
    </div>
  </div>
</template>
