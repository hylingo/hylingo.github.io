import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ArticleItem, StudyLang } from '@/types'

export interface DataItem {
  id: number
  word: string
  reading: string
  meaning: string
  meaningEn?: string
  meaningJp?: string
  example?: string
  exampleCn?: string
  audio?: string
  audioExample?: string
  topic?: string
  level?: string
  ruby?: { t: string; r?: string }[]
  _cat?: string
  _audioFn?: string
}

export interface AppData {
  nouns: DataItem[]
  verbs: DataItem[]
  kana: DataItem[]
}

const KANA_DATA: DataItem[] = [
  // Hiragana
  { id: 1, word: 'あ', reading: 'あ', meaning: 'a' },
  { id: 2, word: 'い', reading: 'い', meaning: 'i' },
  { id: 3, word: 'う', reading: 'う', meaning: 'u' },
  { id: 4, word: 'え', reading: 'え', meaning: 'e' },
  { id: 5, word: 'お', reading: 'お', meaning: 'o' },
  { id: 6, word: 'か', reading: 'か', meaning: 'ka' },
  { id: 7, word: 'き', reading: 'き', meaning: 'ki' },
  { id: 8, word: 'く', reading: 'く', meaning: 'ku' },
  { id: 9, word: 'け', reading: 'け', meaning: 'ke' },
  { id: 10, word: 'こ', reading: 'こ', meaning: 'ko' },
  { id: 11, word: 'さ', reading: 'さ', meaning: 'sa' },
  { id: 12, word: 'し', reading: 'し', meaning: 'shi' },
  { id: 13, word: 'す', reading: 'す', meaning: 'su' },
  { id: 14, word: 'せ', reading: 'せ', meaning: 'se' },
  { id: 15, word: 'そ', reading: 'そ', meaning: 'so' },
  { id: 16, word: 'た', reading: 'た', meaning: 'ta' },
  { id: 17, word: 'ち', reading: 'ち', meaning: 'chi' },
  { id: 18, word: 'つ', reading: 'つ', meaning: 'tsu' },
  { id: 19, word: 'て', reading: 'て', meaning: 'te' },
  { id: 20, word: 'と', reading: 'と', meaning: 'to' },
  { id: 21, word: 'な', reading: 'な', meaning: 'na' },
  { id: 22, word: 'に', reading: 'に', meaning: 'ni' },
  { id: 23, word: 'ぬ', reading: 'ぬ', meaning: 'nu' },
  { id: 24, word: 'ね', reading: 'ね', meaning: 'ne' },
  { id: 25, word: 'の', reading: 'の', meaning: 'no' },
  { id: 26, word: 'は', reading: 'は', meaning: 'ha' },
  { id: 27, word: 'ひ', reading: 'ひ', meaning: 'hi' },
  { id: 28, word: 'ふ', reading: 'ふ', meaning: 'fu' },
  { id: 29, word: 'ほ', reading: 'ほ', meaning: 'ho' },
  { id: 30, word: 'へ', reading: 'へ', meaning: 'he' },
  { id: 31, word: 'ま', reading: 'ま', meaning: 'ma' },
  { id: 32, word: 'み', reading: 'み', meaning: 'mi' },
  { id: 33, word: 'む', reading: 'む', meaning: 'mu' },
  { id: 34, word: 'め', reading: 'め', meaning: 'me' },
  { id: 35, word: 'も', reading: 'も', meaning: 'mo' },
  { id: 36, word: 'や', reading: 'や', meaning: 'ya' },
  { id: 37, word: 'ゆ', reading: 'ゆ', meaning: 'yu' },
  { id: 38, word: 'よ', reading: 'よ', meaning: 'yo' },
  { id: 39, word: 'ら', reading: 'ら', meaning: 'ra' },
  { id: 40, word: 'り', reading: 'り', meaning: 'ri' },
  { id: 41, word: 'る', reading: 'る', meaning: 'ru' },
  { id: 42, word: 'れ', reading: 'れ', meaning: 're' },
  { id: 43, word: 'ろ', reading: 'ろ', meaning: 'ro' },
  { id: 44, word: 'わ', reading: 'わ', meaning: 'wa' },
  { id: 45, word: 'を', reading: 'を', meaning: 'wo' },
  { id: 46, word: 'ん', reading: 'ん', meaning: 'n' },
  // Katakana
  { id: 47, word: 'ア', reading: 'ア', meaning: 'a' },
  { id: 48, word: 'イ', reading: 'イ', meaning: 'i' },
  { id: 49, word: 'ウ', reading: 'ウ', meaning: 'u' },
  { id: 50, word: 'エ', reading: 'エ', meaning: 'e' },
  { id: 51, word: 'オ', reading: 'オ', meaning: 'o' },
  { id: 52, word: 'カ', reading: 'カ', meaning: 'ka' },
  { id: 53, word: 'キ', reading: 'キ', meaning: 'ki' },
  { id: 54, word: 'ク', reading: 'ク', meaning: 'ku' },
  { id: 55, word: 'ケ', reading: 'ケ', meaning: 'ke' },
  { id: 56, word: 'コ', reading: 'コ', meaning: 'ko' },
  { id: 57, word: 'サ', reading: 'サ', meaning: 'sa' },
  { id: 58, word: 'シ', reading: 'シ', meaning: 'shi' },
  { id: 59, word: 'ス', reading: 'ス', meaning: 'su' },
  { id: 60, word: 'セ', reading: 'セ', meaning: 'se' },
  { id: 61, word: 'ソ', reading: 'ソ', meaning: 'so' },
  { id: 62, word: 'タ', reading: 'タ', meaning: 'ta' },
  { id: 63, word: 'チ', reading: 'チ', meaning: 'chi' },
  { id: 64, word: 'ツ', reading: 'ツ', meaning: 'tsu' },
  { id: 65, word: 'テ', reading: 'テ', meaning: 'te' },
  { id: 66, word: 'ト', reading: 'ト', meaning: 'to' },
  { id: 67, word: 'ナ', reading: 'ナ', meaning: 'na' },
  { id: 68, word: 'ニ', reading: 'ニ', meaning: 'ni' },
  { id: 69, word: 'ヌ', reading: 'ヌ', meaning: 'nu' },
  { id: 70, word: 'ネ', reading: 'ネ', meaning: 'ne' },
  { id: 71, word: 'ノ', reading: 'ノ', meaning: 'no' },
  { id: 72, word: 'ハ', reading: 'ハ', meaning: 'ha' },
  { id: 73, word: 'ヒ', reading: 'ヒ', meaning: 'hi' },
  { id: 74, word: 'フ', reading: 'フ', meaning: 'fu' },
  { id: 75, word: 'ホ', reading: 'ホ', meaning: 'ho' },
  { id: 76, word: 'ヘ', reading: 'ヘ', meaning: 'he' },
  { id: 77, word: 'マ', reading: 'マ', meaning: 'ma' },
  { id: 78, word: 'ミ', reading: 'ミ', meaning: 'mi' },
  { id: 79, word: 'ム', reading: 'ム', meaning: 'mu' },
  { id: 80, word: 'メ', reading: 'メ', meaning: 'me' },
  { id: 81, word: 'モ', reading: 'モ', meaning: 'mo' },
  { id: 82, word: 'ヤ', reading: 'ヤ', meaning: 'ya' },
  { id: 83, word: 'ユ', reading: 'ユ', meaning: 'yu' },
  { id: 84, word: 'ヨ', reading: 'ヨ', meaning: 'yo' },
  { id: 85, word: 'ラ', reading: 'ラ', meaning: 'ra' },
  { id: 86, word: 'リ', reading: 'リ', meaning: 'ri' },
  { id: 87, word: 'ル', reading: 'ル', meaning: 'ru' },
  { id: 88, word: 'レ', reading: 'レ', meaning: 're' },
  { id: 89, word: 'ロ', reading: 'ロ', meaning: 'ro' },
  { id: 90, word: 'ワ', reading: 'ワ', meaning: 'wa' },
  { id: 91, word: 'ヲ', reading: 'ヲ', meaning: 'wo' },
  { id: 92, word: 'ン', reading: 'ン', meaning: 'n' },
]

