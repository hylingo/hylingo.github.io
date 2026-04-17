<script setup lang="ts">
import type { RubyToken } from '@/types'

defineProps<{
  tokens: RubyToken[]
}>()
</script>

<template>
  <span class="ruby-text">
    <template v-for="(tk, i) in tokens" :key="i">
      <ruby v-if="tk.r">
        {{ tk.t }}<rp>(</rp><rt>{{ tk.r }}</rt><rp>)</rp>
      </ruby>
      <span v-else>{{ tk.t }}</span>
    </template>
  </span>
</template>

<style scoped>
.ruby-text {
  line-height: 1.9;
  word-spacing: 0.15em;
}
.ruby-text ruby {
  ruby-align: center;
  margin-right: 0.12em;
}
.ruby-text > span {
  margin-right: 0.06em;
}
.ruby-text rt {
  font-size: 0.55em;
  font-weight: normal;
  color: var(--content-ruby, var(--text-secondary));
  letter-spacing: 0.02em;
}
</style>
