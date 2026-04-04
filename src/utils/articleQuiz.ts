import type { ArticleItem, ArticleSegment } from '@/types'
import type { DataItem } from '@/stores/app'

export function flatArticleSegments(art: ArticleItem): ArticleSegment[] {
  if (art.format === 'essay') {
    return art.segments.map((s) => ({ ...s }))
  }
  const out: ArticleSegment[] = []
  for (const sec of art.sections) {
    for (const line of sec.lines) {
      out.push({ ...line })
    }
  }
  return out
}

export type ArticleQuizItem = DataItem & {
  _quizSource: 'article'
  _articleId: string
}

/** 精读一篇 → 与单词练习同结构的逐条题目（顺序与原文一致） */
export function articleToPracticeQuizItems(art: ArticleItem, uiLang: string): ArticleQuizItem[] {
  const segs = flatArticleSegments(art)
  return segs.map((seg, idx) => {
    let meaning = seg.zh
    if (uiLang === 'en') meaning = seg.en || seg.zh
    else if (uiLang === 'ja') meaning = seg.jp || seg.zh

    return {
      id: idx,
      word: seg.word,
      reading: seg.reading,
      meaning,
      meaningEn: seg.en,
      ruby: seg.ruby,
      audio: seg.audio,
      _cat: 'articleSeg',
      _quizSource: 'article',
      _articleId: art.id,
    }
  })
}
