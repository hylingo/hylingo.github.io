import { ref, onUnmounted } from 'vue'

export function useVoiceRecorder() {
  const recording = ref(false)
  const audioUrl = ref<string | null>(null)

  let mediaRecorder: MediaRecorder | null = null
  let chunks: Blob[] = []
  let stream: MediaStream | null = null

  function revokeOldUrl() {
    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
      audioUrl.value = null
    }
  }

  function pickMimeType(): string {
    for (const mime of ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4']) {
      if (MediaRecorder.isTypeSupported(mime)) return mime
    }
    return ''
  }

  async function startRecording() {
    revokeOldUrl()
    chunks = []
    try {
      if (!stream || !stream.active) {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      }
      const mimeType = pickMimeType()
      mediaRecorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream)
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data)
      }
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: mediaRecorder?.mimeType || 'audio/webm' })
        audioUrl.value = URL.createObjectURL(blob)
      }
      mediaRecorder.start()
      recording.value = true
    } catch {
      recording.value = false
    }
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
    }
    recording.value = false
    // 释放麦克风轨道，否则浏览器标签页会一直显示录音指示
    releaseStream()
  }

  function clearRecording() {
    revokeOldUrl()
  }

  function releaseStream() {
    stream?.getTracks().forEach((t) => t.stop())
    stream = null
  }

  onUnmounted(() => {
    revokeOldUrl()
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
    }
    releaseStream()
  })

  return {
    recording,
    audioUrl,
    startRecording,
    stopRecording,
    clearRecording,
  }
}
