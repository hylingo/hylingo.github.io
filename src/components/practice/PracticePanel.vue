<script setup lang="ts">
import { computed, watch, ref, onMounted, onUnmounted } from 'vue'
import { useAppStore } from '../../stores/app'
import { useQuiz } from '../../composables/useQuiz'
import { speakWithExample } from '../../composables/useAudio'
import { useVoiceRecorder } from '../../composables/useVoiceRecorder'
import { useJaSpeechRecognition } from '../../composables/useJaSpeechRecognition'
import { recordReadTime } from '../../composables/useStats'
import { normalizeJpSpeech } from '@/utils/jpSpeechMatch'
import { isStarred, toggleStar, starredTick } from '@/learning'
import { markSentencePerfect, isSentencePerfect, articlePerfectTick } from '@/learning/articlePerfect'
import { useLang, currentLang } from '@/i18n'
import { localMeaning, localExampleCn } from '@/utils/helpers'
import type { QuizMode } from '@/composables/useQuiz'
import RubyText from '@/components/common/RubyText.vue'
import AppIcon from '@/components/common/AppIcon.vue'

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
  showAnswer, hideAnswer, submitStudy, submitSkip, submitKnown, submitMastered, nextQuestion,
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

// 文章精读题：当前句是否已满分过
const currentSentencePerfected = computed(() => {
  articlePerfectTick.value
  const it = currentItem.value as { _quizSource?: string; _articleId?: string; id?: number } | null
  if (!it || it._quizSource !== 'article' || !it._articleId || typeof it.id !== 'number') return false
  return isSentencePerfect(it._articleId, it.id)
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

// === 键盘快捷键：↓ 看答案 / → 下一个 / Space 按住录音 ===
let recKeyHeld = false
function onKeydown(e: KeyboardEvent) {
  const tag = (e.target as HTMLElement)?.tagName
  if (tag === 'INPUT' || tag === 'TEXTAREA') return
  if (store.currentMode !== 'practice') return
  if (!hasQuizItems.value || !currentItem.value) return

  if (e.key === 'ArrowDown') {
    e.preventDefault()
    if (!isAnswered.value) onShowAnswer()
  } else if (e.key === 'ArrowRight') {
    e.preventDefault()
    if (isAnswered.value) nextQuestion()
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault()
    if (!isAnswered.value) onShowAnswer()
  } else if (e.key === 'ArrowUp' && !e.repeat && !e.metaKey && !e.ctrlKey) {
    if (recKeyHeld) return
    recKeyHeld = true
    e.preventDefault()
    recordGuard = true
    sttResult.value = ''
    sttScore.value = null
    stopPlayback()
    clearRecording()
    if (useMediaRecorder) startRecording()
    if (sttSupported.value) startStt(onSttDone)
  }
}
function onKeyup(e: KeyboardEvent) {
  if (e.key === 'ArrowUp' && recKeyHeld) {
    e.preventDefault()
    recKeyHeld = false
    onRecordUp()
  }
}
onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  window.addEventListener('keyup', onKeyup)
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  window.removeEventListener('keyup', onKeyup)
})

const { supported: sttSupported, listening: sttListening, start: startStt, stopListening: stopStt, alternatives: sttAlternatives } = useJaSpeechRecognition()
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

function calcScore(transcript: string, item: { word: string; reading: string }, alts: string[] = []): number {
  const w = normalizeJpSpeech(item.word)
  const r = normalizeJpSpeech(item.reading)
  if (!w.length && !r.length) return 0
  const candidates = [transcript, ...alts].map(normalizeJpSpeech).filter(Boolean)
  if (!candidates.length) return 0
  let best = 0
  for (const tr of candidates) {
    const sW = w.length ? lcsLen(tr, w) / Math.max(tr.length, w.length) : 0
    const sR = r.length ? lcsLen(tr, r) / Math.max(tr.length, r.length) : 0
    const s = Math.max(sW, sR)
    if (s > best) best = s
  }
  return Math.round(best * 100)
}

function scoreColor(score: number) {
  if (score >= 80) return '#4f8a6f'
  if (score >= 50) return '#c49a3c'
  return getComputedStyle(document.documentElement).getPropertyValue('--primary-dark').trim() || '#c45a3e'
}

// === 听音模式：编辑距离打分 ===
const listenInput = ref('')
const listenScore = ref<number | null>(null)
const listenSubmitted = ref(false)
const LISTEN_PASS = 70

