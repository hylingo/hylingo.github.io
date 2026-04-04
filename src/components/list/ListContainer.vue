<script setup lang="ts">
import type { VocabItemWithCat } from '../../types'
import ListItem from './ListItem.vue'
import { useLang } from '@/i18n'

const { t } = useLang()

const emit = defineEmits<{
  playListFrom: [rowNumber: number]
}>()

withDefaults(
  defineProps<{
    items: VocabItemWithCat[]
    /** 当前页在「筛选后全列表」中的起始下标（0-based），用于左侧序号连续 */
    rowOffset?: number
  }>(),
  { rowOffset: 0 },
)
</script>

<template>
  <div class="flex flex-col gap-3 px-4 pb-4 md:px-10">
    <ListItem
      v-for="(item, i) in items"
      :key="item._cat + ':' + item.id"
      :item="item"
      :cat="item._cat"
      :row-number="rowOffset + i + 1"
      @play-list-from="emit('playListFrom', $event)"
    />
    <div v-if="items.length === 0" class="text-center theme-muted py-12 text-sm">
      {{ t('notFound') }}
    </div>
  </div>
</template>
