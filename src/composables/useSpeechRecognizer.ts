/**
 * 统一语音识别入口：根据 localStorage.LOCAL_STT_URL 决定走
 *   - 本地 whisper.cpp server（开发机自用，识别质量高）
 *   - 还是 Web Speech API（线上默认）
 *
 * 调用方只需 start/stop/abort，不关心底层实现。
 * stop = 用户主动结束（松手），拿识别结果；abort = 放弃（切题、卸载）
 */
import { computed } from 'vue'
import { useStt } from './useStt'
import { useLocalStt } from './useLocalStt'
import { safeGet } from '@/storage/safeLS'
import { LS } from '@/storage/keys'

export function useSpeechRecognizer() {
  const localUrl = safeGet(LS.LOCAL_STT_URL) || ''
  const useLocal = !!localUrl.trim()

  const webStt = !useLocal ? useStt() : null
  const localStt = useLocal ? useLocalStt(localUrl.trim()) : null
  const impl = useLocal ? localStt! : webStt!

  // Web Speech 没有独立 stop 语义（onend 自己触发），沿用 abort 作为"结束"
  // 本地模式 stop 才是"结束并上传"
  const stop = useLocal ? impl.stop : impl.abort

  return {
    supported: impl.supported,
    listening: impl.listening,
    interimText: impl.interimText,
    finalText: impl.finalText,
    alternatives: impl.alternatives,
    start: impl.start,
    stop,
    abort: impl.abort,
    mode: computed(() => (useLocal ? 'local' : 'web') as 'local' | 'web'),
  }
}
