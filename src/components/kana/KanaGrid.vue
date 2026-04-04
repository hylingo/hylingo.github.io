<script setup lang="ts">
import { ref } from 'vue'
import { speak } from '@/composables/useAudio'

interface KanaChar {
  kana: string
  romaji: string
}

interface KanaRow {
  label: string
  chars: (KanaChar | null)[]
}

const activeKana = ref('')

const hiragana: KanaRow[] = [
  { label: 'あ', chars: [{ kana: 'あ', romaji: 'a' }, { kana: 'い', romaji: 'i' }, { kana: 'う', romaji: 'u' }, { kana: 'え', romaji: 'e' }, { kana: 'お', romaji: 'o' }] },
  { label: 'か', chars: [{ kana: 'か', romaji: 'ka' }, { kana: 'き', romaji: 'ki' }, { kana: 'く', romaji: 'ku' }, { kana: 'け', romaji: 'ke' }, { kana: 'こ', romaji: 'ko' }] },
  { label: 'さ', chars: [{ kana: 'さ', romaji: 'sa' }, { kana: 'し', romaji: 'shi' }, { kana: 'す', romaji: 'su' }, { kana: 'せ', romaji: 'se' }, { kana: 'そ', romaji: 'so' }] },
  { label: 'た', chars: [{ kana: 'た', romaji: 'ta' }, { kana: 'ち', romaji: 'chi' }, { kana: 'つ', romaji: 'tsu' }, { kana: 'て', romaji: 'te' }, { kana: 'と', romaji: 'to' }] },
  { label: 'な', chars: [{ kana: 'な', romaji: 'na' }, { kana: 'に', romaji: 'ni' }, { kana: 'ぬ', romaji: 'nu' }, { kana: 'ね', romaji: 'ne' }, { kana: 'の', romaji: 'no' }] },
  { label: 'は', chars: [{ kana: 'は', romaji: 'ha' }, { kana: 'ひ', romaji: 'hi' }, { kana: 'ふ', romaji: 'fu' }, { kana: 'ほ', romaji: 'ho' }, { kana: 'へ', romaji: 'he' }] },
  { label: 'ま', chars: [{ kana: 'ま', romaji: 'ma' }, { kana: 'み', romaji: 'mi' }, { kana: 'む', romaji: 'mu' }, { kana: 'め', romaji: 'me' }, { kana: 'も', romaji: 'mo' }] },
  { label: 'や', chars: [{ kana: 'や', romaji: 'ya' }, null, { kana: 'ゆ', romaji: 'yu' }, null, { kana: 'よ', romaji: 'yo' }] },
  { label: 'ら', chars: [{ kana: 'ら', romaji: 'ra' }, { kana: 'り', romaji: 'ri' }, { kana: 'る', romaji: 'ru' }, { kana: 'れ', romaji: 're' }, { kana: 'ろ', romaji: 'ro' }] },
  { label: 'わ', chars: [{ kana: 'わ', romaji: 'wa' }, null, null, null, { kana: 'を', romaji: 'wo' }] },
  { label: 'ん', chars: [{ kana: 'ん', romaji: 'n' }, null, null, null, null] },
]

