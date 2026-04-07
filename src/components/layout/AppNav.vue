<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'
import AppIcon from '@/components/common/AppIcon.vue'

const store = useAppStore()
const { t } = useLang()

const navItems = [
  { mode: 'list', icon: 'listen', key: 'tabList' },
  { mode: 'practice', icon: 'practice', key: 'tabPractice' },
  { mode: 'stats', icon: 'profile', key: 'tabStats' },
] as const
</script>

<template>
  <!-- Mobile: floating island bottom bar -->
  <nav
    class="md:hidden fixed z-[200] left-[20px] right-[20px] theme-nav-mobile rounded-[20px]"
    :style="`bottom: calc(env(safe-area-inset-bottom, 0px) + 4px); box-shadow: 0 4px 24px rgba(0,0,0,0.12);`"
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
        <AppIcon :name="item.icon" :size="20" />
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
