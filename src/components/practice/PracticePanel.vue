<script setup lang="ts">
import { computed, watch, ref, onUnmounted } from 'vue'
import { useAppStore } from '../../stores/app'
import { useQuiz } from '../../composables/useQuiz'
import { speakWithExample } from '../../composables/useAudio'
import { useVoiceRecorder } from '../../composables/useVoiceRecorder'
import { useJaSpeechRecognition } from '../../composables/useJaSpeechRecognition'
import { normalizeJpSpeech } from '@/utils/jpSpeechMatch'
import { isStarred, toggleStar, starredTick } from '@/learning'
import { useLang, currentLang } from '@/i18n'
import { localMeaning } from '@/utils/helpers'
import type { QuizMode } from '@/composables/useQuiz'
import RubyText from '@/components/common/RubyText.vue'

const { t } = useLang()
const lang = computed(() => currentLang.value)
const store = useAppStore()

// 出题模式：原文 / 翻译 / 声音
const quizMode = ref<QuizMode>('word')
const QUIZ_MODES: { key: QuizMode; labelKey: string }[] = [
  { key: 'word', labelKey: 'quizMode_word' },
  { key: 'meaning', labelKey: 'quizMode_meaning' },
  { key: 'audio', labelKey: 'quizMode_audio' },
]
const {
  quizItems, quizIndex, isAnswered,
  articleBlockJustCompleted,
  showAnswer, submitCorrect, advanceAfterWrong,
  dismissArticleBlockComplete,
} = useQuiz()


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
    !articleBlockJustCompleted.value,
)

// 星标
const currentStarred = computed(() => {
  starredTick.value
  const it = currentItem.value
  if (!it) return false
  const cat = it._cat || store.currentCat
  return isStarred(cat, it.id)
})

function onToggleStar() {
  const it = currentItem.value
  if (!it) return
  const cat = it._cat || store.currentCat
  toggleStar(cat, it.id)
}

// 录音 & 语音识别
const { recording, audioUrl, startRecording, stopRecording, clearRecording } = useVoiceRecorder()

// 回放录音
const playbackAudio = ref<HTMLAudioElement | null>(null)
const isPlayingBack = ref(false)
const playbackProgress = ref(0)
let playbackRaf = 0

function togglePlayback() {
  if (!audioUrl.value) return
  if (isPlayingBack.value) { stopPlayback(); return }
  const a = new Audio(audioUrl.value)
  playbackAudio.value = a
  isPlayingBack.value = true
  playbackProgress.value = 0
  a.onended = () => { isPlayingBack.value = false; playbackProgress.value = 100 }
  a.play()
  function tick() {
    if (!isPlayingBack.value) return
    if (a.duration > 0) playbackProgress.value = (a.currentTime / a.duration) * 100
    playbackRaf = requestAnimationFrame(tick)
  }
  tick()
}

function stopPlayback() {
  if (playbackAudio.value) { playbackAudio.value.pause(); playbackAudio.value = null }
  isPlayingBack.value = false
  playbackProgress.value = 0
  cancelAnimationFrame(playbackRaf)
}

onUnmounted(() => stopPlayback())

const { supported: sttSupported, listening: sttListening, start: startStt, stopListening: stopStt } = useJaSpeechRecognition()
const sttResult = ref('')
const sttScore = ref<number | null>(null)

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
  stopPlayback()
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
  stopPlayback()
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
}

function playCurrentAudio() {
  const item = currentItem.value
  if (item) speakWithExample(item.word, item.audio)
}

// 切题时重置
watch(quizIndex, () => resetRecordState())

// 音频模式自动播放
watch([quizMode, quizIndex], () => {
  if (quizMode.value === 'audio' && !isAnswered.value && currentItem.value) {
    playCurrentAudio()
  }
})

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
  return t('allMastered')
})
</script>

