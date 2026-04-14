import { ref } from 'vue'

export interface SttDebugEntry {
  ts: number
  tag: string
  msg: string
}

export const sttDebugLog = ref<SttDebugEntry[]>([])
export const sttDebugVisible = ref(false)

const MAX = 200

export function pushSttDebug(tag: string, msg: string) {
  sttDebugLog.value.push({ ts: Date.now(), tag, msg })
  if (sttDebugLog.value.length > MAX) sttDebugLog.value.splice(0, sttDebugLog.value.length - MAX)
}

export function clearSttDebug() {
  sttDebugLog.value = []
}

export function formatSttDebug(): string {
  return sttDebugLog.value
    .map((e) => {
      const d = new Date(e.ts)
      const hh = String(d.getHours()).padStart(2, '0')
      const mm = String(d.getMinutes()).padStart(2, '0')
      const ss = String(d.getSeconds()).padStart(2, '0')
      const ms = String(d.getMilliseconds()).padStart(3, '0')
      return `${hh}:${mm}:${ss}.${ms} [${e.tag}] ${e.msg}`
    })
    .join('\n')
}
