# Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace current light/dark dual theme with three complete themes (Dusk/Warm Cloud/Ink & Amber), replace all emoji icons with SVG, and convert bottom nav to floating island style.

**Architecture:** CSS custom properties drive all three themes via root class (`.theme-dusk`, `.theme-warm`, `.theme-ink`). SVG icons centralized in a single `icons.ts` map. Theme composable extended to support three modes with localStorage persistence.

**Tech Stack:** Vue 3, Tailwind CSS 4, CSS custom properties, inline SVG

**Spec:** `docs/superpowers/specs/2026-04-07-visual-redesign-design.md`

---

### Task 1: Create SVG Icon System

**Files:**
- Create: `src/components/common/AppIcon.vue`
- Create: `src/icons.ts`

- [ ] **Step 1: Create icon map**

Create `src/icons.ts` with all SVG paths used in the app:

```typescript
// Each icon: [viewBox, innerHTML] — stroke icons use currentColor
export const icons: Record<string, [string, string]> = {
  // Navigation
  listen:    ['0 0 24 24', '<path d="M9 18V5l12-2v13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="6" cy="18" r="3" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="18" cy="16" r="3" fill="none" stroke="currentColor" stroke-width="1.8"/>'],
  practice:  ['0 0 24 24', '<path d="M17 3a2.83 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  stats:     ['0 0 24 24', '<path d="M18 20V10M12 20V4M6 20v-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  // Content
  search:    ['0 0 24 24', '<circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  settings:  ['0 0 24 24', '<line x1="4" y1="21" x2="4" y2="14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="4" y1="10" x2="4" y2="3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="12" y1="21" x2="12" y2="12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="12" y1="8" x2="12" y2="3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="20" y1="21" x2="20" y2="16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="20" y1="12" x2="20" y2="3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="1" y1="14" x2="7" y2="14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="9" y1="8" x2="15" y2="8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="17" y1="16" x2="23" y2="16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  volume:    ['0 0 24 24', '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  play:      ['0 0 24 24', '<polygon points="6 3 20 12 6 21 6 3" fill="currentColor" stroke="none"/>'],
  playOutline: ['0 0 24 24', '<polygon points="6 3 20 12 6 21 6 3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'],
  pause:     ['0 0 24 24', '<rect x="6" y="4" width="4" height="16" rx="1" fill="currentColor"/><rect x="14" y="4" width="4" height="16" rx="1" fill="currentColor"/>'],
  prev:      ['0 0 24 24', '<polygon points="19 20 9 12 19 4 19 20" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="5" y1="19" x2="5" y2="5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  next:      ['0 0 24 24', '<polygon points="5 4 15 12 5 20 5 4" fill="none" stroke="currentColor" stroke-width="1.8"/><line x1="19" y1="5" x2="19" y2="19" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  repeat:    ['0 0 24 24', '<polyline points="17 1 21 5 17 9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M3 11V9a4 4 0 0 1 4-4h14" fill="none" stroke="currentColor" stroke-width="1.8"/><polyline points="7 23 3 19 7 15" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M21 13v2a4 4 0 0 1-4 4H3" fill="none" stroke="currentColor" stroke-width="1.8"/>'],
  back:      ['0 0 24 24', '<polyline points="15 18 9 12 15 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'],
  close:     ['0 0 24 24', '<line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  expand:    ['0 0 24 24', '<polyline points="4 14 10 14 10 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><polyline points="20 10 14 10 14 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="14" y1="10" x2="21" y2="3" stroke="currentColor" stroke-width="1.8"/><line x1="3" y1="21" x2="10" y2="14" stroke="currentColor" stroke-width="1.8"/>'],
  star:      ['0 0 24 24', '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" fill="none" stroke="currentColor" stroke-width="1.5"/>'],
  starFill:  ['0 0 24 24', '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" fill="currentColor" stroke="currentColor" stroke-width="1.5"/>'],
  check:     ['0 0 24 24', '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><polyline points="22 4 12 14.01 9 11.01" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'],
  book:      ['0 0 24 24', '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" fill="none" stroke="currentColor" stroke-width="1.8"/>'],
  chat:      ['0 0 24 24', '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'],
  mic:       ['0 0 24 24', '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M19 10v2a7 7 0 0 1-14 0v-2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="12" y1="19" x2="12" y2="23" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'],
  chevronRight: ['0 0 24 24', '<polyline points="9 18 15 12 9 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'],
}
```

