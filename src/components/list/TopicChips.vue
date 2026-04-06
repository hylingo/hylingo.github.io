<script setup lang="ts">
import { ref, computed } from 'vue'
import { useLang } from '@/i18n'
import { useMenuAnchor } from '@/composables/useMenuAnchor'

const props = defineProps<{
  /** 主题及在当前词表中的条数（仅统计 JSON 里带了 topic 的条目） */
  topics: { topic: string; count: number }[]
  selected: string
  levels?: string[]
  selectedLevels?: string[]
}>()

const { t } = useLang()

const emit = defineEmits<{
  select: [topic: string]
  'toggle-level': [level: string]
  'clear-levels': []
}>()

const dropdownOpen = ref(false)
const levelDropdownOpen = ref(false)

const topicTriggerRef = ref<HTMLElement | null>(null)
const levelTriggerRef = ref<HTMLElement | null>(null)

const DROPDOWN_Z_BACKDROP = 450

const topicMenuStyle = useMenuAnchor(dropdownOpen, topicTriggerRef, { minWidth: 148, maxWidth: 204 })
const levelMenuStyle = useMenuAnchor(levelDropdownOpen, levelTriggerRef, { minWidth: 100 })

const topicPanelStyle = computed(() => ({
  ...topicMenuStyle.value,
  borderColor: 'var(--border)',
}))

const levelPanelStyle = computed(() => ({
  ...levelMenuStyle.value,
  borderColor: 'var(--border)',
}))

function toggleTopicDropdown() {
  const next = !dropdownOpen.value
  dropdownOpen.value = next
  if (next) levelDropdownOpen.value = false
}

function toggleLevelDropdown() {
  const next = !levelDropdownOpen.value
  levelDropdownOpen.value = next
  if (next) dropdownOpen.value = false
}

function closeAllDropdowns() {
  dropdownOpen.value = false
  levelDropdownOpen.value = false
}

const TOPIC_I18N_KEYS: Record<string, string> = {
  '问候寒暄': 'topicGreetings',
  '饮食餐厅': 'topicFoodDining',
  '购物': 'topicShopping',
  '交通出行': 'topicTransportation',
  '住宿旅行': 'topicAccommodationTravel',
  '工作职场': 'topicWorkplace',
  '健康医疗': 'topicHealthMedical',
  '情绪心理': 'topicEmotionsPsychology',
  '日语学习': 'topicJapaneseLearning',
  '日本文化': 'topicJapaneseCulture',
  '科技网络': 'topicTechInternet',
  '天气自然': 'topicWeatherNature',
  '兴趣娱乐': 'topicHobbiesEntertainment',
  '人际关系': 'topicRelationships',
  '家庭亲子': 'topicFamilyParenting',
  '励志感悟': 'topicMotivationInsights',
  '思考议论': 'topicThinkingDiscussion',
  '日常生活': 'topicDailyLife',
  '日常场景': 'topicDailyScenes',
  '地名观光': 'topicGeoSightseeing',
  '社会新闻': 'topicNewsSociety',
  '食物料理': 'topicFoodCooking',
  '行政手续': 'topicAdminProcedures',
  '生活用品': 'topicDailyGoods',
  '住房租房': 'topicHousingRent',
  '购物消费': 'topicShoppingSpending',
  '通信数码': 'topicCommsDigital',
  '学校教育': 'topicSchoolEducation',
}


function getTopicLabel(topic: string): string {
  const key = TOPIC_I18N_KEYS[topic]
  return key ? t(key) : topic
}

function onSelect(topic: string) {
  emit('select', topic)
  dropdownOpen.value = false
}

function onLevelToggle(level: string) {
  emit('toggle-level', level)
}

function onLevelClear() {
  emit('clear-levels')
  levelDropdownOpen.value = false
}
</script>

