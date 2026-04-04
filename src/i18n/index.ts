import { ref, computed } from 'vue'
import type { LangKey } from '@/types'
import { messages } from './messages'

export const currentLang = ref<LangKey>((localStorage.getItem('jp_lang') as LangKey) || 'zh')

export type TParams = Record<string, string | number>

function interpolate(template: string, params?: TParams): string {
  if (!params) return template
  let s = template
  for (const [k, v] of Object.entries(params)) {
    s = s.split(`{${k}}`).join(String(v))
  }
  return s
}

// Plain function for use in non-reactive contexts (composables, etc.)
export function t(key: string, params?: TParams): string {
  const raw = messages[currentLang.value]?.[key] || messages.zh[key] || key
  return interpolate(raw, params)
}

export function switchLang(lang: LangKey) {
  currentLang.value = lang
  localStorage.setItem('jp_lang', lang)
}

export function useLang() {
  // Computed messages object that updates when language changes
  const msgs = computed(() => messages[currentLang.value] || messages.zh)

  // Reactive t function — Vue tracks msgs.value access
  const tr = (key: string, params?: TParams): string => {
    const raw = msgs.value[key] || messages.zh[key] || key
    return interpolate(raw, params)
  }

  return { currentLang, t: tr, switchLang, msgs }
}
