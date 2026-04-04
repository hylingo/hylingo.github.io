<script setup lang="ts">
import { ref, computed, onUnmounted, watch } from 'vue'
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'
import { audioEl } from '@/composables/useAudio'
import { useLoopPlayer } from '@/composables/useLoopPlayer'
import type { ArticleItem, ArticleEssay, ArticleDialogue, ArticleSegment } from '@/types'
import RubyText from '@/components/common/RubyText.vue'
import type { DataItem } from '@/stores/app'
import { readArticlePrefRaw, writeArticlePrefRaw } from '@/learning/learnStorage'
import { useFirebase } from '@/composables/useFirebase'

const props = withDefaults(
  defineProps<{ filterFormat: 'essay' | 'dialogue' }>(),
  { filterFormat: 'essay' },
)

const store = useAppStore()
const { t, currentLang } = useLang()
const { startLoop, stop: stopLoop, loopPlaying, loopIndex } = useLoopPlayer()

const selectedId = ref<string | null>(null)

/** 连播会话：+1 可丢弃未结束的 onended */
let articlePlaySession = 0

const playingAll = ref(false)
/** 当前正在播的原文行（与 audio_map 键一致，即 segment.word） */
const playingWord = ref<string | null>(null)

function readArticleBool(id: 'mode' | 'show_zh' | 'show_reading', defaultVal: boolean): boolean {
  try {
    if (typeof localStorage === 'undefined') return defaultVal
    const v = readArticlePrefRaw(store.studyLang, id)
    if (v === null) return defaultVal
    return v === '1' || v === 'true'
  } catch {
    return defaultVal
  }
}

function readStoredVoice(): 'female' | 'male' {
  try {
    if (typeof localStorage === 'undefined') return 'female'
    const v = readArticlePrefRaw(store.studyLang, 'voice')
    return v === 'male' ? 'male' : 'female'
  } catch {
    return 'female'
  }
}

/** 单句/全文模式（偏好按学习语言存储） */
const singleMode = ref(readArticleBool('mode', false))

/** 构建从指定索引开始的 LoopPlayer 播放列表 */
function buildLoopItems(fromIndex: number) {
  const sentences = flatSentences.value
  const items: (DataItem & { _cat: string })[] = []
  const addItem = (s: ArticleSegment & { speaker?: 'A' | 'B' }, i: number) => {
    const fn = audioFnForJp(s)
    if (fn) {
      items.push({
        id: i,
        word: s.word,
        reading: s.reading,
        meaning: currentLang.value === 'ja' ? (s.jp ?? s.zh) : s.zh,
        ruby: s.ruby,
        _cat: 'articles',
        _audioFn: fn,
      })
    }
  }
  for (let i = fromIndex; i < sentences.length; i++) addItem(sentences[i], i)
  for (let i = 0; i < fromIndex; i++) addItem(sentences[i], i)
  return items
}

const articleVoiceMale = ref(readStoredVoice() === 'male')

watch(articleVoiceMale, (isMale) => {
  try {
    writeArticlePrefRaw(store.studyLang, 'voice', isMale ? 'male' : 'female')
  } catch {
    /* ignore */
  }
  invalidateArticlePlayback()
  stopLoop()
})

/** 当前篇是否有至少一句男声资源 */
const articleOffersMaleVoice = computed(() =>
  flatSentences.value.some((s) => !!s.audioMale),
)

/** 文章朗读用文件名：男声优先（有键时），否则女声 */
function audioFnForJp(seg: ArticleSegment): string | undefined {
  if (articleVoiceMale.value && seg.audioMale) return seg.audioMale
  return seg.audio
}

const showTranslation = ref(readArticleBool('show_zh', true))
const showReading = ref(readArticleBool('show_reading', true))

watch(showTranslation, (v) => {
  try {
    writeArticlePrefRaw(store.studyLang, 'show_zh', v ? '1' : '0')
  } catch {
    /* ignore */
  }
})
watch(showReading, (v) => {
  try {
    writeArticlePrefRaw(store.studyLang, 'show_reading', v ? '1' : '0')
  } catch {
    /* ignore */
  }
})
watch(singleMode, (v) => {
  try {
    writeArticlePrefRaw(store.studyLang, 'mode', v ? '1' : '0')
  } catch {
    /* ignore */
  }
})

