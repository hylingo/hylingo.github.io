<script setup lang="ts">
import SkeletonPulse from './SkeletonPulse.vue'
</script>

<template>
  <div class="px-4 pb-24 md:px-10 md:max-w-[720px] md:mx-auto space-y-3 pt-1">
    <!-- search bar -->
    <SkeletonPulse class="h-10 w-full rounded-xl" />
    <!-- intro text -->
    <SkeletonPulse class="h-4 w-48 rounded" />
    <!-- article cards -->
    <div
      v-for="i in 6"
      :key="i"
      class="rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-4 pl-5 border-0 border-l-[3px] border-l-[var(--border)]"
    >
      <SkeletonPulse class="h-3 w-20 rounded mb-2" />
      <SkeletonPulse class="h-5 rounded mb-1.5" :style="{ width: 140 + (i % 3) * 50 + 'px' }" />
      <SkeletonPulse class="h-4 rounded" :style="{ width: 100 + (i % 2) * 60 + 'px' }" />
    </div>
  </div>
</template>