- [ ] **Step 2: Create AppIcon component**

Create `src/components/common/AppIcon.vue`:

```vue
<script setup lang="ts">
import { icons } from '@/icons'

const props = defineProps<{
  name: string
  size?: number | string
}>()
</script>

<template>
  <svg
    v-if="icons[name]"
    :viewBox="icons[name][0]"
    :width="size ?? 20"
    :height="size ?? 20"
    aria-hidden="true"
    v-html="icons[name][1]"
  />
</template>
```

- [ ] **Step 3: Commit**

```bash
git add src/icons.ts src/components/common/AppIcon.vue
git commit -m "feat: add centralized SVG icon system"
```

---

### Task 2: Rewrite useTheme for Three Themes

**Files:**
- Modify: `src/composables/useTheme.ts`

- [ ] **Step 1: Rewrite useTheme.ts**

Replace the full file content with:

```typescript
import { ref, watch } from 'vue'

export type ThemeMode = 'dusk' | 'warm' | 'ink'

const THEME_KEY = 'app_theme_mode_v1'
const ALL_THEMES: ThemeMode[] = ['dusk', 'warm', 'ink']
const themeMode = ref<ThemeMode>('warm')
let inited = false

function applyTheme(mode: ThemeMode) {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  // Remove all theme classes, then add the current one
  ALL_THEMES.forEach(t => root.classList.remove(`theme-${t}`))
  root.classList.add(`theme-${mode}`)
  root.setAttribute('data-theme', mode)
  // For backwards compat with components checking theme-dark
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

// Keep toggleTheme for quick cycling
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
```

- [ ] **Step 2: Verify the app still loads** (no runtime errors)

Run: `npm run dev` and check browser console.

- [ ] **Step 3: Commit**

```bash
git add src/composables/useTheme.ts
git commit -m "feat: extend useTheme to support three themes (dusk/warm/ink)"
```

---

### Task 3: Rewrite CSS Theme Variables

**Files:**
- Modify: `src/style.css`

- [ ] **Step 1: Replace `:root` and `:root.theme-dark` variable blocks**

Replace lines 21-93 (the `:root { ... }` and `:root.theme-dark { ... }` blocks) with three theme blocks. The `:root` block keeps only non-theme defaults. Each theme gets its own block:

