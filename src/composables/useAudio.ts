import { ref } from 'vue'
import { recordListenTime } from './useStats'
import { SILENT_KEEPALIVE_WAV, getGapWavUri } from '@/utils/silentWavGap'

// Single persistent Audio element — essential on iOS to avoid exhausting audio channels
const audioEl = new Audio()
audioEl.setAttribute('playsinline', '')

function audioPath(fn: string): string {
  return `https://pub-b85a5fcff7574f24b2a311a6506ec730.r2.dev/${fn}`
}

export { audioEl, audioPath }

/**
 * 主轨播放：测页用过麦克风后，部分移动浏览器需 load + 重试 play 才能恢复。
 * onBothFailed：两次 play 均失败时回调（如列表循环里跳过当前条）。
 */
export function playMainTrack(src: string, onBothFailed?: () => void): void {
  audioEl.pause()
  audioEl.src = src
  try {
    audioEl.load()
  } catch {
    /* ignore */
  }
  const fail = onBothFailed ?? (() => {})
  void audioEl.play().catch(() => {
    void audioEl.play().catch(() => fail())
  })
}

export function speakTTS(text: string) {
  speechSynthesis.cancel()
  const u = new SpeechSynthesisUtterance(text)
  u.lang = 'ja-JP'
  u.rate = 0.8
  speechSynthesis.speak(u)
}

export function speak(word: string, audio?: string) {
  if (!audio) { speakTTS(word); return }
  audioEl.onended = null
  playMainTrack(audioPath(audio))
}

/**
 * 单次直接播放：用独立 Audio，不共享 audioEl，不触发 MediaSession／灵动岛。
 * 练习卡片点击这种短促播放走这条路径即可。
 */
let simpleAudio: HTMLAudioElement | null = null
function playSimple(src: string, onDuration?: (d: number) => void) {
  if (simpleAudio) { simpleAudio.pause(); simpleAudio.src = '' }
  const a = new Audio(src)
  a.setAttribute('playsinline', '')
  // @ts-expect-error - 非标准属性，部分 WebKit 支持，用来劝退 Now Playing 出现
  a.disableRemotePlayback = true
  a.preload = 'auto'
  simpleAudio = a
  a.onended = () => { if (onDuration) onDuration(a.duration) }
  void a.play().catch(() => {})
}

/** 仅播词条主音频 */
export function speakWithExample(word: string, audio?: string) {
  if (!audio) { speakTTS(word); return }
  playSimple(audioPath(audio), (d) => recordListenTime(d))
}

/** 播放例句音频（单次） */
export function playExampleAudio(audioFile: string) {
  audioEl.onended = () => {
    recordListenTime(audioEl.duration)
    audioEl.onended = null
  }
  playMainTrack(audioPath(audioFile))
}

export const looping = ref(false)
export const loopingWord = ref('')

/** 与列表循环相同：锁屏时节流 setTimeout，用静音间隙 + 保活 */
let practiceLoopSession = 0
let practiceGapAudio: HTMLAudioElement | null = null
let practiceSilentAudio: HTMLAudioElement | null = null

function clearPracticeGap() {
  if (!practiceGapAudio) return
  practiceGapAudio.onended = null
  practiceGapAudio.pause()
  practiceGapAudio.src = ''
  practiceGapAudio = null
}

function startPracticeKeepAlive() {
  if (practiceSilentAudio) return
  practiceSilentAudio = new Audio(SILENT_KEEPALIVE_WAV)
  practiceSilentAudio.loop = true
  practiceSilentAudio.volume = 0.01
  practiceSilentAudio.play().catch(() => {})
}

function stopPracticeKeepAlive() {
  if (!practiceSilentAudio) return
  practiceSilentAudio.pause()
  practiceSilentAudio.src = ''
  practiceSilentAudio = null
}

function schedulePracticeGap(delayMs: number, session: number, action: () => void) {
  if (session !== practiceLoopSession) return
  if (!looping.value) return
  if (delayMs <= 0) {
    action()
    return
  }
  if (!practiceGapAudio) practiceGapAudio = new Audio()
  practiceGapAudio.onended = () => {
    if (session !== practiceLoopSession) return
    if (!looping.value) return
    action()
  }
  practiceGapAudio.src = getGapWavUri(delayMs)
  practiceGapAudio.play().catch(() => {
    if (session !== practiceLoopSession) return
    if (!looping.value) return
    action()
  })
}

export function speakLoop(word: string, audio?: string) {
  clearPracticeGap()
  practiceLoopSession++
  const session = practiceLoopSession
  looping.value = true
  loopingWord.value = word
  startPracticeKeepAlive()
  function playOnce() {
    if (session !== practiceLoopSession) return
    if (!looping.value) return
    if (!audio) {
      looping.value = false
      stopPracticeKeepAlive()
      return
    }
    audioEl.onended = () => {
      recordListenTime(audioEl.duration)
      if (session !== practiceLoopSession) return
      if (!looping.value) return
      schedulePracticeGap(800, session, playOnce)
    }
    playMainTrack(audioPath(audio))
  }
  playOnce()
}

export function stopLoop() {
  practiceLoopSession++
  looping.value = false
  loopingWord.value = ''
  clearPracticeGap()
  audioEl.onended = null
  audioEl.pause()
  stopPracticeKeepAlive()
  try {
    audioEl.currentTime = 0
  } catch {
    /* ignore */
  }
}


export function pause() {
  audioEl.pause()
}

export function resume() {
  audioEl.play().catch(() => {})
}

export function useAudio() {
  return {
    audioEl,
    speak,
    speakWithExample,
    speakLoop,
    stopLoop,
    looping,
    pause,
    resume,
  }
}
