<script setup lang="ts">
/**
 * 通用面板骨架屏（用于 Practice / Stats 等异步组件加载中）
 */
import SkeletonPulse from './SkeletonPulse.vue'
</script>

<template>
  <div class="space-y-4 pt-2">
    <SkeletonPulse class="h-6 w-40 rounded" />
    <div class="rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-5 space-y-4">
      <SkeletonPulse class="h-5 w-3/4 rounded" />
      <SkeletonPulse class="h-4 w-1/2 rounded" />
      <SkeletonPulse class="h-4 w-2/3 rounded" />
    </div>
    <div class="rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-5 space-y-4">
      <SkeletonPulse class="h-5 w-1/3 rounded" />
      <SkeletonPulse class="h-20 w-full rounded-xl" />
    </div>
  </div>
</template>