```css
/* ── Default (Warm Cloud) ── */
:root {
  --radius: 16px;
  --radius-sm: 10px;
}

/* ── Theme: Warm Cloud (light) ── */
:root.theme-warm {
  --bg: #e8ddd0;
  --bg-gradient: linear-gradient(175deg, #e8ddd0 0%, #ddd2c4 40%, #d8ccbc 100%);
  --bg-glow: radial-gradient(circle at 30% 0%, rgba(255,240,220,0.35) 0%, transparent 60%);
  --card: rgba(255,255,255,0.5);
  --card-border: rgba(255,255,255,0.4);
  --card-blur: blur(20px);
  --card-shadow: 0 4px 20px rgba(0,0,0,0.04);
  --primary: #5a4a38;
  --primary-light: rgba(255,255,255,0.3);
  --primary-dark: #3a3028;
  --accent: #7a9a78;
  --accent-light: rgba(120,160,120,0.1);
  --text: #2a2420;
  --text-secondary: #8a7a68;
  --border: rgba(0,0,0,0.06);
  --shadow: 0 2px 12px rgba(0,0,0,0.03);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.06);
  --header-grad: rgba(255,255,255,0.45);
  --header-blur: saturate(180%) blur(16px);
  --header-title: var(--text);
  --nav-bg: rgba(255,255,255,0.45);
  --nav-blur: blur(24px);
  --nav-border: rgba(255,255,255,0.3);
  --nav-active-bg: rgba(0,0,0,0.06);
  --nav-active-color: #5a4a38;
  --nav-inactive-color: #a09080;
  --grad-primary: rgba(90,74,56,0.85);
  --grad-primary-pressed: rgba(70,58,44,0.9);
  --grad-accent: linear-gradient(135deg, #7a9a78 0%, #5a8060 100%);
  --grad-tab-solid: rgba(255,255,255,0.7);
  --tab-rail-bg: rgba(0,0,0,0.06);
  --tab-active-shadow: 0 1px 4px rgba(0,0,0,0.06);
  --overlay-scrim: rgba(20, 18, 16, 0.2);
  --kana-cell: rgba(255,255,255,0.4);
  --kana-cell-hover: rgba(255,255,255,0.55);
  --content-original: var(--text);
  --content-translation: #6a5a48;
  --content-example: #8a7a68;
  --content-ruby: #a08868;
  --stat-listen: linear-gradient(135deg, rgba(160,130,100,0.35), rgba(160,130,100,0.15));
  --stat-read: linear-gradient(135deg, rgba(120,160,120,0.3), rgba(120,160,120,0.12));
  --stat-practice: linear-gradient(135deg, rgba(140,120,180,0.25), rgba(140,120,180,0.1));
  --stat-mastered: linear-gradient(135deg, rgba(160,130,100,0.3), rgba(160,130,100,0.12));
  --stat-listen-icon: #a08868;
  --stat-read-icon: #7a9a78;
  --stat-practice-icon: #8a7ab0;
  --stat-mastered-icon: #a08868;
}

/* ── Theme: Dusk (cold) ── */
:root.theme-dusk {
  --bg: #1e2028;
  --bg-gradient: linear-gradient(170deg, #2a1f3d 0%, #1a2235 30%, #1c2a30 60%, #1e2520 100%);
  --bg-glow: radial-gradient(ellipse at 30% 0%, rgba(160,120,200,0.15) 0%, transparent 60%);
  --card: rgba(255,255,255,0.05);
  --card-border: rgba(255,255,255,0.07);
  --card-blur: blur(16px);
  --card-shadow: none;
  --primary: #c8a8e8;
  --primary-light: rgba(160,120,200,0.15);
  --primary-dark: #a888c8;
  --accent: #80c8a8;
  --accent-light: rgba(120,180,160,0.12);
  --text: #f0ebe5;
  --text-secondary: rgba(255,255,255,0.35);
  --border: rgba(255,255,255,0.07);
  --shadow: none;
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.3);
  --header-grad: rgba(0,0,0,0.3);
  --header-blur: blur(24px);
  --header-title: #f0ebe5;
  --nav-bg: rgba(0,0,0,0.4);
  --nav-blur: blur(24px);
  --nav-border: rgba(255,255,255,0.06);
  --nav-active-bg: rgba(200,160,120,0.15);
  --nav-active-color: #d4a878;
  --nav-inactive-color: rgba(255,255,255,0.3);
  --grad-primary: linear-gradient(135deg, rgba(160,120,200,0.3), rgba(200,170,120,0.2));
  --grad-primary-pressed: linear-gradient(135deg, rgba(140,100,180,0.4), rgba(180,150,100,0.3));
  --grad-accent: linear-gradient(135deg, rgba(120,180,160,0.3), rgba(100,160,140,0.2));
  --grad-tab-solid: rgba(255,255,255,0.1);
  --tab-rail-bg: transparent;
  --tab-active-shadow: none;
  --overlay-scrim: rgba(0, 0, 0, 0.48);
  --kana-cell: rgba(255,255,255,0.04);
  --kana-cell-hover: rgba(255,255,255,0.08);
  --content-original: #ece6de;
  --content-translation: rgba(255,255,255,0.3);
  --content-example: rgba(255,255,255,0.25);
  --content-ruby: rgba(200,170,240,0.5);
  --stat-listen: linear-gradient(135deg, rgba(160,120,200,0.15), rgba(140,100,180,0.08));
  --stat-read: linear-gradient(135deg, rgba(120,180,160,0.12), rgba(100,160,140,0.06));
  --stat-practice: linear-gradient(135deg, rgba(200,170,120,0.12), rgba(180,150,100,0.06));
  --stat-mastered: linear-gradient(135deg, rgba(200,120,120,0.1), rgba(180,100,100,0.05));
  --stat-listen-icon: rgba(200,170,240,0.5);
  --stat-read-icon: rgba(160,220,200,0.5);
  --stat-practice-icon: rgba(220,200,160,0.5);
  --stat-mastered-icon: rgba(240,180,180,0.5);
}

/* ── Theme: Ink & Amber (dark) ── */
:root.theme-ink {
  --bg: #141518;
  --bg-gradient: linear-gradient(180deg, #141518 0%, #18191e 50%, #141518 100%);
  --bg-glow: radial-gradient(ellipse at 50% 0%, rgba(220,180,120,0.06) 0%, transparent 70%);
  --card: rgba(255,255,255,0.03);
  --card-border: rgba(255,255,255,0.05);
  --card-blur: none;
  --card-shadow: none;
  --primary: #dcb478;
  --primary-light: rgba(220,180,120,0.1);
  --primary-dark: #c49a5a;
  --accent: #80c8a0;
  --accent-light: rgba(120,180,160,0.08);
  --text: #f0ebe5;
  --text-secondary: rgba(255,255,255,0.3);
  --border: rgba(255,255,255,0.05);
  --shadow: none;
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.4);
  --header-grad: rgba(20,21,24,0.85);
  --header-blur: blur(16px);
  --header-title: #f0ebe5;
  --nav-bg: rgba(0,0,0,0.4);
  --nav-blur: blur(24px);
  --nav-border: rgba(255,255,255,0.06);
  --nav-active-bg: rgba(220,180,120,0.15);
  --nav-active-color: #dcb478;
  --nav-inactive-color: rgba(255,255,255,0.3);
  --grad-primary: linear-gradient(135deg, rgba(220,180,120,0.2), rgba(200,160,100,0.15));
  --grad-primary-pressed: linear-gradient(135deg, rgba(200,160,100,0.3), rgba(180,140,80,0.25));
  --grad-accent: linear-gradient(135deg, rgba(120,180,160,0.2), rgba(100,160,140,0.15));
  --grad-tab-solid: rgba(220,180,120,0.1);
  --tab-rail-bg: rgba(255,255,255,0.03);
  --tab-active-shadow: none;
  --overlay-scrim: rgba(0, 0, 0, 0.48);
  --kana-cell: rgba(255,255,255,0.03);
  --kana-cell-hover: rgba(255,255,255,0.06);
  --content-original: #ece6de;
  --content-translation: rgba(255,255,255,0.3);
  --content-example: rgba(255,255,255,0.25);
  --content-ruby: rgba(220,180,120,0.5);
  --stat-listen: linear-gradient(135deg, rgba(220,180,120,0.05), rgba(220,180,120,0.08));
  --stat-read: linear-gradient(135deg, rgba(120,180,160,0.05), rgba(120,180,160,0.08));
  --stat-practice: linear-gradient(135deg, rgba(160,140,200,0.05), rgba(160,140,200,0.08));
  --stat-mastered: linear-gradient(135deg, rgba(220,180,120,0.05), rgba(220,180,120,0.08));
  --stat-listen-icon: rgba(220,180,120,0.4);
  --stat-read-icon: rgba(120,180,160,0.4);
  --stat-practice-icon: rgba(160,140,200,0.4);
  --stat-mastered-icon: rgba(220,180,120,0.4);
}
```

