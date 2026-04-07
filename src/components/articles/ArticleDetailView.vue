<script setup lang="ts">
import { computed, onUnmounted, ref, watch, toRef } from 'vue'
import { useAppStore } from '@/stores/app'
import { useLang } from '@/i18n'
import type { ArticleItem, ArticleEssay, ArticleDialogue, ArticleSegment, GrammarPoint } from '@/types'
import RubyText from '@/components/common/RubyText.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import ArticleCover from '@/components/common/ArticleCover.vue'
import { useFirebase } from '@/composables/useFirebase'
import { useArticlePrefs } from '@/composables/useArticlePrefs'
import { useArticlePlayback } from '@/composables/useArticlePlayback'

const props = defineProps<{ article: ArticleItem }>()
const emit = defineEmits<{ back: [] }>()

const store = useAppStore()
const { t, currentLang } = useLang()

const { singleMode, showTranslation, showReading, articleVoiceMale } = useArticlePrefs()

const article = toRef(props, 'article')
const {
  flatSentences,
  wholeArticleAudioUrl,
  articleOffersMaleVoice,
  canPlayAll,
  currentPlayingIndex,
  currentPlayingWord,
  loopPlaying,
  audioFnForJp,
  playAllWithLoopPlayer,
  playSentenceAt,
  invalidateArticlePlayback,
  stopLoop,
} = useArticlePlayback(article as unknown as import('vue').Ref<ArticleItem | null>)

// 切换文章 / 切换男女声 / 切学习语言 时：暂停 audio + 停 loopPlayer，避免旧资源继续播
watch(
  [() => props.article.id, articleVoiceMale, () => store.studyLang],
  () => {
    invalidateArticlePlayback()
    stopLoop()
  },
)

onUnmounted(() => invalidateArticlePlayback())

// ---- 派生 ----

const articleGrammar = computed((): GrammarPoint[] => {
  if (!props.article.grammar?.length) return []
  const map = store.grammarMap
  return props.article.grammar.map((id) => map[id]).filter(Boolean)
})

const showGrammar = ref(false)

/** 短文按"段"分组：把细切 segment 按字符数/数量阈值合并成段，方便排版。
 * 不改变 segment / audio_map 键，只影响展示。 */
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
  if (props.article.format !== 'essay') return [] as ArticleSegment[][]
  return groupEssayIntoParagraphs(props.article.segments)
})

// ---- 类型守卫 / 工具 ----

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

function startPracticeFromArticle() {
  if (flatSentences.value.length === 0) return
  stopLoop()
  invalidateArticlePlayback()
  store.startArticlePractice(props.article.id)
  useFirebase().debouncedSync()
}

function back() {
  invalidateArticlePlayback()
  stopLoop()
  emit('back')
}
</script>