watch(
  () => store.studyLang,
  () => {
    singleMode.value = readArticleBool('mode', false)
    articleVoiceMale.value = readStoredVoice() === 'male'
    showTranslation.value = readArticleBool('show_zh', true)
    showReading.value = readArticleBool('show_reading', true)
    invalidateArticlePlayback()
    stopLoop()
  },
)

const list = computed(() => store.articles.filter((a) => a.format === props.filterFormat))

const selected = computed(() => {
  if (!selectedId.value) return null
  return list.value.find((a) => a.id === selectedId.value) ?? null
})

/**
 * 短文按「段」分组显示：细切 segment 合并为一段，长段保持单段一段。
 * 不改变 segment / audio_map 键，仅影响全文排版。
 */
function groupEssayIntoParagraphs(segments: ArticleSegment[]): ArticleSegment[][] {
  const out: ArticleSegment[][] = []
  let cur: ArticleSegment[] = []
  let runLen = 0
  const maxChars = 120
  const maxPerGroup = 3
  for (const s of segments) {
    cur.push(s)
    runLen += s.word.length
    if (runLen >= maxChars || cur.length >= maxPerGroup) {
      out.push(cur)
      cur = []
      runLen = 0
    }
  }
  if (cur.length) out.push(cur)
  return out
}

const essayParagraphGroups = computed(() => {
  const it = selected.value
  if (!it || it.format !== 'essay') return [] as ArticleSegment[][]
  return groupEssayIntoParagraphs(it.segments)
})

/** 扁平化的所有句子（用于单句模式和连播） */
const flatSentences = computed((): (ArticleSegment & { speaker?: 'A' | 'B' })[] => {
  const it = selected.value
  if (!it) return []
  if (it.format === 'essay') {
    return it.segments.map((s) => ({ ...s }))
  }
  const out: (ArticleSegment & { speaker?: 'A' | 'B' })[] = []
  for (const sec of it.sections) {
    for (const line of sec.lines) {
      out.push({ ...line })
    }
  }
  return out
})

/** 当前篇按顺序的朗读单元（用于连播） */
const playbackUnits = computed(() => flatSentences.value)

const canPlayAll = computed(() => playbackUnits.value.some((u) => !!audioFnForJp(u)))

/** 当前正在播放的句子在 flatSentences 中的原始索引，-1 表示未播放（用于单句模式） */
const currentPlayingIndex = computed<number>(() => {
  if (!loopPlaying.value) return -1
  const items = playbackUnits.value
    .map((u, idx) => ({ u, idx }))
    .filter(({ u }) => !!audioFnForJp(u))
  return items[loopIndex.value]?.idx ?? -1
})

/** 当前正在播放的句子 word（用于全文模式，word 不重复的场景） */
const currentPlayingWord = computed<string | null>(() => {
  const idx = currentPlayingIndex.value
  if (idx === -1) return null
  return playbackUnits.value[idx]?.word ?? null
})


function invalidateArticlePlayback() {
  articlePlaySession++
  playingAll.value = false
  playingWord.value = null
  audioEl.pause()
  audioEl.onended = null
}

function playAllWithLoopPlayer() {
  invalidateArticlePlayback()
  const items = buildLoopItems(0)
  if (items.length) startLoop(items)
}

function startPracticeFromArticle() {
  if (!selected.value || flatSentences.value.length === 0) return
  stopLoop()
  invalidateArticlePlayback()
  store.startArticlePractice(selected.value.id)
  useFirebase().debouncedSync()
}

/** 单句模式：点击某句，从该句开始启动 LoopPlayer */
function playSentenceAt(index: number) {
  invalidateArticlePlayback()
  const items = buildLoopItems(index)
  if (items.length) startLoop(items)
}

function openItem(id: string) {
  selectedId.value = id
}

function back() {
  invalidateArticlePlayback()
  stopLoop()
  selectedId.value = null
}

watch(selectedId, () => {
  invalidateArticlePlayback()
})

function formatLabel(it: ArticleItem) {
  const kind = it.format === 'essay' ? t('articleKindEssay') : t('articleKindDialogue')
  return `${it.level} · ${kind}`
}

function isEssay(it: ArticleItem | null): it is ArticleEssay {
  return it !== null && it.format === 'essay'
}

function isDialogue(it: ArticleItem | null): it is ArticleDialogue {
  return it !== null && it.format === 'dialogue'
}

function linePlaying(i: number): boolean
function linePlaying(w: string): boolean
function linePlaying(iOrW: number | string): boolean {
  if (typeof iOrW === 'number') return currentPlayingIndex.value === iOrW
  return currentPlayingWord.value === iOrW
}

