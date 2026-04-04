<script setup lang="ts">
import { computed } from 'vue'
import type { VocabItem } from '../../types'
import type { QuizMode } from '../../composables/useQuiz'
import { useLang, currentLang } from '@/i18n'
import { localMeaning, localExampleCn } from '@/utils/helpers'
import RubyText from '@/components/common/RubyText.vue'

const { t } = useLang()
const lang = computed(() => currentLang.value)

defineProps<{
  item: VocabItem | null
  isAnswered: boolean
  mode: QuizMode
}>()

defineEmits<{
  speak: []
  cardClick: []
}>()
</script>

<template>
  <div
    class="w-full max-w-[400px] mx-auto rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.10)] theme-surface p-10 text-center animate-fadeUp"
    :class="isAnswered ? 'cursor-pointer active:scale-[0.98]' : ''"
    @click="isAnswered && $emit('cardClick')"
  >
    <!-- MODE: word (original) — show Japanese word, recall meaning + reading -->
    <template v-if="mode === 'word'">
      <div class="text-3xl font-bold theme-text mb-4 leading-relaxed">
        <template v-if="item?.tokens && item.tokens.length">
          <span
            v-for="(tk, i) in item.tokens"
            :key="i"
            class="inline-block border-b border-[#e8735a]/15"
            :class="i > 0 ? 'ml-[5px]' : ''"
          >{{ tk }}</span>
        </template>
        <template v-else>{{ item?.word ?? '' }}</template>
      </div>
      <div v-if="!isAnswered" class="text-sm theme-muted">
        <span>{{ t('quizHintWord') }}</span>
      </div>
    </template>

    <!-- MODE: audio — play audio only, recall word + meaning -->
    <template v-if="mode === 'audio'">
      <div v-if="!isAnswered" class="flex flex-col items-center gap-4">
        <button
          class="w-20 h-20 rounded-full border-2 text-3xl cursor-pointer transition-all active:scale-95"
          style="border-color: var(--primary); background: var(--primary-light)"
          @click.stop="$emit('speak')"
        >🔊</button>
        <span class="text-sm theme-muted">{{ t('quizHintAudio') }}</span>
      </div>
    </template>

    <!-- MODE: meaning — show Chinese meaning, recall Japanese word + reading -->
    <template v-if="mode === 'meaning'">
      <div v-if="!isAnswered">
        <div class="text-2xl font-bold mb-3" style="color: var(--accent)">{{ item ? localMeaning(item, lang) : '' }}</div>
        <div class="text-sm theme-muted">{{ t('quizHintMeaning') }}</div>
      </div>
    </template>

    <!-- ANSWER (all modes) -->
    <template v-if="isAnswered && item">
      <div v-if="mode !== 'word'" class="text-3xl font-bold theme-text mb-2 leading-relaxed">
        <RubyText v-if="item.ruby" :tokens="item.ruby" />
        <template v-else>{{ item.word }}</template>
      </div>
      <div class="text-xl font-bold theme-text mb-4">{{ localMeaning(item, lang) }}</div>
      <div v-if="item.example" class="text-sm theme-muted leading-relaxed">
        {{ item.example }}
        <br v-if="localExampleCn(item, lang)" />
        <span v-if="localExampleCn(item, lang)" class="text-[13px]" style="color: var(--accent)">{{ localExampleCn(item, lang) }}</span>
      </div>
    </template>
  </div>
</template>
