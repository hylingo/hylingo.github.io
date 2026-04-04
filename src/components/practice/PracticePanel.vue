<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import { useMenuAnchor } from '@/composables/useMenuAnchor'
import { useAppStore } from '../../stores/app'
import { useQuiz } from '../../composables/useQuiz'
import { speakWithExample } from '../../composables/useAudio'
import { useVoiceRecorder } from '../../composables/useVoiceRecorder'
import { useJaSpeechRecognition } from '../../composables/useJaSpeechRecognition'
import { normalizeJpSpeech, speechMatchesVocab } from '@/utils/jpSpeechMatch'
import { useLang, currentLang } from '@/i18n'
import { localMeaning } from '@/utils/helpers'
import RubyText from '@/components/common/RubyText.vue'

const { t } = useLang()
const lang = computed(() => currentLang.value)
const store = useAppStore()
const {
  quizItems, quizIndex, isAnswered, quizScope, quizLevels,
  articleBlockJustCompleted,
  showAnswer, submitCorrect, advanceAfterWrong,
  testPass, testFail, testAdvance, setQuizScope, setQuizLevels,
  dismissArticleBlockComplete,
} = useQuiz()

// 级别筛选
const levelDropdownOpen = ref(false)
const LEVELS = ['N5', 'N4', 'N3', 'N2', 'N1']
const levelTriggerRef = ref<HTMLElement | null>(null)
const LEVEL_DROPDOWN_Z_BACKDROP = 450
const levelMenuStyle = useMenuAnchor(levelDropdownOpen, levelTriggerRef, { minWidth: 100 })
const levelPanelStyle = computed(() => ({ ...levelMenuStyle.value, borderColor: 'var(--border)' }))
function closeLevelDropdown() { levelDropdownOpen.value = false }
function toggleLevel(lv: string) {
  const cur = [...quizLevels.value]
  const idx = cur.indexOf(lv)
  if (idx >= 0) cur.splice(idx, 1); else cur.push(lv)
  setQuizLevels(cur)
}
function clearLevels() { setQuizLevels([]); closeLevelDropdown() }
const showLevelFilter = computed(() => store.currentCat === 'mix')

const isArticleSentencePractice = computed(
  () =>
    !!store.practiceArticleId &&
    quizItems.value.length > 0 &&
    (quizItems.value[0] as { _quizSource?: string })?._quizSource === 'article',
)

const articlePracticeKindLabel = computed(() => {
  if (!store.practiceArticleId) return ''
  const art = store.articles.find((a) => a.id === store.practiceArticleId)
  if (!art) return ''
  return art.format === 'dialogue' ? t('articlePracticeKindDialogue') : t('articlePracticeKindEssay')
})

const currentItem = computed(() => quizItems.value[quizIndex.value] ?? null)
const hasQuizItems = computed(() => quizItems.value.length > 0)

/** 文章/对话分类下无单词池时的练页空态（与「听」详情无分句提示同文案） */
const articleCategoryPracticeEmpty = computed(
  () =>
    (store.currentCat === 'articles' || store.currentCat === 'dialogues') &&
    !store.practiceArticleId &&
    !hasQuizItems.value &&
    !articleBlockJustCompleted.value &&
    quizScope.value === 'practice',
)

// 录音 & 语音识别
const { recording, startRecording, stopRecording, clearRecording } = useVoiceRecorder()
const { supported: sttSupported, listening: sttListening, start: startStt, stopListening: stopStt } = useJaSpeechRecognition()
const sttResult = ref('')
const sttScore = ref<number | null>(null)
const testPassed = ref(false)

function lcsLen(a: string, b: string): number {
  const m = a.length, n = b.length
  if (!m || !n) return 0
  const prev = new Uint16Array(n + 1)
  const curr = new Uint16Array(n + 1)
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++)
      curr[j] = a[i - 1] === b[j - 1] ? prev[j - 1] + 1 : Math.max(prev[j], curr[j - 1])
    prev.set(curr)
  }
  return curr[n]
}

