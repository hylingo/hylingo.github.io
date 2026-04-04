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

  let recInst: SpeechRec | null = null
  let token = 0
  let alive = true

  const supported = computed(() => getSpeechRecognitionCtor() !== null)

  function resetSessionText() {
    interimText.value = ''
    lastFinalText.value = ''
    lastError.value = null
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

  function destroyRecognition() {
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
      let interim = ''
      let finals = lastFinalText.value
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const piece = event.results[i][0]?.transcript ?? ''
        if (event.results[i].isFinal) finals += piece
        else interim += piece
      }
      lastFinalText.value = finals
      interimText.value = interim
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
    start,
    stopListening,
    abortListening,
    resetSessionText,
  }
}
