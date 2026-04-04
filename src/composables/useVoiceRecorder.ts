import { ref, onUnmounted } from 'vue'
import { recordReadTime } from './useStats'

export function useVoiceRecorder() {
  const recording = ref(false)
  const audioUrl = ref<string | null>(null)

  let mediaRecorder: MediaRecorder | null = null
  let chunks: Blob[] = []
  let stream: MediaStream | null = null
  let recordStartTime = 0

  function revokeOldUrl() {
    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
      audioUrl.value = null
    }
  }

  async function startRecording() {
    revokeOldUrl()
    chunks = []
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream)
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data)
      }
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' })
        audioUrl.value = URL.createObjectURL(blob)
        stream?.getTracks().forEach((t) => t.stop())
        stream = null
      }
      mediaRecorder.start()
      recordStartTime = Date.now()
      recording.value = true
    } catch {
      recording.value = false
    }
  }

  function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
      const duration = (Date.now() - recordStartTime) / 1000
      if (duration > 0.5) recordReadTime(duration)
    }
    recording.value = false
  }

  function clearRecording() {
    revokeOldUrl()
  }

  onUnmounted(() => {
    revokeOldUrl()
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
    }
    stream?.getTracks().forEach((t) => t.stop())
  })

  return {
    recording,
    audioUrl,
    startRecording,
    stopRecording,
    clearRecording,
  }
}