export const useAppStore = defineStore('app', () => {
  const studyLang = ref<StudyLang>((localStorage.getItem('study_lang') as StudyLang) || 'ja')


  async function switchStudyLang(lang: StudyLang) {
    if (studyLang.value === lang && isDataLoaded.value) return
    studyLang.value = lang
    localStorage.setItem('study_lang', lang)
    if (lang === 'en' && currentCat.value === 'kana') {
      currentCat.value = 'articles'
    }
    if (lang === 'en' && currentCat.value === 'verbs') {
      currentCat.value = 'nouns'
    }
    await loadData()
  }

  const currentMode = ref<string>('list')
  const currentCat = ref<string>('articles')
  const data = ref<AppData>({ nouns: [], verbs: [], kana: KANA_DATA })
  /** 精读文章（短文 / 对话）：日语 ja_articles.json，英语 en_articles.json */
  const articles = ref<ArticleItem[]>([])
  const isDataLoaded = ref(false)

  // --- 本篇练习：按 format 分别存储（essay / dialogue 各一篇） ---

  type PracticeSlot = { id: string; title: string; index: number }

  function readSlot(format: string): PracticeSlot | null {
    const id = localStorage.getItem(`practice_${format}_id`)
    if (!id) return null
    return {
      id,
      title: localStorage.getItem(`practice_${format}_title`) || '',
      index: Number(localStorage.getItem(`practice_${format}_index`) || '0'),
    }
  }

  function writeSlot(format: string, slot: PracticeSlot | null) {
    if (slot) {
      localStorage.setItem(`practice_${format}_id`, slot.id)
      localStorage.setItem(`practice_${format}_title`, slot.title)
      localStorage.setItem(`practice_${format}_index`, String(slot.index))
    } else {
      localStorage.removeItem(`practice_${format}_id`)
      localStorage.removeItem(`practice_${format}_title`)
      localStorage.removeItem(`practice_${format}_index`)
    }
  }

  // 当前激活的本篇练习（根据 currentCat 动态切换）
  const practiceArticleId = ref<string | null>(null)
  const practiceArticleTitle = ref('')
  const practiceArticleIndex = ref(0)

  function catToFormat(cat: string): string | null {
    if (cat === 'articles') return 'essay'
    if (cat === 'dialogues') return 'dialogue'
    return null
  }

  /** 从 localStorage 加载当前分类对应的练习槽位 */
  function syncSlotToCat() {
    const fmt = catToFormat(currentCat.value)
    if (!fmt) {
      // 单词/50音分类，不清除内存，只是不显示
      practiceArticleId.value = null
      practiceArticleTitle.value = ''
      practiceArticleIndex.value = 0
      return
    }
    const slot = readSlot(fmt)
    if (slot) {
      practiceArticleId.value = slot.id
      practiceArticleTitle.value = slot.title
      practiceArticleIndex.value = slot.index
    } else {
      practiceArticleId.value = null
      practiceArticleTitle.value = ''
      practiceArticleIndex.value = 0
    }
  }

  function clearArticlePractice() {
    const fmt = catToFormat(currentCat.value)
    if (fmt) writeSlot(fmt, null)
    practiceArticleId.value = null
    practiceArticleTitle.value = ''
    practiceArticleIndex.value = 0
  }

  function savePracticeArticleIndex(index: number) {
    practiceArticleIndex.value = index
    // 找到这篇文章的 format 来存到对应槽位
    const art = articles.value.find((a) => a.id === practiceArticleId.value)
    const fmt = art?.format || catToFormat(currentCat.value)
    if (fmt) {
      localStorage.setItem(`practice_${fmt}_index`, String(index))
    }
  }

  function startArticlePractice(articleId: string) {
    const art = articles.value.find((a) => a.id === articleId)
    if (!art) return
    const fmt = art.format // 'essay' | 'dialogue'
    const slot: PracticeSlot = { id: articleId, title: art.titleWord ?? '', index: 0 }
    writeSlot(fmt, slot)
    practiceArticleId.value = articleId
    practiceArticleTitle.value = slot.title
    practiceArticleIndex.value = 0
    switchMode('practice')
  }

  /** 云端拉取后从 localStorage 刷新练习状态到 Pinia */
  function restorePracticeArticleFromLS() {
    syncSlotToCat()
    if (practiceArticleId.value) {
      currentMode.value = 'practice'
    }
  }

  function switchMode(mode: string) {
    // 精读列表切到练：无指定篇目时仍进单词练习
    if (mode === 'practice') {
      syncSlotToCat()
      if (!practiceArticleId.value && (currentCat.value === 'articles' || currentCat.value === 'dialogues')) {
        currentCat.value = 'nouns'
      }
    }
    currentMode.value = mode
  }

  function switchCat(cat: string) {
    currentCat.value = cat
    if (currentMode.value === 'practice') {
      syncSlotToCat()
    }
  }

  async function loadData() {
    try {
      const base = import.meta.env.BASE_URL
      const ja = studyLang.value === 'ja'

      const nounPath = ja ? 'data/nouns.json' : 'data/en_nouns.json'
      const verbPath = ja ? 'data/verbs.json' : ''
      const artPath = ja ? 'data/ja_articles.json' : 'data/en_articles.json'

      const [nouns, verbsRes, articlesData] = await Promise.all([
        fetch(`${base}${nounPath}`).then(r => r.json()),
        verbPath
          ? fetch(`${base}${verbPath}`).then(r => r.json())
          : Promise.resolve([]),
        fetch(`${base}${artPath}`).then(r => r.json()),
      ])
      data.value.nouns = nouns
      data.value.verbs = Array.isArray(verbsRes) ? verbsRes : []
      articles.value = Array.isArray(articlesData?.items) ? articlesData.items : []
      isDataLoaded.value = true

      // 恢复上次未完成的本篇练习
      syncSlotToCat()
      if (practiceArticleId.value) {
        const art = articles.value.find((a) => a.id === practiceArticleId.value)
        if (art) {
          currentMode.value = 'practice'
        } else {
          clearArticlePractice()
        }
      }
    } catch (e) {
      console.error('Failed to load data', e)
      throw e
    }
  }

  return {
    studyLang,
    switchStudyLang,
    currentMode,
    currentCat,
    data,
    articles,
    isDataLoaded,
    practiceArticleId,
    practiceArticleTitle,
    practiceArticleIndex,
    savePracticeArticleIndex,
    startArticlePractice,
    clearArticlePractice,
    restorePracticeArticleFromLS,
    switchMode,
    switchCat,
    loadData,
  }
})
