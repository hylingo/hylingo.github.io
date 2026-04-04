<script setup lang="ts">
import { ref, watch } from 'vue'
import { useLang } from '@/i18n'
import { enableListSpeakSequenceRange } from '@/config/features'

const { t } = useLang()

const props = defineProps<{
  totalItems: number
  isSpeaking: boolean
  canUseRange: boolean
}>()

const emit = defineEmits<{
  search: [query: string]
  speak: [from: number, to: number]
  stop: []
}>()

const searchQuery = ref('')
const listenFrom = ref(1)
const listenTo = ref<number | undefined>(undefined)
const showRange = ref(false)

watch(
  () => props.canUseRange,
  (canUseRange) => {
    if (!canUseRange) showRange.value = false
  }
)

function onSearch() {
  emit('search', searchQuery.value)
}

function onToggleSpeak() {
  if (props.isSpeaking) {
    emit('stop')
    showRange.value = false
  } else if (enableListSpeakSequenceRange && props.canUseRange) {
    showRange.value = !showRange.value
  } else {
    emit('speak', 1, props.totalItems)
  }
}

function onSpeakRange() {
  const rangeMax = Math.max(1, props.totalItems)
  const from = Math.max(1, Math.min(listenFrom.value || 1, rangeMax))
  const to = Math.max(from, Math.min(listenTo.value || rangeMax, rangeMax))
  emit('speak', from, to)
}
</script>

<template>
  <div class="flex flex-col gap-2.5">
    <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-3">
      <div class="relative min-w-0 flex-1">
        <input
          v-model="searchQuery"
          type="text"
          :placeholder="t('search')"
          class="list-toolbar-search theme-text w-full rounded-xl border border-[var(--border)] bg-transparent py-2 pr-3 pl-9 text-sm outline-none transition-[border-color,box-shadow] focus:border-[var(--primary)] focus:shadow-[0_0_0_3px_color-mix(in_srgb,var(--primary)_18%,transparent)]"
          @input="onSearch"
        />
        <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 theme-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
        </svg>
      </div>
      <div class="flex shrink-0 items-center gap-2 self-stretch sm:self-center sm:justify-end">
        <!-- 实心渐变 + 胶囊形：与浅色搜索框区分，明确为「播放」操作而非第二个输入框 -->
        <button
          v-if="!isSpeaking"
          type="button"
          class="list-toolbar-play-btn inline-flex min-h-[36px] flex-1 items-center justify-center gap-1.5 rounded-full px-3 py-1.5 text-[13px] font-semibold transition-[filter,box-shadow,opacity] sm:min-h-[36px] sm:max-w-[min(100%,220px)] sm:flex-none sm:px-4"
          :class="
            totalItems < 1
              ? 'cursor-not-allowed bg-[var(--border)] text-[var(--text-secondary)] opacity-55 shadow-none'
              : enableListSpeakSequenceRange && canUseRange && showRange
                ? 'btn-grad-primary btn-grad-primary--borderless btn-grad-primary--pressed cursor-pointer text-white'
                : 'btn-grad-primary btn-grad-primary--borderless cursor-pointer text-white'
          "
          :disabled="totalItems < 1"
          :aria-label="t('listSpeak')"
          @click="onToggleSpeak"
        >
          <svg
            class="ml-0.5 h-3.5 w-3.5 shrink-0"
            :class="totalItems < 1 ? 'text-[var(--text-secondary)]' : 'text-white'"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          ><path d="M8 5v14l11-7z"/></svg>
          <span class="whitespace-nowrap">{{ t('listSpeak') }}</span>
        </button>
        <button
          v-else
          type="button"
          class="inline-flex min-h-[36px] flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-full border-2 border-[var(--primary)] bg-[var(--card)] px-3 py-1.5 text-[13px] font-semibold text-[var(--primary-dark)] shadow-sm transition-colors hover:bg-[var(--primary-light)] sm:min-h-[36px] sm:max-w-[min(100%,220px)] sm:flex-none sm:px-4"
          :aria-label="t('listStop')"
          @click="onToggleSpeak"
        >
          <svg class="h-3.5 w-3.5 shrink-0 text-[var(--primary-dark)]" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 6h12v12H6z"/></svg>
          <span class="whitespace-nowrap">{{ t('listStop') }}</span>
        </button>
      </div>
    </div>
    <div
      v-if="enableListSpeakSequenceRange && canUseRange && showRange"
      class="theme-surface flex flex-col gap-2 rounded-xl border border-[var(--border)] px-3 py-2.5"
    >
      <div class="flex items-center justify-center gap-2">
        <span class="text-[13px] whitespace-nowrap theme-muted">{{ t('from') }}</span>
        <input
          v-model.number="listenFrom"
          type="number"
          min="1"
          :max="totalItems"
          class="w-14 rounded-lg border border-[var(--border)] px-1 py-1 text-center text-sm theme-surface outline-none focus:border-[var(--primary)]"
        />
        <span class="text-[13px] whitespace-nowrap theme-muted">{{ t('to') }}</span>
        <input
          v-model.number="listenTo"
          type="number"
          min="1"
          :max="totalItems"
          :placeholder="String(totalItems)"
          class="w-14 rounded-lg border border-[var(--border)] px-1 py-1 text-center text-sm theme-surface outline-none focus:border-[var(--primary)]"
        />
      </div>
      <div class="flex items-center justify-end gap-2">
        <button
          class="rounded-lg border border-[var(--border)] px-3 py-1.5 text-xs font-medium theme-muted hover:border-[var(--border)]"
          @click="showRange = false"
        >
          {{ t('cancel') }}
        </button>
        <button
          class="btn-grad-primary btn-grad-primary--borderless rounded-lg px-3 py-1.5 text-xs font-semibold text-white"
          @click="onSpeakRange"
        >
          {{ t('confirm') }}
        </button>
      </div>
    </div>
  </div>
</template>
