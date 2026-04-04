import { ref } from 'vue'
import { type DataItem } from '../stores/app'
import { audioEl, playMainTrack } from './useAudio'
import { recordListenTime } from './useStats'
import { recordItemListened } from './useSpacedRepetition'
import { t } from '@/i18n'
import { SILENT_KEEPALIVE_WAV, getGapWavUri } from '@/utils/silentWavGap'

const LOOP_DEBUG_KEY = 'loop_debug_logs_v1'
const LOOP_DEBUG_MAX = 200

const loopPlaylist = ref<(DataItem & { _cat: string })[]>([])
const loopIndex = ref(0)
const loopRound = ref(1)
const loopPlaying = ref(false)
const loopPaused = ref(false)
const loopRepeat = ref(false)
const loopPauseAutoAdvance = ref(false)
const listSpeaking = ref(false)

let _loopTimers: ReturnType<typeof setTimeout>[] = []
let silentAudio: HTMLAudioElement | null = null
let gapAudio: HTMLAudioElement | null = null

/** 每次开始播一条（含切歌）递增，用于丢弃上一轨残留的 play().catch / 旧闭包 */
let loopPlaySession = 0

/** iOS 上每次 setActionHandler 会触发锁屏界面重绘；与曲目无关，只注册一次 */
let mediaSessionActionsRegistered = false

type LoopDebugEntry = {
  ts: string
  event: string
  index: number
  round: number
  hidden: boolean
  src: string
  detail?: string
}

function safeAudioSrc(src: string): string {
  if (!src) return ''
  const i = src.lastIndexOf('/audio/')
  return i >= 0 ? src.slice(i + 7) : src
}

function readLoopDebugLogs(): LoopDebugEntry[] {
  try {
    const raw = localStorage.getItem(LOOP_DEBUG_KEY)
    if (!raw) return []
    const arr = JSON.parse(raw)
    return Array.isArray(arr) ? arr as LoopDebugEntry[] : []
  } catch {
    return []
  }
}

function appendLoopDebug(event: string, detail?: string) {
  const entry: LoopDebugEntry = {
    ts: new Date().toISOString(),
    event,
    index: loopIndex.value + 1,
    round: loopRound.value,
    hidden: typeof document !== 'undefined' ? document.hidden : false,
    src: safeAudioSrc(audioEl.src),
    detail,
  }
  const logs = readLoopDebugLogs()
  logs.push(entry)
  while (logs.length > LOOP_DEBUG_MAX) logs.shift()
  try {
    localStorage.setItem(LOOP_DEBUG_KEY, JSON.stringify(logs))
  } catch {
    // Ignore quota/serialization failures
  }
}

function clearLoopDebugLogs() {
  localStorage.removeItem(LOOP_DEBUG_KEY)
}

function exportLoopDebugLogs(): string {
  const logs = readLoopDebugLogs()
  if (!logs.length) return 'no loop logs'
  return logs.map((l) =>
    `${l.ts} | ${l.event} | idx=${l.index} | round=${l.round} | hidden=${l.hidden ? 1 : 0} | src=${l.src}${l.detail ? ` | ${l.detail}` : ''}`,
  ).join('\n')
}

function playGapInBackground(delayMs: number, session: number, action: () => void) {
  if (!loopPlaying.value || loopPaused.value) return
  if (delayMs <= 0) {
    if (session === loopPlaySession) action()
    return
  }
  if (!gapAudio) gapAudio = new Audio()
  gapAudio.onended = () => {
    if (session !== loopPlaySession) return
    if (!loopPlaying.value || loopPaused.value) return
    action()
  }
  gapAudio.src = getGapWavUri(delayMs)
  gapAudio.play().catch(() => {
    appendLoopDebug('gap_play_failed', `delayMs=${delayMs}`)
    if (session !== loopPlaySession) return
    if (!loopPlaying.value || loopPaused.value) return
    action()
  })
}

function runNextStep(session: number, action: () => void, delayMs: number) {
  if (!loopPlaying.value || loopPaused.value) return
  // Always schedule gaps via short silent audio — not setTimeout.
  // Timers are heavily throttled when the screen locks; list play feels OK when
  // lock happens mid-utterance, but 单曲循环 often hits the 500/800ms gaps while
  // locked and only continues after unlock.
  if (delayMs <= 0) {
    if (session === loopPlaySession) action()
    return
  }
  appendLoopDebug('run_next_gap', `delayMs=${delayMs}`)
  playGapInBackground(delayMs, session, action)
}

function playCurrentAudio(src: string, session: number, onFail: () => void) {
  if (session !== loopPlaySession) return
  appendLoopDebug('play_audio', safeAudioSrc(src))
  playMainTrack(src, () => {
    appendLoopDebug('play_audio_failed', safeAudioSrc(src))
    if (session !== loopPlaySession) return
    if (!loopPlaying.value || loopPaused.value) return
    onFail()
  })
}

