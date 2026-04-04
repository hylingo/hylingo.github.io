/** 听过次数：合并、读写时统一成非负整数，避免字符串拼接或 NaN */
export function coerceListenCount(v: unknown): number {
  if (typeof v === 'number' && Number.isFinite(v)) {
    return Math.min(Math.max(0, Math.floor(v)), 999_999)
  }
  const n = Number(v)
  if (!Number.isFinite(n) || n < 0) return 0
  return Math.min(Math.floor(n), 999_999)
}

/** 同步合并：每个 cat:id 取本地与云端较大值（不会把两台设备的次数相加） */
export function mergeListenCountMaps(
  local: Record<string, unknown>,
  cloud: Record<string, unknown>,
): Record<string, number> {
  const keys = new Set([...Object.keys(local || {}), ...Object.keys(cloud || {})])
  const out: Record<string, number> = {}
  for (const k of keys) {
    out[k] = Math.max(coerceListenCount(local?.[k]), coerceListenCount(cloud?.[k]))
  }
  return out
}