- [ ] **Step 2: Update body and body::before to use new variables**

Replace the `body { ... }` block (lines ~57-65) with:

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Noto Sans JP", "Yu Gothic", sans-serif;
  background: var(--bg-gradient, var(--bg));
  color: var(--text);
  min-height: 100vh;
  min-height: 100svh;
  overflow-x: clip;
  overscroll-behavior-y: none;
}

body::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: var(--bg-glow, none);
  z-index: 0;
  pointer-events: none;
}
```

Remove the old `:root.theme-dark body` and `:root.theme-dark body::before` rules.

- [ ] **Step 3: Update all `:root.theme-dark` rules in style.css**

Search for every `:root.theme-dark` selector in style.css and either:
- Remove it (if the variable it was overriding is now handled by the three theme blocks)
- Convert to `:root.theme-dusk, :root.theme-ink` if it was a dark-mode-specific rule

Key changes:
- `.category-tab-rail` dark rules → use CSS variables `--tab-rail-bg`, `--border`
- `.filter-chip--off` dark rules → use CSS variables
- `.theme-nav-mobile/desktop` dark rules → use CSS variables `--nav-bg`
- `.stat-card` dark rules → remove, stats will use new `--stat-*` variables
- Other component-level dark overrides → use variables or `:root:not(.theme-warm)` if needed

- [ ] **Step 4: Update `.theme-card` to use new card variables**

Replace the `.theme-card` rule:

```css
.theme-card {
  border-radius: 12px;
  border: 1px solid var(--card-border, var(--border));
  background: var(--card);
  color: var(--text);
  backdrop-filter: var(--card-blur, none);
  -webkit-backdrop-filter: var(--card-blur, none);
  box-shadow: var(--card-shadow, none);
}
```

- [ ] **Step 5: Update `.theme-header` and nav classes**

```css
.theme-header {
  background: var(--header-grad);
  color: var(--header-title);
  backdrop-filter: var(--header-blur);
  -webkit-backdrop-filter: var(--header-blur);
  padding-top: calc(env(safe-area-inset-top, 0px) + 0.625rem);
  padding-bottom: 0.625rem;
}