const katakana: KanaRow[] = [
  { label: 'ア', chars: [{ kana: 'ア', romaji: 'a' }, { kana: 'イ', romaji: 'i' }, { kana: 'ウ', romaji: 'u' }, { kana: 'エ', romaji: 'e' }, { kana: 'オ', romaji: 'o' }] },
  { label: 'カ', chars: [{ kana: 'カ', romaji: 'ka' }, { kana: 'キ', romaji: 'ki' }, { kana: 'ク', romaji: 'ku' }, { kana: 'ケ', romaji: 'ke' }, { kana: 'コ', romaji: 'ko' }] },
  { label: 'サ', chars: [{ kana: 'サ', romaji: 'sa' }, { kana: 'シ', romaji: 'shi' }, { kana: 'ス', romaji: 'su' }, { kana: 'セ', romaji: 'se' }, { kana: 'ソ', romaji: 'so' }] },
  { label: 'タ', chars: [{ kana: 'タ', romaji: 'ta' }, { kana: 'チ', romaji: 'chi' }, { kana: 'ツ', romaji: 'tsu' }, { kana: 'テ', romaji: 'te' }, { kana: 'ト', romaji: 'to' }] },
  { label: 'ナ', chars: [{ kana: 'ナ', romaji: 'na' }, { kana: 'ニ', romaji: 'ni' }, { kana: 'ヌ', romaji: 'nu' }, { kana: 'ネ', romaji: 'ne' }, { kana: 'ノ', romaji: 'no' }] },
  { label: 'ハ', chars: [{ kana: 'ハ', romaji: 'ha' }, { kana: 'ヒ', romaji: 'hi' }, { kana: 'フ', romaji: 'fu' }, { kana: 'ホ', romaji: 'ho' }, { kana: 'ヘ', romaji: 'he' }] },
  { label: 'マ', chars: [{ kana: 'マ', romaji: 'ma' }, { kana: 'ミ', romaji: 'mi' }, { kana: 'ム', romaji: 'mu' }, { kana: 'メ', romaji: 'me' }, { kana: 'モ', romaji: 'mo' }] },
  { label: 'ヤ', chars: [{ kana: 'ヤ', romaji: 'ya' }, null, { kana: 'ユ', romaji: 'yu' }, null, { kana: 'ヨ', romaji: 'yo' }] },
  { label: 'ラ', chars: [{ kana: 'ラ', romaji: 'ra' }, { kana: 'リ', romaji: 'ri' }, { kana: 'ル', romaji: 'ru' }, { kana: 'レ', romaji: 're' }, { kana: 'ロ', romaji: 'ro' }] },
  { label: 'ワ', chars: [{ kana: 'ワ', romaji: 'wa' }, null, null, null, { kana: 'ヲ', romaji: 'wo' }] },
  { label: 'ン', chars: [{ kana: 'ン', romaji: 'n' }, null, null, null, null] },
]

const tab = ref<'hiragana' | 'katakana'>('hiragana')

function playKana(kana: string) {
  activeKana.value = kana
  speak(kana)
  setTimeout(() => { activeKana.value = '' }, 800)
}

const currentRows = () => tab.value === 'hiragana' ? hiragana : katakana
</script>

<template>
  <div class="px-4 pt-2 pb-5 md:px-10 md:max-w-[600px]">
    <!-- Hiragana / Katakana toggle -->
    <div class="flex justify-center gap-2 mb-4">
      <button
        class="px-5 py-[7px] rounded-full text-[13px] font-medium cursor-pointer transition-all duration-300"
        :class="tab === 'hiragana' ? 'border-2 kana-tab-pill--active' : 'border-2 border-[var(--border)] bg-transparent theme-muted'"
        @click="tab = 'hiragana'"
      >平仮名</button>
      <button
        class="px-5 py-[7px] rounded-full text-[13px] font-medium cursor-pointer transition-all duration-300"
        :class="tab === 'katakana' ? 'border-2 kana-tab-pill--active' : 'border-2 border-[var(--border)] bg-transparent theme-muted'"
        @click="tab = 'katakana'"
      >片仮名</button>
    </div>

    <!-- Grid -->
    <div class="space-y-1">
      <div
        v-for="row in currentRows()"
        :key="row.label"
        class="grid grid-cols-5 gap-1"
      >
        <template v-for="(ch, i) in row.chars" :key="i">
          <button
            v-if="ch"
            class="aspect-square rounded-xl flex flex-col items-center justify-center cursor-pointer transition-all duration-150 active:scale-95"
            :class="activeKana === ch.kana
              ? 'btn-grad-primary btn-grad-primary--borderless text-white shadow-md'
              : 'kana-cell theme-text'"
            @click="playKana(ch.kana)"
          >
            <span class="text-2xl font-bold leading-none">{{ ch.kana }}</span>
            <span
              class="text-[11px] mt-1"
              :class="activeKana === ch.kana ? 'text-white/85' : ''"
              :style="activeKana === ch.kana ? '' : 'color: var(--primary)'"
            >{{ ch.romaji }}</span>
          </button>
          <div v-else class="aspect-square" />
        </template>
      </div>
    </div>
  </div>
</template>
