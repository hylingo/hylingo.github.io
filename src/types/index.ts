export interface RubyToken {
  t: string
  r?: string
}

export interface VocabItem {
  id: number
  word: string
  reading: string
  meaning: string
  meaningEn?: string
  meaningEs?: string
  /** 学英语语料：英文词条/句子对应的日语释义或译文 */
  meaningJp?: string
  example?: string
  exampleCn?: string
  exampleEn?: string
  exampleJp?: string
  topic?: string
  level?: string
  ruby?: RubyToken[]
  tokens?: string[]
  audio?: string
  audioExample?: string
}

export interface VocabItemWithCat extends VocabItem {
  _cat: CategoryKey
}

export type CategoryKey = 'nouns' | 'sentences' | 'kana' | 'articles'

/** 精读文章：短文或对话；word=该篇原文（日语或英语），jp/en/zh 为日英中对照 */
export interface ArticleSegment {
  word: string
  jp: string
  en: string
  zh: string
  reading: string
  ruby?: RubyToken[]
  audio?: string
  audioMale?: string
}

export interface ArticleDialogueLine extends ArticleSegment {
  speaker: 'A' | 'B'
}

export interface ArticleDialogueSection {
  badge?: string
  headingWord: string
  headingJp: string
  headingEn: string
  headingZh: string
  lines: ArticleDialogueLine[]
}

export interface ArticleEssay {
  id: string
  level: string
  format: 'essay'
  titleWord: string
  titleJp: string
  titleEn: string
  titleZh: string
  titleRuby?: RubyToken[]
  segments: ArticleSegment[]
}

export interface ArticleDialogue {
  id: string
  level: string
  format: 'dialogue'
  titleWord: string
  titleJp: string
  titleEn: string
  titleZh: string
  titleRuby?: RubyToken[]
  sections: ArticleDialogueSection[]
}

export type ArticleItem = ArticleEssay | ArticleDialogue
export type ModeKey = 'list' | 'practice' | 'stats'
export type LangKey = 'zh' | 'en' | 'ja'
export type StudyLang = 'ja' | 'en'

export interface DayStats {
  studied: number
  quizzed: number
  correct: number
  listened?: number
  recorded?: number
  wrong: Record<string, number>
}

export type StatsMap = Record<string, DayStats>
export type ItemCounts = Record<string, number>
export type DelayMap = Record<string, string>

export interface AudioMap {
  [text: string]: string
}
