<script setup lang="ts">
import SkeletonPulse from './SkeletonPulse.vue'
</script>

<template>
  <div class="px-4 md:px-10">
    <!-- toolbar skeleton -->
    <div class="pb-3 md:pb-4">
      <SkeletonPulse class="h-10 w-full rounded-xl" />
    </div>
    <!-- card skeletons -->
    <div class="space-y-2">
      <div
        v-for="i in 8"
        :key="i"
        class="rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-4"
      >
        <div class="flex items-center gap-3">
          <SkeletonPulse class="h-4 w-10 rounded-full" />
          <SkeletonPulse class="h-5 rounded" :style="{ width: 60 + (i % 3) * 30 + 'px' }" />
          <div class="flex-1" />
          <SkeletonPulse class="h-4 rounded" :style="{ width: 80 + (i % 2) * 40 + 'px' }" />
        </div>
      </div>
    </div>
  </div>
</template>
