<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { useLoopPlayer } from '../../composables/useLoopPlayer'
import { useJaSpeechRecognition } from '../../composables/useJaSpeechRecognition'
import { useVoiceRecorder } from '../../composables/useVoiceRecorder'
import { useLang } from '@/i18n'
import { localMeaning } from '@/utils/helpers'
import { normalizeJpSpeech } from '@/utils/jpSpeechMatch'
import { recordFollowComplete } from '@/composables/useStats'
import { isStarred, toggleStar, starredTick } from '@/learning'
import RubyText from '@/components/common/RubyText.vue'
import ArticleCover from '@/components/common/ArticleCover.vue'
import { enablePlayerDebugLogButtons } from '@/config/features'

const { t, currentLang } = useLang()

const {
  loopPlaylist, loopIndex, loopPlaying, loopPaused, loopRepeat, loopPauseAutoAdvance,
  togglePlay, stop, toggleRepeat, prevTrack, nextTrack,
  exportLoopDebugLogs, clearLoopDebugLogs,
} = useLoopPlayer()

const { supported: sttSupported, start: startStt, stopListening, abortListening } = useJaSpeechRecognition()
const { recording, audioUrl, startRecording, stopRecording, clearRecording } = useVoiceRecorder()

const visible = computed(() => loopPlaying.value || loopPaused.value)
const currentItem = computed(() => loopPlaylist.value[loopIndex.value])
const collapsed = ref(false)

// === 跟读 ===
const followMode = ref(false)
const sttResult = ref('')
const sttScore = ref<number | null>(null)
const readPassedSet = ref(new Set<number>())
const allPassed = ref(false)

// 回放
const playbackAudio = ref<HTMLAudioElement | null>(null)
const isPlayingBack = ref(false)
const playbackProgress = ref(0)
let playbackRaf = 0

const readProgress = computed(() => `${readPassedSet.value.size}/${loopPlaylist.value.length}`)
const currentPassed = computed(() => readPassedSet.value.has(loopIndex.value))

watch(loopIndex, () => {
  sttResult.value = ''
  sttScore.value = null
  stopPlayback()
  clearRecording()
})

// 显隐切换：展开时取消折叠；隐藏时清掉跟读相关瞬时状态
watch(visible, (v) => {
  if (v) {
    collapsed.value = false
    return
  }
  followMode.value = false
  readPassedSet.value = new Set()
  allPassed.value = false
  sttResult.value = ''
  sttScore.value = null
  stopPlayback()
  clearRecording()
})

function lcsLen(a: string, b: string): number {
  const m = a.length, n = b.length
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0))
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      dp[i][j] = a[i - 1] === b[j - 1] ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1])
  return dp[m][n]
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

function onFollowToggle() {
  followMode.value = !followMode.value
  loopPauseAutoAdvance.value = followMode.value
  if (followMode.value) {
    // 进入跟读：暂停播放
    if (!loopPaused.value) togglePlay()
  } else {
    abortListening()
    if (recording.value) stopRecording()
    stopPlayback()
    sttResult.value = ''
    sttScore.value = null
  }
}

/** 跟读模式下播放当前句原音 */
function playOriginal() {
  togglePlay()
}

let recordGuard = false

function onRecordDown(e: PointerEvent) {
  // 锁定 pointer 防止 pointerleave 误触发
  ;(e.target as HTMLElement)?.setPointerCapture?.(e.pointerId)
  recordGuard = true
  sttResult.value = ''
  sttScore.value = null
  stopPlayback()
  clearRecording()
  startRecording()
  if (sttSupported.value) {
    startStt((text: string) => {
      sttResult.value = text || ''
      if (currentItem.value) {
        const score = text ? calcScore(text, currentItem.value) : 0
        sttScore.value = score
        if (score >= 80) {
          readPassedSet.value.add(loopIndex.value)
          if (!allPassed.value && readPassedSet.value.size >= loopPlaylist.value.length) {
            allPassed.value = true
            recordFollowComplete(loopPlaylist.value.length)
          }
        }
      }
    })
  }
}