<template>
  <div class="flex items-center gap-1">
    <!-- 全部 -->
    <button
      type="button"
      class="shrink-0 rounded-full px-2.5 py-0.5 text-[11px] font-medium cursor-pointer transition-all border-none outline-none whitespace-nowrap"
      :class="selected === '' && (!selectedLevels || selectedLevels.length === 0)
        ? 'bg-[var(--primary)]/12 text-[var(--primary)]'
        : 'bg-transparent theme-muted hover:text-[var(--primary)]'"
      @click="onSelect(''); onLevelClear()"
    >
      {{ t('allTopics') }}
    </button>

    <!-- 级别下拉 -->
    <button
      v-if="levels && levels.length > 0"
      ref="levelTriggerRef"
      type="button"
      class="shrink-0 rounded-full px-2.5 py-0.5 text-[11px] font-medium cursor-pointer transition-all border-none outline-none whitespace-nowrap"
      :class="selectedLevels && selectedLevels.length > 0
        ? 'bg-[var(--primary)]/12 text-[var(--primary)]'
        : 'bg-transparent theme-muted hover:text-[var(--primary)]'"
      @click="toggleLevelDropdown"
    >
      {{ selectedLevels && selectedLevels.length > 0 ? selectedLevels.join(' ') : t('levelSelect') }}
      <svg class="inline-block ml-0.5" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
    </button>

    <!-- 分类下拉 -->
    <button
      ref="topicTriggerRef"
      type="button"
      class="shrink-0 rounded-full px-2.5 py-0.5 text-[11px] font-medium cursor-pointer transition-all border-none outline-none whitespace-nowrap"
      :class="selected !== ''
        ? 'bg-[var(--primary)]/12 text-[var(--primary)]'
        : 'bg-transparent theme-muted hover:text-[var(--primary)]'"
      @click="toggleTopicDropdown"
    >
      {{ selected ? getTopicLabel(selected) : t('topicSelect') }}
      <svg class="inline-block ml-0.5" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
    </button>

    <Teleport to="body">
      <template v-if="dropdownOpen || levelDropdownOpen">
        <div
          class="fixed inset-0"
          :style="{
            position: 'fixed',
            inset: 0,
            zIndex: DROPDOWN_Z_BACKDROP,
            background: 'var(--overlay-scrim)',
          }"
          aria-hidden="true"
          @pointerdown.prevent="closeAllDropdowns"
        />
        <div
          v-if="dropdownOpen"
          class="dropdown-scroll max-h-[min(60vh,320px)] overflow-y-auto overflow-x-hidden rounded-xl theme-surface shadow-[0_8px_32px_rgba(0,0,0,0.15)] border py-1 pr-1"
          :style="topicPanelStyle"
          @pointerdown.stop
        >
          <button
            type="button"
            class="w-full min-w-0 text-left pl-3 pr-2 py-2 text-[13px] font-medium leading-snug break-words cursor-pointer transition-colors hover:bg-primary/10"
            :class="!selected ? 'text-primary' : 'theme-text'"
            @click="onSelect('')"
          >
            {{ t('filterNone') }}
          </button>
          <button
            v-for="row in topics"
            :key="row.topic"
            type="button"
            class="w-full min-w-0 text-left pl-3 pr-2 py-2 text-[13px] font-medium leading-snug break-words cursor-pointer transition-colors hover:bg-primary/10 flex items-baseline justify-between gap-2"
            :class="selected === row.topic ? 'text-primary' : 'theme-text'"
            @click="onSelect(row.topic)"
          >
            <span class="min-w-0">{{ getTopicLabel(row.topic) }}</span>
            <span class="shrink-0 text-[11px] font-medium tabular-nums opacity-70">{{ row.count }}</span>
          </button>
        </div>
        <div
          v-if="levelDropdownOpen"
          class="rounded-xl theme-surface shadow-[0_8px_32px_rgba(0,0,0,0.15)] border py-1"
          :style="levelPanelStyle"
          @pointerdown.stop
        >
          <button
            type="button"
            class="w-full text-left px-3 py-2 text-[13px] font-medium cursor-pointer transition-colors hover:bg-primary/10"
            :class="!selectedLevels || selectedLevels.length === 0 ? 'text-primary' : 'theme-text'"
            @click="onLevelClear()"
          >
            {{ t('filterNone') }}
          </button>
          <button
            v-for="lv in levels"
            :key="lv"
            type="button"
            class="w-full text-left px-3 py-2 text-[13px] font-medium cursor-pointer transition-colors hover:bg-primary/10 flex items-center gap-2"
            @click="onLevelToggle(lv)"
          >
            <svg v-if="selectedLevels?.includes(lv)" class="shrink-0 text-primary" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
            <span v-else class="shrink-0 w-[14px]" />
            <span :class="selectedLevels?.includes(lv) ? 'text-primary' : 'theme-text'">{{ lv }}</span>
          </button>
        </div>
      </template>
    </Teleport>
  </div>
</template>
