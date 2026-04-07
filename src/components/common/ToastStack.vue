<script setup lang="ts">
import { useToasts } from '@/composables/useToasts'

const { toasts, dismiss } = useToasts()

function onAction(id: number, fn?: () => void) {
  fn?.()
  dismiss(id)
}
</script>

<template>
  <div
    class="pointer-events-none fixed left-1/2 z-[400] flex w-[min(92vw,420px)] -translate-x-1/2 flex-col gap-2"
    :style="`top: calc(env(safe-area-inset-top, 0px) + 12px);`"
    role="region"
    aria-live="polite"
    aria-label="notifications"
  >
    <transition-group name="toast" tag="div" class="flex flex-col gap-2">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="pointer-events-auto flex items-center gap-3 rounded-xl px-4 py-3 text-sm shadow-lg backdrop-blur"
        :class="
          t.kind === 'error'
            ? 'bg-[color-mix(in_srgb,#ef4444_92%,transparent)] text-white'
            : 'bg-[color-mix(in_srgb,var(--card)_94%,transparent)] text-[var(--text)] border border-[var(--border)]'
        "
        role="alert"
      >
        <span class="min-w-0 flex-1 break-words">{{ t.message }}</span>
        <button
          v-if="t.actionLabel"
          type="button"
          class="shrink-0 rounded-md px-2 py-1 text-xs font-semibold underline-offset-2 hover:underline cursor-pointer bg-transparent border-none text-inherit"
          @click="onAction(t.id, t.onAction)"
        >
          {{ t.actionLabel }}
        </button>
        <button
          type="button"
          class="shrink-0 inline-flex h-6 w-6 items-center justify-center rounded-full bg-transparent border-none cursor-pointer text-inherit opacity-80 hover:opacity-100"
          aria-label="close"
          @click="dismiss(t.id)"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="h-3.5 w-3.5">
            <path d="M6 6l12 12M18 6L6 18" stroke-linecap="round" />
          </svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
