import { ref, computed, onUnmounted } from 'vue'

type SpeechRec = SpeechRecognition
type SpeechRecCtor = new () => SpeechRec

function getSpeechRecognitionCtor(): SpeechRecCtor | null {
  if (typeof window === 'undefined') return null
  return window.SpeechRecognition || window.webkitSpeechRecognition || null
}

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
    if (!Ctor) {
      onDone?.('')
      return
    }

    const myToken = ++token
    destroyRecognition()
    resetSessionText()

    const rec = new Ctor()
    rec.lang = 'ja-JP'
    rec.continuous = true
    rec.interimResults = true

    rec.onresult = (event: SpeechRecognitionEvent) => {
      if (myToken !== token) return
      resetSilenceTimer()
      let interim = ''
      let finals = lastFinalText.value
      const alts: string[] = []
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i]
        const piece = result[0]?.transcript ?? ''
        if (result.isFinal) {
          finals += piece
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
    }

    let settled = false
    const settle = () => {
      if (settled) return
      settled = true
      if (myToken !== token) return
      listening.value = false
      recInst = null
      if (!alive) return
      const full = `${lastFinalText.value}${interimText.value}`.trim()
      onDone?.(full)
    }

    rec.onerror = (event: SpeechRecognitionErrorEvent) => {
      lastError.value = event.error || 'error'
      settle()
    }

    rec.onend = () => {
      settle()
    }

    try {
      recInst = rec
      rec.start()
      resetSilenceTimer()
      listening.value = true
    } catch {
      lastError.value = 'start_failed'
      listening.value = false
      recInst = null
      if (alive) onDone?.('')
    }
  }

  onUnmounted(() => {
    alive = false
    token++
    destroyRecognition()
  })

  /** 正常结束录音（等待最终结果后触发 onDone） */
  function stopListening() {
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
