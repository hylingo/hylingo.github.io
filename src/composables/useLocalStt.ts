/**
 * 本地 whisper.cpp server 模式：MediaRecorder 按住录音，松手 POST 到本机 whisper 服务。
 * 仅在配置了 LOCAL_STT_URL 时启用，用于开发机自用——线上部署不依赖。
 *
 * 服务约定：POST multipart/form-data 到 {url}，字段名 `file`，返回 { text: string }
 * （whisper.cpp 的 examples/server 原生接口；如端点不同可在 URL 里直接带路径）
 */
import { ref, onUnmounted } from 'vue'
import { pushSttDebug } from '@/utils/sttDebug'

type DoneCb = (text: string) => void

export function useLocalStt(endpointUrl: string) {
  const supported = ref(typeof navigator !== 'undefined' && !!navigator.mediaDevices?.getUserMedia && typeof MediaRecorder !== 'undefined')
  const listening = ref(false)
  const interimText = ref('') // 本地模式无 interim，保留字段对齐接口
  const finalText = ref('')
  const alternatives = ref<string[]>([])

  let mediaStream: MediaStream | null = null
  let recorder: MediaRecorder | null = null
  let chunks: Blob[] = []
  let currentOnDone: DoneCb | null = null
  let settled = false
  let token = 0

  function releaseStream() {
    mediaStream?.getTracks().forEach((t) => t.stop())
    mediaStream = null
  }

  function finish(text: string) {
    if (settled) return
    settled = true
    listening.value = false
    const cb = currentOnDone
    currentOnDone = null
    finalText.value = text
    cb?.(text)
  }

  async function postAudio(blob: Blob): Promise<string> {
    const fd = new FormData()
    // whisper.cpp server 要求字段名 file；response_format=json 是默认
    fd.append('file', blob, 'audio.webm')
    fd.append('response_format', 'json')
    fd.append('language', 'ja')
    fd.append('temperature', '0')
    const res = await fetch(endpointUrl, { method: 'POST', body: fd })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json().catch(() => ({} as Record<string, unknown>))
    // whisper.cpp: { text: "..." }；OpenAI 兼容: { text: "..." }
    const text = typeof (data as { text?: unknown }).text === 'string' ? (data as { text: string }).text : ''
    return text.trim()
  }

  async function start(onDone: DoneCb) {
    if (!supported.value) { onDone(''); return }
    // 上一个会话还在就先杀掉
    if (recorder || mediaStream) abort()

    token++
    const myToken = token
    settled = false
    currentOnDone = onDone
    interimText.value = ''
    finalText.value = ''
    alternatives.value = []
    listening.value = true
    chunks = []

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    } catch (err) {
      pushSttDebug('local-mic-fail', String((err as Error)?.message || err))
      finish('')
      return
    }
    if (myToken !== token) { releaseStream(); return }

    try {
      recorder = new MediaRecorder(mediaStream)
    } catch (err) {
      pushSttDebug('local-rec-fail', String((err as Error)?.message || err))
      releaseStream()
      finish('')
      return
    }

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) chunks.push(e.data)
    }
    recorder.onstop = async () => {
      releaseStream()
      if (myToken !== token) return
      const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' })
      chunks = []
      if (blob.size < 500) {
        pushSttDebug('local-too-short', `${blob.size}B`)
        finish('')
        return
      }
      pushSttDebug('local-post', `${blob.size}B → ${endpointUrl}`)
      try {
        const text = await postAudio(blob)
        if (myToken !== token) return
        pushSttDebug('local-done', `"${text}"`)
        finish(text)
      } catch (err) {
        pushSttDebug('local-http-fail', String((err as Error)?.message || err))
        finish('')
      }
    }
    recorder.onerror = (e) => {
      pushSttDebug('local-rec-err', String((e as Event & { error?: Error }).error?.message || 'unknown'))
      releaseStream()
      finish('')
    }

    try {
      recorder.start()
      pushSttDebug('local-start', endpointUrl)
    } catch (err) {
      pushSttDebug('local-start-throw', String((err as Error)?.message || err))
      releaseStream()
      finish('')
    }
  }

  /** 松手时调用：停止录音，触发 onstop → 上传 */
  function stop() {
    if (!recorder) return
    try { recorder.stop() } catch { /* ignore */ }
  }

  /** 放弃当前会话，不上传 */
  function abort() {
    token++
    if (recorder && recorder.state !== 'inactive') {
      try { recorder.stop() } catch { /* ignore */ }
    }
    recorder = null
    releaseStream()
    finish('')
  }

  onUnmounted(() => {
    token++
    if (recorder && recorder.state !== 'inactive') {
      try { recorder.stop() } catch { /* ignore */ }
    }
    recorder = null
    releaseStream()
  })

  return { supported, listening, interimText, finalText, alternatives, start, stop, abort }
}
