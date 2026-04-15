<script setup lang="ts">
import { ref } from 'vue'
import StatsGrid from './StatsGrid.vue'
import WeeklyChart from './WeeklyChart.vue'
import MasteredList from './MasteredList.vue'
import LoginOverlay from '../auth/LoginOverlay.vue'
import { useFirebase } from '../../composables/useFirebase'
import { clearAllLearnProgressLocal } from '@/learning/learnStorage'
import { useLang } from '@/i18n'
import { useTheme } from '@/composables/useTheme'
import { useAppStore } from '@/stores/app'
import { APP_VERSION } from '@/version'

const { t, currentLang, switchLang } = useLang()
const store = useAppStore()

const studyLangs = [
  { key: 'ja' as const, icon: 'JP', label: '日本語' },
  { key: 'en' as const, icon: 'EN', label: 'English' },
]

const uiLangs = [
  { key: 'zh' as const, label: '中' },
  { key: 'en' as const, label: 'EN' },
  { key: 'ja' as const, label: 'JP' },
]
const showMasteredList = ref(false)
const { userId, logout, flushDataToCloud } = useFirebase()

function handleLogout() {
  logout()
  window.location.reload()
}
const { themeMode, setTheme, ALL_THEMES } = useTheme()
const showLogin = ref(false)
const confirmStep = ref<0 | 1 | 2>(0)

function openResetConfirm() {
  confirmStep.value = 1
}

function closeResetConfirm() {
  confirmStep.value = 0
}

async function onConfirmReset() {
  if (confirmStep.value === 1) {
    confirmStep.value = 2
    return
  }

  clearAllLearnProgressLocal()
  await flushDataToCloud()
  confirmStep.value = 0
  window.location.reload()
}

function resetStats() {
  openResetConfirm()
}
</script>

