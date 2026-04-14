import { ref, computed, onUnmounted } from 'vue'
import { pushSttDebug } from '@/utils/sttDebug'

type SpeechRec = SpeechRecognition
type SpeechRecCtor = new () => SpeechRec

function getSpeechRecognitionCtor(): SpeechRecCtor | null {
  if (typeof window === 'undefined') return null
  return window.SpeechRecognition || window.webkitSpeechRecognition || null
}

/** Android Chrome 不支持 continuous: 设了反而拿不到任何结果，需要单次模式 + 自动 restart */
const IS_ANDROID = typeof navigator !== 'undefined' && /Android/i.test(navigator.userAgent)

/**
 * 日语口述识别（Web Speech API），仅用于「测」等需要 ja-JP 的场景。
 */
export function useJaSpeechRecognition() {
  const listening = ref(false)
  const interimText = ref('')
  const lastFinalText = ref('')
  const lastError = ref<string | null>(null)
  /** 所有候选识别结果（含同音异字），用于模糊匹配 */
  const alternatives = ref<string[]>([])

  let recInst: SpeechRec | null = null
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

  /** 用户主动取消当前聆听（会触发结束回调，可与正常结束同样处理） */
  function abortListening() {
    if (!recInst) return
    try {
      recInst.abort()
    } catch {
      /* ignore */
    }
  }

  function clearSilenceTimer() {
    if (silenceTimer) { clearTimeout(silenceTimer); silenceTimer = null }
  }

  function resetSilenceTimer() {
    clearSilenceTimer()
    silenceTimer = setTimeout(() => { stopListening() }, SILENCE_TIMEOUT)
  }

  function destroyRecognition() {
    clearSilenceTimer()
    if (recInst) {
      try {
        recInst.abort()
      } catch {
        /* ignore */
      }
    }
    recInst = null
    listening.value = false
  }

  /**
   * 开始一次识别（continuous=true，停顿不会结束会话；须调用 stopListening 才结束）。
   * 结束后调用 onDone(合并后的识别文本)。
   */
  function start(onDone?: (fullText: string) => void) {
    const Ctor = getSpeechRecognitionCtor()
    pushSttDebug('start', `android=${IS_ANDROID} supported=${!!Ctor} secure=${typeof window !== 'undefined' && window.isSecureContext} ua=${typeof navigator !== 'undefined' ? navigator.userAgent.slice(0, 80) : ''}`)
    if (!Ctor) {
      pushSttDebug('error', 'no SpeechRecognition ctor')
      onDone?.('')
      return
    }

    // 显式申请麦克风：Android Chrome 没权限时 SpeechRecognition.start() 会立即 aborted 而非抛错
    if (typeof navigator !== 'undefined' && navigator.mediaDevices?.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          pushSttDebug('mic', 'permission granted')
          // 立刻关掉，识别引擎自己会再开
          stream.getTracks().forEach((t) => t.stop())
        })
        .catch((e) => {
          pushSttDebug('mic', `permission denied: ${(e as Error)?.name || e}`)
        })
    }

    const myToken = ++token
    destroyRecognition()
    resetSessionText()

    let userStopped = false
    let settled = false

    const settle = () => {
      if (settled) return
      settled = true
      if (myToken !== token) return
      listening.value = false
      recInst = null
      if (!alive) return
      // 拼接 interim 是为了 Android 单次模式下 onend 时尚未升格为 final 的尾段
      const full = `${lastFinalText.value}${interimText.value}`.trim()
      onDone?.(full)
    }

    const bind = (r: SpeechRec) => {
      let lastLoggedFinal = ''
      let lastLoggedInterim = ''
      let hadFinalThisSession = false
      r.onresult = (event: SpeechRecognitionEvent) => {
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

        // 节流日志：只在 final 出现或 interim 文本真正变了时写一条
        if (sawFinal && finals !== lastLoggedFinal) {
          pushSttDebug('final', JSON.stringify(finals))
          lastLoggedFinal = finals
          hadFinalThisSession = true
        } else if (!sawFinal && interim && interim !== lastLoggedInterim) {
          pushSttDebug('interim', JSON.stringify(interim))
          lastLoggedInterim = interim
        }
        // suppress unused-var lint
        void hadFinalThisSession
      }

      r.onerror = (event: SpeechRecognitionErrorEvent) => {
        lastError.value = event.error || 'error'
        pushSttDebug('error', `${event.error}${event.message ? ' / ' + event.message : ''}`)
        userStopped = true
        settle()
      }

      r.onend = () => {
        if (myToken !== token) return
        pushSttDebug('end', `userStopped=${userStopped} final="${lastFinalText.value}" interim="${interimText.value}"`)
        settle()
      }
    }

    const buildRec = (): SpeechRec => {
      const r = new Ctor()
      r.lang = 'ja-JP'
      // Android Chrome 设 continuous=true 会导致 onresult 永不触发，必须用单次模式
      r.continuous = !IS_ANDROID
      r.interimResults = true
      return r
    }

    const rec = buildRec()
    bind(rec)

    try {
      recInst = rec
      rec.start()
      resetSilenceTimer()
      listening.value = true
    } catch (e) {
      lastError.value = 'start_failed'
      pushSttDebug('error', `start threw: ${(e as Error)?.message || e}`)
      listening.value = false
      recInst = null
      if (alive) onDone?.('')
    }

    // 暴露给 stopListening 用的“用户主动停”信号
    setUserStopped = () => { userStopped = true }
  }

  onUnmounted(() => {
    alive = false
    token++
    destroyRecognition()
  })

  /** 正常结束录音（等待最终结果后触发 onDone） */
  function stopListening() {
    setUserStopped()
    if (!recInst) return
    try {
      recInst.stop()
    } catch {
      /* ignore */
    }
  }

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
