<script setup lang="ts">
import { icons } from '@/icons'

const props = defineProps<{
  name: string
  size?: number | string
}>()
</script>

<template>
  <svg
    v-if="icons[name]"
    :viewBox="icons[name][0]"
    :width="size ?? 20"
    :height="size ?? 20"
    aria-hidden="true"
    v-html="icons[name][1]"
  />
</template>