<template>
  <div class="pt-1">
    <button
      type="button"
      class="mb-4 text-sm font-medium theme-muted hover:theme-text cursor-pointer border-0 bg-transparent px-0"
      @click="back"
    >
      ← {{ t('articleBack') }}
    </button>

    <header class="mb-6">
      <ArticleCover
        v-if="false"
        :article-id="article.id"
        variant="banner"
        :icon="article.format === 'dialogue' ? 'chat' : 'book'"
        :alt="article.titleWord"
        class="mb-4"
      />
      <h1 v-if="showReading && article.titleRuby" class="text-xl font-bold text-content-original">
        <RubyText :tokens="article.titleRuby" />
      </h1>
      <h1 v-else class="text-xl font-bold text-content-original leading-snug">{{ article.titleWord }}</h1>
      <template v-if="showTranslation">
        <p v-if="currentLang === 'zh'" class="mt-2 text-base text-content-translation">{{ article.titleZh }}</p>
        <p v-else-if="currentLang === 'ja'" class="mt-2 text-base text-content-translation opacity-90">{{ article.titleJp ?? article.titleZh }}</p>
        <p v-else class="mt-2 text-base text-content-translation opacity-90">{{ article.titleEn ?? article.titleZh }}</p>
      </template>

      <div class="flex flex-wrap items-center gap-2 mt-4">
        <button
          type="button"
          class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border transition-colors cursor-pointer"
          :class="
            showTranslation
              ? 'bg-primary/15 border-primary/40 text-primary-dark'
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
              ? 'bg-primary/15 border-primary/40 text-primary-dark'
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
            :class="!articleVoiceMale ? 'bg-primary/15 text-primary-dark' : 'theme-muted'"
          >{{ t('articleVoiceFemale') }}</span>
          <span
            class="px-2 py-0.5 rounded-full transition-colors"
            :class="articleVoiceMale ? 'bg-primary/15 text-primary-dark' : 'theme-muted'"
          >{{ t('articleVoiceMale') }}</span>
        </div>
        <template v-if="canPlayAll">
          <button
            v-if="!loopPlaying"
            type="button"
            class="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-[10px] text-xs font-medium cursor-pointer transition-all active:scale-[0.97] border theme-surface theme-muted"
            style="border-color: var(--border)"
            @click="playAllWithLoopPlayer"
          >
            <AppIcon name="play" :size="14" />
            {{ t('articlePlayAll') }}
          </button>
          <button
            v-else
            type="button"
            class="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-[10px] text-xs font-medium cursor-pointer transition-all active:scale-[0.97] border theme-surface theme-muted"
            style="border-color: var(--border)"
            @click="stopLoop"
          >
            <AppIcon name="pause" :size="14" />
            {{ t('articleStopPlayback') }}
          </button>
        </template>
        <button
          v-if="flatSentences.length > 0"
          type="button"
          class="inline-flex items-center justify-center px-4 py-1.5 rounded-[10px] text-xs font-medium cursor-pointer transition-all active:scale-[0.98] border theme-surface theme-muted"
          style="border-color: var(--border)"
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
            :class="!singleMode ? 'bg-primary/15 text-primary-dark' : 'theme-muted'"
          >{{ t('articleModeFull') }}</span>
          <span
            class="px-2 py-0.5 rounded-full transition-colors"
            :class="singleMode ? 'bg-primary/15 text-primary-dark' : 'theme-muted'"
          >{{ t('articleModeSingle') }}</span>
        </div>
      </div>
      <p v-if="flatSentences.length > 0" class="mt-3 text-xs theme-muted leading-relaxed opacity-90">
        {{ t('articlePracticeHowToHint') }}
      </p>
      <p v-else class="mt-3 text-sm theme-muted">
        {{ t('articlePracticeEmptyShort') }}
      </p>
    </header>

    <!-- ====== 单句列表模式 ====== -->
    <div v-if="singleMode" class="space-y-3">
      <div
        v-for="(seg, i) in flatSentences"
        :key="i"
        class="relative rounded-2xl theme-surface p-4 md:p-5 shadow-[0_2px_16px_rgba(0,0,0,0.06)] transition"
        :class="linePlaying(i) ? 'ring-2 ring-primary/40' : 'ring-0'"
      >
        <div class="flex items-start gap-3">
          <div class="flex-1 min-w-0">
            <div v-if="seg.speaker" class="text-xs font-bold mb-1" style="color: var(--primary)">{{ seg.speaker }}</div>
            <p v-if="showReading && seg.ruby" class="text-[17px] font-medium text-content-original leading-relaxed">
              <RubyText :tokens="seg.ruby" />
            </p>
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
            class="shrink-0 w-9 h-9 mt-0.5 rounded-[10px] flex items-center justify-center cursor-pointer transition-all active:scale-95 border theme-surface theme-muted"
            style="border-color: var(--border)"
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
        v-if="isEssay(article)"
        class="relative rounded-2xl theme-surface p-5 md:p-6 shadow-[0_2px_16px_rgba(0,0,0,0.06)]"
      >
        <span
          class="pointer-events-none absolute top-3 right-4 z-[1] text-[9px] font-medium tabular-nums leading-none theme-muted opacity-[0.38] md:top-4 md:right-5 md:text-[10px]"
          aria-hidden="true"
        >{{ article.level }}</span>
        <audio
          v-if="wholeArticleAudioUrl"
          :src="wholeArticleAudioUrl"
          controls
          preload="metadata"
          class="w-full mb-4"
        ></audio>
        <div class="space-y-5">
          <div
            v-for="(para, pi) in essayParagraphGroups"
            :key="pi"
            class="rounded-md -mx-0.5 px-0.5 py-0.5"
          >
            <p v-if="showReading" class="text-[17px] font-medium text-content-original leading-[1.85] [text-indent:1em]">
              <span
                v-for="(seg, si) in para"
                :key="`${pi}-${si}`"
                class="rounded-sm"
                :class="linePlaying(seg.word) ? 'bg-primary/25 ring-1 ring-primary/30' : ''"
              ><RubyText v-if="seg.ruby" :tokens="seg.ruby" /><template v-else>{{ seg.word }}</template></span>
            </p>
            <p v-else class="text-[17px] font-medium text-content-original leading-[1.85] [text-indent:1em]">
              <span
                v-for="(seg, si) in para"
                :key="`${pi}-${si}-nr`"
                class="rounded-sm"
                :class="linePlaying(seg.word) ? 'bg-primary/25 ring-1 ring-primary/30' : ''"
              >{{ seg.word }}</span>
            </p>
            <template v-if="showTranslation">
              <p v-if="currentLang === 'zh'" class="mt-2 pl-[1em] text-sm leading-relaxed text-content-translation">{{ para.map((s) => s.zh).join('') }}</p>
              <p v-else-if="currentLang === 'ja'" class="mt-2 pl-[1em] text-sm leading-relaxed text-content-translation opacity-90">{{ para.map((s) => s.jp ?? s.zh).join('') }}</p>
              <p v-else class="mt-2 pl-[1em] text-sm leading-relaxed text-content-translation opacity-90">{{ para.map((s) => s.en ?? s.zh).join('') }}</p>
            </template>
          </div>
        </div>
      </article>

      <!-- 对话 -->
      <article
        v-else-if="isDialogue(article)"
        class="relative rounded-2xl theme-surface p-5 md:p-6 shadow-[0_2px_16px_rgba(0,0,0,0.06)] space-y-6"
      >
        <span
          class="pointer-events-none absolute top-3 right-4 z-[1] text-[9px] font-medium tabular-nums leading-none theme-muted opacity-[0.38] md:top-4 md:right-5 md:text-[10px]"
          aria-hidden="true"
        >{{ article.level }}</span>
        <audio
          v-if="wholeArticleAudioUrl"
          :src="wholeArticleAudioUrl"
          controls
          preload="metadata"
          class="w-full"
        ></audio>
        <section v-for="(sec, si) in (article as ArticleDialogue).sections" :key="si" class="space-y-4">
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
            :class="linePlaying(line.word) ? 'bg-primary/10' : ''"
          >
            <div class="text-xs font-bold mb-0.5" style="color: var(--primary)">{{ line.speaker }}</div>
            <p v-if="showReading && line.ruby" class="text-[17px] text-content-original leading-relaxed">
              <RubyText :tokens="line.ruby" />
            </p>
            <p v-else class="text-[17px] text-content-original leading-relaxed">{{ line.word }}</p>
            <template v-if="showTranslation">
              <p v-if="currentLang === 'zh'" class="mt-2 text-sm text-content-translation">{{ line.zh }}</p>
              <p v-else-if="currentLang === 'ja'" class="mt-2 text-sm text-content-translation opacity-90">{{ line.jp ?? line.zh }}</p>
              <p v-else class="mt-2 text-sm text-content-translation opacity-90">{{ line.en ?? line.zh }}</p>
            </template>
          </div>
        </section>
      </article>
    </template>

    <!-- ====== 本文句型 ====== -->
    <div v-if="articleGrammar.length" class="mt-4">
      <button
        type="button"
        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors cursor-pointer"
        :class="
          showGrammar
            ? 'bg-primary/15 border-primary/40 text-primary-dark'
            : 'theme-muted border-[var(--border)] bg-transparent hover:theme-text'
        "
        @click="showGrammar = !showGrammar"
      >
        {{ t('grammarTitle') }}
        <span class="opacity-60">{{ articleGrammar.length }}</span>
        <svg class="w-3 h-3 transition-transform" :class="showGrammar ? 'rotate-180' : ''" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd"/></svg>
      </button>
      <div v-if="showGrammar" class="mt-3 rounded-2xl theme-surface p-4 md:p-5 shadow-[0_2px_16px_rgba(0,0,0,0.06)]">
        <div class="flex flex-wrap gap-2">
          <div
            v-for="g in articleGrammar"
            :key="g.id"
            class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs border border-[var(--border)] hover:border-primary/30 transition-colors"
          >
            <span class="font-mono text-[10px] leading-none px-1 py-0.5 rounded bg-[var(--bg)] theme-muted">{{ g.level }}</span>
            <span class="font-medium text-content-original">{{ g.pattern }}</span>
            <span class="theme-muted">{{ currentLang === 'en' ? g.meaningEn : g.meaning }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
