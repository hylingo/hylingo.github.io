import { describe, expect, it } from 'vitest'
import type { ArticleEssay, ArticleDialogue } from '@/types'
import { flatArticleSegments, articleToPracticeQuizItems } from './articleQuiz'

const essayFixture: ArticleEssay = {
  id: 'e1',
  level: 'N5',
  format: 'essay',
  titleWord: '题',
  titleJp: '題',
  titleEn: 'Title',
  titleZh: '标题',
  segments: [
    { word: 'こんにちは', jp: 'こんにちは', en: 'Hello', zh: '你好', reading: 'こんにちは' },
    { word: 'さようなら', jp: 'さようなら', en: 'Goodbye', zh: '再见', reading: 'さようなら' },
  ],
}

const dialogueFixture: ArticleDialogue = {
  id: 'd1',
  level: 'N5',
  format: 'dialogue',
  titleWord: '对话',
  titleJp: '会話',
  titleEn: 'Dialogue',
  titleZh: '对话',
  sections: [
    {
      headingWord: 'Sec1',
      headingJp: 'セ1',
      headingEn: 'Sec1',
      headingZh: '段1',
      lines: [
        { word: 'A1', jp: 'A1', en: 'A1', zh: 'A1', reading: 'A1', speaker: 'A' },
        { word: 'B1', jp: 'B1', en: 'B1', zh: 'B1', reading: 'B1', speaker: 'B' },
      ],
    },
    {
      headingWord: 'Sec2',
      headingJp: 'セ2',
      headingEn: 'Sec2',
      headingZh: '段2',
      lines: [
        { word: 'A2', jp: 'A2', en: 'A2', zh: 'A2', reading: 'A2', speaker: 'A' },
      ],
    },
  ],
}

describe('flatArticleSegments', () => {
  it('returns essay segments in original order', () => {
    const out = flatArticleSegments(essayFixture)
    expect(out.map((s) => s.word)).toEqual(['こんにちは', 'さようなら'])
  })

  it('flattens dialogue sections preserving order', () => {
    const out = flatArticleSegments(dialogueFixture)
    expect(out.map((s) => s.word)).toEqual(['A1', 'B1', 'A2'])
  })

  it('returns shallow copies, not references', () => {
    const out = flatArticleSegments(essayFixture)
    out[0].word = 'mutated'
    expect(essayFixture.segments[0].word).toBe('こんにちは')
  })
})

describe('articleToPracticeQuizItems', () => {
  it('produces quiz items with sequential ids and article id markers', () => {
    const items = articleToPracticeQuizItems(essayFixture, 'zh')
    expect(items).toHaveLength(2)
    expect(items[0].id).toBe(0)
    expect(items[1].id).toBe(1)
    expect(items[0]._quizSource).toBe('article')
    expect(items[0]._articleId).toBe('e1')
    expect(items[0]._cat).toBe('articleSeg')
  })

  it('picks Chinese meaning by default', () => {
    const items = articleToPracticeQuizItems(essayFixture, 'zh')
    expect(items[0].meaning).toBe('你好')
  })

  it('picks English meaning when uiLang=en', () => {
    const items = articleToPracticeQuizItems(essayFixture, 'en')
    expect(items[0].meaning).toBe('Hello')
  })

  it('picks Japanese meaning when uiLang=ja', () => {
    const items = articleToPracticeQuizItems(essayFixture, 'ja')
    expect(items[0].meaning).toBe('こんにちは')
  })

  it('falls back to zh when target lang field is empty', () => {
    const broken: ArticleEssay = {
      ...essayFixture,
      segments: [{ word: 'X', jp: '', en: '', zh: '中文', reading: 'X' }],
    }
    expect(articleToPracticeQuizItems(broken, 'en')[0].meaning).toBe('中文')
    expect(articleToPracticeQuizItems(broken, 'ja')[0].meaning).toBe('中文')
  })

  it('handles dialogue articles', () => {
    const items = articleToPracticeQuizItems(dialogueFixture, 'zh')
    expect(items).toHaveLength(3)
    expect(items.map((i) => i.word)).toEqual(['A1', 'B1', 'A2'])
    expect(items.every((i) => i._articleId === 'd1')).toBe(true)
  })
})
