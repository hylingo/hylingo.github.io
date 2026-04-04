<script setup lang="ts">
import AppNav from './AppNav.vue'
</script>

<template>
  <div class="flex min-h-screen">
    <AppNav />
    <div class="flex-1 min-w-0 pb-20 md:ml-[200px] md:pb-10">
      <slot />
    </div>
  </div>
</template>
