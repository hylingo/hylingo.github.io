import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'
import {
  copyFileSync,
  existsSync,
  readFileSync,
  readdirSync,
  rmSync,
  statSync,
  writeFileSync,
} from 'fs'

// GH Pages SPA fallback：把 dist/index.html 复制成 dist/404.html，
// 这样直接访问 /ja/articles 这种深链接刷新也能命中 SPA。
function ghPagesSpaFallback(): Plugin {
  return {
    name: 'gh-pages-spa-fallback',
    apply: 'build',
    closeBundle() {
      const src = resolve(__dirname, 'dist/index.html')
      const dst = resolve(__dirname, 'dist/404.html')
      if (existsSync(src)) copyFileSync(src, dst)
    },
  }
}

/**
 * 把 public/data/ 里的 JSON 数据：
 *  - 压缩（去除 indent，70%+ 体积节省）
 *  - 剔除运行时不用、只供 Python 脚本用的中间产物
 *
 * 源文件 public/data/*.json 仍保留 pretty 形式以便 git diff 友好和数据生成脚本兼容；
 * 仅产物 dist/data/*.json 是压缩版本。
 */
function compactPublicJson(): Plugin {
  // 这些文件只被 scripts/*.py 引用，运行时从不 fetch；不应进 dist
  const RUNTIME_UNUSED = new Set([
    'audio_map.json',
    'article_audio_map_male.json',
  ])

  return {
    name: 'compact-public-json',
    apply: 'build',
    closeBundle() {
      const dataDir = resolve(__dirname, 'dist/data')
      if (!existsSync(dataDir)) return
      let totalBefore = 0
      let totalAfter = 0
      let removed = 0
      for (const name of readdirSync(dataDir)) {
        if (!name.endsWith('.json')) continue
        const full = resolve(dataDir, name)
        const before = statSync(full).size
        if (RUNTIME_UNUSED.has(name)) {
          rmSync(full)
          removed += before
          continue
        }
        try {
          const parsed = JSON.parse(readFileSync(full, 'utf8'))
          const compact = JSON.stringify(parsed)
          writeFileSync(full, compact)
          totalBefore += before
          totalAfter += compact.length
        } catch (e) {
          console.warn(`[compact-public-json] skip ${name}: parse failed`, e)
        }
      }
      const saved = totalBefore - totalAfter + removed
      console.log(
        `[compact-public-json] minified ${(totalBefore / 1024).toFixed(0)}KB → ` +
          `${(totalAfter / 1024).toFixed(0)}KB; removed unused ${(removed / 1024).toFixed(0)}KB; ` +
          `total saved ${(saved / 1024).toFixed(0)}KB`,
      )
    },
  }
}

export default defineConfig({
  plugins: [vue(), tailwindcss(), compactPublicJson(), ghPagesSpaFallback()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  base: '/',
  publicDir: 'public',
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/firebase') || id.includes('node_modules/@firebase')) {
            return 'firebase'
          }
        },
      },
    },
  },
})
