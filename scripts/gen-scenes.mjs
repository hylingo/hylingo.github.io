/**
 * gen-scenes.mjs
 * 调用 Claude CLI 切场景，输出 scenes_draft.json 供 review
 *
 * 用法：
 *   node scripts/gen-scenes.mjs --id n5-food-i-like-essay   # 单篇
 *   node scripts/gen-scenes.mjs                              # 全量（跳过已有条目）
 */

import { spawnSync } from 'child_process'
import { readFileSync, writeFileSync, existsSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const root = resolve(__dirname, '..')

// ── CLI 参数 ──────────────────────────────────────────────
const args = process.argv.slice(2)
const idFlagIdx = args.indexOf('--id')
const targetId = idFlagIdx !== -1 ? args[idFlagIdx + 1] : null
const limitFlagIdx = args.indexOf('--limit')
const limit = limitFlagIdx !== -1 ? parseInt(args[limitFlagIdx + 1]) : null

// ── 加载文章 ──────────────────────────────────────────────
const data = JSON.parse(readFileSync(resolve(root, 'public/data/ja_articles.json'), 'utf8'))
let articles = data.items

if (targetId) {
  articles = articles.filter(a => a.id === targetId)
  if (!articles.length) {
    console.error(`找不到文章: ${targetId}`)
    process.exit(1)
  }
}

// ── 加载已有草稿（断点续跑） ───────────────────────────────
const draftPath = resolve(root, 'scripts/scenes_draft.json')
const draft = existsSync(draftPath)
  ? JSON.parse(readFileSync(draftPath, 'utf8'))
  : {}

// ── 将文章展平为带序号的句子列表 ──────────────────────────
function flattenArticle(article) {
  if (article.format === 'essay') {
    return article.segments.map((s, i) => ({
      i,
      text: s.en || s.word,
    }))
  }
  // dialogue
  const lines = []
  let i = 0
  for (const sec of article.sections) {
    for (const line of sec.lines) {
      lines.push({ i: i++, text: `[${line.speaker}] ${line.en || line.word}` })
    }
  }
  return lines
}

// ── Prompt 模板 ───────────────────────────────────────────
const STYLE_SUFFIX =
  'watercolor children\'s book illustration, soft pastel colors, dreamy atmosphere, no text, no logos, no clearly visible human faces'

function buildPrompt(article, sentences) {
  const isDialogue = article.format === 'dialogue'
  const sentencesText = sentences.map(s => `[${s.i}] ${s.text}`).join('\n')

  return `You are analyzing a Japanese language learning article to identify visual scenes for watercolor illustration.

Article title: "${article.titleEn || article.titleWord}"
Format: ${isDialogue ? 'dialogue' : 'essay'}
Total sentences: ${sentences.length}

Sentences (0-based index):
${sentencesText}

Task:
1. Identify 2-4 distinct visual scenes. ${isDialogue ? 'Base scenes on WHERE the conversation takes place.' : 'Base scenes on visual setting changes.'}
2. Also create one "cover" image representing the whole article.

Each scene needs:
- "range": [start, end] inclusive 0-based indices
- "summary": brief description in Chinese (one sentence)
- "prompt": English Stable Diffusion prompt. Must end with: "${STYLE_SUFFIX}"

Rules:
- The ranges must cover all sentences without overlap or gap
- Keep prompts vivid and scene-focused (setting, lighting, mood, objects), not character-portrait-focused
- cover.prompt should capture the most iconic moment of the article

Respond with ONLY valid JSON, no markdown, no explanation:
{
  "scenes": [
    { "range": [0, 3], "summary": "...", "prompt": "..." }
  ],
  "cover": { "summary": "...", "prompt": "..." }
}`
}

// ── 调用 Claude CLI ───────────────────────────────────────
function callClaude(prompt) {
  const result = spawnSync('claude', ['-p', prompt], {
    encoding: 'utf8',
    timeout: 90000,
    maxBuffer: 2 * 1024 * 1024,
  })

  if (result.error) throw result.error
  if (result.status !== 0) {
    throw new Error(`claude 退出码 ${result.status}: ${result.stderr?.slice(0, 300)}`)
  }

  const output = result.stdout.trim()
  // Claude 有时会加 ```json ... ``` 围栏，提取纯 JSON
  const jsonMatch = output.match(/\{[\s\S]*\}/)
  if (!jsonMatch) {
    throw new Error(`输出里找不到 JSON:\n${output.slice(0, 400)}`)
  }
  return JSON.parse(jsonMatch[0])
}

// ── 处理单篇 ─────────────────────────────────────────────
async function processArticle(article) {
  const sentences = flattenArticle(article)
  if (sentences.length === 0) {
    console.log('  跳过（无句子，可能是整段音频文章）')
    return null
  }

  const prompt = buildPrompt(article, sentences)
  console.log(`  calling claude... (${sentences.length} 句)`)

  const result = callClaude(prompt)

  // 基本校验
  if (!Array.isArray(result.scenes) || !result.cover) {
    throw new Error('返回格式不对，缺少 scenes 或 cover')
  }

  return result
}

// ── 主流程 ────────────────────────────────────────────────
let processed = 0
let skipped = 0
let failed = 0

for (const article of articles) {
  // 全量模式下跳过已有条目（单篇模式强制重跑）
  if (!targetId && draft[article.id]) {
    console.log(`[跳过] ${article.id}`)
    skipped++
    continue
  }

  if (limit && processed >= limit) break

  processed++
  console.log(`\n[${processed}] ${article.id} (${article.format})`)

  try {
    const result = await processArticle(article)
    if (result) {
      draft[article.id] = {
        title: article.titleEn || article.titleWord,
        format: article.format,
        ...result,
      }
      // 每篇完成后立即写盘，断点续跑不丢进度
      writeFileSync(draftPath, JSON.stringify(draft, null, 2))
      console.log(`  ✓ ${result.scenes.length} 个场景 + cover`)
    }
  } catch (err) {
    console.error(`  ✗ 失败: ${err.message}`)
    failed++
  }

  // 避免触发速率限制
  await new Promise(r => setTimeout(r, 800))
}

console.log(`\n完成。草稿已写入 scripts/scenes_draft.json`)
console.log(`处理: ${processed}  跳过(已有): ${skipped}  失败: ${failed}`)