<template>
  <div class="pb-8">
    <MasteredList v-if="showMasteredList" @back="showMasteredList = false" />
    <template v-else>
    <!-- 账户信息（合并到设置区） -->
    <div v-if="!userId" class="theme-card mt-4 p-4 flex items-center justify-between">
      <div>
        <div class="text-sm font-semibold">{{ t('syncBanner') }}</div>
      </div>
      <button
        class="px-4 py-1.5 rounded-full text-white text-xs font-semibold cursor-pointer btn-grad-primary btn-grad-primary--borderless"
        @click="showLogin = true"
      >{{ t('registerOrLogin') }}</button>
    </div>
    <div v-else class="theme-card mt-4 p-4 flex items-center justify-between">
      <div class="flex items-center gap-3 min-w-0">
        <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0" style="background: var(--grad-primary)">
          {{ userId.slice(0, 1).toUpperCase() }}
        </div>
        <div class="min-w-0">
          <div class="text-sm font-semibold truncate">{{ userId }}</div>
          <div class="text-[11px]" style="color: var(--text-secondary)">{{ t('syncEnabled') }}</div>
        </div>
      </div>
      <button
        type="button"
        class="px-3 py-1.5 rounded-lg border text-xs cursor-pointer"
        style="border-color: var(--border); color: var(--text-secondary)"
        @click="handleLogout"
      >{{ t('logoutBtn') }}</button>
    </div>

    <div class="theme-card mt-4 p-4 flex items-center justify-between">
      <div>
        <div class="text-sm font-semibold">学习语言</div>
        <div class="text-xs opacity-75">{{ store.studyLang === 'ja' ? 'JP 日本語' : 'EN English' }}</div>
      </div>
      <div class="study-lang-toggle">
        <button
          v-for="sl in studyLangs"
          :key="sl.key"
          type="button"
          class="study-lang-toggle-btn"
          :class="{ 'study-lang-toggle-btn--active': store.studyLang === sl.key }"
          @click="store.switchStudyLang(sl.key)"
        >
          {{ sl.icon }}
        </button>
      </div>
    </div>

    <div class="theme-card mt-4 p-4 flex items-center justify-between">
      <div>
        <div class="text-sm font-semibold">界面语言</div>
        <div class="text-xs opacity-75">{{ currentLang === 'zh' ? '中文' : currentLang === 'ja' ? '日本語' : 'English' }}</div>
      </div>
      <div class="study-lang-toggle">
        <button
          v-for="ul in uiLangs"
          :key="ul.key"
          type="button"
          class="study-lang-toggle-btn study-lang-toggle-btn--text"
          :class="{ 'study-lang-toggle-btn--active': currentLang === ul.key }"
          @click="switchLang(ul.key)"
        >
          {{ ul.label }}
        </button>
      </div>
    </div>

    <div class="theme-card mt-4 p-4 flex items-center justify-between">
      <div>
        <div class="text-sm font-semibold">皮肤</div>
        <div class="text-xs opacity-75">{{ themeMode === 'dusk' ? '暮色' : themeMode === 'watercolor' ? '水彩' : '墨金' }}</div>
      </div>
      <div class="flex gap-3">
        <button
          v-for="tm in ALL_THEMES"
          :key="tm"
          type="button"
          class="w-[36px] h-[36px] cursor-pointer transition-all shrink-0 border-0 p-0"
          :style="`
            border-radius: 50%;
            background: ${tm === 'dusk'
              ? 'linear-gradient(135deg,#2a1f3d 0%,#1a2235 35%,#1c2a30 70%,#c8a8e8 100%)'
              : tm === 'watercolor'
                ? 'linear-gradient(135deg,#f5c0c8 0%,#ffe4b8 35%,#c5e4f0 70%,#d8c5e8 100%)'
                : 'linear-gradient(135deg,#141518 0%,#18191e 55%,#dcb478 100%)'};
            outline: 2px solid ${themeMode === tm ? 'var(--primary)' : 'transparent'};
            outline-offset: 2px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transform: ${themeMode === tm ? 'scale(1.08)' : 'scale(1)'};
          `"
          @click="setTheme(tm)"
          :aria-label="tm"
        />
      </div>
    </div>

    <StatsGrid @mastered="showMasteredList = true" />
    <WeeklyChart />

    <button
      type="button"
      class="btn-soft-danger"
      @click="resetStats"
    >
      {{ t('resetBtn2') }}
    </button>

    <LoginOverlay :visible="showLogin" @close="showLogin = false" />

    <div
      v-if="confirmStep > 0"
      class="fixed inset-0 z-[9998] flex items-center justify-center bg-black/35 backdrop-blur-[2px]"
      @click.self="closeResetConfirm"
    >
      <div class="w-[90%] max-w-md rounded-2xl theme-card p-5 shadow-[0_18px_40px_rgba(0,0,0,0.2)]">
        <div class="mb-3 flex items-center gap-2">
          <span class="inline-flex h-7 w-7 items-center justify-center rounded-full text-[#8a4a48] theme-soft" style="border: 1px solid color-mix(in srgb, #7a4444 25%, var(--border))">!</span>
          <h3 class="text-[15px] font-semibold theme-text">{{ t('resetBtn2') }}</h3>
        </div>

        <p class="whitespace-pre-line text-sm leading-6 theme-muted">
          {{ confirmStep === 1 ? t('resetConfirm1') : t('resetConfirm2') }}
        </p>

        <div class="mt-4 flex items-center justify-end gap-2">
          <button
            type="button"
            class="px-4 py-2 rounded-lg border border-[var(--border)] theme-muted text-sm theme-surface cursor-pointer hover:opacity-90"
            @click="closeResetConfirm"
          >
            {{ t('cancel') }}
          </button>
          <button
            type="button"
            class="btn-soft-danger-solid"
            @click="onConfirmReset"
          >
            {{ t('confirm') }}
          </button>
        </div>
      </div>
    </div>
    </template>
    <div class="text-center text-[11px] text-[var(--text-secondary)] opacity-50 mt-6 pb-2 select-none">v{{ APP_VERSION }}</div>
  </div>
</template>