// 主轨 play/pause 事件会与锁屏不同步：句间切轨会短暂 pause，不能把锁屏打成「已暂停」
audioEl.addEventListener('play', () => {
  if (loopPlaying.value && !loopPaused.value && 'mediaSession' in navigator) {
    navigator.mediaSession.playbackState = 'playing'
  }
})
audioEl.addEventListener('pause', () => {
  if (loopPlaying.value && loopPaused.value && 'mediaSession' in navigator) {
    navigator.mediaSession.playbackState = 'paused'
  }
})
audioEl.addEventListener('ended', () => appendLoopDebug('audio_ended'))
audioEl.addEventListener('error', () => {
  const mediaError = audioEl.error
  appendLoopDebug('audio_error', mediaError ? `code=${mediaError.code}` : 'unknown')
})

function clearLoopTimers() {
  _loopTimers.forEach(t => clearTimeout(t))
  _loopTimers = []
}

function clearPendingGap() {
  if (!gapAudio) return
  gapAudio.onended = null
  gapAudio.pause()
  gapAudio.src = ''
  gapAudio = null
}

/** 取消待执行的 setTimeout 与进行中的间隙音（暂停 / 切歌 / 停止） */
function clearLoopScheduling() {
  clearLoopTimers()
  clearPendingGap()
}

function startSilentKeepAlive() {
  if (silentAudio) return
  silentAudio = new Audio(SILENT_KEEPALIVE_WAV)
  silentAudio.loop = true
  silentAudio.volume = 0.01
  silentAudio.play().catch(() => {
    appendLoopDebug('keepalive_failed')
  })
}

function stopSilentKeepAlive() {
  if (!silentAudio) return
  silentAudio.pause()
  silentAudio.src = ''
  silentAudio = null
}

/** 与主音频一起暂停，否则 iOS 仍认为有媒体在播，锁屏按钮状态会错位 */
function pauseSilentKeepAlive() {
  if (silentAudio) silentAudio.pause()
}

function resumeSilentKeepAlive() {
  if (!silentAudio) return
  silentAudio.play().catch(() => {
    appendLoopDebug('keepalive_resume_failed')
  })
}

function flushMediaSessionPaused() {
  if (!('mediaSession' in navigator)) return
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      if (loopPlaying.value && loopPaused.value) {
        navigator.mediaSession.playbackState = 'paused'
      }
    })
  })
}

function flushMediaSessionPlaying() {
  if (!('mediaSession' in navigator)) return
  requestAnimationFrame(() => {
    if (loopPlaying.value && !loopPaused.value) {
      navigator.mediaSession.playbackState = 'playing'
    }
  })
}

function registerMediaSessionActionsOnce() {
  if (!('mediaSession' in navigator) || mediaSessionActionsRegistered) return
  mediaSessionActionsRegistered = true
  // iOS 锁屏/控制中心常会直接 pause 主轨而不触发本回调，导致 loopPaused 仍为 false；
  // 此时用户点「播放」必须恢复主轨，不能只依赖 togglePlay（其仅在 loopPaused 时继续）。
  navigator.mediaSession.setActionHandler('play', () => {
    if (!loopPlaying.value) return
    if (loopPaused.value) {
      togglePlay()
      return
    }
    // 句间间隙主轨常为 ended+paused，此时应由 gap 音推进，勿对主轨 play（避免误重播）
    if (audioEl.paused && !audioEl.ended) {
      appendLoopDebug('media_session_play_desync')
      resumeSilentKeepAlive()
      void audioEl.play().catch(() => {
        void audioEl.play().catch(() => {
          appendLoopDebug('media_session_play_desync_failed')
        })
      })
      flushMediaSessionPlaying()
    }
  })
  navigator.mediaSession.setActionHandler('pause', () => {
    if (!loopPaused.value) togglePlay()
  })
  navigator.mediaSession.setActionHandler('nexttrack', () => nextTrack())
  navigator.mediaSession.setActionHandler('previoustrack', () => prevTrack())
}

/** 仅更新当前曲目标题与进度；勿在每条重复 registerActionHandler，避免锁屏「一直刷」 */
function updateMediaSessionMetadata() {
  if (!('mediaSession' in navigator)) return
  const it = loopPlaylist.value[loopIndex.value]
  if (!it) return
  navigator.mediaSession.metadata = new MediaMetadata({
    title: it.word + ' - ' + it.meaning,
    artist:
      t('loopRound') +
      loopRound.value +
      t('loopRoundSuffix') +
      ' · ' +
      (loopIndex.value + 1) +
      '/' +
      loopPlaylist.value.length,
    album: t('title'),
    artwork: [{ src: 'cover.jpg', sizes: '1024x1024', type: 'image/jpeg' }],
  })
  navigator.mediaSession.playbackState = loopPaused.value ? 'paused' : 'playing'
}

function setupMediaSession() {
  registerMediaSessionActionsOnce()
  updateMediaSessionMetadata()
}