/** Levenshtein 编辑距离 */
function editDistance(a: string, b: string): number {
  if (a === b) return 0
  if (!a.length) return b.length
  if (!b.length) return a.length
  let prev = new Array(b.length + 1)
  let curr = new Array(b.length + 1)
  for (let j = 0; j <= b.length; j++) prev[j] = j
  for (let i = 1; i <= a.length; i++) {
    curr[0] = i
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1
      curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
    }
    ;[prev, curr] = [curr, prev]
  }
  return prev[b.length]
}

function calcListenScore(input: string, item: { word: string; reading?: string }): number {
  const norm = (s: string) => normalizeJpSpeech(s || '')
  const a = norm(input)
  if (!a) return 0
  const w = norm(item.word)
  const r = norm(item.reading || '')
  const score = (target: string) => {
    if (!target) return 0
    const d = editDistance(a, target)
    return Math.max(0, Math.round((1 - d / Math.max(a.length, target.length)) * 100))
  }
  return Math.max(score(w), score(r))
}

function resetInteractionState() {
  sttResult.value = ''
  sttScore.value = null
  listenInput.value = ''
  listenScore.value = null
  listenSubmitted.value = false
  stopPlayback()
  clearRecording()
  hideAnswer()
}

// === 录音（按住录音按钮）===
let recordGuard = false
// Android 和 iOS 都会让 MediaRecorder 与 SpeechRecognition 抢麦：
//   Android Chrome → SR 立即 aborted
//   iOS Safari     → SR 只收到静音，反复 "No speech detected"
// 移动端统一只跑 STT，放弃回放录音。
const UA = typeof navigator !== 'undefined' ? navigator.userAgent : ''
const IS_MOBILE = /Android/i.test(UA) || /iPhone|iPad|iPod/i.test(UA)
const useMediaRecorder = !IS_MOBILE

function onRecordDown(e: PointerEvent) {
  ;(e.target as HTMLElement)?.setPointerCapture?.(e.pointerId)
  recordGuard = true
  sttResult.value = ''
  sttScore.value = null
  stopPlayback()
  clearRecording()
  if (useMediaRecorder) startRecording()
  if (sttSupported.value) startStt(onSttDone)
}

function onRecordUp() {
  if (!recordGuard) return
  recordGuard = false
  // 松开即算一次"录"（无论识别好坏）
  recordReadTime()
  setTimeout(() => {
    if (useMediaRecorder && recording.value) stopRecording()
    if (sttListening.value) stopStt()
  }, 350)
}

function onSttDone(text: string) {
  sttResult.value = text || ''
  const item = currentItem.value
  if (!item) return
  const score = text ? calcScore(text, item, sttAlternatives.value) : 0
  sttScore.value = score
  // 高分（≥95）且是文章精读题：打印记（容许 STT 轻微误差）
  if (score >= 95) {
    const asArt = item as { _quizSource?: string; _articleId?: string; id?: number }
    if (asArt._quizSource === 'article' && asArt._articleId && typeof asArt.id === 'number') {
      markSentencePerfect(asArt._articleId, asArt.id)
    }
  }
}

// === 听音模式：提交输入 ===
function onListenSubmit() {
  const item = currentItem.value
  if (!item) return
  const score = calcListenScore(listenInput.value, item)
  listenScore.value = score
  listenSubmitted.value = true
  if (score >= LISTEN_PASS) {
    // 听音满分也标记句子掌握
    if (score >= 95) {
      const asArt = item as { _quizSource?: string; _articleId?: string; id?: number }
      if (asArt._quizSource === 'article' && asArt._articleId && typeof asArt.id === 'number') {
        markSentencePerfect(asArt._articleId, asArt.id)
      }
    }
    submitStudy()
    // 略停顿让用户看到分数再进下一题
    setTimeout(() => {
      nextQuestion()
    }, 600)
  }
}

// === 底部按钮 ===
function onShowAnswer() {
  showAnswer()
  playCurrentAudio()
  // 主动看答案 = 没记住：counts 回退 + 近期重排
  submitSkip()
}

function onMastered() {
  submitMastered()
  resetInteractionState()
}

function playCurrentAudio() {
  const item = currentItem.value
  if (item) speakWithExample(item.word, item.audio)
}