onUnmounted(() => {
  invalidateArticlePlayback()
})
</script>

<template>
  <div class="px-4 pb-24 md:px-10 md:max-w-[720px] md:mx-auto">
    <!-- 列表 -->
    <div v-if="!selected" class="space-y-3 pt-1">
      <p class="text-sm theme-muted mb-3">
        {{ props.filterFormat === 'dialogue' ? t('dialogueIntro') : t('articleIntro') }}
      </p>
      <button
        v-for="it in list"
        :key="it.id"
        type="button"
        class="w-full text-left rounded-2xl theme-surface shadow-[0_2px_16px_rgba(0,0,0,0.06)] p-4 transition hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] active:scale-[0.99] cursor-pointer border-0"
        @click="openItem(it.id)"
      >
        <div class="text-xs font-medium theme-muted mb-1">{{ formatLabel(it) }}</div>
        <div class="text-base font-bold text-content-original leading-snug">{{ it.titleWord }}</div>
        <div v-if="currentLang === 'zh'" class="text-sm mt-1 text-content-translation">{{ it.titleZh }}</div>
        <div v-else-if="currentLang === 'en'" class="text-sm mt-1 text-content-translation opacity-90">{{ it.titleEn }}</div>
        <div v-else class="text-sm mt-1 text-content-translation opacity-90">{{ it.titleJp ?? it.titleZh }}</div>
      </button>
      <p v-if="!list.length" class="text-sm theme-muted py-8 text-center">{{ t('articleEmpty') }}</p>
    </div>

    <!-- 详情 -->
    <div v-else class="pt-1">
      <button
        type="button"
        class="mb-4 text-sm font-medium theme-muted hover:theme-text cursor-pointer border-0 bg-transparent px-0"
        @click="back"
      >
        ← {{ t('articleBack') }}
      </button>

      <header class="mb-6">
        <h1 v-if="showReading && selected!.titleRuby" class="text-xl font-bold text-content-original"><RubyText :tokens="selected!.titleRuby" /></h1>
        <h1 v-else class="text-xl font-bold text-content-original leading-snug">{{ selected!.titleWord }}</h1>
        <template v-if="showTranslation">
          <p v-if="currentLang === 'zh'" class="mt-2 text-base text-content-translation">{{ selected!.titleZh }}</p>
          <p v-else-if="currentLang === 'ja'" class="mt-2 text-base text-content-translation opacity-90">{{ selected!.titleJp ?? selected!.titleZh }}</p>
          <p v-else class="mt-2 text-base text-content-translation opacity-90">{{ selected!.titleEn ?? selected!.titleZh }}</p>
        </template>

        <div class="flex flex-wrap items-center gap-2 mt-4">
          <button
            type="button"
            class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border transition-colors cursor-pointer"
            :class="
              showTranslation
                ? 'bg-[#e8735a]/15 border-[#e8735a]/40 text-[#c45a3e]'
                : 'theme-muted border-[var(--border)] bg-transparent opacity-90'
            "
            :aria-pressed="showTranslation"
            @click="showTranslation = !showTranslation"
          >
            {{ t('articleToggleTranslation') }}
          </button>
          <button
            type="button"
            class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border transition-colors cursor-pointer"
            :class="
              showReading
                ? 'bg-[#e8735a]/15 border-[#e8735a]/40 text-[#c45a3e]'
                : 'theme-muted border-[var(--border)] bg-transparent opacity-90'
            "
            :aria-pressed="showReading"
            @click="showReading = !showReading"
          >
            {{ t('articleToggleReading') }}
          </button>
          <div
            v-if="articleOffersMaleVoice"
            class="inline-flex items-center rounded-full border border-[var(--border)] p-0.5 text-xs font-medium cursor-pointer select-none"
            @click="articleVoiceMale = !articleVoiceMale"
          >
            <span
              class="px-2 py-0.5 rounded-full transition-colors"
              :class="!articleVoiceMale ? 'bg-[#e8735a]/15 text-[#c45a3e]' : 'theme-muted'"
            >{{ t('articleVoiceFemale') }}</span>
            <span
              class="px-2 py-0.5 rounded-full transition-colors"
              :class="articleVoiceMale ? 'bg-[#e8735a]/15 text-[#c45a3e]' : 'theme-muted'"
            >{{ t('articleVoiceMale') }}</span>
          </div>
          <template v-if="canPlayAll">
            <button
              v-if="!loopPlaying"
              type="button"
              class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border transition-colors cursor-pointer theme-muted border-[var(--border)] bg-transparent hover:theme-text"
              @click="playAllWithLoopPlayer"
            >
              {{ t('articlePlayAll') }}
            </button>
            <button
              v-else
              type="button"
              class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border transition-colors cursor-pointer bg-[#e8735a]/15 border-[#e8735a]/40 text-[#c45a3e]"
              @click="stopLoop"
            >
              {{ t('articleStopPlayback') }}
            </button>
          </template>
          <button
            v-if="flatSentences.length > 0"
            type="button"
            class="inline-flex items-center justify-center px-3 py-1.5 rounded-lg text-xs font-semibold cursor-pointer transition-all active:scale-[0.98] btn-grad-primary btn-grad-primary--borderless text-white shadow-[0_3px_12px_rgba(232,115,90,0.3)]"
            @click="startPracticeFromArticle"
          >
            {{ t('articlePracticeButton') }}
          </button>
          <!-- 单句/全文 切换滑块 -->
          <div
            class="inline-flex items-center rounded-full border border-[var(--border)] p-0.5 ml-auto cursor-pointer select-none text-xs font-medium"
            @click="singleMode = !singleMode"
          >
            <span
              class="px-2 py-0.5 rounded-full transition-colors"
              :class="!singleMode ? 'bg-[#e8735a]/15 text-[#c45a3e]' : 'theme-muted'"
            >{{ t('articleModeFull') }}</span>
            <span
              class="px-2 py-0.5 rounded-full transition-colors"
              :class="singleMode ? 'bg-[#e8735a]/15 text-[#c45a3e]' : 'theme-muted'"
            >{{ t('articleModeSingle') }}</span>
          </div>
        </div>
        <p
          v-if="flatSentences.length > 0"
          class="mt-3 text-xs theme-muted leading-relaxed opacity-90"
        >
          {{ t('articlePracticeHowToHint') }}
        </p>
        <p
          v-else
          class="mt-3 text-sm theme-muted"
        >
          {{ t('articlePracticeEmptyShort') }}
        </p>
      </header>

      <!-- ====== 单句列表模式 ====== -->
      <div v-if="singleMode" class="space-y-3">
        <div
          v-for="(seg, i) in flatSentences"
          :key="i"
          class="relative rounded-2xl theme-surface p-4 md:p-5 shadow-[0_2px_16px_rgba(0,0,0,0.06)] transition"
          :class="linePlaying(i) ? 'ring-2 ring-[#e8735a]/40' : 'ring-0'"
        >
          <div class="flex items-start gap-3">
            <div class="flex-1 min-w-0">
              <div v-if="seg.speaker" class="text-xs font-bold mb-1" style="color: var(--primary)">{{ seg.speaker }}</div>
              <p v-if="showReading && seg.ruby" class="text-[15px] font-medium text-content-original"><RubyText :tokens="seg.ruby" /></p>
              <p v-else class="text-[15px] font-medium text-content-original leading-relaxed">{{ seg.word }}</p>
              <template v-if="showTranslation">
                <p v-if="currentLang === 'zh'" class="mt-2 text-sm leading-relaxed text-content-translation">{{ seg.zh }}</p>
                <p v-else-if="currentLang === 'ja'" class="mt-2 text-sm leading-relaxed text-content-translation opacity-90">{{ seg.jp ?? seg.zh }}</p>
                <p v-else class="mt-2 text-sm leading-relaxed text-content-translation opacity-90">{{ seg.en ?? seg.zh }}</p>
              </template>
            </div>
            <button
              v-if="audioFnForJp(seg)"
              type="button"
              class="shrink-0 w-9 h-9 mt-0.5 rounded-full flex items-center justify-center cursor-pointer border-0 transition-transform active:scale-95"
              style="background: linear-gradient(135deg, #e8735a 0%, #d4624d 100%); color: #fff;"
              @click="playSentenceAt(i)"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- ====== 全文模式 ====== -->
      <template v-else-if="!singleMode">
        <!-- 短文 -->
        <article
          v-if="isEssay(selected)"
          class="relative rounded-2xl theme-surface p-5 md:p-6 shadow-[0_2px_16px_rgba(0,0,0,0.06)]"
        >
          <span
            class="pointer-events-none absolute top-3 right-4 z-[1] text-[9px] font-medium tabular-nums leading-none theme-muted opacity-[0.38] md:top-4 md:right-5 md:text-[10px]"
            aria-hidden="true"
            >{{ selected!.level }}</span>
          <div class="space-y-5">
            <div
              v-for="(para, pi) in essayParagraphGroups"
              :key="pi"
              class="rounded-md -mx-0.5 px-0.5 py-0.5"
            >
              <p v-if="showReading" class="text-[15px] font-medium text-content-original leading-[1.85] [text-indent:1em]">
                <span
                  v-for="(seg, si) in para"
                  :key="`${pi}-${si}`"
                  class="rounded-sm"
                  :class="linePlaying(seg.word) ? 'bg-[#e8735a]/25 ring-1 ring-[#e8735a]/30' : ''"
                ><RubyText v-if="seg.ruby" :tokens="seg.ruby" /><template v-else>{{ seg.word }}</template></span>
              </p>
              <p v-else class="text-[15px] font-medium text-content-original leading-[1.85] [text-indent:1em]">
                <span
                  v-for="(seg, si) in para"
                  :key="`${pi}-${si}-nr`"
                  class="rounded-sm"
                  :class="linePlaying(seg.word) ? 'bg-[#e8735a]/25 ring-1 ring-[#e8735a]/30' : ''"
                >{{ seg.word }}</span>
              </p>
              <template v-if="showTranslation">
                <p
                  v-if="currentLang === 'zh'"
                  class="mt-2 pl-[1em] text-sm leading-relaxed text-content-translation"
                >{{ para.map((s) => s.zh).join('') }}</p>
                <p
                  v-else-if="currentLang === 'ja'"
                  class="mt-2 pl-[1em] text-sm leading-relaxed text-content-translation opacity-90"
                >{{ para.map((s) => s.jp ?? s.zh).join('') }}</p>
                <p
                  v-else
                  class="mt-2 pl-[1em] text-sm leading-relaxed text-content-translation opacity-90"
                >{{ para.map((s) => s.en ?? s.zh).join('') }}</p>
              </template>
            </div>
          </div>
        </article>

        <!-- 对话 -->
        <article
          v-else-if="isDialogue(selected)"
          class="relative rounded-2xl theme-surface p-5 md:p-6 shadow-[0_2px_16px_rgba(0,0,0,0.06)] space-y-6"
        >
          <span
            class="pointer-events-none absolute top-3 right-4 z-[1] text-[9px] font-medium tabular-nums leading-none theme-muted opacity-[0.38] md:top-4 md:right-5 md:text-[10px]"
            aria-hidden="true"
            >{{ selected!.level }}</span>
          <section v-for="(sec, si) in (selected as ArticleDialogue).sections" :key="si" class="space-y-4">
            <div class="flex items-center gap-2 flex-wrap">
              <span v-if="sec.badge" class="text-lg" aria-hidden="true">{{ sec.badge }}</span>
              <span class="text-sm font-semibold text-content-original">{{ sec.headingWord }}</span>
              <span v-if="showTranslation && currentLang === 'zh'" class="text-xs text-content-translation">（{{ sec.headingZh }}）</span>
              <span v-else-if="showTranslation && currentLang === 'ja'" class="text-xs text-content-translation opacity-90">（{{ sec.headingJp ?? sec.headingZh }}）</span>
              <span v-else-if="showTranslation && currentLang === 'en'" class="text-xs text-content-translation opacity-90">（{{ sec.headingEn ?? sec.headingZh }}）</span>
            </div>
            <div
              v-for="(line, li) in sec.lines"
              :key="li"
              class="transition-colors rounded-md -mx-0.5 px-0.5 py-0.5"
              :class="linePlaying(line.word) ? 'bg-[#e8735a]/10' : ''"
            >
              <div class="text-xs font-bold mb-0.5" style="color: var(--primary)">{{ line.speaker }}</div>
              <p v-if="showReading && line.ruby" class="text-[15px] text-content-original"><RubyText :tokens="line.ruby" /></p>
              <p v-else class="text-[15px] text-content-original leading-relaxed">{{ line.word }}</p>
              <template v-if="showTranslation">
                <p v-if="currentLang === 'zh'" class="mt-2 text-sm text-content-translation">{{ line.zh }}</p>
                <p v-else-if="currentLang === 'ja'" class="mt-2 text-sm text-content-translation opacity-90">{{ line.jp ?? line.zh }}</p>
                <p v-else class="mt-2 text-sm text-content-translation opacity-90">{{ line.en ?? line.zh }}</p>
              </template>
            </div>
          </section>
        </article>
      </template>
    </div>
  </div>
</template>
