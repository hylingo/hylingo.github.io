<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useAppStore } from '../../stores/app'
import { quizQueueTick } from '@/learning'
import { useMasteryTest } from '../../composables/useMasteryTest'
import { useJaSpeechRecognition } from '../../composables/useJaSpeechRecognition'
import { speakLoop, stopLoop, looping } from '../../composables/useAudio'
import { useLang, currentLang } from '@/i18n'
import { speechMatchesVocab } from '@/utils/jpSpeechMatch'
import { localMeaning, localExampleCn } from '@/utils/helpers'
import RubyText from '@/components/common/RubyText.vue'

const { t } = useLang()
const lang = computed(() => currentLang.value)
const {
  supported: sttSupported,
  listening: sttListening,
  interimText: sttInterim,
  lastFinalText: sttFinal,
  lastError: sttLastError,
  start: startJaStt,
  stopListening: stopJaStt,
  abortListening: abortJaStt,
  resetSessionText: resetJaStt,
} = useJaSpeechRecognition()
const lastHeard = ref('')
const sttMismatch = ref(false)
const justPassed = ref(false)
const store = useAppStore()
const {
  currentItem,
  isAnswered,
  passedCount,
  totalCount,
  hasItems,
  testPhase,
  rebuildItems,
  markPassed,
  passPhase1,
  skip,
  nextAfterPass,
  returnToListenPractice,
  speakCurrent,
} = useMasteryTest()

watch(
  () => store.isDataLoaded,
  (ok) => {
    if (ok) rebuildItems()
  },
  { immediate: true },
)

watch(quizQueueTick, () => rebuildItems())

watch(() => store.currentCat, () => {
  rebuildItems()
})

watch(currentItem, () => {
  abortJaStt()
  resetJaStt()
  lastHeard.value = ''
  sttMismatch.value = false
  justPassed.value = false
})

const sttLiveText = computed(() => {
  const f = sttFinal.value
  const i = sttInterim.value
  return (f + i).trim()
})

const sttErrorHint = computed(() => {
  const e = sttLastError.value
  if (!e || e === 'aborted') return ''
  if (e === 'not-allowed') return t('sttDenied')
  return t('sttError')
})

function onSttDone(full: string) {
  lastHeard.value = full
  const item = currentItem.value
  if (!item || isAnswered.value) return
  if (!full) {
    sttMismatch.value = false
    return
  }
  if (speechMatchesVocab(full, item)) {
    sttMismatch.value = false
    if (testPhase.value === 'read') {
      // 第一步通过，标记并回到随机池
      passPhase1()
      resetJaStt()
      lastHeard.value = ''
      return
    } else {
      // 第二步也通过，整体通过
      justPassed.value = true
      markPassed()
    }
  } else {
    sttMismatch.value = true
  }
}

function onRecordDown() {
  sttMismatch.value = false
  startJaStt(onSttDone)
}

function onRecordUp() {
  if (sttListening.value) stopJaStt()
}

function handleNext() {
  if (isAnswered.value) {
    nextAfterPass()
  } else {
    skip()
  }
}

function toggleLoop() {
  if (looping.value) {
    stopLoop()
  } else {
    const it = currentItem.value
    if (it) speakLoop(it.word, it.audio)
  }
}

const progressText = computed(() => {
  if (totalCount.value === 0 && passedCount.value === 0) return ''
  return t('testProgress').replace('{passed}', String(passedCount.value)).replace('{total}', String(totalCount.value))
})
</script>

