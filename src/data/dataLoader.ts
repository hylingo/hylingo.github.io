/**
 * 远端数据 fetch 工具：纯函数，不持有状态。
 *
 * 与 store 解耦的好处：
 *  - 单元测试时可以 mock fetch 而无需 mock 整个 Pinia store
 *  - 数据形状（json 路径选择、字段校验）集中在一处
 *  - store 只保留 in-memory 缓存与生命周期标记
 */
import type { ArticleItem, GrammarPoint, StudyLang } from '@/types'
import type { DataItem } from '@/stores/app'

export interface VocabBundle {
  nouns: DataItem[]
  verbs: DataItem[]
}

export interface ArticleBundle {
  articles: ArticleItem[]
  grammarMap: Record<string, GrammarPoint>
}

function base(): string {
  return import.meta.env.BASE_URL
}

/** 抓 nouns + verbs（学习语言决定文件路径；en 没有 verbs，返回空数组） */
export async function fetchVocabBundle(lang: StudyLang): Promise<VocabBundle> {
  const ja = lang === 'ja'
  const nounPath = ja ? 'data/nouns.json' : 'data/en_nouns.json'
  const verbPath = ja ? 'data/verbs.json' : ''

  const [nouns, verbsRes] = await Promise.all([
    fetch(`${base()}${nounPath}`).then((r) => r.json()),
    verbPath
      ? fetch(`${base()}${verbPath}`).then((r) => r.json())
      : Promise.resolve([] as DataItem[]),
  ])

  return {
    nouns: Array.isArray(nouns) ? (nouns as DataItem[]) : [],
    verbs: Array.isArray(verbsRes) ? (verbsRes as DataItem[]) : [],
  }
}

/** 抓 articles + grammar；grammar 失败时降级为空表，不影响 articles */
export async function fetchArticleBundle(lang: StudyLang): Promise<ArticleBundle> {
  const ja = lang === 'ja'
  const artPath = ja ? 'data/ja_articles.json' : 'data/en_articles.json'

  const [articlesData, grammarData] = await Promise.all([
    fetch(`${base()}${artPath}`).then((r) => r.json()),
    fetch(`${base()}data/grammar.json`)
      .then((r) => r.json())
      .catch(() => ({ items: [] as GrammarPoint[] })),
  ])

  const articles: ArticleItem[] = Array.isArray(articlesData?.items) ? articlesData.items : []
  const grammarMap: Record<string, GrammarPoint> = {}
  for (const g of (grammarData?.items ?? []) as GrammarPoint[]) {
    grammarMap[g.id] = g
  }
  return { articles, grammarMap }
}