function calcScore(transcript: string, item: { word: string; reading: string }): number {
  const tr = normalizeJpSpeech(transcript)
  if (!tr) return 0
  const w = normalizeJpSpeech(item.word)
  const r = normalizeJpSpeech(item.reading)
  const scoreW = w.length ? lcsLen(tr, w) / Math.max(tr.length, w.length) : 0
  const scoreR = r.length ? lcsLen(tr, r) / Math.max(tr.length, r.length) : 0
  return Math.round(Math.max(scoreW, scoreR) * 100)
}

function scoreColor(score: number) {
  if (score >= 80) return '#4f8a6f'
  if (score >= 50) return '#c49a3c'
  return '#c45a3e'
}

function resetRecordState() {
  sttResult.value = ''
  sttScore.value = null
  testPassed.value = false
  clearRecording()
}

// === 练习模式 ===
function onPracticeCorrect() {
  submitCorrect()
  resetRecordState()
}

function onPracticeWrong() {
  showAnswer()
  resetRecordState()
}

function onPracticeWrongNext() {
  advanceAfterWrong()
  resetRecordState()
}

// === 测试模式 ===
let recordGuard = false

function onTestRecordDown(e: PointerEvent) {
  ;(e.target as HTMLElement)?.setPointerCapture?.(e.pointerId)
  recordGuard = true
  sttResult.value = ''
  sttScore.value = null
  testPassed.value = false
  clearRecording()
  startRecording()
  if (sttSupported.value) startStt(onTestSttDone)
}

function onTestRecordUp() {
  if (!recordGuard) return
  recordGuard = false
  if (recording.value) stopRecording()
  if (sttListening.value) stopStt()
}

function onTestSttDone(text: string) {
  sttResult.value = text || ''
  const item = currentItem.value
  if (!item) return
  const score = text ? calcScore(text, item) : 0
  sttScore.value = score
  const matched = score >= 80 || (text ? speechMatchesVocab(text, item) : false)
  if (matched) {
    testPassed.value = true
    testPass()
  } else {
    testFail()
  }
}

function onTestNext() {
  testAdvance()
  resetRecordState()
}

function playCurrentAudio() {
  const item = currentItem.value
  if (item) speakWithExample(item.word, item.audio)
}

// 切题时重置
watch(quizIndex, () => resetRecordState())

const progressText = computed(() => {
  if (articleBlockJustCompleted.value) return ''
  if (isArticleSentencePractice.value && store.practiceArticleTitle) {
    return t('articlePracticeProgressLine', {
      kind: articlePracticeKindLabel.value,
      title: store.practiceArticleTitle,
      current: quizIndex.value + 1,
      total: quizItems.value.length,
    })
  }
  if (hasQuizItems.value) return `${quizIndex.value + 1} / ${quizItems.value.length}`
  if (articleCategoryPracticeEmpty.value) return ''
  return quizScope.value === 'test' ? t('testEmpty') : t('allMastered')
})
</script>

