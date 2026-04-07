import { ref, watch } from 'vue'
import { safeGet, safeSet } from '@/storage/safeLS'
import { LS } from '@/storage/keys'

export type ThemeMode = 'dusk' | 'watercolor' | 'ink'

const ALL_THEMES: ThemeMode[] = ['dusk', 'watercolor', 'ink']
const themeMode = ref<ThemeMode>('watercolor')
let inited = false

function applyTheme(mode: ThemeMode) {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  ALL_THEMES.forEach(t => root.classList.remove(`theme-${t}`))
  root.classList.add(`theme-${mode}`)
  root.setAttribute('data-theme', mode)
  // Backwards compat: components checking theme-dark
  root.classList.toggle('theme-dark', mode !== 'watercolor')
}

function initTheme() {
  if (inited) return
  const raw = safeGet(LS.THEME)
  if (raw && (ALL_THEMES as string[]).includes(raw)) {
    themeMode.value = raw as ThemeMode
  } else if (raw === 'warm') {
    // legacy 值迁移：老的暖云主题映射到水彩
    themeMode.value = 'watercolor'
  } else if (raw === 'dark') {
    // legacy 值迁移
    themeMode.value = 'ink'
  } else {
    themeMode.value = 'watercolor'
  }
  applyTheme(themeMode.value)
  watch(themeMode, (mode) => {
    safeSet(LS.THEME, mode)
    applyTheme(mode)
  })
  inited = true
}

function setTheme(mode: ThemeMode) {
  themeMode.value = mode
}

function toggleTheme() {
  const idx = ALL_THEMES.indexOf(themeMode.value)
  themeMode.value = ALL_THEMES[(idx + 1) % ALL_THEMES.length]
}

export function useTheme() {
  return {
    themeMode,
    initTheme,
    setTheme,
    toggleTheme,
    ALL_THEMES,
  }
}