function playLoopItem() {
  if (!loopPlaying.value) return
  const session = ++loopPlaySession
  const it = loopPlaylist.value[loopIndex.value]
  if (!it) return
  appendLoopDebug('play_item', `${it.word}`)

  audioEl.onended = null

  setupMediaSession()

  const fn1 = it._audioFn ?? it.audio
  if (!fn1) {
    appendLoopDebug('missing_audio', it.word)
    nextLoopItemInternal()
    return
  }

  /** 仅播一条音频（词条/句子），句间一段静音；文章略短、听列表略长（锁屏仍走静音轨） */
  const gapMs = it._cat === 'articles' ? 0 : 500

  // 「听过」仅在主音频完整播完时 +1；部分环境会重复触发 ended，只计一次
  let wordListenCounted = false
  audioEl.onended = () => {
    if (session !== loopPlaySession) return
    if (!wordListenCounted) {
      wordListenCounted = true
      recordItemListened(it._cat, it.id)
    }
    recordListenTime(audioEl.duration)
    if (!loopPlaying.value || loopPaused.value) return
    runNextStep(session, () => nextLoopItemInternal(), gapMs)
  }
  playCurrentAudio(`https://pub-b85a5fcff7574f24b2a311a6506ec730.r2.dev/` + fn1, session, () => nextLoopItemInternal())
}

function nextLoopItemInternal() {
  if (!loopPlaying.value) return
  if (loopPauseAutoAdvance.value) {
    // 跟读模式：播完不跳，暂停等用户操作
    loopPaused.value = true
    return
  }
  if (!loopRepeat.value) {
    loopIndex.value++
    if (loopIndex.value >= loopPlaylist.value.length) {
      loopIndex.value = 0
      loopRound.value++
    }
  }
  playLoopItem()
}

function startLoop(items: (DataItem & { _cat: string })[]) {
  if (!items.length) return
  appendLoopDebug('start_loop', `count=${items.length}`)
  startSilentKeepAlive()
  loopPlaylist.value = items
  loopIndex.value = 0
  loopRound.value = 1
  loopPlaying.value = true
  loopPaused.value = false
  listSpeaking.value = false
  setupMediaSession()
  playLoopItem()
}

function startListPlayback(items: (DataItem & { _cat: string })[], from: number, to: number) {
  const slice = items.slice(from - 1, to)
  if (!slice.length) return
  appendLoopDebug('start_list_playback', `from=${from},to=${to},count=${slice.length}`)
  startSilentKeepAlive()
  loopPlaylist.value = slice
  loopIndex.value = 0
  loopRound.value = 1
  loopPlaying.value = true
  loopPaused.value = false
  listSpeaking.value = true
  setupMediaSession()
  playLoopItem()
}

function togglePlay() {
  if (loopPaused.value) {
    appendLoopDebug('resume')
    loopPaused.value = false
    resumeSilentKeepAlive()
    if ('mediaSession' in navigator) navigator.mediaSession.playbackState = 'playing'
    // Resume mid-playback audio, not restart
    if (audioEl.src && audioEl.paused && audioEl.currentTime > 0) {
      audioEl
        .play()
        .then(() => {
          flushMediaSessionPlaying()
        })
        .catch(() => {})
    } else {
      playLoopItem()
      flushMediaSessionPlaying()
    }
  } else {
    appendLoopDebug('pause')
    loopPaused.value = true
    clearLoopScheduling()
    pauseSilentKeepAlive()
    audioEl.pause()
    if ('mediaSession' in navigator) navigator.mediaSession.playbackState = 'paused'
    flushMediaSessionPaused()
  }
}

function stop() {
  appendLoopDebug('stop')
  loopPlaying.value = false
  loopPaused.value = false
  loopRepeat.value = false
  listSpeaking.value = false
  clearLoopScheduling()
  audioEl.onended = null
  audioEl.pause()
  if ('mediaSession' in navigator) navigator.mediaSession.playbackState = 'none'
  stopSilentKeepAlive()
}

function toggleRepeat() {
  loopRepeat.value = !loopRepeat.value
}

function nextTrack() {
  clearLoopScheduling()
  loopIndex.value = (loopIndex.value + 1) % loopPlaylist.value.length
  playLoopItem()
}

function prevTrack() {
  clearLoopScheduling()
  loopIndex.value = (loopIndex.value - 1 + loopPlaylist.value.length) % loopPlaylist.value.length
  playLoopItem()
}

export function useLoopPlayer() {
  return {
    loopPlaylist,
    loopIndex,
    loopRound,
    loopPlaying,
    loopPaused,
    loopRepeat,
    loopPauseAutoAdvance,
    listSpeaking,
    clearLoopTimers,
    startLoop,
    startListPlayback,
    togglePlay,
    stop,
    toggleRepeat,
    nextTrack,
    prevTrack,
    clearLoopDebugLogs,
    exportLoopDebugLogs,
  }
}
