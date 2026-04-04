<script setup lang="ts">
import { ref } from 'vue'
import ProfileSection from './ProfileSection.vue'
import StatsGrid from './StatsGrid.vue'
import WeeklyChart from './WeeklyChart.vue'
import MasteredList from './MasteredList.vue'
import LoginOverlay from '../auth/LoginOverlay.vue'
import { useFirebase } from '../../composables/useFirebase'
import { clearAllLearnProgressLocal } from '@/learning/learnStorage'
import { useLang } from '@/i18n'
import { useTheme } from '@/composables/useTheme'
import { useAppStore } from '@/stores/app'

const { t, currentLang, switchLang } = useLang()
const store = useAppStore()

const studyLangs = [
  { key: 'ja' as const, icon: '🇯🇵', label: '日本語' },
  { key: 'en' as const, icon: '🇬🇧', label: 'English' },
]

const uiLangs = [
  { key: 'zh' as const, label: '中' },
  { key: 'en' as const, label: 'EN' },
  { key: 'ja' as const, label: 'JP' },
]
const showMasteredList = ref(false)
const { flushDataToCloud } = useFirebase()
const { themeMode, toggleTheme } = useTheme()
const showLogin = ref(false)
const confirmStep = ref<0 | 1 | 2>(0)

function openResetConfirm() {
  confirmStep.value = 1
}

function closeResetConfirm() {
  confirmStep.value = 0
}

function onConfirmReset() {
  if (confirmStep.value === 1) {
    confirmStep.value = 2
    return
  }

  clearAllLearnProgressLocal()
  flushDataToCloud()
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
    <div class="theme-card mt-4 p-4 flex items-center justify-between">
      <div>
        <div class="text-sm font-semibold">学习语言</div>
        <div class="text-xs opacity-75">{{ store.studyLang === 'ja' ? '🇯🇵 日本語' : '🇬🇧 English' }}</div>
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
        <div class="text-sm font-semibold">{{ t('darkMode') }}</div>
        <div class="text-xs opacity-75">{{ themeMode === 'dark' ? t('darkModeOn') : t('darkModeOff') }}</div>
      </div>
      <button
        class="theme-switch"
        :class="{ 'theme-switch--on': themeMode === 'dark' }"
        @click="toggleTheme"
        :aria-label="t('darkMode')"
      >
        <span class="theme-switch__thumb" />
      </button>
    </div>
    <ProfileSection @login="showLogin = true" />
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
  </div>
</template>
