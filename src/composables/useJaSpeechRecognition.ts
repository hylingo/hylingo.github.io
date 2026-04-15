import { ref, computed, onUnmounted } from 'vue'
import { pushSttDebug } from '@/utils/sttDebug'

type SpeechRec = SpeechRecognition
type SpeechRecCtor = new () => SpeechRec

const IS_ANDROID = typeof navigator !== 'undefined' && /Android/i.test(navigator.userAgent)
const SILENCE_TIMEOUT = 15_000

function getCtor(): SpeechRecCtor | null {
  if (typeof window === 'undefined') return null
  return window.SpeechRecognition || window.webkitSpeechRecognition || null
}

/**
 * iOS Safari 对多次 new SpeechRecognition 释放不彻底，单例复用避免"第二次静默失败"。
 *
 * 状态机：
 *   idle → start() → starting → (onstart) → running → stop() → stopping → (onend) → idle
 *
 * - 在 starting 期间调用 stop() → 标记 wantStop，onstart 触发后立即 stop()
 * - 在 running 时调用 start() → 直接 abort，等 onend 触发再递归启动
 * - 多处 .start() / .stop() 抛 InvalidState 都 catch 掉，状态机兜底
 */
type RecState = 'idle' | 'starting' | 'running' | 'stopping'

interface Session {
  token: number
  onResult: (e: SpeechRecognitionEvent) => void
  onError: (e: SpeechRecognitionErrorEvent) => void
  onEnd: () => void
}

let rec: SpeechRec | null = null
let state: RecState = 'idle'
let wantStop = false
let currentSession: Session | null = null
let queuedSession: Session | null = null

function ensureRec(Ctor: SpeechRecCtor): SpeechRec {
  if (rec) return rec
  const r = new Ctor()
  r.lang = 'ja-JP'
  r.continuous = !IS_ANDROID
  r.interimResults = true
  r.addEventListener('start', () => {
    state = 'running'
    if (wantStop) {
      wantStop = false
      safeStop()
    }
  })
  r.onresult = (e) => currentSession?.onResult(e)
  r.onerror = (e) => currentSession?.onError(e)
  r.onend = () => {
    const ended = currentSession
    currentSession = null
    state = 'idle'
    wantStop = false
    ended?.onEnd()
    // 如果有被挤掉的会话在排队，现在启动它
    if (queuedSession) {
      const next = queuedSession
      queuedSession = null
      runStart(next)
    }
  }
  rec = r
  return r
}

function safeStart(): boolean {
  try { rec!.start(); return true } catch { return false }
}
function safeStop() {
  try { rec!.stop() } catch { /* ignore */ }
}
function safeAbort() {
  try { rec!.abort() } catch { /* ignore */ }
}

function runStart(s: Session) {
  currentSession = s
  state = 'starting'
  wantStop = false
  if (!safeStart()) {
    // 罕见：start 抛出（例如 Safari 老版本并发），回退 abort 后换队列重试
    safeAbort()
    state = 'idle'
    currentSession = null
    queuedSession = s
  }
}

export function useJaSpeechRecognition() {
  const listening = ref(false)
  const interimText = ref('')
  const lastFinalText = ref('')
  const lastError = ref<string | null>(null)
  const alternatives = ref<string[]>([])

  let sessionToken = 0
  let silenceTimer: ReturnType<typeof setTimeout> | null = null

  const supported = computed(() => getCtor() !== null)

  function resetSilence() {
    if (silenceTimer) clearTimeout(silenceTimer)
    silenceTimer = setTimeout(() => stopListening(), SILENCE_TIMEOUT)
  }
  function clearSilence() {
    if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null }
  }

  function start(onDone?: (fullText: string) => void) {
    const Ctor = getCtor()
    if (!Ctor) { onDone?.(''); return }

    const token = ++sessionToken
    ensureRec(Ctor)
    pushSttDebug('start', `state=${state} android=${IS_ANDROID}`)

    // 清空本次会话文本
    interimText.value = ''
    lastFinalText.value = ''
    lastError.value = null
    alternatives.value = []
    listening.value = true

    let userStopped = false
    let settled = false
    let loggedFinal = ''
    let loggedInterim = ''

    const finish = () => {
      if (settled) return
      settled = true
      if (token !== sessionToken) return
      listening.value = false
      clearSilence()
      const full = (lastFinalText.value + interimText.value).trim()
      onDone?.(full)
    }

    const session: Session = {
      token,
      onResult: (event) => {
        if (token !== sessionToken) return
        resetSilence()
        let interim = ''
        let finals = lastFinalText.value
        const alts: string[] = []
        let sawFinal = false
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i]
          const piece = result[0]?.transcript ?? ''
          if (result.isFinal) {
            finals += piece
            sawFinal = true
            for (let j = 0; j < result.length; j++) {
              const alt = result[j]?.transcript
              if (alt) alts.push(alt)
            }
          } else {
            interim += piece
          }
        }
        lastFinalText.value = finals
        interimText.value = interim
        if (alts.length) alternatives.value = alts
        if (sawFinal && finals !== loggedFinal) {
          pushSttDebug('final', JSON.stringify(finals))
          loggedFinal = finals
        } else if (!sawFinal && interim && interim !== loggedInterim) {
          pushSttDebug('interim', JSON.stringify(interim))
          loggedInterim = interim
        }
      },
      onError: (event) => {
        lastError.value = event.error || 'error'
        pushSttDebug('error', event.error + (event.message ? ` / ${event.message}` : ''))
        userStopped = true
        finish()
      },
      onEnd: () => {
        if (token !== sessionToken) return
        pushSttDebug('end', `userStopped=${userStopped} final="${lastFinalText.value}"`)
        finish()
      },
    }

    // 关键分派：空闲直接启，繁忙时挤掉旧会话
    if (state === 'idle') {
      runStart(session)
    } else {
      // running / starting / stopping → 终结当前，排队这次
      queuedSession = session
      if (state === 'running') safeAbort() // 触发 onend → 从队列启动
      // starting / stopping 状态自然会走到 onend，也会消化队列
    }

    resetSilence()
    // expose userStopped setter to stopListening closure
    stopListeningImpl = () => { userStopped = true; requestStop() }
  }

  let stopListeningImpl: () => void = () => {}

  function requestStop() {
    if (!rec) return
    if (state === 'running') {
      state = 'stopping'
      safeStop()
    } else if (state === 'starting') {
      // onstart 还没到：挂个信号，等它触发自动 stop
      wantStop = true
      pushSttDebug('stop', 'pending (starting)')
    }
    // idle / stopping：没动作
  }

  function stopListening() { stopListeningImpl() }

  function abortListening() {
    if (rec && state !== 'idle') safeAbort()
  }

  onUnmounted(() => {
    sessionToken++
    clearSilence()
    // 只关自己的 session，单例不销毁（别的组件可能还要用）
  })

  return {
    supported,
    listening,
    interimText,
    lastFinalText,
    lastError,
    alternatives,
    start,
    stopListening,
    abortListening,
  }
}
