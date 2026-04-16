import { useAppStore } from '@/stores/app'

export function escHtml(s: string): string {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

export function todayKey(): string {
  return new Date().toISOString().slice(0, 10)
}

export function generateId(): string {
  const words = ['sakura','kaze','yama','umi','sora','hana','tsuki','hoshi','kumo','ame','yuki','mori','kawa','take','ishi']
  const word = words[Math.floor(Math.random() * words.length)]
  const num = Math.floor(1000 + Math.random() * 9000)
  return word + '-' + num
}

/** uiLang：界面语言。学英语且界面为日语时优先显示 meaningJp。 */
export function localMeaning(
  item: { meaning: string; meaningEn?: string; meaningJp?: string },
  uiLang: string,
): string {
  const studyLang = useAppStore().studyLang
  if (studyLang === 'en' && uiLang === 'ja' && item.meaningJp?.trim()) {
    return item.meaningJp
  }
  if (uiLang === 'en' && item.meaningEn) return item.meaningEn
  return item.meaning
}

export function localExampleCn(
  item: { exampleCn?: string; exampleEn?: string; exampleJp?: string },
  uiLang: string,
): string | undefined {
  if (uiLang === 'ja' && item.exampleJp) return item.exampleJp
  if (uiLang === 'en' && item.exampleEn) return item.exampleEn
  return item.exampleCn
}

export function formatListenTime(sec: number, t: (k: string) => string): string {
  sec = Math.round(sec || 0)
  if (sec < 60) return '0' + t('min')
  const m = Math.floor(sec / 60)
  if (m < 60) return m + t('min')
  const h = Math.floor(m / 60)
  return h + t('hour') + (m % 60) + t('min')
}
