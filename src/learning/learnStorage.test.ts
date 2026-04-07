import { describe, expect, it, beforeEach } from 'vitest'
import {
  learnLocalStorageKey,
  listenedTodayKey,
  quizScopeKey,
  articlePrefKey,
  readSyncedJson,
  writeSyncedJson,
  readListenedTodayRaw,
  writeListenedTodayRaw,
  readQuizScopeRaw,
  writeQuizScopeRaw,
  readArticlePrefRaw,
  writeArticlePrefRaw,
  clearAllLearnProgressLocal,
  STUDY_LANGS,
} from './learnStorage'

describe('learnStorage key builders', () => {
  it('learnLocalStorageKey is namespaced by lang and uses suffix map', () => {
    expect(learnLocalStorageKey('ja', 'counts')).toBe('learn_ja_item_counts')
    expect(learnLocalStorageKey('en', 'counts')).toBe('learn_en_item_counts')
    expect(learnLocalStorageKey('ja', 'masteryQuizPassed')).toBe('learn_ja_mastery_quiz_passed')
  })

  it('listenedTodayKey / quizScopeKey are namespaced by lang', () => {
    expect(listenedTodayKey('ja')).toBe('learn_ja_listened_today')
    expect(quizScopeKey('en')).toBe('learn_en_quiz_scope')
  })

  it('articlePrefKey uses the suffix map', () => {
    expect(articlePrefKey('ja', 'mode')).toBe('learn_ja_article_mode')
    expect(articlePrefKey('en', 'show_zh')).toBe('learn_en_article_show_zh')
    expect(articlePrefKey('ja', 'voice')).toBe('learn_ja_article_tts_voice')
  })

  it('STUDY_LANGS contains exactly ja and en', () => {
    expect(STUDY_LANGS).toEqual(['ja', 'en'])
  })
})

describe('learnStorage round-trips', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('writeSyncedJson then readSyncedJson preserves an object', () => {
    writeSyncedJson('ja', 'counts', { 'nouns:1': 3, 'verbs:5': 1 })
    expect(readSyncedJson('ja', 'counts')).toEqual({ 'nouns:1': 3, 'verbs:5': 1 })
  })

  it('readSyncedJson returns {} for missing key', () => {
    expect(readSyncedJson('en', 'counts')).toEqual({})
  })

  it('readSyncedJson returns {} for malformed JSON', () => {
    localStorage.setItem(learnLocalStorageKey('ja', 'counts'), '{not valid')
    expect(readSyncedJson('ja', 'counts')).toEqual({})
  })

  it('writeSyncedJson on null/undefined writes empty object', () => {
    writeSyncedJson('ja', 'counts', null)
    expect(readSyncedJson('ja', 'counts')).toEqual({})
  })

  it('ja and en buckets do not collide', () => {
    writeSyncedJson('ja', 'counts', { x: 1 })
    writeSyncedJson('en', 'counts', { x: 99 })
    expect(readSyncedJson('ja', 'counts')).toEqual({ x: 1 })
    expect(readSyncedJson('en', 'counts')).toEqual({ x: 99 })
  })

  it('listenedToday raw round-trip', () => {
    writeListenedTodayRaw('ja', 'foo')
    expect(readListenedTodayRaw('ja')).toBe('foo')
    expect(readListenedTodayRaw('en')).toBeNull()
  })

  it('quizScope raw round-trip', () => {
    writeQuizScopeRaw('en', 'N5')
    expect(readQuizScopeRaw('en')).toBe('N5')
  })

  it('articlePref raw round-trip', () => {
    writeArticlePrefRaw('ja', 'mode', '1')
    expect(readArticlePrefRaw('ja', 'mode')).toBe('1')
    expect(readArticlePrefRaw('ja', 'show_zh')).toBeNull()
  })
})

describe('clearAllLearnProgressLocal', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('removes all learn_* family keys for all langs but leaves unrelated keys', () => {
    writeSyncedJson('ja', 'counts', { a: 1 })
    writeSyncedJson('en', 'masteryQuizPassed', { b: true })
    writeListenedTodayRaw('ja', 'today')
    writeQuizScopeRaw('en', 'N3')
    writeArticlePrefRaw('ja', 'mode', '1')
    writeArticlePrefRaw('en', 'voice', 'male')

    // 不应被清除的无关 key
    localStorage.setItem('jp_user_id', 'alice')
    localStorage.setItem('app_theme_mode_v1', 'ink')

    clearAllLearnProgressLocal()

    // 学习数据全清
    expect(readSyncedJson('ja', 'counts')).toEqual({})
    expect(readSyncedJson('en', 'masteryQuizPassed')).toEqual({})
    expect(readListenedTodayRaw('ja')).toBeNull()
    expect(readQuizScopeRaw('en')).toBeNull()
    expect(readArticlePrefRaw('ja', 'mode')).toBeNull()
    expect(readArticlePrefRaw('en', 'voice')).toBeNull()

    // 用户身份和主题不动
    expect(localStorage.getItem('jp_user_id')).toBe('alice')
    expect(localStorage.getItem('app_theme_mode_v1')).toBe('ink')
  })
})
