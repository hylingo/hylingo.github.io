<script setup lang="ts">
import { computed, ref } from 'vue'
import type { VocabItem, CategoryKey } from '../../types'
import { getListenedCount, getItemCount, itemCountsTick, listenedCountsTick, recordItemListened } from '../../composables/useSpacedRepetition'
import { speakWithExample, playExampleAudio } from '../../composables/useAudio'
import { isStarred, toggleStar, starredTick } from '@/learning'
import { markMastered, milestoneStateTick } from '@/learning/milestones'
import { useLang } from '@/i18n'
import { localMeaning, localExampleCn } from '@/utils/helpers'
import RubyText from '@/components/common/RubyText.vue'

const { t, currentLang } = useLang()

const props = defineProps<{
  item: VocabItem
  cat: CategoryKey
  rowNumber: number
}>()

const emit = defineEmits<{
  playListFrom: [rowNumber: number]
}>()

function onPlayListFromRow() {
  emit('playListFrom', props.rowNumber)
}

function onSpeak() {
  speakWithExample(props.item.word, props.item.audio)
  recordItemListened(props.cat, props.item.id)
}

function playExample(e: Event) {
  e.stopPropagation()
  if (props.item.audioExample) {
    playExampleAudio(props.item.audioExample)
  }
}

const statsLine = computed(() => {
  itemCountsTick.value
  listenedCountsTick.value
  return t('listStatsCounts')
    .replace('{listen}', String(getListenedCount(props.cat, props.item.id)))
    .replace('{practice}', String(getItemCount(props.cat, props.item.id)))
})

const starred = computed(() => {
  starredTick.value
  return isStarred(props.cat, props.item.id)
})

function onToggleStar(e: Event) {
  e.stopPropagation()
  toggleStar(props.cat, props.item.id)
}

// ---- 右滑标记掌握（触摸 + 鼠标） ----
const swipeX = ref(0)
const swiping = ref(false)
const dismissed = ref(false)
let startX = 0
let startY = 0
let isHorizontal: boolean | null = null
let pointerDown = false

function onPointerDown(e: PointerEvent) {
  startX = e.clientX
  startY = e.clientY
  isHorizontal = null
  pointerDown = true
  swiping.value = false
  ;(e.currentTarget as HTMLElement)?.setPointerCapture(e.pointerId)
}

function onPointerMove(e: PointerEvent) {
  if (!pointerDown) return
  const dx = e.clientX - startX
  const dy = e.clientY - startY
  if (isHorizontal === null) {
    if (Math.abs(dx) > 8 || Math.abs(dy) > 8) {
      isHorizontal = Math.abs(dx) > Math.abs(dy)
    }
    return
  }
  if (!isHorizontal) return
  if (dx > 0) {
    swiping.value = true
    swipeX.value = Math.min(dx, 200)
    e.preventDefault()
  }
}

function onPointerUp() {
  if (!pointerDown) return
  pointerDown = false
  if (swipeX.value > 100) {
    dismissed.value = true
    swipeX.value = 300
    setTimeout(() => {
      markMastered(props.cat, props.item.id)
      milestoneStateTick.value++
    }, 250)
  } else {
    swipeX.value = 0
  }
  swiping.value = false
}
</script>

<template>
  <div
    class="relative rounded-2xl overflow-hidden animate-fadeUp"
    :class="dismissed ? 'opacity-0 scale-95 pointer-events-none' : ''"
    :style="{ transition: dismissed ? 'all 0.25s ease' : '' }"
    @pointerdown="onPointerDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
  >
    <!-- 底层：掌握标记 -->
    <div
      class="absolute inset-0 flex items-center pl-5 rounded-2xl text-white font-bold text-sm"
      :style="{ background: 'linear-gradient(90deg, #4ade80 0%, #22c55e 100%)', opacity: Math.min(swipeX / 100, 1) }"
    >✓ {{ t('practiceMastered') }}</div>
    <!-- 卡片本体 -->
    <div
      class="flex flex-col rounded-2xl shadow-[0_2px_16px_rgba(0,0,0,0.06)] overflow-hidden theme-surface cursor-pointer active:scale-[0.99] border-l-[3px] border-l-[var(--primary)]/30 relative"
      :style="{ transform: `translateX(${swipeX}px)`, transition: swiping ? 'none' : 'transform 0.2s ease' }"
      @click="onSpeak"
    >
    <div class="flex items-center gap-3 px-4 py-3">
      <div
        class="w-8 h-8 rounded-full theme-soft text-primary flex items-center justify-center text-[11px] font-bold tabular-nums shrink-0"
      >
        {{ rowNumber }}
      </div>
      <div class="flex-1 min-w-0">
        <div class="text-[15px] font-bold text-content-original leading-snug">
          <RubyText v-if="item.ruby" :tokens="item.ruby" />
          <template v-else>{{ item.word }}</template>
        </div>
        <div class="text-[13px] mt-0.5 text-content-translation">{{ localMeaning(item, currentLang) }}</div>
        <div
          v-if="item.example"
          class="text-content-example mt-1 text-xs leading-relaxed"
          :class="item.audioExample ? 'cursor-pointer active:opacity-60' : ''"
          @pointerdown.stop
          @click.stop="playExample"
        >
          {{ item.example }}
          <br v-if="localExampleCn(item, currentLang)" />
          <span v-if="localExampleCn(item, currentLang)">{{ localExampleCn(item, currentLang) }}</span>
        </div>
      </div>
      <div class="flex flex-col items-end shrink-0 gap-1.5">
        <div class="flex items-center gap-1.5">
          <span
            class="theme-muted text-[10px] leading-tight tabular-nums whitespace-nowrap pointer-events-none"
          >{{ statsLine }}</span>
          <button
            type="button"
            class="w-6 h-6 flex items-center justify-center cursor-pointer transition-all active:scale-90 bg-transparent border-none outline-none p-0"
            @pointerdown.stop
            @click.stop="onToggleStar"
          >
            <svg v-if="starred" class="w-4 h-4 text-[#e8a44c]" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            <svg v-else class="w-4 h-4 theme-muted opacity-40 hover:opacity-70" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          </button>
        </div>
        <button
          type="button"
          class="w-9 h-9 rounded-full border-2 flex items-center justify-center cursor-pointer transition-all border-[#e8e2dc] theme-surface text-primary shadow-[0_2px_8px_rgba(0,0,0,0.06)] hover:border-primary hover:shadow-[0_4px_12px_rgba(232,115,90,0.2)] active:scale-[0.96]"
          :aria-label="t('listPlayFromHere')"
          @pointerdown.stop
          @click.stop="onPlayListFromRow"
        >
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
        </button>
      </div>
    </div>
    </div>
  </div>
</template>
