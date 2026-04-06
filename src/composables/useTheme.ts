import { ref, watch } from 'vue'

export type ThemeMode = 'dusk' | 'warm' | 'ink'

const THEME_KEY = 'app_theme_mode_v1'
const ALL_THEMES: ThemeMode[] = ['dusk', 'warm', 'ink']
const themeMode = ref<ThemeMode>('warm')
let inited = false

function applyTheme(mode: ThemeMode) {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  ALL_THEMES.forEach(t => root.classList.remove(`theme-${t}`))
  root.classList.add(`theme-${mode}`)
  root.setAttribute('data-theme', mode)
  // Backwards compat: components checking theme-dark
  root.classList.toggle('theme-dark', mode !== 'warm')
}

function initTheme() {
  if (inited) return
  const stored = localStorage.getItem(THEME_KEY) as ThemeMode | null
  if (stored && ALL_THEMES.includes(stored)) {
    themeMode.value = stored
  } else {
    // Migrate old values
    const legacy = localStorage.getItem(THEME_KEY)
    if (legacy === 'dark') themeMode.value = 'ink'
    else themeMode.value = 'warm'
  }
  applyTheme(themeMode.value)
  watch(themeMode, (mode) => {
    localStorage.setItem(THEME_KEY, mode)
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
