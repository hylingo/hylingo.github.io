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
  /** 用户是否还按着录音键。true = onend 时自动重启续录；false = 结束并回调 */
  let userHolding = false

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
    userHolding = false
    listening.value = false
    const text = (finalText.value + interimText.value).trim()
    const cb = currentOnDone
    currentOnDone = null
    // 结束时额外再 abort 一次，确保底层实例被彻底回收
    hardAbort()
    cb?.(text)
  }

  /** 创建并启动一个识别实例；finals/interim 的累积由闭包 ref 持有，重启不会丢 */
  function spawnRec(myToken: number) {
    const Ctor = getCtor()
    if (!Ctor) return
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
      // no-speech / aborted 等错误：若用户还按着，也要续录
      if (userHolding && e.error !== 'not-allowed' && e.error !== 'service-not-allowed') return
      finish()
    }
    r.onend = () => {
      if (myToken !== token) return
      pushSttDebug('end', `final="${finalText.value}" holding=${userHolding}`)
      cleanup()
      if (userHolding) {
        // 用户还按着录音键，自动续录（finalText 已保留）
        try { spawnRec(myToken) } catch (err) {
          pushSttDebug('respawn-throw', String((err as Error)?.message || err))
          finish()
        }
        return
      }
      finish()
    }

    try {
      r.start()
    } catch (err) {
      pushSttDebug('start-throw', String((err as Error)?.message || err))
      finish()
    }
  }

  async function start(onDone: (text: string) => void) {
    const Ctor = getCtor()
    if (!Ctor) { onDone(''); return }

    // 若上一个会话还在，先强制杀掉
    if (rec) hardAbort()

    // 提前占 token：async 流程中若被 abort()，token 会再 ++，下面流程全部跳过
    token++
    const myToken = token
    settled = false
    currentOnDone = onDone
    interimText.value = ''
    finalText.value = ''
    alternatives.value = []
    listening.value = true
    userHolding = true

    // 冷却：距离上次结束不足 COOLDOWN_MS 就等等
    const wait = COOLDOWN_MS - (Date.now() - lastEndAt)
    if (wait > 0) {
      pushSttDebug('cooldown', `${wait}ms`)
      await new Promise((r) => setTimeout(r, wait))
    }
    if (myToken !== token) return

    // 唤醒音频会话（iOS Chrome 关键）
    await wakeAudio()
    if (myToken !== token) return

    spawnRec(myToken)
  }

  function stop() {
    userHolding = false
    if (!rec) return
    try { rec.stop() } catch { /* ignore */ }
  }

  function abort() {
    userHolding = false
    token++ // 作废任何进行中的 async start
    if (rec) {
      try { rec.abort() } catch { /* ignore */ }
    }
    finish()
  }

  onUnmounted(() => {
    userHolding = false
    token++
    hardAbort()
  })

  return { supported, listening, interimText, finalText, alternatives, start, stop, abort }
}