<template>
  <div class="flex flex-col items-center gap-4 px-4 py-6">
    <div class="w-full max-w-[420px] mx-auto text-[11px] theme-muted text-center leading-relaxed px-2 space-y-1.5">
      <p>{{ t('masteryGraduateHint') }}</p>
    </div>
    <div v-if="progressText" class="text-sm theme-muted font-medium text-center px-1">{{ progressText }}</div>

    <!-- Phase indicator -->
    <div v-if="currentItem && hasItems && !isAnswered" class="text-xs font-medium px-3 py-1 rounded-full" :class="testPhase === 'read' ? 'bg-[#e8735a]/10 text-[#e8735a]' : 'bg-[#5b8a72]/10 text-[#5b8a72]'">
      {{ testPhase === 'read' ? t('testPhaseRead') : t('testPhaseRecall') }}
    </div>

    <!-- Card -->
    <div
      v-if="currentItem && hasItems"
      class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center animate-fadeUp"
      :class="isAnswered ? '' : 'cursor-pointer active:scale-[0.98]'"
      @click="speakCurrent"
    >
      <!-- Phase 1 read: 显示日文原文 -->
      <template v-if="testPhase === 'read' && !isAnswered">
        <div class="text-3xl font-bold theme-text mb-3">
          <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
          <template v-else>{{ currentItem.word }}</template>
        </div>
        <div v-if="currentItem.example" class="text-sm theme-muted leading-relaxed">
          {{ currentItem.example }}
        </div>
      </template>

      <!-- Phase 2 recall: 只显示释义 -->
      <template v-else-if="testPhase === 'recall' && !isAnswered">
        <div class="text-xl font-bold theme-text mb-4">{{ localMeaning(currentItem, lang) }}</div>
        <div v-if="localExampleCn(currentItem, lang)" class="text-sm theme-muted leading-relaxed">
          {{ localExampleCn(currentItem, lang) }}
        </div>
      </template>

      <!-- 通过后：显示全部 -->
      <template v-else>
        <div class="text-3xl font-bold theme-text mb-3">
          <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
          <template v-else>{{ currentItem.word }}</template>
        </div>
        <div class="text-xl font-bold theme-text mb-4">{{ localMeaning(currentItem, lang) }}</div>
        <div v-if="currentItem.example" class="text-sm theme-muted leading-relaxed">
          {{ currentItem.example }}
          <br v-if="localExampleCn(currentItem, lang)" />
          <span v-if="localExampleCn(currentItem, lang)" class="text-[13px]" style="color: var(--accent)">{{ localExampleCn(currentItem, lang) }}</span>
        </div>
      </template>

      <!-- Pass indicator -->
      <div
        v-if="justPassed"
        class="mt-4 py-2 px-4 rounded-xl bg-[#5b8a72]/10 text-[#5b8a72] font-semibold text-sm animate-fadeUp"
      >
        {{ t('testPassed') }}
      </div>
    </div>

    <div v-if="!hasItems" class="text-sm theme-muted text-center py-8">
      {{ t('masteryEmptyQueue') }}
    </div>

    <!-- STT controls -->
    <div
      v-if="hasItems && !isAnswered"
      class="w-full max-w-[400px] flex flex-col gap-2 text-sm"
    >
      <p v-if="!sttSupported" class="text-xs theme-muted text-center leading-relaxed">
        {{ t('sttNotSupported') }}
      </p>
      <template v-else>
        <button
          type="button"
          class="w-full min-h-[48px] py-3 px-3 rounded-[10px] text-sm font-medium transition-all border-2 select-none"
          :class="sttListening
            ? 'btn-grad-primary btn-grad-primary--pressed text-white scale-[1.02]'
            : 'theme-surface theme-muted hover:border-[#e8735a]'"
          @pointerdown.prevent="onRecordDown"
          @pointerup.prevent="onRecordUp"
          @pointerleave="onRecordUp"
          @contextmenu.prevent
        >
          {{ sttListening ? t('sttListening') : t('sttHoldToRecord') }}
        </button>
        <p v-if="sttListening && sttLiveText" class="text-xs theme-muted break-words">
          {{ t('sttHeard') }}：{{ sttLiveText }}
        </p>
        <p v-else-if="lastHeard" class="text-xs theme-muted break-words">
          {{ t('sttHeard') }}：{{ lastHeard }}
        </p>
        <p v-if="sttMismatch" class="text-xs text-amber-800 dark:text-amber-200/90 leading-relaxed">
          {{ t('sttMismatch') }}
        </p>
        <p v-if="sttErrorHint" class="text-xs text-red-600 dark:text-red-400/90">
          {{ sttErrorHint }}
        </p>
      </template>
    </div>

    <button
      v-if="hasItems && currentItem && !isAnswered"
      type="button"
      class="w-full max-w-[400px] py-2.5 px-3 rounded-[10px] text-sm font-medium border-2 cursor-pointer transition-all theme-surface theme-muted hover:border-[#5b8a72]"
      @click="returnToListenPractice"
    >
      {{ t('quizReturnToListenPractice') }}
    </button>

    <!-- Action buttons -->
    <div v-if="hasItems" class="flex items-center gap-3 w-full max-w-[400px]">
      <button
        v-if="isAnswered"
        type="button"
        class="py-3 px-5 rounded-[10px] border-2 flex items-center justify-center cursor-pointer transition-all"
        :class="looping ? 'btn-grad-primary text-white' : 'border-[#e8e2dc] theme-surface hover:border-[#e8735a]'"
        @click="toggleLoop"
      >
        <svg v-if="looping" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 2l4 4-4 4"/><path d="M3 11v-1a4 4 0 014-4h14"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v1a4 4 0 01-4 4H3"/></svg>
      </button>
      <button
        type="button"
        class="flex-1 py-3 rounded-[10px] text-base font-semibold cursor-pointer transition-all btn-grad-primary"
        @click="handleNext"
      >
        {{ t('testNext') }}
      </button>
    </div>
  </div>
</template>