function onRecordUp() {
  if (!recordGuard) return
  recordGuard = false
  if (recording.value) stopRecording()
  stopListening()
}

// 回放控制
function togglePlayback() {
  if (!audioUrl.value) return
  if (isPlayingBack.value) {
    stopPlayback()
    return
  }
  const a = new window.Audio(audioUrl.value)
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
  if (playbackAudio.value) {
    playbackAudio.value.pause()
    playbackAudio.value = null
  }
  isPlayingBack.value = false
  playbackProgress.value = 0
  cancelAnimationFrame(playbackRaf)
}

onUnmounted(() => { stopPlayback() })

function scoreColor(score: number) {
  if (score >= 80) return '#4f8a6f'
  if (score >= 50) return '#c49a3c'
  return getComputedStyle(document.documentElement).getPropertyValue('--primary-dark').trim() || '#c45a3e'
}

function scoreLabel(score: number) {
  if (score >= 80) return '✓'
  if (score >= 50) return '△'
  return '✗'
}

const miniTitle = computed(() => currentItem.value?.word ?? '—')

/** 当前播放项是否来自文章（含 _articleId） */
const currentArticleId = computed<string | null>(() => {
  return currentItem.value?._articleId ?? null
})
const isArticleItem = computed(() => !!currentArticleId.value)

const currentStarred = computed(() => {
  starredTick.value
  const it = currentItem.value
  if (!it) return false
  return isStarred(it._cat ?? '', it.id)
})

function onToggleStar() {
  const it = currentItem.value
  if (!it) return
  toggleStar(it._cat ?? '', it.id)
}

async function copyDebugLogs() {
  try { await navigator.clipboard.writeText(exportLoopDebugLogs()); alert(t('debugCopied')) } catch (e) { alert(exportLoopDebugLogs()) }
}
function clearDebugLogs() { clearLoopDebugLogs(); alert(t('debugCleared')) }
function minimize() { collapsed.value = true }

/** 点击卡片主体：普通模式暂停/播放；跟读模式且未在录音时播放原音 */
function onCardMainClick() {
  if (followMode.value) {
    if (recording.value) return
    playOriginal()
  } else {
    togglePlay()
  }
}
</script>

