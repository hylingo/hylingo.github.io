/**
 * 文章详情的播放编排：把当前选中文章 + 男/女声偏好桥接到 useLoopPlayer。
 *
 * 不持有 selected 自身，调用方传入 (因为 selected 派生自 list / route，应保持单一来源)。
 */
import { computed, type Ref } from 'vue'
import type { ArticleItem, ArticleSegment } from '@/types'
import type { DataItem } from '@/stores/app'
import { audioEl, audioPath } from '@/composables/useAudio'
import { useLoopPlayer } from '@/composables/useLoopPlayer'
import { useArticlePrefs } from '@/composables/useArticlePrefs'
import { currentLang } from '@/i18n'

type SentenceLike = ArticleSegment & { speaker?: 'A' | 'B' }

export function useArticlePlayback(selected: Ref<ArticleItem | null>) {
  const { startLoop, stop: stopLoop, loopPlaying, loopIndex } = useLoopPlayer()
  const { articleVoiceMale } = useArticlePrefs()

  /** 文章朗读用文件名：男声优先（有键时），否则女声 */
  function audioFnForJp(seg: ArticleSegment): string | undefined {
    if (articleVoiceMale.value && seg.audioMale) return seg.audioMale
    return seg.audio
  }

  /** 扁平化所有句子（essay 直出 segments，dialogue 把所有 section 的 lines 拼起来）。
   * 整段音频模式 (articleAudio) 下返回空，表示不做单句/连播 UI。 */
  const flatSentences = computed<SentenceLike[]>(() => {
    const it = selected.value
    if (!it || it.articleAudio) return []
    if (it.format === 'essay') return it.segments.map((s) => ({ ...s }))
    const out: SentenceLike[] = []
    for (const sec of it.sections) {
      for (const line of sec.lines) out.push({ ...line })
    }
    return out
  })

  /** 整段音频 URL（仅当文章设置了 articleAudio 字段） */
  const wholeArticleAudioUrl = computed<string | null>(() => {
    const fn = selected.value?.articleAudio
    return fn ? audioPath(fn) : null
  })

  /** 当前篇是否有至少一句男声资源 */
  const articleOffersMaleVoice = computed(() =>
    flatSentences.value.some((s) => !!s.audioMale),
  )

  const canPlayAll = computed(() => flatSentences.value.some((u) => !!audioFnForJp(u)))

  /** 当前正在播放的句子在 flatSentences 中的原始索引；-1 = 未播放 */
  const currentPlayingIndex = computed<number>(() => {
    if (!loopPlaying.value) return -1
    const items = flatSentences.value
      .map((u, idx) => ({ u, idx }))
      .filter(({ u }) => !!audioFnForJp(u))
    return items[loopIndex.value]?.idx ?? -1
  })

  /** 当前正在播放的句子 word（用于全文模式按 word 高亮） */
  const currentPlayingWord = computed<string | null>(() => {
    const idx = currentPlayingIndex.value
    if (idx === -1) return null
    return flatSentences.value[idx]?.word ?? null
  })

  /** 构建从指定索引开始的 LoopPlayer 播放列表（环绕：fromIndex...end + 0...fromIndex-1） */
  function buildLoopItems(fromIndex: number): (DataItem & { _cat: string })[] {
    const sentences = flatSentences.value
    const items: (DataItem & { _cat: string })[] = []
    const artId = selected.value?.id ?? ''
    const addItem = (s: SentenceLike, i: number) => {
      const fn = audioFnForJp(s)
      if (!fn) return
      items.push({
        id: i,
        word: s.word,
        reading: s.reading,
        meaning: currentLang.value === 'ja' ? (s.jp ?? s.zh) : s.zh,
        ruby: s.ruby,
        _cat: 'articles',
        _audioFn: fn,
        _articleId: artId,
      })
    }
    for (let i = fromIndex; i < sentences.length; i++) addItem(sentences[i], i)
    for (let i = 0; i < fromIndex; i++) addItem(sentences[i], i)
    return items
  }

  function invalidateArticlePlayback() {
    audioEl.pause()
    audioEl.onended = null
  }

  function playAllWithLoopPlayer() {
    invalidateArticlePlayback()
    const items = buildLoopItems(0)
    if (items.length) startLoop(items)
  }

  function playSentenceAt(index: number) {
    invalidateArticlePlayback()
    const items = buildLoopItems(index)
    if (items.length) startLoop(items)
  }

  return {
    // 派生数据
    flatSentences,
    wholeArticleAudioUrl,
    articleOffersMaleVoice,
    canPlayAll,
    currentPlayingIndex,
    currentPlayingWord,
    loopPlaying,
    // 工具
    audioFnForJp,
    // 动作
    playAllWithLoopPlayer,
    playSentenceAt,
    invalidateArticlePlayback,
    stopLoop,
  }
}