// 切题或切 Tab：先重置上一种交互的残留状态，再在音频模式下自动播放
watch([quizMode, quizIndex], () => {
  resetInteractionState()
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
  <div class="flex flex-col items-center gap-2 pt-2 pb-6" :class="{ 'no-select-while-hold': recording || sttListening }">
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

    <!-- ========== 练习模式（统一布局，无 isAnswered 分屏）========== -->
    <template v-if="hasQuizItems && currentItem">
      <!-- Tab 切换 -->
      <div class="flex items-center justify-center gap-1">
        <button
          v-for="m in QUIZ_MODES" :key="m.key"
          type="button"
          class="rounded-full px-3 py-1 text-[11px] font-medium cursor-pointer transition-all border-none outline-none"
          :class="quizMode === m.key ? 'bg-[var(--primary)]/12 text-[var(--primary)]' : 'bg-transparent theme-muted hover:text-[var(--primary)]'"
          @click="quizMode = m.key"
        >{{ t(m.labelKey) }}</button>
      </div>

      <!-- 题面卡片 -->
      <div
        class="relative w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center transition-all"
        :class="{ 'cursor-pointer hover:bg-black/[0.03] active:scale-[0.98] dark:hover:bg-white/[0.05]': isAnswered }"
        @click="isAnswered && playCurrentAudio()"
      >
        <span
          v-if="currentItem.level"
          class="pointer-events-none absolute top-3 left-4 z-[1] text-[10px] font-medium tabular-nums leading-none theme-muted opacity-40"
          aria-hidden="true"
        >{{ currentItem.level }}</span>
        <span
          v-if="currentSentencePerfected"
          class="pointer-events-none absolute top-2.5 right-10 z-[1] text-base leading-none select-none"
          :title="'已满分'"
          aria-label="已满分"
        >💯</span>
        <button
          type="button"
          class="absolute top-3 right-3 w-7 h-7 flex items-center justify-center cursor-pointer bg-transparent border-none outline-none active:scale-90 transition-transform"
          @click.stop="onToggleStar"
        >
          <svg v-if="currentStarred" class="w-4 h-4 text-[#e8a44c]" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <svg v-else class="w-4 h-4 theme-muted opacity-30 hover:opacity-60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
        </button>

        <!-- 原文模式：显示原文 -->
        <div v-if="quizMode === 'word'" class="text-content-original text-3xl font-bold leading-relaxed">
          <RubyText v-if="isAnswered && currentItem.ruby" :tokens="currentItem.ruby" />
          <template v-else>{{ currentItem.word }}</template>
        </div>
        <!-- 翻译模式：显示中文 -->
        <div v-else-if="quizMode === 'meaning'" class="text-2xl font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>
        <!-- 听音模式：扬声器按钮 -->
        <div v-else class="flex flex-col items-center gap-3">
          <button
            type="button"
            class="w-20 h-20 rounded-full border-2 cursor-pointer transition-all active:scale-95 flex items-center justify-center"
            style="border-color: var(--primary); background: var(--primary-light); color: var(--primary)"
            @click.stop="playCurrentAudio"
          ><AppIcon name="volume" :size="32" /></button>
        </div>

        <!-- 看答案后展开：补充对照 + 例句 -->
        <template v-if="isAnswered">
          <div v-if="quizMode === 'word'" class="mt-4 text-xl font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>
          <div v-else-if="quizMode === 'meaning'" class="mt-4 text-2xl font-bold text-content-original">
            <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
            <template v-else>{{ currentItem.word }}</template>
          </div>
          <div v-else class="mt-4 text-2xl font-bold text-content-original">
            <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
            <template v-else>{{ currentItem.word }}</template>
            <div class="mt-1 text-base font-bold text-content-translation">{{ localMeaning(currentItem, lang) }}</div>
          </div>
          <div v-if="currentItem.example" class="mt-3 text-sm text-content-example leading-relaxed opacity-80">
            {{ currentItem.example }}
            <template v-if="localExampleCn(currentItem, lang)"><br />{{ localExampleCn(currentItem, lang) }}</template>
          </div>
        </template>
      </div>

      <!-- 交互区：录音 (word/meaning) 或 输入 (audio) -->
      <div class="w-full max-w-[400px] flex flex-col items-center gap-2">
        <!-- ========== 录音模式（word + meaning） ========== -->
        <template v-if="quizMode !== 'audio'">
          <!-- 评分结果（始终占位，避免录音按钮按下时布局跳动导致误选中文本） -->
          <div class="flex items-center justify-center gap-2 w-full min-w-0 h-7" :style="{ visibility: sttScore !== null ? 'visible' : 'hidden' }">
            <span v-if="sttScore !== null" class="text-lg font-bold tabular-nums shrink-0" :style="{ color: scoreColor(sttScore) }">{{ sttScore }}</span>
            <span v-if="sttResult" class="text-sm theme-text truncate min-w-0">{{ sttResult }}</span>
          </div>

          <!-- 回放条 -->
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

          <!-- 录音按钮 -->
          <div class="flex items-center justify-center gap-3">
            <div class="flex items-center gap-[3px] h-8">
              <span v-for="i in 5" :key="i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
            </div>
            <button type="button" class="select-none w-14 h-14 flex items-center justify-center rounded-full cursor-pointer active:scale-[0.96] transition-all" :style="recording ? { background: 'var(--primary)', color: '#fff', boxShadow: '0 2px 8px rgba(0,0,0,0.18)', touchAction: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' } : { background: 'color-mix(in srgb, var(--primary) 18%, transparent)', color: 'var(--primary)', touchAction: 'none', WebkitUserSelect: 'none', WebkitTouchCallout: 'none' }" @pointerdown.prevent="onRecordDown" @pointerup.prevent="onRecordUp" @pointercancel="onRecordUp" @contextmenu.prevent>
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/></svg>
            </button>
            <div class="flex items-center gap-[3px] h-8">
              <span v-for="i in 5" :key="'r'+i" class="w-[3px] rounded-full transition-all duration-300" :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'" :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }" />
            </div>
          </div>
        </template>

        <!-- ========== 听音输入模式 ========== -->
        <template v-else>
          <input
            v-model="listenInput"
            type="text"
            :placeholder="t('listenInputPlaceholder')"
            class="w-full rounded-xl border-2 theme-surface theme-text px-4 py-3 text-base outline-none transition-colors"
            :class="listenSubmitted && listenScore !== null && listenScore < 70 ? 'border-[var(--primary-dark)]' : 'border-[var(--border)] focus:border-[var(--primary)]'"
            @keyup.enter="onListenSubmit"
          />
          <div v-if="listenSubmitted && listenScore !== null" class="flex items-center justify-center gap-2 w-full">
            <span class="text-lg font-bold tabular-nums" :style="{ color: scoreColor(listenScore) }">{{ listenScore }}</span>
            <span v-if="listenScore < 70" class="text-xs theme-muted">{{ t('listenScoreFail') }}</span>
          </div>
          <button
            type="button"
            class="w-full py-2.5 rounded-[10px] text-sm font-semibold cursor-pointer transition-all btn-grad-primary"
            @click="onListenSubmit"
          >{{ t('listenSubmit') }}</button>
        </template>
      </div>

      <!-- 底部按钮：翻开前 认识了|看答案，翻开后 下一个 -->
      <div class="flex flex-col items-center gap-7 w-full max-w-[400px] mt-1">
        <div class="flex items-center gap-2 w-full">
          <template v-if="!isAnswered">
            <button
              type="button"
              class="flex-1 py-3.5 rounded-[12px] text-base font-medium cursor-pointer transition-all border theme-surface"
              style="border-color: var(--primary); color: var(--primary)"
              @click="submitKnown"
            >{{ t('practiceKnown') }}</button>
            <button
              type="button"
              class="flex-1 py-3.5 rounded-[12px] text-base font-medium cursor-pointer transition-all border theme-surface theme-muted"
              style="border-color: var(--border)"
              @click="onShowAnswer"
            >{{ t('practiceShowAnswer') }}</button>
          </template>
          <button
            v-else
            type="button"
            class="flex-1 py-3.5 rounded-[12px] text-base font-medium cursor-pointer transition-all border theme-surface theme-muted"
            style="border-color: var(--border)"
            @click="nextQuestion"
          >{{ t('next') }}</button>
        </div>
        <button
          type="button"
          class="py-1.5 px-3 text-xs cursor-pointer bg-transparent border-none outline-none theme-muted hover:opacity-80 transition-opacity"
          @click="onMastered"
        >{{ t('practiceMastered') }}</button>
        <div class="hidden md:block text-[11px] theme-muted opacity-60 tracking-wide select-none">{{ t('practiceShortcuts') }}</div>
      </div>
    </template>
    <template v-else>
      <div class="text-sm theme-muted text-center py-10">
        {{ articleCategoryPracticeEmpty ? t('articlePracticeEmptyShort') : t('allMastered') }}
      </div>
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
