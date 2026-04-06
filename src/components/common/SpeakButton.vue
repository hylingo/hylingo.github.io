<script setup lang="ts">
import { useAudio } from '@/composables/useAudio'
import AppIcon from '@/components/common/AppIcon.vue'

const props = defineProps<{
  word: string
  example?: string
}>()

const { speakWithExample } = useAudio()

function handleSpeak() {
  speakWithExample(props.word, props.example)
}
</script>

<template>
  <button
    class="speak-btn shrink-0 w-10 h-10 border-none rounded-full theme-soft text-primary text-lg cursor-pointer transition-all flex items-center justify-center"
    @click.stop="handleSpeak"
  >
    <AppIcon name="volume" :size="16" />
  </button>
</template>
