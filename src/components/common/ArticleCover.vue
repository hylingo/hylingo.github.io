<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import AppIcon from '@/components/common/AppIcon.vue'

const props = defineProps<{
  articleId: string | null | undefined
  variant?: 'thumb' | 'banner' | 'hero'
  alt?: string
  /** 占位图标名（默认 book） */
  icon?: string
}>()

const store = useAppStore()
const failed = ref(false)

const src = computed(() => {
  if (!props.articleId) return ''
  return `/images/${store.studyLang}/${props.articleId}/cover.webp`
})

watch(src, () => { failed.value = false })
</script>

<template>
  <div
    v-if="articleId"
    class="article-cover"
    :class="[`article-cover--${variant ?? 'thumb'}`, { 'article-cover--placeholder': failed }]"
  >
    <img
      v-show="!failed"
      :src="src"
      :alt="alt ?? ''"
      loading="lazy"
      decoding="async"
      @error="failed = true"
      @load="failed = false"
    />
    <div v-if="failed" class="article-cover__ph">
      <AppIcon :name="icon ?? 'book'" :size="variant === 'thumb' ? 22 : 36" />
    </div>
  </div>
</template>

<style scoped>
.article-cover {
  position: relative;
  overflow: hidden;
  background: var(--card);
}
.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.article-cover__ph {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: color-mix(in srgb, var(--primary) 55%, transparent);
}
.article-cover--placeholder {
  background:
    linear-gradient(135deg,
      color-mix(in srgb, var(--primary) 22%, transparent),
      color-mix(in srgb, var(--primary) 6%, transparent));
}

.article-cover--thumb {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  flex-shrink: 0;
}
.article-cover--banner {
  width: 100%;
  aspect-ratio: 21 / 9;
  border-radius: 16px;
}
.article-cover--hero {
  width: 100%;
  aspect-ratio: 16 / 9;
}
</style>
