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
  <div class="flex flex-col gap-2 px-4 pb-3 md:px-10">
    <div class="relative">
      <input
        v-model="searchQuery"
        type="text"
        :placeholder="t('search')"
        class="w-full pl-10 pr-4 py-2.5 rounded-[10px] border border-[#e8e2dc] theme-surface text-sm outline-none focus:border-[#e8735a] transition-colors"
        @input="onSearch"
      />
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 theme-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
      </svg>
    </div>
    <div class="w-full flex flex-col gap-2">
      <div class="flex flex-wrap items-center gap-2">
        <button
          v-if="!isSpeaking"
          type="button"
          class="inline-flex items-center justify-center gap-2 min-h-[44px] px-4 py-2 rounded-xl text-sm font-semibold border-2 transition-all shadow-[0_2px_10px_rgba(0,0,0,0.06)]"
          :class="
            totalItems < 1
              ? 'opacity-40 cursor-not-allowed border-[var(--border)] theme-muted'
              : enableListSpeakSequenceRange && canUseRange && showRange
                ? 'bg-[#e8735a]/15 border-[#e8735a]/45 text-[#c45a3e] cursor-pointer'
                : 'border-[#e8e2dc] theme-surface theme-text hover:border-[#e8735a]/50 hover:shadow-[0_4px_14px_rgba(232,115,90,0.12)] cursor-pointer'
          "
          :disabled="totalItems < 1"
          @click="onToggleSpeak"
        >
          <svg class="w-5 h-5 shrink-0 text-[#e8735a]" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
          <span>{{ t('listSpeak') }}</span>
        </button>
        <button
          v-else
          type="button"
          class="inline-flex items-center justify-center gap-2 min-h-[44px] px-4 py-2 rounded-xl text-sm font-semibold border-2 transition-all cursor-pointer bg-[#e8735a]/12 border-[#e8735a]/45 text-[#c45a3e] shadow-[0_2px_10px_rgba(232,115,90,0.15)]"
          @click="onToggleSpeak"
        >
          <svg class="w-5 h-5 shrink-0" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 6h12v12H6z"/></svg>
          <span>{{ t('listStop') }}</span>
        </button>
      </div>
      <div
        v-if="enableListSpeakSequenceRange && canUseRange && showRange"
        class="flex flex-col gap-2 px-3 py-2.5 rounded-xl theme-surface border border-[var(--border)]"
      >
        <div class="flex items-center justify-center gap-2">
        <span class="text-[13px] theme-muted whitespace-nowrap">{{ t('from') }}</span>
        <input
          v-model.number="listenFrom"
          type="number"
          min="1"
          :max="totalItems"
          class="w-14 py-1 px-1 border border-[#e8e2dc] rounded-lg text-sm text-center theme-surface outline-none focus:border-[#e8735a]"
        />
        <span class="text-[13px] theme-muted whitespace-nowrap">{{ t('to') }}</span>
        <input
          v-model.number="listenTo"
          type="number"
          min="1"
          :max="totalItems"
          :placeholder="String(totalItems)"
          class="w-14 py-1 px-1 border border-[#e8e2dc] rounded-lg text-sm text-center theme-surface outline-none focus:border-[#e8735a]"
        />
        </div>
        <div class="flex items-center justify-end gap-2">
          <button
            class="px-3 py-1.5 rounded-lg border border-[#e8e2dc] theme-muted text-xs font-medium hover:border-[#d8d2cc]"
            @click="showRange = false"
          >
            {{ t('cancel') }}
          </button>
          <button
            class="px-3 py-1.5 rounded-lg text-white text-xs font-semibold btn-grad-primary btn-grad-primary--borderless"
            @click="onSpeakRange"
          >
            {{ t('confirm') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
