<script setup lang="ts">
import { computed } from 'vue'
import type { VocabItem } from '../../types'
import RubyText from '@/components/common/RubyText.vue'
import { getListenedCount, getItemCount, itemCountsTick, listenedCountsTick, recordItemListened } from '../../composables/useSpacedRepetition'
import { speakWithExample } from '../../composables/useAudio'
import { useListenListCardSwipe } from '@/composables/useListenListCardSwipe'
import { useLang } from '@/i18n'
import { localMeaning, localExampleCn } from '@/utils/helpers'

const { t, currentLang } = useLang()

const props = defineProps<{
  item: VocabItem
  rowNumber: number
}>()

const emit = defineEmits<{
  playListFrom: [rowNumber: number]
}>()

function onPlayListFromRow() {
  emit('playListFrom', props.rowNumber)
}

const cat = 'sentences' as const

const statsLine = computed(() => {
  itemCountsTick.value
  listenedCountsTick.value
  return t('listStatsCounts')
    .replace('{listen}', String(getListenedCount(cat, props.item.id)))
    .replace('{practice}', String(getItemCount(cat, props.item.id)))
})

function onSpeak() {
  speakWithExample(props.item.word, props.item.audio)
  recordItemListened(cat, props.item.id)
}

const {
  onPointerDown,
  onCardClick,
  onAddQuiz,
  inQueue,
  cardTransform,
  cardTransitionClass,
} = useListenListCardSwipe(
  () => 'sentences',
  () => props.item.id,
  onSpeak,
)
</script>

<template>
  <div class="flex flex-col rounded-2xl shadow-[0_2px_16px_rgba(0,0,0,0.06)] overflow-hidden animate-fadeUp">
    <div class="relative flex-1 min-w-0 overflow-hidden">
      <div class="absolute inset-y-0 right-0 flex w-[100px] z-0" aria-hidden="true">
        <button
          type="button"
          class="w-full flex items-center justify-center text-white text-xs font-semibold px-2 leading-tight border-0 cursor-pointer active:opacity-90 hover:opacity-95"
          :class="inQueue ? 'bg-[#999] cursor-default' : 'btn-grad-primary btn-grad-primary--borderless'"
          :disabled="inQueue"
          @pointerdown.stop
          @click.stop="onAddQuiz"
        >
          {{ inQueue ? t('quizQueueReady') : t('quizQueueAdd') }}
        </button>
      </div>
      <div
        class="relative z-10 theme-surface p-4 select-none touch-pan-y cursor-grab active:cursor-grabbing"
        :class="cardTransitionClass"
        :style="cardTransform"
        @click="onCardClick"
        @pointerdown="onPointerDown"
      >
        <div class="flex items-start gap-3 -mt-2">
          <div
            class="min-w-9 h-9 max-w-[3.25rem] px-1 rounded-full theme-soft text-[#e8735a] flex items-center justify-center text-xs font-bold tabular-nums shrink-0 leading-none mt-0.5"
          >
            {{ rowNumber }}
          </div>
          <div class="flex-1 min-w-0 min-h-0">
            <div class="text-base font-bold theme-text">
              <template v-if="item.ruby && item.ruby.length">
                <RubyText :tokens="item.ruby" />
              </template>
              <template v-else>{{ item.word }}</template>
            </div>
            <div class="text-sm theme-text mt-0.5">{{ localMeaning(item, currentLang) }}</div>
            <div v-if="item.example" class="text-xs theme-muted mt-1 leading-relaxed">
              {{ item.example }}
              <br v-if="localExampleCn(item, currentLang)" />
              <span v-if="localExampleCn(item, currentLang)" class="text-[#5b8a72]">{{ localExampleCn(item, currentLang) }}</span>
            </div>
          </div>
          <div class="flex flex-col items-end shrink-0 gap-2">
            <div
              class="theme-muted text-[10px] leading-tight tabular-nums text-right whitespace-nowrap pointer-events-none"
            >
              {{ statsLine }}
            </div>
            <button
              type="button"
              class="w-10 h-10 rounded-full border-2 flex items-center justify-center cursor-pointer transition-all border-[#e8e2dc] theme-surface text-[#e8735a] shadow-[0_2px_8px_rgba(0,0,0,0.06)] hover:border-[#e8735a] hover:shadow-[0_4px_12px_rgba(232,115,90,0.2)] active:scale-[0.96]"
              :aria-label="t('listPlayFromHere')"
              @pointerdown.stop
              @click.stop="onPlayListFromRow"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