<template>
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
    <div class="text-sm theme-muted font-medium text-center px-1 whitespace-pre-line">{{ progressText }}</div>

    <!-- ========== 练习模式 ========== -->
    <template v-if="true">
      <template v-if="hasQuizItems && currentItem">
        <!-- 不认识：显示答案 -->
        <template v-if="isAnswered">
          <div class="relative w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center cursor-pointer active:scale-[0.98] transition-transform" @click="playCurrentAudio">
            <button
              type="button"
              class="absolute top-3 right-3 w-7 h-7 flex items-center justify-center cursor-pointer bg-transparent border-none outline-none active:scale-90 transition-transform"
              @click.stop="onToggleStar"
            >
              <svg v-if="currentStarred" class="w-4 h-4 text-[#e8a44c]" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              <svg v-else class="w-4 h-4 theme-muted opacity-30 hover:opacity-60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            </button>
            <div class="text-content-original mb-2 text-3xl font-bold leading-relaxed">
              <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
              <template v-else>{{ currentItem.word }}</template>
            </div>
            <div class="text-xl font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>
          </div>

          <!-- 评分 + 回放 + 录音（固定高度区域，避免布局跳动） -->
          <div class="w-full max-w-[400px] flex flex-col items-center gap-2">
            <!-- 评分结果 -->
            <div v-if="sttScore !== null" class="flex items-center justify-center gap-2 w-full min-w-0">
              <span class="text-lg font-bold tabular-nums shrink-0" :style="{ color: scoreColor(sttScore) }">{{ sttScore }}</span>
              <span v-if="sttResult" class="text-sm theme-text truncate min-w-0">{{ sttResult }}</span>
            </div>

            <!-- 回放条（始终占位） -->
            <div
              class="relative h-9 rounded-xl overflow-hidden w-full"
              :class="audioUrl ? (recording ? 'opacity-40 pointer-events-none' : 'cursor-pointer') : 'opacity-0 pointer-events-none'"
              style="background: color-mix(in srgb, var(--text) 8%, transparent)"
              @click="togglePlayback"
            >
              <div
                class="absolute inset-y-0 left-0 rounded-xl transition-[width] duration-100"
                :style="{ width: playbackProgress + '%', background: (sttScore !== null ? scoreColor(sttScore) : 'var(--primary)') + '20' }"
              />
              <div class="relative flex items-center justify-center gap-2 h-full px-4">
                <svg v-if="!isPlayingBack" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" :style="{ color: sttScore !== null ? scoreColor(sttScore) : 'var(--primary)' }"><polygon points="8,6 18,12 8,18" /></svg>
                <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" :style="{ color: sttScore !== null ? scoreColor(sttScore) : 'var(--primary)' }"><line x1="9" y1="6" x2="9" y2="18" /><line x1="15" y1="6" x2="15" y2="18" /></svg>
                <span class="text-[11px] font-medium" :style="{ color: sttScore !== null ? scoreColor(sttScore) : 'var(--primary)' }">{{ isPlayingBack ? t('followPlaying') : t('followPlayback') }}</span>
              </div>
            </div>

            <!-- 录音 -->
            <div class="flex items-center justify-center gap-3">
              <div class="flex items-center gap-[3px] h-8">
                <span v-for="i in 5" :key="i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
              </div>
              <button type="button" class="w-14 h-14 flex items-center justify-center rounded-full text-white cursor-pointer active:scale-[0.96] transition-all" :class="recording ? 'bg-red-500 shadow-[0_6px_20px_rgba(239,68,68,0.35)]' : 'bg-gradient-to-b from-[#f38a73] to-[#e8735a] shadow-[0_6px_20px_rgba(232,115,90,0.3)]'" style="touch-action: none" @pointerdown.prevent="onTestRecordDown" @pointerup.prevent="onTestRecordUp" @pointercancel="onTestRecordUp">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>
              </button>
              <div class="flex items-center gap-[3px] h-8">
                <span v-for="i in 5" :key="'r'+i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
              </div>
            </div>
          </div>

          <button class="w-full max-w-[400px] py-3 rounded-[10px] text-base font-semibold cursor-pointer transition-all btn-grad-primary" @click="onPracticeWrongNext">{{ t('masteryNext') }}</button>
        </template>

        <!-- 出题：原文/翻译/声音 → 认识/不认识 -->
        <template v-else>
          <!-- 模式切换 -->
          <div class="flex items-center justify-center gap-1 mb-2">
            <button
              v-for="m in QUIZ_MODES" :key="m.key"
              type="button"
              class="rounded-full px-3 py-1 text-[11px] font-medium cursor-pointer transition-all border-none outline-none"
              :class="quizMode === m.key ? 'bg-[var(--primary)]/12 text-[var(--primary)]' : 'bg-transparent theme-muted hover:text-[var(--primary)]'"
              @click="quizMode = m.key"
            >{{ t(m.labelKey) }}</button>
          </div>

          <div class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center">
            <!-- 原文模式 -->
            <div v-if="quizMode === 'word'" class="text-content-original text-3xl font-bold leading-relaxed">{{ currentItem.word }}</div>
            <!-- 翻译模式 -->
            <div v-else-if="quizMode === 'meaning'" class="text-2xl font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>
            <!-- 声音模式 -->
            <div v-else class="flex flex-col items-center gap-3">
              <button
                type="button"
                class="w-20 h-20 rounded-full border-2 text-3xl cursor-pointer transition-all active:scale-95"
                style="border-color: var(--primary); background: var(--primary-light)"
                @click.stop="playCurrentAudio"
              >🔊</button>
            </div>
          </div>

          <div class="flex gap-3 w-full max-w-[400px]">
            <button class="flex-1 py-3 rounded-[10px] text-base font-semibold cursor-pointer transition-all btn-grad-primary" @click="onPracticeCorrect">{{ t('correct') }}</button>
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
