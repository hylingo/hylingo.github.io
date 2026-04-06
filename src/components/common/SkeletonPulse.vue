<script setup lang="ts">
/**
 * 骨架屏基础脉冲块。通过 class 控制形状和大小。
 * 用法: <SkeletonPulse class="h-4 w-32 rounded" />
 */
</script>

<template>
  <div class="skeleton-pulse" />
</template>

<style scoped>
.skeleton-pulse {
  background: var(--skeleton-base, color-mix(in srgb, var(--text) 6%, transparent));
  border-radius: 6px;
  animation: skeletonShimmer 1.6s ease-in-out infinite;
}

@keyframes skeletonShimmer {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
