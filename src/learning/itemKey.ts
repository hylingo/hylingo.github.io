/** 跨听列表、练习、里程碑、Firebase 的统一词条键 */
export function makeItemKey(cat: string, id: number): string {
  return `${cat}:${id}`
}

/** 解析 `nouns:12` / `verbs:3`；仅支持当前词库分类 */
export function parseItemKey(key: string): { cat: string; id: number } | null {
  const i = key.lastIndexOf(':')
  if (i <= 0) return null
  const cat = key.slice(0, i)
  const id = Number(key.slice(i + 1))
  if (!Number.isFinite(id)) return null
  if (cat !== 'nouns' && cat !== 'verbs') return null
  return { cat, id }
}
