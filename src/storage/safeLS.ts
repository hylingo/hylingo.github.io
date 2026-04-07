/**
 * localStorage 安全包装：隐私模式 / quota 满 / 关闭存储 时不抛异常。
 *
 * 设计原则：
 * - 读失败 → 返回 fallback（默认 null）
 * - 写失败 → 返回 false，不抛
 * - 不做加密、不做版本迁移（这里只管底层 IO）
 */

const hasLS = (() => {
  try {
    const k = '__hylingo_ls_probe__'
    localStorage.setItem(k, '1')
    localStorage.removeItem(k)
    return true
  } catch {
    return false
  }
})()

export function safeGet(key: string): string | null {
  if (!hasLS) return null
  try {
    return localStorage.getItem(key)
  } catch {
    return null
  }
}

export function safeSet(key: string, value: string): boolean {
  if (!hasLS) return false
  try {
    localStorage.setItem(key, value)
    return true
  } catch {
    return false
  }
}

export function safeRemove(key: string): void {
  if (!hasLS) return
  try {
    localStorage.removeItem(key)
  } catch {
    /* ignore */
  }
}

export function safeGetJSON<T>(key: string, fallback: T): T {
  const raw = safeGet(key)
  if (raw == null) return fallback
  try {
    return JSON.parse(raw) as T
  } catch {
    return fallback
  }
}

export function safeSetJSON(key: string, value: unknown): boolean {
  try {
    return safeSet(key, JSON.stringify(value))
  } catch {
    return false
  }
}

export function safeGetNumber(key: string, fallback = 0): number {
  const raw = safeGet(key)
  if (raw == null) return fallback
  const n = Number(raw)
  return Number.isFinite(n) ? n : fallback
}
