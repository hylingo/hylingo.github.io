<script setup lang="ts">
import { useFirebase } from '@/composables/useFirebase'
import { useAppStore } from '@/stores/app'

const { userId } = useFirebase()
const store = useAppStore()
</script>

<template>
  <header
    class="sticky top-0 z-[400] px-6 py-2.5 md:px-10 md:py-3 theme-header flex items-center justify-between gap-4"
    style="box-shadow: 0 4px 20px rgba(0,0,0,0.22)"
  >
    <h1 class="text-[22px] font-bold tracking-wider leading-none flex items-center shrink-0 min-w-0">
      <template v-if="store.studyLang === 'ja'">
        <ruby style="ruby-position: over">
          日本語学習
          <rp>(</rp>
          <rt class="text-[10px] font-normal tracking-[2px] opacity-90 leading-tight">にほんご がくしゅう</rt>
          <rp>)</rp>
        </ruby>
      </template>
      <span v-else class="tracking-wide">English Study</span>
    </h1>
    <span
      v-if="userId"
      class="bg-white/25 px-3 py-1 rounded-xl text-xs tracking-wide shrink-0"
    >
      {{ userId }}
    </span>
  </header>
</template>
