# 水彩主题（watercolor）设计方案

## 背景

原 `warm`（暖云）主题用纯 CSS 渐变做底，缺少真实纸纹和颜料质感。
现替换为真实水彩背景图，主题更名为 `watercolor`。

## 目标

- 新背景：真实水彩 PNG 图片，四角颜料晕染 + 纸纹，中间留白
- 三主题结构不变：`dusk | watercolor | ink`（替换 `warm`）
- 不同路由显示图片的不同区域，让每个页面有细微差异
- 卡片/导航变半透明，让背景透出来
- 兼容已存的 `warm` localStorage 值，自动迁移

## 资源

- 图片：`public/bg2.webp`（36 KB，1024×1536，竖版边缘水彩晕染）
- 原 PNG `public/bg2.png` 未使用，可删（本次一并删除）

## 改动清单

### 1. 主题改名 `warm` → `watercolor`

- `src/composables/useTheme.ts`
  - `ThemeMode` 类型：`'dusk' | 'watercolor' | 'ink'`
  - `ALL_THEMES` 数组、默认值 `ref<ThemeMode>('watercolor')`
  - `applyTheme`：`classList.toggle('theme-dark', mode !== 'watercolor')`
  - localStorage 迁移：`if (raw === 'warm') themeMode.value = 'watercolor'`
- `src/style.css`
  - `:root.theme-warm` → `:root.theme-watercolor`（两处：L28, L402）
- `src/components/stats/WeeklyChart.vue`
  - `:root:not(.theme-warm)` → `:root:not(.theme-watercolor)`（四处）
- `src/components/stats/StatsPanel.vue`
  - L135 label: `themeMode === 'warm' ? '暖云'` → `themeMode === 'watercolor' ? '水彩'`
  - L147 按钮渐变：水彩预览换成 `linear-gradient(135deg, #f5c0c8 0%, #ffe4b8 35%, #c5e4f0 70%, #d8c5e8 100%)`

### 2. 背景图挂载（伪元素 fixed 层）

`src/style.css` 中，`:root.theme-watercolor` 主题下新增：

```css
:root.theme-watercolor body::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  background: url('/bg2.webp') center top / cover no-repeat;
  pointer-events: none;
}
:root.theme-watercolor.mode-practice body::before { background-position: center center; }
:root.theme-watercolor.mode-stats    body::before { background-position: center bottom; }
```

水彩主题下，`--bg-gradient` 去掉或设为 `transparent`，让伪元素的图显出来。
已有的 `body { background-attachment: fixed; }` 对 watercolor 无影响（背景由伪元素负责）。

### 3. 路由 → mode class

在 `src/App.vue`（或合适的根组件）里 watch 路由名，更新 `<html>` 的 class：

```ts
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const MODE_CLASSES = ['mode-list', 'mode-practice', 'mode-stats'] as const

function routeToMode(name: unknown): typeof MODE_CLASSES[number] {
  if (name === 'practice' || name === 'practice-article') return 'mode-practice'
  if (name === 'stats') return 'mode-stats'
  return 'mode-list'
}

watch(() => route.name, (name) => {
  const root = document.documentElement
  MODE_CLASSES.forEach(c => root.classList.remove(c))
  root.classList.add(routeToMode(name))
}, { immediate: true })
```

理由：挂在 `<html>`（documentElement）上，跟 `theme-*` class 同位置，选择器 `:root.theme-watercolor.mode-practice` 可以直接命中。

### 4. CSS 变量微调（watercolor 主题内）

先做最小调整让背景透出来，其余保留，上线后再迭代：

- `--card`: `rgba(255,255,255,0.55)`（原 `rgba(255,255,255,0.5)`，稍提）
- `--card-blur`: `blur(8px)`（原 `blur(20px)`，减弱磨砂让纸纹更明显）
- `--card-border`: `rgba(255,255,255,0.6)`
- `--bg-gradient`: 设为 `transparent`（或删掉让 fallback 生效）
- `--bg-glow`: `none`（避免额外发光干扰水彩色）

其他变量（`--text`、`--primary`、`--accent` 等）保持 warm 原值，跑起来观察后再调。

## 不做的事

- 不改 dusk / ink 主题
- 不动 nav / loop panel / stats 卡片等组件的自身样式（只靠 CSS 变量驱动）
- 不做路由切换时背景图的动画过渡（YAGNI，后续需要再加）

## 验证

- `yarn lint` 通过
- `yarn build` 通过（vue-tsc + vite）
- 手动：
  - 切换三主题，watercolor 背景显示正常
  - 老用户 localStorage 里 `'warm'` 自动映射为 watercolor
  - 切换 list/practice/stats 三个 tab，背景位置变化
  - 滚动长列表，背景固定不动
