<script setup lang="ts">
defineProps<{
  emoji: string
  label: string
  color: string
}>()
</script>

<template>
  <div class="col-span-2 rounded-xl p-4 text-center theme-card">
    <div class="text-3xl">{{ emoji }}</div>
    <div class="text-sm mt-1" :style="{ color }">{{ label }}</div>
  </div>
</template>
