import { ref, computed, onUnmounted } from 'vue'
import { pushSttDebug } from '@/utils/sttDebug'

type SpeechRec = SpeechRecognition
type SpeechRecCtor = new () => SpeechRec

function getSpeechRecognitionCtor(): SpeechRecCtor | null {
  if (typeof window === 'undefined') return null
  return window.SpeechRecognition || window.webkitSpeechRecognition || null
}

const IS_ANDROID = typeof navigator !== 'undefined' && /Android/i.test(navigator.userAgent)

/**
 * 全局单例 SR 实例：iOS Safari 对多次 new SpeechRecognition 释放不彻底，第二次
 * start() 常被静默拒绝（连麦克风指示器都不亮）。改为全页面共用一个实例，
 * 每次会话只换 handler，不重建对象。
 */
let sharedRec: SpeechRec | null = null
let sharedRecRunning = false
/** 在 onstart 之前就被要求停止 → 等 onstart 触发后立刻 stop */
let sharedRecPendingStop = false
let sharedRecHandlers: {
  onresult?: (e: SpeechRecognitionEvent) => void
  onerror?: (e: SpeechRecognitionErrorEvent) => void
  onend?: () => void
} = {}

function ensureSharedRec(Ctor: SpeechRecCtor): SpeechRec {
  if (sharedRec) return sharedRec
  const r = new Ctor()
  r.lang = 'ja-JP'
  r.continuous = !IS_ANDROID
  r.interimResults = true
  r.onresult = (e) => sharedRecHandlers.onresult?.(e)
  r.onerror = (e) => sharedRecHandlers.onerror?.(e)
  r.onend = () => {
    sharedRecRunning = false
    sharedRecPendingStop = false
    sharedRecHandlers.onend?.()
  }
  r.addEventListener('start', () => {
    sharedRecRunning = true
    // 用户在 start 真正触发之前就松手了 —— 立刻停
    if (sharedRecPendingStop) {
      sharedRecPendingStop = false
      try { r.stop() } catch { /* ignore */ }
    }
  })
  sharedRec = r
  return r
}

export function useJaSpeechRecognition() {
  const listening = ref(false)
  const interimText = ref('')
  const lastFinalText = ref('')
  const lastError = ref<string | null>(null)
  const alternatives = ref<string[]>([])

  let token = 0
  let alive = true
  let setUserStopped: () => void = () => {}
  let silenceTimer: ReturnType<typeof setTimeout> | null = null
  const SILENCE_TIMEOUT = 15_000

  const supported = computed(() => getSpeechRecognitionCtor() !== null)

  function resetSessionText() {
    interimText.value = ''
    lastFinalText.value = ''
    lastError.value = null
    alternatives.value = []
  }

  function clearSilenceTimer() {
    if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null }
  }

  function resetSilenceTimer() {
    clearSilenceTimer()
    silenceTimer = setTimeout(() => { stopListening() }, SILENCE_TIMEOUT)
  }

  /**
   * 启动识别。若上一会话仍在收尾，等它结束再启，避免 iOS 静默失败。
   */
  function start(onDone?: (fullText: string) => void) {
    const Ctor = getSpeechRecognitionCtor()
    pushSttDebug('start', `android=${IS_ANDROID} supported=${!!Ctor} running=${sharedRecRunning} secure=${typeof window !== 'undefined' && window.isSecureContext} ua=${typeof navigator !== 'undefined' ? navigator.userAgent.slice(0, 80) : ''}`)
    if (!Ctor) {
      pushSttDebug('error', 'no SpeechRecognition ctor')
      onDone?.('')
      return
    }

    const myToken = ++token
    const rec = ensureSharedRec(Ctor)
    sharedRecPendingStop = false
    resetSessionText()

    let userStopped = false
    let settled = false

    const settle = () => {
      if (settled) return
      settled = true
      if (myToken !== token) return
      listening.value = false
      if (!alive) return
      const full = `${lastFinalText.value}${interimText.value}`.trim()
      onDone?.(full)
    }

    let lastLoggedFinal = ''
    let lastLoggedInterim = ''

    sharedRecHandlers = {
      onresult: (event) => {
        if (myToken !== token) return
        resetSilenceTimer()
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
        if (sawFinal && finals !== lastLoggedFinal) {
          pushSttDebug('final', JSON.stringify(finals))
          lastLoggedFinal = finals
        } else if (!sawFinal && interim && interim !== lastLoggedInterim) {
          pushSttDebug('interim', JSON.stringify(interim))
          lastLoggedInterim = interim
        }
      },
      onerror: (event) => {
        lastError.value = event.error || 'error'
        pushSttDebug('error', `${event.error}${event.message ? ' / ' + event.message : ''}`)
        userStopped = true
        settle()
      },
      onend: () => {
        if (myToken !== token) return
        pushSttDebug('end', `userStopped=${userStopped} final="${lastFinalText.value}" interim="${interimText.value}"`)
        settle()
      },
    }

    const tryStart = () => {
      try {
        rec.start()
        resetSilenceTimer()
        listening.value = true
      } catch (e) {
        const msg = (e as Error)?.message || String(e)
        pushSttDebug('error', `start threw: ${msg}`)
        // Safari 已在运行中再 start 会抛 "already started" —— 当成上一会话尚未完全收尾，稍等再试
        if (/already|InvalidState/i.test(msg)) {
          try { rec.abort() } catch { /* ignore */ }
          setTimeout(() => {
            if (myToken !== token) return
            try {
              rec.start()
              resetSilenceTimer()
              listening.value = true
              pushSttDebug('start', 'retry ok')
            } catch (e2) {
              pushSttDebug('error', `retry failed: ${(e2 as Error)?.message || e2}`)
              lastError.value = 'start_failed'
              listening.value = false
              if (alive) onDone?.('')
            }
          }, 150)
          return
        }
        lastError.value = 'start_failed'
        listening.value = false
        if (alive) onDone?.('')
      }
    }

    // 若上次的 SR 还在 running（来不及收尾），先 abort 再稍等启动
    if (sharedRecRunning) {
      pushSttDebug('start', 'waiting for previous session to end')
      try { rec.abort() } catch { /* ignore */ }
      setTimeout(tryStart, 120)
    } else {
      tryStart()
    }

    setUserStopped = () => { userStopped = true }
  }

  function stopListening() {
    setUserStopped()
    if (!sharedRec) return
    if (!sharedRecRunning) {
      // onstart 还没触发，先挂个 pending 信号，等 onstart 自动收尾
      sharedRecPendingStop = true
      pushSttDebug('stop', 'pending (start not fired yet)')
      return
    }
    try {
      sharedRec.stop()
    } catch {
      /* ignore */
    }
  }

  function abortListening() {
    if (!sharedRec) return
    try { sharedRec.abort() } catch { /* ignore */ }
  }

  onUnmounted(() => {
    alive = false
    token++
    clearSilenceTimer()
    // 不销毁 sharedRec，留给其他消费者用
    if (sharedRecRunning) {
      try { sharedRec?.abort() } catch { /* ignore */ }
    }
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
    resetSessionText,
  }
}
