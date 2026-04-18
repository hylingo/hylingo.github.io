/**
 * 极简 Web Speech API 包装 + iOS Chrome 音频会话唤醒。
 * 仅支持 Chrome（桌面 / Android / iOS Chrome）。
 *
 * iOS Chrome 会话泄漏缓解策略：
 *   1. 每次 start 前 getUserMedia 抓一下麦克风再立刻 release，强制刷新音频会话
 *   2. 结束后 abort + 200ms 冷却，让底层有时间释放
 *   3. 冷却期内再次 start 会等冷却结束
 */
import { ref, onUnmounted } from 'vue'
import { pushSttDebug } from '@/utils/sttDebug'

type SpeechRecCtor = new () => SpeechRecognition

function getCtor(): SpeechRecCtor | null {
  if (typeof window === 'undefined') return null
  return window.SpeechRecognition || window.webkitSpeechRecognition || null
}

const IS_ANDROID = typeof navigator !== 'undefined' && /Android/i.test(navigator.userAgent)
const COOLDOWN_MS = 200

/** 唤醒 iOS Chrome 音频会话：抓一下麦克风立即释放 */
async function wakeAudio() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    stream.getTracks().forEach((t) => t.stop())
    pushSttDebug('wake', 'ok')
  } catch (err) {
    pushSttDebug('wake-fail', String((err as Error)?.message || err))
  }
}

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
  let lastEndAt = 0

  function cleanup() {
    if (!rec) return
    rec.onresult = null
    rec.onerror = null
    rec.onend = null
    rec = null
  }

  function hardAbort() {
    if (!rec) return
    try { rec.abort() } catch { /* ignore */ }
    cleanup()
    lastEndAt = Date.now()
  }

  function finish() {
    if (settled) return
    settled = true
    listening.value = false
    const text = (finalText.value + interimText.value).trim()
    const cb = currentOnDone
    currentOnDone = null
    // 结束时额外再 abort 一次，确保底层实例被彻底回收
    hardAbort()
    cb?.(text)
  }

  async function start(onDone: (text: string) => void) {
    const Ctor = getCtor()
    if (!Ctor) { onDone(''); return }

    // 若上一个会话还在，先强制杀掉
    if (rec) hardAbort()

    // 冷却：距离上次结束不足 COOLDOWN_MS 就等等
    const wait = COOLDOWN_MS - (Date.now() - lastEndAt)
    if (wait > 0) {
      pushSttDebug('cooldown', `${wait}ms`)
      await new Promise((r) => setTimeout(r, wait))
    }

    // 唤醒音频会话（iOS Chrome 关键）
    await wakeAudio()

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
    if (rec) {
      try { rec.abort() } catch { /* ignore */ }
    }
    finish()
  }

  onUnmounted(() => {
    token++
    hardAbort()
  })

  return { supported, listening, interimText, finalText, alternatives, start, stop, abort }
}
