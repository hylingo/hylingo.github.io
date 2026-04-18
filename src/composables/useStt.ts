/**
 * 极简 Web Speech API 包装：按下 new、松开 abort、无单例、无状态机、无队列。
 * 仅支持 Chrome（桌面 / Android / iOS Chrome）。
 */
import { ref, onUnmounted } from 'vue'
import { pushSttDebug } from '@/utils/sttDebug'

type SpeechRecCtor = new () => SpeechRecognition

function getCtor(): SpeechRecCtor | null {
  if (typeof window === 'undefined') return null
  return window.SpeechRecognition || window.webkitSpeechRecognition || null
}

const IS_ANDROID = typeof navigator !== 'undefined' && /Android/i.test(navigator.userAgent)

export function useStt() {
  const supported = ref(!!getCtor())
  const listening = ref(false)
  const interimText = ref('')
  const finalText = ref('')
  const alternatives = ref<string[]>([])

  let rec: SpeechRecognition | null = null
  let token = 0
  let currentOnDone: ((text: string) => void) | null = null
  let settled = false

  function cleanup() {
    if (!rec) return
    rec.onresult = null
    rec.onerror = null
    rec.onend = null
    rec = null
  }

  function finish() {
    if (settled) return
    settled = true
    listening.value = false
    const text = (finalText.value + interimText.value).trim()
    const cb = currentOnDone
    currentOnDone = null
    cleanup()
    cb?.(text)
  }

  function start(onDone: (text: string) => void) {
    const Ctor = getCtor()
    if (!Ctor) { onDone(''); return }

    // 若上一个会话还在，先强制清理（本地层面，底层由 new 覆盖）
    if (rec) {
      try { rec.abort() } catch { /* ignore */ }
      cleanup()
    }

    token++
    const myToken = token
    settled = false
    currentOnDone = onDone
    interimText.value = ''
    finalText.value = ''
    alternatives.value = []
    listening.value = true

    const r = new Ctor()
    r.lang = 'ja-JP'
    r.continuous = !IS_ANDROID
    r.interimResults = true
    rec = r

    r.addEventListener('start', () => pushSttDebug('start', ''))
    r.onresult = (e: SpeechRecognitionEvent) => {
      if (myToken !== token) return
      let interim = ''
      let finals = finalText.value
      const alts: string[] = []
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const result = e.results[i]
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
      finalText.value = finals
      interimText.value = interim
      if (alts.length) alternatives.value = alts
    }
    r.onerror = (e: SpeechRecognitionErrorEvent) => {
      if (myToken !== token) return
      pushSttDebug('error', e.error || '')
      finish()
    }
    r.onend = () => {
      if (myToken !== token) return
      pushSttDebug('end', `final="${finalText.value}"`)
      finish()
    }

    try {
      r.start()
    } catch (err) {
      pushSttDebug('start-throw', String((err as Error)?.message || err))
      finish()
    }
  }

  function stop() {
    if (!rec) return
    try { rec.stop() } catch { /* ignore */ }
  }

  function abort() {
    if (!rec) return
    try { rec.abort() } catch { /* ignore */ }
    finish()
  }

  onUnmounted(() => {
    token++
    if (rec) {
      try { rec.abort() } catch { /* ignore */ }
      cleanup()
    }
  })

  return { supported, listening, interimText, finalText, alternatives, start, stop, abort }
}
