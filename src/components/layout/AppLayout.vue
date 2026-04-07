<script setup lang="ts">
import AppNav from './AppNav.vue'
</script>

<template>
  <div class="flex min-h-[100dvh]">
    <AppNav />
    <div class="flex-1 min-w-0 pb-[6.5rem] md:ml-[200px] md:pb-10">
      <slot />
    </div>
  </div>
</template>
