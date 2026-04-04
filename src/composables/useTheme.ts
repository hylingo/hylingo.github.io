import { ref, watch } from 'vue'

export type ThemeMode = 'light' | 'dark'

const THEME_KEY = 'app_theme_mode_v1'
const themeMode = ref<ThemeMode>('light')
let inited = false

function applyTheme(mode: ThemeMode) {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  root.classList.toggle('theme-dark', mode === 'dark')
  root.setAttribute('data-theme', mode)
}

function initTheme() {
  if (inited) return
  const stored = localStorage.getItem(THEME_KEY)
  if (stored === 'dark' || stored === 'light') {
    themeMode.value = stored
  } else if (typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: dark)').matches) {
    themeMode.value = 'dark'
  }
  applyTheme(themeMode.value)
  watch(themeMode, (mode) => {
    localStorage.setItem(THEME_KEY, mode)
    applyTheme(mode)
  })
  inited = true
}

function toggleTheme() {
  themeMode.value = themeMode.value === 'dark' ? 'light' : 'dark'
}

export function useTheme() {
  return {
    themeMode,
    initTheme,
    toggleTheme,
  }
}