<template>
  <!-- 级别筛选 -->
  <div v-if="showLevelFilter" class="pb-2 relative">
    <button ref="levelTriggerRef" type="button" class="filter-chip px-3 py-1.5 rounded-full text-[13px] font-medium cursor-pointer whitespace-nowrap" :class="quizLevels.length > 0 ? 'filter-chip--on' : 'filter-chip--off'" @click="levelDropdownOpen = !levelDropdownOpen">
      {{ quizLevels.length > 0 ? quizLevels.join(' ') : t('levelSelect') }}
      <svg class="inline-block ml-1 -mr-0.5" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
    </button>
    <Teleport to="body">
      <template v-if="levelDropdownOpen">
        <div class="fixed inset-0" :style="{ position: 'fixed', inset: 0, zIndex: LEVEL_DROPDOWN_Z_BACKDROP, background: 'var(--overlay-scrim)' }" @pointerdown.prevent="closeLevelDropdown" />
        <div class="rounded-xl theme-surface shadow-[0_8px_32px_rgba(0,0,0,0.15)] border py-1" :style="levelPanelStyle" @pointerdown.stop>
          <button type="button" class="w-full text-left px-3 py-2 text-[13px] font-medium cursor-pointer transition-colors hover:bg-[#e8735a]/10" :class="quizLevels.length === 0 ? 'text-[#e8735a]' : 'theme-text'" @click="clearLevels()">{{ t('filterNone') }}</button>
          <button v-for="lv in LEVELS" :key="lv" type="button" class="w-full text-left px-3 py-2 text-[13px] font-medium cursor-pointer transition-colors hover:bg-[#e8735a]/10 flex items-center gap-2" @click="toggleLevel(lv)">
            <svg v-if="quizLevels.includes(lv)" class="shrink-0 text-[#e8735a]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
            <span v-else class="shrink-0 w-[14px]" />
            <span :class="quizLevels.includes(lv) ? 'text-[#e8735a]' : ''">{{ lv }}</span>
          </button>
        </div>
      </template>
    </Teleport>
  </div>

  <div class="flex flex-col items-center gap-4 py-6">
    <!-- 本篇练完 -->
    <template v-if="articleBlockJustCompleted">
      <div class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-8 text-center space-y-3">
        <div class="text-lg font-bold text-content-original">{{ t('articlePracticeCompleteTitle') }}</div>
        <p class="text-sm theme-muted leading-relaxed">
          {{ t('articlePracticeCompleteBody', { n: articleBlockJustCompleted.sentenceCount, title: articleBlockJustCompleted.title }) }}
        </p>
        <button
          type="button"
          class="w-full py-3 rounded-[10px] text-base font-semibold cursor-pointer btn-grad-primary"
          @click="dismissArticleBlockComplete"
        >
          {{ t('articlePracticeDismiss') }}
        </button>
      </div>
    </template>

    <template v-else>
    <!-- 练习 / 测试 切换（本篇逐句练仅练习模式） -->
    <div v-if="!isArticleSentencePractice" class="flex gap-2 w-full max-w-[400px]">
      <button
        v-for="s in (['practice', 'test'] as const)" :key="s"
        class="flex-1 py-2 rounded-lg text-sm font-medium transition-all border-2"
        :class="quizScope === s ? 'btn-grad-primary text-white' : 'theme-surface theme-muted hover:border-[#e8735a]'"
        @click="setQuizScope(s)"
      >
        {{ s === 'practice' ? t('scopePractice') : t('scopeTest') }}
      </button>
    </div>

    <div class="text-sm theme-muted font-medium text-center px-1 whitespace-pre-line">{{ progressText }}</div>

    <!-- ========== 测试模式 ========== -->
    <template v-if="quizScope === 'test'">
      <template v-if="hasQuizItems && currentItem">
        <!-- 卡片：只显示释义 -->
        <div class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center">
          <div class="mb-4 text-xl font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>

          <template v-if="testPassed">
            <div class="text-content-original mb-2 text-2xl font-bold">
              <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
              <template v-else>{{ currentItem.word }}</template>
            </div>
            <div class="text-sm text-content-translation">✓ {{ t('masteryPassed') }}</div>
          </template>

          <template v-else-if="sttScore !== null && !recording">
            <div class="text-lg font-bold tabular-nums mb-1" :style="{ color: scoreColor(sttScore) }">{{ sttScore }}</div>
            <div v-if="sttResult" class="text-base theme-text mb-1">{{ sttResult }}</div>
            <div class="text-xs theme-muted">{{ t('masteryTryAgain') }}</div>
          </template>
        </div>

        <!-- 录音按钮 -->
        <div v-if="!testPassed" class="flex items-center justify-center gap-3">
          <div class="flex items-center gap-[3px] h-8">
            <span v-for="i in 5" :key="i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
          </div>
          <button type="button" class="w-14 h-14 flex items-center justify-center rounded-full text-white cursor-pointer active:scale-[0.96] transition-all" :class="recording ? 'bg-red-500 shadow-[0_6px_20px_rgba(239,68,68,0.35)]' : 'bg-gradient-to-b from-[#f38a73] to-[#e8735a] shadow-[0_6px_20px_rgba(232,115,90,0.3)]'" style="touch-action: none" @pointerdown.prevent="onTestRecordDown" @pointerup.prevent="onTestRecordUp" @pointercancel="onTestRecordUp">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>
          </button>
          <div class="flex items-center gap-[3px] h-8">
            <span v-for="i in 5" :key="'r'+i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? ((6-i) * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
          </div>
        </div>

        <!-- 播放原音（测试通过后可以听） -->
        <button v-if="testPassed" type="button" class="w-12 h-12 rounded-full border-2 border-[#e8735a] text-[#e8735a] flex items-center justify-center mx-auto cursor-pointer hover:bg-[#e8735a]/10 active:scale-95" @click="playCurrentAudio">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,6 18,12 8,18" /></svg>
        </button>
      </template>
      <template v-else>
        <div class="text-sm theme-muted text-center py-10">{{ t('testEmpty') }}</div>
      </template>
    </template>

    <!-- ========== 练习模式 ========== -->
    <template v-else>
      <template v-if="hasQuizItems && currentItem">
        <!-- 不认识：显示答案 -->
        <template v-if="isAnswered">
          <div class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center">
            <div class="text-content-original mb-2 text-3xl font-bold leading-relaxed">
              <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
              <template v-else>{{ currentItem.word }}</template>
            </div>
            <div class="mb-4 text-xl font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>
            <button type="button" class="w-12 h-12 rounded-full border-2 border-[#e8735a] text-[#e8735a] flex items-center justify-center mx-auto cursor-pointer hover:bg-[#e8735a]/10 active:scale-95" @click="playCurrentAudio">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,6 18,12 8,18" /></svg>
            </button>
            <div v-if="sttScore !== null && !recording" class="mt-3">
              <div class="text-lg font-bold tabular-nums" :style="{ color: scoreColor(sttScore) }">{{ sttScore }}</div>
              <div v-if="sttResult" class="text-sm theme-text mt-0.5">{{ sttResult }}</div>
            </div>
          </div>

          <!-- 录音跟读 -->
          <div class="flex items-center justify-center gap-3">
            <div class="flex items-center gap-[3px] h-8">
              <span v-for="i in 5" :key="i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
            </div>
            <button type="button" class="w-14 h-14 flex items-center justify-center rounded-full text-white cursor-pointer active:scale-[0.96] transition-all" :class="recording ? 'bg-red-500 shadow-[0_6px_20px_rgba(239,68,68,0.35)]' : 'bg-gradient-to-b from-[#f38a73] to-[#e8735a] shadow-[0_6px_20px_rgba(232,115,90,0.3)]'" style="touch-action: none" @pointerdown.prevent="onTestRecordDown" @pointerup.prevent="onTestRecordUp" @pointercancel="onTestRecordUp">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>
            </button>
            <div class="flex items-center gap-[3px] h-8">
              <span v-for="i in 5" :key="'r'+i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? ((6-i) * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
            </div>
          </div>

          <button class="w-full max-w-[400px] py-3 rounded-[10px] text-base font-semibold cursor-pointer transition-all btn-grad-primary" @click="onPracticeWrongNext">{{ t('masteryNext') }}</button>
        </template>

        <!-- 出题：看日文（无注音） → 认识/不认识 -->
        <template v-else>
          <div class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center">
            <div class="text-content-original text-3xl font-bold leading-relaxed">{{ currentItem.word }}</div>
          </div>
          <div class="flex gap-3 w-full max-w-[400px]">
            <button class="flex-1 py-3 rounded-[10px] text-base font-semibold cursor-pointer transition-all btn-grad-accent" @click="onPracticeCorrect">{{ t('correct') }}</button>
            <button class="flex-1 py-3 rounded-[10px] text-base font-semibold cursor-pointer transition-all border-2 theme-surface theme-muted hover:border-[#c45a3e]" @click="onPracticeWrong">{{ t('wrong') }}</button>
          </div>
        </template>
      </template>
      <template v-else>
        <div class="text-sm theme-muted text-center py-10">
          {{ articleCategoryPracticeEmpty ? t('articlePracticeEmptyShort') : t('allMastered') }}
        </div>
      </template>
    </template>
    </template>
  </div>
</template>

<style scoped>
@keyframes wave {
  0%, 100% { height: 6px; }
  50% { height: 24px; }
}
.animate-wave {
  animation: wave 0.8s ease-in-out infinite;
}
</style>
