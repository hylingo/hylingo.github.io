<script setup lang="ts">
/**
 * 文章面板：壳组件。
 * 仅托管 selectedId 状态，其余都拆到子组件 / composable：
 *   - 列表/搜索  → ArticleListView
 *   - 详情/播放  → ArticleDetailView + useArticlePlayback + useArticlePrefs
 */
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import SkeletonArticleList from '@/components/common/SkeletonArticleList.vue'
import ArticleListView from './ArticleListView.vue'
import ArticleDetailView from './ArticleDetailView.vue'

const props = withDefaults(
  defineProps<{ filterFormat: 'essay' | 'dialogue' }>(),
  { filterFormat: 'essay' },
)

const store = useAppStore()

// 按需加载 articles 数据
onMounted(() => { store.ensureArticles() })

const selectedId = ref<string | null>(null)
const listViewRef = ref<InstanceType<typeof ArticleListView> | null>(null)

const selected = computed(() => {
  if (!selectedId.value) return null
  return store.articles.find((a) => a.id === selectedId.value) ?? null
})

function onSelect(id: string) {
  selectedId.value = id
  store.articleDetailOpen = true
}

function onBack() {
  selectedId.value = null
  store.articleDetailOpen = false
  // 回到列表时刷新进度（详情里可能更新过 listen/shadow 计数）
  listViewRef.value?.refreshProgressMap()
}

// 切换 cat（散文/对话 tab 互切）或卸载时，复位标志
watch(() => props.filterFormat, () => {
  selectedId.value = null
  store.articleDetailOpen = false
})
onBeforeUnmount(() => { store.articleDetailOpen = false })
</script>

<template>
  <SkeletonArticleList v-if="!store.isArticlesLoaded" />
  <div v-else class="px-4 pb-24 md:px-10 md:max-w-[720px] md:mx-auto">
    <ArticleListView
      v-if="!selected"
      ref="listViewRef"
      :filter-format="props.filterFormat"
      @select="onSelect"
    />
    <ArticleDetailView v-else :article="selected" @back="onBack" @select="onSelect" />
  </div>
</template>