.theme-nav-mobile,
.theme-nav-desktop {
  background: var(--nav-bg);
  backdrop-filter: var(--nav-blur);
  -webkit-backdrop-filter: var(--nav-blur);
  border-color: var(--nav-border);
}
```

Remove the separate `:root.theme-dark .theme-header` and `:root.theme-dark .theme-nav-*` rules.

- [ ] **Step 6: Update `.category-tab-rail` and tab button classes to use variables**

```css
.category-tab-rail {
  background: var(--tab-rail-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 3px;
}

.category-tab-btn--active {
  background: var(--grad-tab-solid);
  color: var(--text);
  box-shadow: var(--tab-active-shadow);
  border-radius: 10px;
}

.category-tab-btn--inactive {
  color: var(--text-secondary);
}
```

Remove all `:root.theme-dark .category-tab-*` rules.

- [ ] **Step 7: Update stat card classes to use variables**

Replace stat card gradient rules:

```css
.stat-card { box-shadow: var(--card-shadow, 0 4px 14px rgba(0,0,0,0.08)); }
.stat-card--listen { background: var(--stat-listen); }
.stat-card--read { background: var(--stat-read); }
.stat-card--practice { background: var(--stat-practice); }
.stat-card--mastered { background: var(--stat-mastered); }
```

Remove all `:root.theme-dark .stat-card*` rules.

- [ ] **Step 8: Update remaining component-level dark overrides**

Convert `.filter-chip`, `.btn-grad-primary`, `.btn-soft-danger`, `.dropdown-scroll`, and other component rules to use CSS variables instead of `:root.theme-dark` overrides. Key pattern:

```css
/* Before: */
.filter-chip--off { background: color-mix(..., #ffffff); }
:root.theme-dark .filter-chip--off { background: var(--card); }

/* After: */
.filter-chip--off { background: var(--card); border-color: var(--border); color: var(--text-secondary); }
```

- [ ] **Step 9: Commit**

```bash
git add src/style.css
git commit -m "feat: rewrite CSS theme system for three themes (dusk/warm/ink)"
```

---

### Task 4: Rewrite AppNav to Floating Island

**Files:**
- Modify: `src/components/layout/AppNav.vue`

- [ ] **Step 1: Replace AppNav.vue content**

```vue
<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'
import AppIcon from '@/components/common/AppIcon.vue'

const store = useAppStore()
const { t } = useLang()

const navItems = [
  { mode: 'list', icon: 'listen', key: 'tabList' },
  { mode: 'practice', icon: 'practice', key: 'tabPractice' },
  { mode: 'stats', icon: 'stats', key: 'tabStats' },
] as const
</script>

<template>
  <!-- Mobile: floating island bottom bar -->
  <nav
    class="md:hidden fixed z-[200] left-[20px] right-[20px] theme-nav-mobile rounded-[20px]"
    :style="`bottom: calc(env(safe-area-inset-bottom, 0px) + 16px); box-shadow: 0 4px 24px rgba(0,0,0,0.12);`"
  >
    <div class="flex justify-center gap-1 p-[8px_6px]">
      <button
        v-for="item in navItems"
        :key="item.mode"
        class="flex items-center gap-[5px] border-none bg-transparent cursor-pointer transition-all rounded-[14px] px-5 py-2"
        :class="store.currentMode === item.mode
          ? 'nav-island-active'
          : ''"
        :style="store.currentMode === item.mode
          ? `background: var(--nav-active-bg); color: var(--nav-active-color);`
          : `color: var(--nav-inactive-color);`"
        @click="store.switchMode(item.mode)"
      >
        <AppIcon :name="item.icon" :size="17" />
        <span class="text-[11px] font-semibold">{{ t(item.key) }}</span>
      </button>
    </div>
  </nav>

  <!-- Desktop: fixed left sidebar -->
  <nav
    class="hidden md:flex fixed top-0 left-0 bottom-0 w-[200px] flex-col gap-1 pt-20 px-3 pb-6 theme-nav-desktop z-[300] overflow-hidden"
    style="box-shadow: 2px 0 12px rgba(0,0,0,0.04)"
  >
    <div class="text-lg font-bold px-3 pb-5" style="color: var(--primary)">
    </div>
    <button
      v-for="item in navItems"
      :key="item.mode"
      class="flex items-center gap-2.5 px-4 py-3.5 border-none bg-transparent rounded-[10px] text-[15px] font-semibold cursor-pointer transition-all text-left relative z-[1]"
      :class="store.currentMode === item.mode ? 'app-nav-pill--active' : ''"
      :style="store.currentMode !== item.mode ? 'color: var(--text-secondary)' : ''"
      @click="store.switchMode(item.mode)"
    >
      <span class="inline-flex h-8 w-8 shrink-0 items-center justify-center" aria-hidden="true">
        <AppIcon :name="item.icon" :size="20" />
      </span>
      <span>{{ t(item.key) }}</span>
    </button>

    <!-- Flag background decoration -->
    <div class="nav-flag-bg" aria-hidden="true">
      <svg v-if="store.studyLang === 'ja'" viewBox="0 0 300 200" class="nav-flag-svg">
        <rect width="300" height="200" rx="6" fill="#ffffff" />
        <circle cx="150" cy="100" r="60" fill="#bc002d" />
      </svg>
      <svg v-else viewBox="0 0 300 200" class="nav-flag-svg">
        <rect width="300" height="200" fill="#012169" rx="6" />
        <path d="M0,0 L300,200 M300,0 L0,200" stroke="#ffffff" stroke-width="40" />
        <path d="M0,0 L300,200" stroke="#c8102e" stroke-width="14" />
        <path d="M300,0 L0,200" stroke="#c8102e" stroke-width="14" />
        <rect x="0" y="75" width="300" height="50" fill="#ffffff" />
        <rect x="125" y="0" width="50" height="200" fill="#ffffff" />
        <rect x="0" y="83" width="300" height="34" fill="#c8102e" />
        <rect x="133" y="0" width="34" height="200" fill="#c8102e" />
      </svg>
    </div>
  </nav>
</template>
```

- [ ] **Step 2: Update AppLayout.vue bottom padding**

The floating island nav needs more bottom spacing on mobile. Find the main content area in `AppLayout.vue` and increase the mobile bottom padding from `pb-[5rem]` to `pb-[6.5rem]` to account for the floating island's position.

- [ ] **Step 3: Verify nav renders correctly**

Run `npm run dev`, check mobile viewport (375px) and desktop (>768px).

- [ ] **Step 4: Commit**

```bash
git add src/components/layout/AppNav.vue src/components/layout/AppLayout.vue
git commit -m "feat: floating island bottom nav + SVG icons"
```

---

### Task 5: Replace Emoji Icons in All Components

**Files:**
- Modify: `src/components/common/SpeakButton.vue`
- Modify: `src/components/practice/QuizCard.vue`
- Modify: `src/components/practice/PracticePanel.vue`
- Modify: `src/components/stats/MasteredList.vue`
- Modify: `src/components/stats/StatsPanel.vue`
- Modify: `src/components/stats/StatsGrid.vue`
- Modify: `src/components/articles/ArticlesPanel.vue`
- Modify: `src/components/articles/TopicChips.vue`
- Modify: `src/i18n/messages.ts`

- [ ] **Step 1: Replace SpeakButton emoji**

In `SpeakButton.vue`, replace the `🔊` emoji with `<AppIcon name="volume" :size="16" />`. Import AppIcon at the top of the script.

- [ ] **Step 2: Replace QuizCard emoji**

In `QuizCard.vue`, replace `🔊` with `<AppIcon name="volume" :size="20" />`. Import AppIcon.

- [ ] **Step 3: Replace PracticePanel emoji**

In `PracticePanel.vue`, replace `🔊` with `<AppIcon name="volume" :size="20" />`. Import AppIcon.

- [ ] **Step 4: Replace MasteredList emoji**

In `MasteredList.vue`, replace `🔊` with `<AppIcon name="volume" :size="16" />`. Import AppIcon.

- [ ] **Step 5: Replace StatsPanel emojis**

In `StatsPanel.vue`:
- Replace `🇯🇵` / `🇬🇧` flag emojis with text labels: `'JP'` / `'EN'` (these are already inside toggle buttons)
- Line 97: Replace the flag display with the text key
- Replace the dark mode toggle section with a three-theme selector (see Task 6)

- [ ] **Step 6: Replace StatsGrid emoji icons**

In `StatsGrid.vue`, replace any emoji stat icons with `<AppIcon>` using: `listen`, `book`, `practice`, `check` icon names.

- [ ] **Step 7: Replace ArticlesPanel emojis**

In `ArticlesPanel.vue`, replace `💬` and `📖` with `<AppIcon name="chat" :size="14" />` and `<AppIcon name="book" :size="14" />`. Import AppIcon.

- [ ] **Step 8: Replace TopicChips emojis**

In `TopicChips.vue`, the topic emoji map (25+ entries) should be removed. Replace with a simple text-based approach — use the first character of the topic name or a neutral dot, since there are too many categories for custom SVG icons. Example: replace `{ icon: '🍜', ... }` with no icon at all (chips already have text labels).

- [ ] **Step 9: Clean i18n messages**

In `src/i18n/messages.ts`, remove `🔊` and `💡` emoji from all message strings. Replace with empty string or text equivalent where needed.

- [ ] **Step 10: Commit**

```bash
git add -u src/components src/i18n
git commit -m "feat: replace all emoji with SVG icons across components"
```

---

### Task 6: Theme Selector in StatsPanel

**Files:**
- Modify: `src/components/stats/StatsPanel.vue`

- [ ] **Step 1: Replace dark mode toggle with theme selector**

Replace the dark mode toggle card (the `theme-card` div containing `theme-switch`) with a three-circle theme picker:

```vue
<div class="theme-card mt-4 p-4 flex items-center justify-between">
  <div>
    <div class="text-sm font-semibold">{{ t('darkMode') }}</div>
  </div>
  <div class="flex gap-[6px]">
    <button
      v-for="tm in ALL_THEMES"
      :key="tm"
      type="button"
      class="w-[22px] h-[22px] rounded-full border-2 cursor-pointer transition-all"
      :class="themeMode === tm ? 'ring-1 ring-offset-1' : ''"
      :style="`
        background: ${tm === 'dusk' ? 'linear-gradient(135deg,#2a1f3d,#1c2a30)' : tm === 'warm' ? 'linear-gradient(135deg,#e8ddd0,#d8ccbc)' : 'linear-gradient(135deg,#141518,#18191e)'};
        border-color: ${themeMode === tm ? 'var(--primary)' : 'var(--border)'};
        ring-color: var(--primary);
      `"
      @click="setTheme(tm)"
      :aria-label="tm"
    />
  </div>
</div>
```

Update the script to import `setTheme` and `ALL_THEMES`:

```typescript
const { themeMode, setTheme, ALL_THEMES } = useTheme()
```

Remove the `toggleTheme` import.

- [ ] **Step 2: Commit**

```bash
git add src/components/stats/StatsPanel.vue
git commit -m "feat: three-circle theme picker in settings"
```

---

### Task 7: Update WeeklyChart Dark Mode Rules

**Files:**
- Modify: `src/components/stats/WeeklyChart.vue`

- [ ] **Step 1: Replace `:global(:root.theme-dark)` selectors**

In WeeklyChart.vue's `<style scoped>`, replace all `:global(:root.theme-dark)` rules with `:global(:root:not(.theme-warm))` (since both dusk and ink are dark backgrounds):

Search and replace:
- `:global(:root.theme-dark)` → `:global(:root:not(.theme-warm))`

- [ ] **Step 2: Commit**

```bash
git add src/components/stats/WeeklyChart.vue
git commit -m "fix: update WeeklyChart dark rules for three-theme system"
```

---

### Task 8: Final Polish and Verify

**Files:**
- All modified files

- [ ] **Step 1: Run the dev server**

```bash
npm run dev
```

- [ ] **Step 2: Test all three themes**

Open the app, go to Stats → Theme selector. Click each circle and verify:
- Dusk: purple-green gradient background, purple accents, floating nav
- Warm Cloud: warm brown background, glass cards, floating nav
- Ink & Amber: dark background, gold accents, floating nav

- [ ] **Step 3: Test all pages in each theme**

Check: list page, article detail, player (LoopBar), practice/quiz, stats, kana grid, mastered list.

- [ ] **Step 4: Test mobile and desktop viewports**

- Mobile (375px): floating island nav, safe area spacing
- Desktop (>768px): sidebar nav, content centered

- [ ] **Step 5: Check for any remaining emoji**

```bash
grep -rn '[🔊✏️👂🤪📖💬🇯🇵🇬🇧💡]' src/ --include='*.vue' --include='*.ts'
```

Fix any remaining occurrences.

- [ ] **Step 6: Run build to verify no errors**

```bash
npm run build
```

- [ ] **Step 7: Final commit**

```bash
git add -A
git commit -m "fix: final polish for three-theme visual redesign"
```
