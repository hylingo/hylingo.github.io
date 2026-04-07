<script setup lang="ts">
import { ref } from 'vue'
import { useFirebase } from '../../composables/useFirebase'
import { useLang } from '@/i18n'

const { t } = useLang()

defineProps<{ visible: boolean }>()
const emit = defineEmits<{ close: [] }>()

const { register, login } = useFirebase()

const tab = ref<'login' | 'register'>('login')
const username = ref('')
const password = ref('')
const message = ref('')
const isError = ref(false)
const loading = ref(false)
const showPwd = ref(false)

function reset() {
  username.value = ''
  password.value = ''
  message.value = ''
  isError.value = false
}

function switchTab(t: 'login' | 'register') {
  tab.value = t
  reset()
}

async function onSubmit() {
  if (loading.value) return
  loading.value = true
  message.value = ''

  const fn = tab.value === 'register' ? register : login
  const result = await fn(username.value, password.value)
  message.value = result.message
  isError.value = !result.success
  loading.value = false

  if (result.success) {
    setTimeout(() => {
      emit('close')
      window.location.reload()
    }, 1000)
  }
}
</script>

<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-[9999] flex items-center justify-center"
    style="background: var(--overlay-scrim); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);"
  >
    <div class="theme-card rounded-2xl p-8 w-[90%] max-w-sm" style="box-shadow: var(--shadow-lg); background: color-mix(in srgb, var(--card) 92%, transparent); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
      <!-- Tabs -->
      <div class="flex mb-6 border-b" style="border-color: var(--border)">
        <button
          class="flex-1 pb-2 text-sm font-semibold border-b-2 transition-colors cursor-pointer bg-transparent"
          :style="tab === 'login' ? 'border-color: var(--primary); color: var(--primary)' : 'border-color: transparent; color: var(--text-secondary)'"
          @click="switchTab('login')"
        >{{ t('loginTab') }}</button>
        <button
          class="flex-1 pb-2 text-sm font-semibold border-b-2 transition-colors cursor-pointer bg-transparent"
          :style="tab === 'register' ? 'border-color: var(--primary); color: var(--primary)' : 'border-color: transparent; color: var(--text-secondary)'"
          @click="switchTab('register')"
        >{{ t('registerTab') }}</button>
      </div>

      <p class="text-sm mb-4 text-center" style="color: var(--text-secondary)">
        {{ tab === 'register' ? t('registerDesc') : t('loginDescShort') }}
      </p>

      <input
        v-model="username"
        class="w-full px-4 py-3 border rounded-xl text-base outline-none transition-colors"
        style="border-color: var(--border); color: var(--text); background: var(--card);"
        :placeholder="t('usernamePlaceholder')"
        maxlength="30"
        autocomplete="username"
        @keyup.enter="onSubmit"
      />

      <div class="relative mt-3">
        <input
          v-model="password"
          :type="showPwd ? 'text' : 'password'"
          class="w-full px-4 py-3 pr-12 border rounded-xl text-base outline-none transition-colors"
          style="border-color: var(--border); color: var(--text); background: var(--card);"
          :placeholder="tab === 'register' ? t('passwordPlaceholder') : t('passwordInput')"
          maxlength="50"
          autocomplete="current-password"
          @keyup.enter="onSubmit"
        />
        <button
          type="button"
          class="absolute right-3 top-1/2 -translate-y-1/2 bg-transparent border-none cursor-pointer transition-colors"
          style="color: var(--text-secondary)"
          @click="showPwd = !showPwd"
        >
          <svg v-if="showPwd" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/><path d="M14.12 14.12a3 3 0 11-4.24-4.24"/></svg>
        </button>
      </div>

      <button
        class="w-full mt-4 py-3 rounded-xl text-white font-semibold text-base cursor-pointer transition-colors disabled:opacity-50 btn-grad-primary btn-grad-primary--borderless"
        :disabled="loading || !username.trim() || !password"
        @click="onSubmit"
      >
        {{ loading ? t('loginConnecting') : (tab === 'register' ? t('registerBtn') : t('loginBtn2')) }}
      </button>

      <div
        v-if="message"
        class="mt-3 text-sm text-center"
        :class="isError ? 'text-red-500' : 'text-green-600'"
      >
        {{ message }}
      </div>

      <button
        class="w-full mt-3 border-none bg-transparent text-[13px] cursor-pointer underline"
        style="color: var(--text-secondary)"
        @click="emit('close')"
      >
        {{ t('cancel') }}
      </button>
    </div>
  </div>
</template>
