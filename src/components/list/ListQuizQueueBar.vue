<script setup lang="ts">
import { computed } from 'vue'
import { useLang } from '@/i18n'
import { quizQueueTick, isInQuizQueue, addToQuizQueue } from '@/learning'

const { t } = useLang()

const props = withDefaults(
  defineProps<{
    cat: string
    id: number
    slim?: boolean
  }>(),
  { slim: false },
)

const inQueue = computed(() => {
  quizQueueTick.value
  return isInQuizQueue(props.cat, props.id)
})

function onAdd(e: Event) {
  e.stopPropagation()
  addToQuizQueue(props.cat, props.id)
}
</script>

<template>
  <div
    class="w-full flex flex-col items-center gap-1"
    :class="slim ? 'pt-1' : 'mt-2 pt-2 border-t'"
    style="border-color: var(--border)"
    @click.stop
  >
    <!-- 已在队列：一行小字 -->
    <div
      v-if="inQueue"
      class="inline-flex items-center gap-1 text-[11px] font-medium"
      style="color: var(--accent)"
    >
      <svg
        class="shrink-0 opacity-90"
        width="12"
        height="12"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <path d="M20 6L9 17l-5-5" />
      </svg>
      {{ t('quizQueueReady') }}
    </div>

    <!-- 可加入：小号次要按钮，非全宽，降低误触 -->
    <button
      v-else
      type="button"
      class="quiz-queue-add-btn max-w-full inline-flex items-center gap-0.5 rounded-md border px-2 py-1 text-[11px] font-medium cursor-pointer transition-colors duration-150"
      style="
        border-color: var(--border);
        color: var(--text-secondary);
        background: transparent;
      "
      @click="onAdd"
    >
      <svg
        class="shrink-0 opacity-80"
        width="11"
        height="11"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.5"
        stroke-linecap="round"
        aria-hidden="true"
      >
        <path d="M12 5v14M5 12h14" />
      </svg>
      {{ t('quizQueueAdd') }}
    </button>
  </div>
</template>

<style scoped>
.quiz-queue-add-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-light);
}
.quiz-queue-add-btn:active {
  transform: scale(0.98);
}
</style>