<template>
  <!-- 收起 -->
  <div
    v-if="visible && collapsed"
    class="fixed left-0 right-0 z-[199] flex items-center gap-2 px-3 py-2.5 theme-loop-panel border-t shadow-[0_-4px_18px_rgba(0,0,0,0.08)] max-md:bottom-[calc(4rem+env(safe-area-inset-bottom,0px))] md:bottom-6 md:left-[200px] md:right-4 md:border-x md:border-b md:rounded-b-xl"
    style="border-color: var(--border)"
  >
    <button
      type="button"
      class="shrink-0 w-10 h-10 flex items-center justify-center rounded-full text-white shadow-md active:scale-[0.93] transition-transform"
      style="background: var(--grad-primary)"
      @click="togglePlay"
    >
      <svg v-if="loopPaused" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,6 18,12 8,18" /></svg>
      <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="9" y1="6" x2="9" y2="18" /><line x1="15" y1="6" x2="15" y2="18" /></svg>
    </button>
    <div class="flex-1 min-w-0 text-left">
      <div class="text-sm font-semibold text-content-original truncate">{{ miniTitle }}</div>
      <div class="text-[11px] theme-muted">{{ loopIndex + 1 }} / {{ loopPlaylist.length }}</div>
    </div>
    <button type="button" class="shrink-0 w-9 h-9 flex items-center justify-center rounded-full cursor-pointer theme-surface border" style="border-color: var(--border); color: var(--text-secondary)" @click="collapsed = false">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 15l-6-6-6 6" stroke-linecap="round" stroke-linejoin="round" /></svg>
    </button>
    <button type="button" class="shrink-0 w-9 h-9 flex items-center justify-center rounded-full cursor-pointer text-sm" style="color: var(--text-secondary)" @click="stop">✕</button>
  </div>

  <!-- 展开 -->
  <div v-if="visible && !collapsed" class="fixed inset-0 z-[200] flex items-center justify-center backdrop-blur-sm" :style="{ background: 'var(--overlay-scrim)' }">
    <div
      class="theme-loop-panel rounded-3xl overflow-hidden max-h-[min(92svh,900px)] flex flex-col shadow-[0_20px_60px_rgba(0,0,0,0.15)]"
      :class="isArticleItem
        ? 'w-[95%] max-w-xl md:w-[92%] md:max-w-lg'
        : 'w-[95%] max-w-lg md:w-[90%] md:max-w-sm'"
    >
      <!-- Info bar -->
      <div class="flex items-center justify-between px-4 pt-3 pb-2 md:px-5 shrink-0">
        <span class="text-[13px]" style="color: var(--text-secondary)">
          {{ loopIndex + 1 }} / {{ loopPlaylist.length }}
          <template v-if="followMode">
            <span class="mx-1 opacity-40">·</span>
            <span class="text-[#4f8a6f] font-medium">{{ readProgress }}</span>
          </template>
        </span>
        <div class="flex items-center gap-0.5">
          <button type="button" class="w-9 h-9 flex items-center justify-center rounded-full cursor-pointer" style="color: var(--text-secondary)" @click="minimize">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </button>
          <button type="button" class="w-9 h-9 flex items-center justify-center rounded-full cursor-pointer text-sm" style="color: var(--text-secondary)" @click="stop">✕</button>
        </div>
      </div>

      <!-- 文章模式：顶部场景图（占位，未生成时显示渐变图标） -->
      <div v-if="false && isArticleItem" class="px-4 md:px-5 shrink-0">
        <ArticleCover
          :article-id="currentArticleId"
          variant="hero"
          icon="book"
          class="rounded-2xl"
        />
      </div>

      <!-- Word card：点击原文区播放（普通模式 暂停/继续；跟读未录音时 播原音） -->
      <div v-if="currentItem" class="flex min-h-0 flex-1 flex-col overflow-y-auto px-4 py-5 text-center md:px-5 md:py-6">
        <div
          class="-mx-1 cursor-pointer rounded-2xl px-4 py-4 text-center outline-none transition-all hover:bg-black/[0.03] active:scale-[0.98] focus-visible:ring-2 focus-visible:ring-[var(--primary)]/30 dark:hover:bg-white/[0.05]"
          role="button"
          tabindex="0"
          :title="t('loopTapToPlay')"
          @click="onCardMainClick"
          @keydown.enter.prevent="onCardMainClick"
          @keydown.space.prevent="onCardMainClick"
        >
          <div class="text-content-original text-3xl font-bold leading-snug">
            <RubyText v-if="currentItem.ruby" :tokens="currentItem.ruby" />
            <template v-else>{{ currentItem.word }}</template>
          </div>
          <div class="mt-2 text-[15px] text-content-translation">{{ localMeaning(currentItem, currentLang) }}</div>
        </div>
        <!-- 星标 -->
        <button
          type="button"
          class="mt-2 mx-auto w-8 h-8 flex items-center justify-center cursor-pointer transition-all active:scale-90 bg-transparent border-none outline-none"
          @click.stop="onToggleStar"
        >
          <svg v-if="currentStarred" class="w-5 h-5 text-[#e8a44c]" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          <svg v-else class="w-5 h-5 theme-muted opacity-30 hover:opacity-60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
        </button>

        <!-- 跟读区域：固定结构，不因状态变化改变高度 -->
        <div v-if="followMode" class="mt-4 flex flex-col items-center" @click.stop>

          <!-- 结果区域（固定高度，在录音按钮上方） -->
          <div class="h-[100px] flex flex-col items-center justify-center w-full">
            <!-- 有结果 -->
            <template v-if="audioUrl && sttScore !== null && !recording">
              <div class="flex items-center justify-center gap-2 mb-1">
                <span class="text-2xl font-bold" :style="{ color: scoreColor(sttScore) }">{{ scoreLabel(sttScore) }}</span>
                <span class="text-lg font-bold tabular-nums" :style="{ color: scoreColor(sttScore) }">{{ sttScore }}</span>
              </div>
              <div v-if="sttResult" class="text-base theme-text mb-2 leading-relaxed px-2">{{ sttResult }}</div>
              <!-- 回放条 -->
              <div
                class="relative h-9 rounded-xl overflow-hidden cursor-pointer w-full max-w-[260px]"
                style="background: color-mix(in srgb, var(--text) 8%, transparent)"
                @click="togglePlayback"
              >
                <div class="absolute inset-y-0 left-0 rounded-xl transition-[width] duration-100" :style="{ width: playbackProgress + '%', background: scoreColor(sttScore) + '20' }" />
                <div class="relative flex items-center justify-center gap-2 h-full px-4">
                  <svg v-if="!isPlayingBack" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" :style="{ color: scoreColor(sttScore) }"><polygon points="8,6 18,12 8,18" /></svg>
                  <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" :style="{ color: scoreColor(sttScore) }"><line x1="9" y1="6" x2="9" y2="18" /><line x1="15" y1="6" x2="15" y2="18" /></svg>
                  <span class="text-[11px] font-medium" :style="{ color: scoreColor(sttScore) }">{{ isPlayingBack ? t('followPlaying') : t('followPlayback') }}</span>
                </div>
              </div>
            </template>

            <!-- 已通过 -->
            <template v-else-if="currentPassed && !recording">
              <div class="text-sm font-medium text-[#4f8a6f]">✓ {{ t('followPassed') }}</div>
            </template>

            <!-- 录音中 / 待录音（录音按钮在底栏） -->
            <template v-else>
              <div v-if="recording" class="text-xs theme-muted opacity-50">{{ t('followRecording') }}</div>
            </template>
          </div>

          <!-- 全部完成 -->
          <div v-if="allPassed" class="px-3 py-2 rounded-xl bg-[#4f8a6f]/10 text-sm font-medium text-[#4f8a6f]">
            🎉 {{ t('followAllPassed') }}
          </div>
        </div>
      </div>

      <!-- Controls：跟读模式底栏 = 音波+录音（原播放位）+ 下一首；听原音点原文区 -->
      <div class="flex shrink-0 items-center justify-center gap-3 px-4 pt-1 pb-4 md:gap-4 md:px-5 md:pb-5">
        <template v-if="followMode">
          <div class="flex w-full max-w-md items-center gap-2">
            <button
              type="button"
              class="flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full border transition-colors"
              :style="{ background: 'var(--primary-light)', color: 'var(--primary)', borderColor: 'var(--primary)' }"
              :aria-pressed="followMode"
              :title="t('loopFollowToggle')"
              @click="onFollowToggle"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>
              </svg>
            </button>
            <div class="flex min-w-0 flex-1 items-center justify-center gap-3">
              <div class="flex h-8 items-center gap-[3px]">
                <span
                  v-for="i in 5"
                  :key="i"
                  class="w-[3px] rounded-full transition-all duration-300"
                  :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'"
                  :style="{ height: recording ? undefined : '8px', animationDelay: recording ? (i * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }"
                />
              </div>
              <button
                type="button"
                class="flex h-16 w-16 shrink-0 cursor-pointer items-center justify-center rounded-full text-white transition-transform active:scale-[0.96]"
                :class="recording ? 'bg-red-500 shadow-[0_6px_20px_rgba(239,68,68,0.35)]' : 'shadow-[0_6px_20px_rgba(232,115,90,0.3)]'"
                :style="!recording ? { background: 'var(--grad-primary)', touchAction: 'none' } : { touchAction: 'none' }"
                :title="t('followHint')"
                @pointerdown.prevent="onRecordDown"
                @pointerup.prevent="onRecordUp"
                @pointercancel="onRecordUp"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                </svg>
              </button>
              <div class="flex h-8 items-center gap-[3px]">
                <span
                  v-for="i in 5"
                  :key="'r' + i"
                  class="w-[3px] rounded-full transition-all duration-300"
                  :class="recording ? 'bg-red-400 animate-wave' : 'bg-current opacity-20'"
                  :style="{ height: recording ? undefined : '8px', animationDelay: recording ? ((6 - i) * 0.12) + 's' : undefined, color: 'var(--text-secondary)' }"
                />
              </div>
            </div>
            <button
              type="button"
              class="flex h-10 w-10 shrink-0 cursor-pointer items-center justify-center rounded-full border"
              style="border-color: var(--border); background: var(--card); color: var(--text-secondary)"
              @click="nextTrack"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="19" y2="19" /><polygon points="17 12 7 19 7 5 17 12" /></svg>
            </button>
          </div>
        </template>

        <template v-else>
          <button
            type="button"
            class="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border transition-colors"
            style="border-color: var(--border); background: var(--card); color: var(--text-secondary)"
            :title="t('loopFollowToggle')"
            @click="onFollowToggle"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>
            </svg>
          </button>
          <button class="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border transition-all hover:scale-105 active:scale-95" style="border-color: var(--border); background: var(--card); color: var(--text-secondary)" @click="prevTrack">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="5" x2="5" y2="19" /><polygon points="7 12 17 19 17 5 7 12" /></svg>
          </button>
          <button
            type="button"
            class="flex h-14 w-14 cursor-pointer items-center justify-center rounded-full text-white shadow-[0_2px_8px_rgba(232,115,90,0.18)] transition-all active:scale-[0.93] hover:shadow-[0_3px_10px_rgba(232,115,90,0.22)]"
            style="background: var(--grad-primary)"
            :title="t('loopTapToPlay')"
            @click="togglePlay"
          >
            <svg v-if="loopPaused" width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,6 18,12 8,18" /></svg>
            <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><line x1="9" y1="6" x2="9" y2="18" /><line x1="15" y1="6" x2="15" y2="18" /></svg>
          </button>
          <button class="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border transition-all hover:scale-105 active:scale-95" style="border-color: var(--border); background: var(--card); color: var(--text-secondary)" @click="nextTrack">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="5" x2="19" y2="19" /><polygon points="17 12 7 19 7 5 17 12" /></svg>
          </button>
          <button
            class="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border transition-colors"
            :style="loopRepeat ? { background: 'var(--primary-light)', color: 'var(--primary)', borderColor: 'var(--primary)' } : { background: 'var(--card)', color: 'var(--text-secondary)', borderColor: 'var(--border)' }"
            @click="toggleRepeat"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="17 1 21 5 17 9" /><path d="M3 11V9a4 4 0 0 1 4-4h14" /><polyline points="7 23 3 19 7 15" /><path d="M21 13v2a4 4 0 0 1-4 4H3" />
              <text x="10" y="14" font-size="7" font-weight="bold" stroke="none" fill="currentColor" text-anchor="middle">1</text>
            </svg>
          </button>
        </template>
      </div>

      <div v-if="enablePlayerDebugLogButtons" class="flex items-center justify-end gap-2 px-4 pb-4 md:px-5 shrink-0">
        <button class="px-3 py-1.5 rounded-lg border text-xs cursor-pointer theme-surface" style="border-color: var(--border); color: var(--text-secondary)" @click="copyDebugLogs">{{ t('copyDebugLogs') }}</button>
        <button class="px-3 py-1.5 rounded-lg border text-xs cursor-pointer" style="border-color: var(--primary); background: var(--primary-light); color: var(--primary)" @click="clearDebugLogs">{{ t('clearDebugLogs') }}</button>
      </div>
    </div>
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
