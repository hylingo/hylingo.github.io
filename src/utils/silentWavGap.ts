/** 极短静音循环，用于保活（与列表循环共用） */
export const SILENT_KEEPALIVE_WAV =
  'data:audio/wav;base64,UklGRjQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YRAAAAAAAAAAAAAAAAAAAAAAAAAA'

const gapWavCache = new Map<number, string>()

function toBase64(bytes: Uint8Array): string {
  let binary = ''
  const chunkSize = 0x8000
  for (let i = 0; i < bytes.length; i += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunkSize))
  }
  return btoa(binary)
}

function createSilentWavDataUri(ms: number): string {
  const clampedMs = Math.max(20, Math.min(2000, Math.floor(ms)))
  const sampleRate = 8000
  const channels = 1
  const bitsPerSample = 16
  const bytesPerSample = bitsPerSample / 8
  const numSamples = Math.floor((sampleRate * clampedMs) / 1000)
  const dataSize = numSamples * channels * bytesPerSample
  const buffer = new ArrayBuffer(44 + dataSize)
  const view = new DataView(buffer)

  const writeString = (offset: number, text: string) => {
    for (let i = 0; i < text.length; i++) view.setUint8(offset + i, text.charCodeAt(i))
  }

  writeString(0, 'RIFF')
  view.setUint32(4, 36 + dataSize, true)
  writeString(8, 'WAVE')
  writeString(12, 'fmt ')
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true)
  view.setUint16(22, channels, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * channels * bytesPerSample, true)
  view.setUint16(32, channels * bytesPerSample, true)
  view.setUint16(34, bitsPerSample, true)
  writeString(36, 'data')
  view.setUint32(40, dataSize, true)
  for (let i = 0; i < numSamples; i++) {
    const sample = i % 2 === 0 ? 1 : -1
    view.setInt16(44 + i * 2, sample, true)
  }

  return `data:audio/wav;base64,${toBase64(new Uint8Array(buffer))}`
}

/** 用于句间停顿的静音片段（锁屏时节流 setTimeout 不可靠，用 audio onended 推进） */
export function getGapWavUri(ms: number): string {
  const key = Math.round(ms / 20) * 20
  const cached = gapWavCache.get(key)
  if (cached) return cached
  const wav = createSilentWavDataUri(key)
  gapWavCache.set(key, wav)
  return wav
}
