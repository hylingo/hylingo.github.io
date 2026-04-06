<script setup lang="ts">
import { useFirebase } from '../../composables/useFirebase'
import { useLang } from '@/i18n'

const { t } = useLang()
const { userId, logout } = useFirebase()

const emit = defineEmits<{
  login: []
}>()

function handleLogout() {
  logout()
  window.location.reload()
}
</script>

<template>
  <!-- Not logged in: sync banner -->
  <div v-if="!userId" class="theme-card p-4 mt-4 text-center">
    <div class="text-sm text-[#8a7040] mb-2">{{ t('syncBanner') }}</div>
    <button
      class="px-5 py-2 rounded-full text-white text-sm font-semibold cursor-pointer transition-colors btn-grad-primary btn-grad-primary--borderless"
      @click="emit('login')"
    >{{ t('registerOrLogin') }}</button>
  </div>

  <!-- Logged in: account info -->
  <div v-else class="theme-card p-5 text-center mt-4">
    <div class="text-[13px] text-[#777] mb-1">{{ t('loggedInAs') }}</div>
    <div class="text-2xl font-extrabold tracking-widest text-primary">{{ userId }}</div>
    <div class="text-[12px] text-[#aaa] mt-1">{{ t('syncEnabled') }}</div>
    <button
      type="button"
      class="btn-soft-secondary"
      @click="handleLogout"
    >{{ t('logoutBtn') }}</button>
  </div>
</template>
